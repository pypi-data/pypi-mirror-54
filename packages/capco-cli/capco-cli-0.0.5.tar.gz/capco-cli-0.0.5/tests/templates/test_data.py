import unittest

from src.templates.data import DataParser


class TestDataParserClass(unittest.TestCase):

    def test_parse_info_returns_data_from_manifest(self):
        manifest = '''
        version: 1.0
        description: A template for testing
        options:
            option1:
                default: gradle
                configurable: no
                accepted_values:
                    - value1
                    - value2
        '''

        returned = DataParser.parse_info_data(manifest)

        self.assertEqual(returned[0], '1.0')
        self.assertEqual(returned[1], 'A template for testing')
        self.assertEqual(returned[2], False)
