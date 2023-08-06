import http

from requests import HTTPError

from src.common import security
from src.connectors.api import RestApiRunner
from src.utils import printer


identifier = 'bb'
base_uri = 'https://api.bitbucket.org'
owner = 'ilabs-capco'


class Repository:

    DEFAULT_BRANCH = 'master'

    def __init__(self, name):
        self.name = name

        username, password = _get_credentials()
        self.runner = RestApiRunner(base_uri, username, password)

    def get_file_content(self, path_to_file, branch=DEFAULT_BRANCH):
        return self._get_source(path_to_file, branch).text

    def get_dir_content(self, path_to_dir, files_only=False, recursive=False, branch=DEFAULT_BRANCH):
        paths = []
        queue = [path_to_dir]

        while queue:
            current_path = queue.pop(0)
            response = self._get_source(current_path, branch)

            for value in _read_values(response):
                next_type = value.get('type')
                next_path = value.get('path')

                if next_type == 'commit_directory':
                    if recursive:
                        queue.append(next_path)

                    if not files_only:
                        paths.append(next_path)

                if next_type == 'commit_file':
                    paths.append(next_path)

        return paths

    def _get_source(self, path_to_source='', branch=DEFAULT_BRANCH):
        uri = '2.0/repositories/{owner}/{repository}/src/{branch}/{path}'.format(
            owner=owner,
            repository=self.name,
            branch=branch,
            path=path_to_source)

        try:
            response = self.runner.get(uri)
            return response
        except HTTPError as e:
            if e.response.status_code == http.client.NOT_FOUND:
                raise ValueError('Specified path [{}] not found in repository {}'.format(path_to_source, self.name))


def _get_credentials():
    warning = """
No credentials configured locally for bitbucket. Please generate a new app password as per this guide:
https://confluence.atlassian.com/bitbucket/app-passwords-828781300.html#Apppasswords-Createanapppassword
with read-access to repositories and projects. Once done, input your app password and username below."""

    username, password = security.read_credentials(identifier)
    if username is None or password is None:
        printer.print_warning(warning)

        password = input('Input app password: ')
        username = input('Input username: ')

        security.write_credentials(identifier, username, password)

    return username, password


def _read_values(response):
    return response.json().get('values')
