from jinja2 import FileSystemLoader, Environment, StrictUndefined, Template


class JinjaRenderer:

    @staticmethod
    def render_from_path(path, options):
        environment = Environment(loader=FileSystemLoader('/'), undefined=StrictUndefined)
        template = environment.get_template(path)
        return template.render(options)

    @staticmethod
    def render_from_stream(content, options):
        template = Template(content)
        return template.render(options)

    @staticmethod
    def get_file_extension():
        return '.jinja2'
