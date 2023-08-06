import glob
import os
from dataclasses import dataclass

from src.templates.data import DataParser
from src.utils import renderers, printer, os_utils


BASE_DIR = '{template_name}'
FILES_DIR = os.path.join(BASE_DIR, 'files')
INFO_MANIFEST_PATH = os.path.join(BASE_DIR, 'info.yml')
FILE_MANIFEST_PATH = os.path.join(BASE_DIR, 'files.yml')

COMMON_SUB_TEMPLATES = ['common']


class Template:
    """
    Represents the top-level template object, comprised by a main template and,
    potentially, a list of sub-templates.

    It can be instantiated directly, but for most use cases .load() should be
    called. In case of loading, data can be provided from either a remote or a
    local source.

    Only static data is included in this object; any dynamic data can only be
    obtained via .render().

    Example usage:
        Template.load(name='sample-template')
            .render(options={'option1=value1'})
            .write(prefix='$HOME/my-sample-project/')
    """
    def __init__(self, main, subs=None):
        self._main = main
        self._subs = subs or []

        self.name = self._main.name
        self.version = self._main.version
        self.description = self._main.description
        self.is_hidden = self._main.is_hidden

    @classmethod
    def load(cls, name, data_source):
        main = SingleTemplate.load(name, data_source)

        # add default sub-templates provided the current
        # template is not a default sub-template itself
        subs = []
        if name not in COMMON_SUB_TEMPLATES:
            for sub_name in COMMON_SUB_TEMPLATES:
                subs.append(SingleTemplate.load(sub_name, data_source))

        return cls(main, subs)

    @property
    def accepted_options(self):
        accepted_options = self._main.accepted_options

        # options from main take precedence over options from sub templates
        for sub in self._subs:
            for option in sub.accepted_options:
                if option not in accepted_options:
                    accepted_options.append(option)

        return accepted_options

    def render(self, custom_options):
        self._validate_options(custom_options)
        options = self._fill_options_from_defaults(custom_options)

        return RenderedTemplate(
            main=self._main.render(options),
            subs=[sub.render(options) for sub in self._subs])

    def _fill_options_from_defaults(self, custom_options):
        options = {}
        for option in self.accepted_options:
            options[option.name] =\
                custom_options.get(option.name, option.default)
        return options

    def _validate_options(self, custom_options):
        for name, value in custom_options.items():
            for option in self.accepted_options:
                if option.name == name:
                    option.validate(value)
                    # validate only the first match since options from main
                    # take precedence over options from sub templates
                    return

            raise ValueError('Specified option [{}] not found'.format(name))


class SingleTemplate:
    """
    Represents the core template object.

    It can be instantiated directly, but for most use cases .load() should be
    called. In case of loading, data can be provided from either a remote or a
    local source.

    Only static data is included in this object; any dynamic data can only be
    obtained via .render().
    """
    def __init__(self, name, version, description, is_hidden, accepted_options, data_source):
        self.name = name
        self.version = version
        self.description = description
        self.is_hidden = is_hidden
        self.accepted_options = accepted_options

        self.data_source = data_source

    @classmethod
    def load(cls, name, data_source):
        manifest = data_source.read_file(INFO_MANIFEST_PATH.format(template_name=name))

        version, description, is_hidden = DataParser.parse_info_data(manifest)
        option_data = DataParser.parse_option_data(manifest)

        accepted_options = []
        for option in option_data:
            option_name, default, is_configurable, accepted_values = option
            accepted_options.append(OptionInfo(
                name=option_name,
                default=default,
                is_configurable=is_configurable,
                accepted_values=accepted_values))

        return cls(name, version, description, is_hidden, accepted_options, data_source)

    def render(self, options):
        manifest = self.data_source.read_file(FILE_MANIFEST_PATH.format(template_name=self.name))

        location_data = DataParser.parse_location_data(manifest, options)

        locations = []
        for location in location_data:
            source, target, condition = location

            locations.append(FileLocation(
                source=source,
                target=target,
                condition=condition
            ))

        return RenderedSingleTemplate(self, locations, options)


class RenderedTemplate(Template):
    """
    Represents the rendered version of a top-level template, comprised by the
    rendered versions of its single templates.
    """
    def __init__(self, main, subs=None):
        super().__init__(main, subs)

    def write(self, prefix):
        for template in [self._main] + self._subs:
            template.write(prefix)


class RenderedSingleTemplate(SingleTemplate):
    """
    Represents the rendered version of a single template.

    The rendered version includes fields that cannot be included in the
    SingleTemplate() since they need to be computed based on the options
    specified by the caller.
    """
    def __init__(self, template, locations, options):
        super().__init__(
            template.name, template.version, template.description, template.is_hidden,
            template.accepted_options, template.data_source)

        self.locations = locations
        self.options = options

    @property
    def files(self):
        files_dir = self.data_source.get_as_local_dir(FILES_DIR.format(template_name=self.name))

        files = set()
        # looping in reverse so the values defined later for two equal files
        # take precedence over the ones defined earlier
        for location in reversed(self.locations):
            files.update(location.get_files(files_dir))

        return files

    def write(self, prefix):
        for file in self.files:
            if file.condition or file.condition is None:
                rendered = file.renderer.render_from_path(os.path.join(file.source_dir, file.source_name), self.options)

                os_utils.write(rendered, os.path.join(prefix, file.target_dir, file.target_name))


@dataclass
class OptionInfo:

    def __init__(self, name, default, is_configurable, accepted_values):
        self.name = name
        self.default = default
        self.is_configurable = is_configurable or False
        self.accepted_values = accepted_values

    def __eq__(self, other):
        if type(other) is type(self):
            return self.name == other.name
        return False

    def __hash__(self):
        return hash(self.name)

    def validate(self, value):
        if not self.is_configurable:
            raise ValueError('Specified option [{}] not configurable'.format(self.name))

        if value not in self.accepted_values:
            raise ValueError('Specified value [{}] not valid. Valid values are {}'.format(value, self.accepted_values))


@dataclass
class FileLocation:

    def __init__(self, source, target, condition):
        self.source_pattern = source
        self.source_stripped = source.strip('**').strip('*')
        self.source_dir = os.path.dirname(self.source_stripped)

        self.target_dir = self.source_dir
        self.target_filename = None

        if target is not None:
            self.target_dir = os.path.dirname(target)
            self.target_filename = os.path.basename(target)

        self.condition = condition

    def get_files(self, root_dir):
        matching_abs_paths = glob.glob(os.path.join(root_dir, self.source_pattern), recursive=True)

        if not matching_abs_paths:
            printer.print_warning('Found no files in source {}'.format(self.source_pattern))
            return []

        files = set()
        for abs_path in matching_abs_paths:
            if os.path.isfile(abs_path):
                rel_dir = os.path.dirname(os.path.relpath(abs_path, os.path.join(root_dir, self.source_dir)))

                files.add(File(
                    source_dir=os.path.dirname(abs_path),
                    source_name=os.path.basename(abs_path),
                    target_dir=os.path.join(self.target_dir, rel_dir),
                    target_name=self.target_filename,
                    condition=self.condition
                ))

        return files


@dataclass
class File:

    def __init__(self, source_name, source_dir, target_dir, target_name, condition):
        self.source_name = source_name
        self.source_dir = source_dir
        self.target_dir = target_dir
        self.condition = condition

        self.renderer = renderers.JinjaRenderer()
        # by default remove file extension from source name
        self.target_name = target_name or source_name.replace(self.renderer.get_file_extension(), '')

    def __eq__(self, other):
        if type(other) is type(self):
            return self.source_name == other.source_name and self.source_dir == other.source_dir
        return False

    def __hash__(self):
        return hash((self.source_name, self.source_dir))


def get_templates(data_source, include_hidden=False):
    names = data_source.read_dir('')
    templates = []
    for name in names:
        try:
            template = Template.load(name, data_source)
            if include_hidden or not template.is_hidden:
                templates.append(template)
        except (ValueError, IOError):
            printer.print_warning('Invalid configuration for template {}'.format(name))

    return templates
