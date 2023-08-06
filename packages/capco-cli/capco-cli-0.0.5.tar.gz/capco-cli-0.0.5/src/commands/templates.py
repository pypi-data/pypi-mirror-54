import click

from src.common import data
from src.templates import template
from src.common.data import DataSourceType, DataSource
from src.utils import printer


@click.group()
def templates():
    """[View or inspect templates on local or remote directory] Default:remote"""
    pass


@templates.command('list', help='[View all the available templates in remote or local directory]')
@click.option('--source_type', default=DataSourceType.REMOTE.name,
              type=click.Choice(DataSourceType.get_keys(), case_sensitive=False), help='[Template type]')
@click.option('--source_repository', default='capco-templates')
@click.option('--source_branch', default='master')
@click.option('--source_dir', default='.', help='[If local source, specify the path]')
def list_(source_type, source_repository, source_branch, source_dir):
    try:
        data_source = DataSource.from_type(source_type, source_repository, source_branch, source_dir)
        info = [(t.name, t.description) for t in template.get_templates(data_source=data_source)]
        printer.print_table(info, descriptors=['name', 'description'])
    finally:
        data.cleanup()


@templates.command(help='[Inspect all the available configurable options]')
@click.argument('name', required=True)
@click.option('--source_type', default=DataSourceType.REMOTE.name,
              type=click.Choice(DataSourceType.get_keys(), case_sensitive=False), help='[Template type]')
@click.option('--source_repository', default='capco-templates')
@click.option('--source_branch', default='master')
@click.option('--source_dir', default='.', help='[If local source, specify the path]')
def inspect(name, source_type, source_repository, source_branch, source_dir):
    try:
        data_source = DataSource.from_type(source_type, source_repository, source_branch, source_dir)
        temp = template.Template.load(name, data_source=data_source)

        printer.print_header('Info')
        info = [[temp.description, temp.version]]
        printer.print_table(info, descriptors=['description', 'version'], include_headers=False)

        printer.print_header('Options')
        options = [o for o in temp.accepted_options if o.is_configurable]
        options = sorted([[o.name, o.default, o.accepted_values] for o in options])
        printer.print_table(options, descriptors=['name', 'default', 'accepted values'])
    finally:
        data.cleanup()
