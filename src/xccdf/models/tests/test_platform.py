# -*- coding: utf-8 -*-

# Python stdlib
import unittest
import os
import io
from xml.etree import ElementTree

# XCCDF
from xccdf.models.platform import Platform
from xccdf.exceptions import RequiredAttributeException


class PlatformTestCase(unittest.TestCase):

    """
    Test cases for Title class
    """

    def load_example_element(self, xml_file_type='ok'):
        """
        Helper method to load an XML element
        """

        file_name = 'example_xccdf_platform_{type}.xml'.format(
            type=xml_file_type)

        xml_path = os.path.abspath(os.path.dirname(__file__))
        xml_file = io.open(os.path.join(
            xml_path,
            'examples',
            file_name))

        xml_string = xml_file.read()
        xml_file.close()

        element_tree = ElementTree.fromstring(xml_string)

        return element_tree[0]

    def create_platform_object(self, object_type='ok'):
        """
        Helper method to create the Platform object

        :returns: Platform object
        :rtype: xccdf.models.platform.Platform
        """

        xml_element = self.load_example_element(object_type)

        return Platform(xml_element)

    def test_init_all_ok(self):
        """
        Tests the class constructor
        """

        xccdf_platform = self.create_platform_object('ok')

        self.assertEqual(xccdf_platform.tag_name, 'platform',
                         'platform tag name does not match')

        self.assertTrue(hasattr(xccdf_platform, 'idref'))

    def test_init_no_idref(self):
        """
        Tests the class constructor without an id
        """

        error_msg = 'idref attribute required'
        with self.assertRaisesRegex(RequiredAttributeException,
                                    error_msg):
            self.create_platform_object('no_idref')

    def test_print_object(self):
        """
        Tests the string representation of an Platform object
        """

        xccdf_platform = self.create_platform_object('ok')

        string_value = '{idref}'.format(idref=xccdf_platform.idref)
        self.assertEqual(str(xccdf_platform), string_value,
                         'String representation does not match')


def suite():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTest(loader.loadTestsFromTestCase(PlatformTestCase))
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
