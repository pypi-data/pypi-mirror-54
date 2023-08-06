import unittest

from src.templates.template import OptionInfo, Template, SingleTemplate


def _make_option(name='option', default='default', configurable=False, accepted_values=None):
    return OptionInfo(name, default, configurable, accepted_values or [])


def _make_template(main, subs=None):
    return Template(main, subs or [])


def _make_single_template(
        name='single-template', version='1.0', description='single template', hidden=False, options=None):
    return SingleTemplate(name, version, description, hidden, options or [], None)


class TestTemplateClass(unittest.TestCase):

    def test_accepted_options_returns_values_from_main_and_sub_templates(self):
        sub_option = _make_option('sub-option-1', 'sub-default-1')
        main_option = _make_option('main-option-1', 'main-default-1')

        sub = _make_single_template(options=[sub_option])
        main = _make_single_template(options=[main_option])
        template = _make_template(main, [sub])

        returned = template.accepted_options

        self.assertEqual(len(returned), 2)
        self.assertTrue(main_option in returned)
        self.assertTrue(sub_option in returned)

    def test_accepted_options_returns_value_from_main_template_when_option_in_both_main_and_sub_template(self):
        name = 'option-1'
        default_main = 'main-default-1'
        default_sub = 'sub-default-1'

        sub_option = _make_option(name, default_sub)
        main_option = _make_option(name, default_main)

        sub = _make_single_template(options=[sub_option])
        main = _make_single_template(options=[main_option])
        template = _make_template(main, [sub])

        returned = template.accepted_options

        self.assertEqual(len(returned), 1)
        self.assertEqual(returned[0].name, name)
        self.assertEqual(returned[0].default, default_main)
