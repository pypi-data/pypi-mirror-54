import click

from src.commands.projects import projects
from src.commands.templates import templates
from src.utils import printer


class ExceptionHandler(click.Group):

    def __call__(self, *args, **kwargs):
        try:
            return self.main(*args, **kwargs)
        except ValueError as e:
            printer.print_error(e.__str__())


@click.group(cls=ExceptionHandler)
def commands():
    """[Thanks for using Capco-CLI. This tool is used to generates the file structure with relevant code snippets
     based on the selected template] """
    pass


commands.add_command(projects)
commands.add_command(templates)
