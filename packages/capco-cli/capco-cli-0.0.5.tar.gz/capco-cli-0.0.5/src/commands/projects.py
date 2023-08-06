import click

from src.common import data
from src.common.data import DataSourceType, DataSource
from src.templates.project import Project
from src.templates.template import Template
from src.utils import printer


@click.group()
def projects():
    """[Create boilerplate projects using available configurations]"""
    pass


@projects.command(help='[To create the project]')
@click.option('--template', required=True, help='[Name of the available template]')
@click.option('--option', multiple=True, help='[Run <capco templates inspect TEMPLATE_NAME>, to view all the options]')
@click.option('--source_type', default=DataSourceType.REMOTE.name,
              type=click.Choice(DataSourceType.get_keys(), case_sensitive=False), help='[Available options: remote,'
                                                                                       'local]')
@click.option('--source_repository', default='capco-templates')
@click.option('--source_branch', default='master')
@click.option('--source_dir', default='.', help='[If source_type is local, specify the template path]')
@click.option('--target_dir', default='.', help='[Path to the target directory]')
def create(template, option, source_type, source_repository, source_branch, source_dir, target_dir):
    options_dict = dict()
    for o in option:
        key, value = o.split('=')
        options_dict[key] = value

    try:
        data_source = DataSource.from_type(source_type, source_repository, source_branch, source_dir)
        template = Template.load(template, data_source=data_source)
        Project.generate(template, options_dict, target_dir)
    finally:
        data.cleanup()

    printer.print_success('Project created at {}'.format(target_dir))
