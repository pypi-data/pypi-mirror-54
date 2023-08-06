from src.utils import loaders, renderers


class DataParser:

    @staticmethod
    def parse_info_data(info_manifest):
        """
        Returns generic, static information associated with a given template.

        :return: (version, description, is_hidden)
        :rtype: (string, string, bool)
        """
        dict_ = loaders.YamlLoader().load_from_stream(info_manifest)
        version = str(dict_.get('version'))
        description = dict_.get('description')
        is_hidden = dict_.get('hidden', False)

        return version, description, is_hidden

    @staticmethod
    def parse_option_data(info_manifest):
        """
        Returns static information on the available options for a given template.

        :return: list of (default, is_configurable, accepted_values)
        :rtype: list of (string, int, list of string)
        """
        dict_ = loaders.YamlLoader().load_from_stream(info_manifest)
        options_dict = dict_.get('options', {})
        options = []
        for name, info in options_dict.items():
            options.append((name, info.get('default'), info.get('configurable'), info.get('accepted_values')))

        return options

    @staticmethod
    def parse_location_data(file_manifest, options):
        """
        Returns dynamic information on the locations to scan for a given template.
        The information is considered 'dynamic' because certain values in the manifest are variable
        and must be rendered before being parsed.

        :return list of (source, target, condition)
        :rtype: list of (string, string, expression)
        """
        rendered = renderers.JinjaRenderer().render_from_stream(file_manifest, options)

        dict_ = loaders.YamlLoader().load_from_stream(rendered)
        locations_list = dict_.get('locations', [])
        locations = []
        for location in locations_list:
            source = location.get('source')
            target = location.get('target')
            condition = location.get('condition')

            locations.append((source, target, condition))

        return locations
