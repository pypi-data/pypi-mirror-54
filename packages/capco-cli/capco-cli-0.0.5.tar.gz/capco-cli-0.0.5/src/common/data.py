import os
import shutil
from abc import ABC, abstractmethod
from enum import Enum, auto

from src.common import constants
from src.connectors import bitbucket
from src.utils import os_utils, printer


LOCAL_DOWNLOAD_DIR = os.path.join(constants.LOCAL_BASE_DIR, 'download')


class DataSourceType(Enum):
    LOCAL = auto()
    REMOTE = auto()

    @staticmethod
    def get_keys():
        return [name for name, value in vars(DataSourceType).items()]


class DataSource(ABC):

    def __init__(self, dir_):
        self.dir = dir_

    @classmethod
    def from_type(cls, type_, repository, branch, dir_):
        if type_ == DataSourceType.REMOTE.name:
            return RemoteDataSource(repository, branch, dir_)

        printer.print_warning(
            'Retrieving template information from local disk. '
            'Values for repository and branch will be ignored.')
        return LocalDataSource(dir_)

    @abstractmethod
    def read_file(self, path_to_file):
        """
        Returns the contents of the file located at the given path, in unicode.

        The value of path_to_file must be relative to self._dir.
        """
        pass

    @abstractmethod
    def read_dir(self, path_to_dir):
        """
        Returns a list of absolute paths to the files and subdirectories
        inside a given directory.

        The value of path_to_dir must be relative to self._dir.
        """
        pass

    @abstractmethod
    def get_as_local_dir(self, path_to_dir):
        """
        Returns an absolute path in local disk to a given directory. If the
        directory is not originally in local disk it will be downloaded first.

        The value of path_to_dir must be relative to self._dir.
        """
        pass

    def _complete_path(self, path_to_resource):
        return os.path.join(self.dir, path_to_resource)


class RemoteDataSource(DataSource):
    """
    Represents a data source located remotely; currently a remote source always
    refers to a directory located in a bitbucket repository.

    Optionally the branch in the repository can also be specified.
    """
    def __init__(self, repo_name, branch, dir_):
        super().__init__(dir_)

        self._repository = bitbucket.Repository(repo_name)
        self._branch = branch

    def read_file(self, path_to_file):
        return self._repository.get_file_content(
            self._complete_path(path_to_file), branch=self._branch)

    def read_dir(self, path_to_dir):
        return self._repository.get_dir_content(
            os.path.join(self.dir, path_to_dir), branch=self._branch)

    def get_as_local_dir(self, path_to_dir):
        paths = self._repository.get_dir_content(
            os.path.join(self.dir, path_to_dir), files_only=True, recursive=True, branch=self._branch)

        for path in paths:
            self._download_file(path, os.path.join(LOCAL_DOWNLOAD_DIR, path))

        return os.path.join(LOCAL_DOWNLOAD_DIR, path_to_dir)

    def _download_file(self, path_in_source, path_in_local):
        content = self.read_file(path_in_source)

        os_utils.write(content, path_in_local)

        printer.print_success('Downloaded file {} from repository {} to {}'.format(
            os.path.join(self.dir, path_in_source), self._repository.name, path_in_local))


class LocalDataSource(DataSource):
    """
    Represents a data source located locally; currently a local source always
    refers to a directory located in local disk.
    """
    def __init__(self, dir_):
        super().__init__(dir_)

    def read_file(self, path_to_file):
        return os_utils.read(os.path.join(self.dir, path_to_file))

    def read_dir(self, path_to_dir):
        return os.listdir(os.path.join(self.dir, path_to_dir))

    def get_as_local_dir(self, path_to_dir):
        # directory already exists in local disk
        return os.path.join(self.dir, path_to_dir)


def cleanup():
    shutil.rmtree(LOCAL_DOWNLOAD_DIR, ignore_errors=True)
