import unittest
from click.testing import CliRunner
from unittest import mock
from unittest.mock import patch

from src.commands.projects import create


class TestCliProjectCreation(unittest.TestCase):

    def setUp(self):
        self.runner = CliRunner()

    @patch('src.commands.projects.Template')
    def test_create_accepts_template_name(self, mock_template):
        result = self.runner.invoke(create, '--template test-template')

        self.assertEqual(0, result.exit_code, 'Returned output was "{}"'.format(result.output))
        mock_template.load.assert_called_once_with('test-template', data_source=mock.ANY)

    def test_create_requires_template_name(self):
        result = self.runner.invoke(create)

        self.assertIn('Missing option', result.output)
        self.assertEqual(2, result.exit_code)

    @patch('src.commands.projects.Project')
    @patch('src.commands.projects.Template')
    def test_create_accepts_single_option(self, mock_template, mock_project):
        result = self.runner.invoke(create, '--template test-template --option key=value')

        self.assertEqual(0, result.exit_code, 'Returned output was "{}"'.format(result.output))
        mock_project.generate.assert_called_once_with(mock.ANY, {'key': 'value'}, mock.ANY)

    @patch('src.commands.projects.Project')
    @patch('src.commands.projects.Template')
    def test_create_accepts_multiple_options(self, mock_template, mock_project):
        result = self.runner.invoke(create, '--template test-template --option key1=value1 --option key2=value2')

        self.assertEqual(0, result.exit_code, 'Returned output was "{}"'.format(result.output))
        mock_project.generate.assert_called_once_with(mock.ANY, {'key1': 'value1', 'key2': 'value2'}, mock.ANY)

    @patch('src.commands.projects.Project')
    @patch('src.commands.projects.Template')
    def test_create_accepts_target_dir(self, mock_template, mock_project):
        result = self.runner.invoke(create, '--template test-template --target_dir test')

        self.assertEqual(0, result.exit_code, 'Returned output was "{}"'.format(result.output))
        mock_project.generate.assert_called_once_with(mock.ANY, mock.ANY, 'test')
