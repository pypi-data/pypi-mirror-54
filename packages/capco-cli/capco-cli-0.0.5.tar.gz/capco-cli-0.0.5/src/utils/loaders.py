import yaml

from src.utils import printer


class YamlLoader:

    @staticmethod
    def load_from_path(path):
        with open(path, 'r') as stream:
            return YamlLoader.load_from_stream(stream)

    @staticmethod
    def load_from_stream(stream):
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as e:
            printer.print_error(e.__str__())
