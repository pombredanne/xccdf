# -*- coding: utf-8 -*-

# Python stdlib
import unittest
import os
import io
import sys

# lxml
from lxml import etree

# XCCDF
from xccdf.models.rule import Rule
from xccdf.exceptions import RequiredAttributeException
from xccdf.exceptions import CardinalityException


class RuleTestCase(unittest.TestCase):

    """
    Test cases for Rule class
    """

    def load_example_element(self, xml_file_type='ok'):
        """
        Helper method to load an XML element
        """

        file_name = 'example_xccdf_rule_{type}.xml'.format(
            type=xml_file_type)

        xml_path = os.path.abspath(os.path.dirname(__file__))
        xml_file = io.open(os.path.join(
            xml_path,
            'examples',
            file_name))

        xml_string = xml_file.read()
        xml_file.close()

        element_tree = etree.fromstring(xml_string.encode('utf-8'))

        return element_tree[1]

    def create_rule_object(self, object_type='ok'):
        """
        Helper method to create the Rule object

        :returns: Rule object
        :rtype: xccdf.models.description.Rule
        """

        xml_element = self.load_example_element(object_type)

        return Rule(xml_element)

    def test_init_with_xml_element(self):
        """
        Tests the class constructor with a xml element
        """

        xccdf_rule = self.create_rule_object('ok')

        self.assertEqual(xccdf_rule.name, 'Rule',
                         'Rule tag name does not match')
        self.assertTrue(hasattr(xccdf_rule, 'id'),
                        'Rule ID must be defined')

    def test_init_no_id(self):
        """
        Tests the class constructor with a xml element
        """

        error_msg = 'id attribute required'

        if sys.version_info[0] >= 3 and sys.version_info[1] >= 2:
            with self.assertRaisesRegex(RequiredAttributeException,
                                        error_msg):
                self.create_rule_object('no_id')
        else:
            with self.assertRaisesRegexp(RequiredAttributeException,
                                         error_msg):
                self.create_rule_object('no_id')

    def test_init_with_empty_instance(self):
        """
        Tests the class constructor with an empty instance
        """

        error_msg = 'either xml_element or id are required'

        if sys.version_info[0] >= 3 and sys.version_info[1] >= 2:
            with self.assertRaisesRegex(ValueError,
                                        error_msg):
                Rule()
        else:
            with self.assertRaisesRegexp(ValueError,
                                         error_msg):
                Rule()

    def test_init_no_xml_element(self):
        """
        Tests the class constructor with no xml_element
        """

        id = "usgcb-rhel5desktop-rule-2.2.2.5.b"
        xccdf_rule = Rule(id=id)

        self.assertEqual(xccdf_rule.name, 'Rule',
                         'Rule tag name does not match')
        self.assertEqual(xccdf_rule.id, id,
                         'Rule id does not match')
        self.assertEqual(xccdf_rule.children, list(),
                         'Rule children list must be empty')

    def test_init_duplicated_version(self):
        """
        Tests the class constructor with more than one version
        """

        error_msg = 'version element found more than once'

        if sys.version_info[0] >= 3 and sys.version_info[1] >= 2:
            with self.assertRaisesRegex(CardinalityException,
                                        error_msg):
                self.create_rule_object('duplicated_version')
        else:
            with self.assertRaisesRegexp(CardinalityException,
                                         error_msg):
                self.create_rule_object('duplicated_version')

    def test_print_object(self):
        """
        Tests the string representation of an Rule object
        """

        xccdf_rule = self.create_rule_object('ok')

        string_value = 'Rule {id}'.format(
            id=xccdf_rule.id)
        self.assertEqual(str(xccdf_rule), string_value,
                         'String representation does not match')

    def test_print_object_empty_instance(self):
        """
        Tests the string representation of an Rule object
        from an empty instance
        """

        id = "usgcb-rhel5desktop-rule-2.2.2.5.b"
        xccdf_rule = Rule(id=id)

        string_value = 'Rule {id}'.format(
            id=id)
        self.assertEqual(str(xccdf_rule), string_value,
                         'String representation does not match')

    def test_method_update_xml_element(self):
        """
        Tests the update_xml_element method
        """

        xccdf_rule = self.create_rule_object('ok')

        new_id = 'new_rule_id_test'

        self.assertNotEqual(xccdf_rule.id, new_id,
                            'New id is equal to original')

        xccdf_rule.id = new_id
        xccdf_rule.update_xml_element()

        self.assertEqual(xccdf_rule.xml_element.attrib['id'], new_id,
                         'XML id does not match new id')
        self.assertEqual(xccdf_rule.id, new_id,
                         'Title id does not match new id')

    def test_method_update_xml_element_empty_instance(self):
        """
        Tests the update_xml_element method with an empty instance
        """

        id = 'united_states_government_configuration_baseline'
        xccdf_rule = Rule(id=id)

        self.assertFalse(hasattr(xccdf_rule, 'xml_element'),
                         'XML element is defined')

        xccdf_rule.update_xml_element()

        self.assertTrue(hasattr(xccdf_rule, 'xml_element'),
                        'XML element is not defined')


def suite():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTest(loader.loadTestsFromTestCase(RuleTestCase))
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
