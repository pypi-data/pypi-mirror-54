import click
from tabulate import tabulate


TABLE_FORMAT = 'fancy_grid'


def print_info(text):
    click.secho(text)


def print_success(text):
    click.secho(text, fg='green')


def print_warning(text):
    click.secho(text, fg='yellow')


def print_error(text):
    click.secho(text, fg='red')


def print_header(text):
    click.echo('\n{}'.format(text))


def print_table(data, descriptors, include_headers=True):
    table = _get_table(data, descriptors, include_headers)
    click.echo('\n{}\n'.format(table))


def _get_table(data, descriptors, include_headers):
    if include_headers:
        return _tabulate(data, descriptors)

    merged_data = []
    for d in data:
        merged_data.extend(list(zip(descriptors, d)))

    return _tabulate(merged_data)


def _tabulate(data, headers=None):
    if headers:
        return tabulate(data, headers=headers, tablefmt=TABLE_FORMAT)

    return tabulate(data, tablefmt=TABLE_FORMAT)
