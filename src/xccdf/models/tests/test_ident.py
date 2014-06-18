# -*- coding: utf-8 -*-

# Python stdlib
import unittest
import os
import io
import sys

# lxml
from lxml import etree

# XCCDF
from xccdf.models.ident import Ident
from xccdf.exceptions import RequiredAttributeException


class IdentTestCase(unittest.TestCase):

    """
    Test cases for Ident class
    """

    def load_example_element(self, xml_file_type='ok'):
        """
        Helper method to load an XML element
        """

        file_name = 'example_xccdf_ident_{type}.xml'.format(
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

    def create_ident_object(self, object_type='ok'):
        """
        Helper method to create the Ident object

        :returns: Ident object
        :rtype: xccdf.models.ident.Ident
        """

        xml_element = self.load_example_element(object_type)

        return Ident(xml_element)

    def test_init_all_ok(self):
        """
        Tests the class constructor
        """

        xccdf_ident = self.create_ident_object('ok')

        self.assertEqual(xccdf_ident.name, 'ident',
                         'ident tag name does not match')
        self.assertEqual(xccdf_ident.system,
                         xccdf_ident.xml_element.attrib['system'],
                         'ident system attribute does not match')
        self.assertEqual(xccdf_ident.text, xccdf_ident.xml_element.text,
                         'ident tag name does not match')

    def test_init_no_ident(self):
        """
        Tests the class constructor without a ident code
        """

        error_msg = 'ident is required'

        if sys.version_info[0] >= 3 and sys.version_info[1] >= 2:
            with self.assertRaisesRegex(RequiredAttributeException,
                                        error_msg):
                self.create_ident_object('no_ident')
        else:
            with self.assertRaisesRegexp(RequiredAttributeException,
                                         error_msg):
                self.create_ident_object('no_ident')

    def test_init_no_system(self):
        """
        Tests the class constructor without a system uri
        """

        error_msg = 'system attribute is required'

        if sys.version_info[0] >= 3 and sys.version_info[1] >= 2:
            with self.assertRaisesRegex(RequiredAttributeException,
                                        error_msg):
                self.create_ident_object('no_system')
        else:
            with self.assertRaisesRegexp(RequiredAttributeException,
                                         error_msg):
                self.create_ident_object('no_system')

    def test_init_no_xml_element(self):
        """
        Tests the class constructor from an empty instance
        """

        ident = 'CCE-14457-6'
        system = 'http://cce.mitre.org'
        xccdf_ident = Ident(ident=ident, system=system)

        self.assertEqual(xccdf_ident.name, 'ident',
                         'ident tag name does not match')
        self.assertEqual(xccdf_ident.text, ident,
                         'ident does not match')
        self.assertEqual(xccdf_ident.system, system,
                         'system attribute does not match')

        self.assertFalse(hasattr(xccdf_ident, 'xml_element'))

    def test_init_empty_instance(self):
        """
        Tests the class constructor with an empty instance
        """

        error_msg = 'either xml_element or ident and system are required'

        if sys.version_info[0] >= 3 and sys.version_info[1] >= 2:
            with self.assertRaisesRegex(ValueError,
                                        error_msg):
                Ident()
        else:
            with self.assertRaisesRegexp(ValueError,
                                         error_msg):
                Ident()

    def test_print_object(self):
        """
        Tests the string representation of an Version object
        """

        xccdf_ident = self.create_ident_object('ok')

        string_value = 'ident {ident}'.format(ident=xccdf_ident.text)
        self.assertEqual(str(xccdf_ident), string_value,
                         'String representation does not match')

    def test_print_object_empty_instance(self):
        """
        Tests the string representation of an Version object
        from an empty instance
        """

        ident = 'CCE-14457-6'
        system = 'http://cce.mitre.org'
        xccdf_ident = Ident(ident=ident, system=system)

        string_value = 'ident {ident}'.format(ident=ident)
        self.assertEqual(str(xccdf_ident), string_value,
                         'String representation does not match')

    def test_method_update_xml_element(self):
        """
        Tests the update_xml_element method
        """

        xccdf_ident = self.create_ident_object('ok')

        new_text = 'CCE-22222-4'

        self.assertNotEqual(xccdf_ident.text, new_text,
                            'New text is equal to original')

        xccdf_ident.text = new_text
        xccdf_ident.update_xml_element()

        self.assertEqual(xccdf_ident.xml_element.text, new_text,
                         'XML text does not match new text')
        self.assertEqual(xccdf_ident.text, new_text,
                         'Title text does not match new text')

    def test_method_update_xml_element_empty_instance(self):
        """
        Tests the update_xml_element method
        """

        ident = 'CCE-14457-6'
        system = 'http://cce.mitre.org'
        xccdf_ident = Ident(ident=ident, system=system)

        self.assertFalse(hasattr(xccdf_ident, 'xml_element'),
                         'XML element is defined')

        xccdf_ident.update_xml_element()

        self.assertTrue(hasattr(xccdf_ident, 'xml_element'),
                        'XML element is not defined')

    def test_method_to_xml_string(self):
        """
        Tests the to_xml_string method
        """

        xccdf_ident = self.create_ident_object('ok')

        xml_content = xccdf_ident.to_xml_string()

        new_xccdf_ident = Ident(
            etree.fromstring(xml_content.encode('utf-8')))

        self.assertEqual(xccdf_ident.text, new_xccdf_ident.text,
                         'Ident text does not match')


def suite():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTest(loader.loadTestsFromTestCase(IdentTestCase))
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
