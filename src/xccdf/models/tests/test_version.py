# -*- coding: utf-8 -*-

# Python stdlib
import unittest
import os
import io
from xml.etree import ElementTree

# XCCDF
from xccdf.models.version import Version
from xccdf.exceptions import RequiredAttributeException


class VersionTestCase(unittest.TestCase):

    """
    Test cases for Title class
    """

    def load_example_element(self, xml_file_type='ok'):
        """
        Helper method to load an XML element
        """

        file_name = 'example_xccdf_version_{type}.xml'.format(
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

    def create_version_object(self, object_type='ok'):
        """
        Helper method to create the Version object

        :returns: Version object
        :rtype: xccdf.models.version.Version
        """

        xml_element = self.load_example_element(object_type)

        return Version(xml_element)

    def test_init_all_ok(self):
        """
        Tests the class constructor
        """

        xccdf_version = self.create_version_object('ok')

        self.assertEqual(xccdf_version.name, 'version',
                         'version tag name does not match')

        self.assertTrue(hasattr(xccdf_version, 'text'))

    def test_init_no_version(self):
        """
        Tests the class constructor without a version number
        """

        error_msg = 'version content is required'
        with self.assertRaisesRegex(RequiredAttributeException,
                                    error_msg):
            self.create_version_object('no_content')

    def test_init_no_xml_element(self):
        """
        Tests the class constructor from an empty instance
        """
        version = '1.0.0'
        xccdf_version = Version(version=version)

        self.assertEqual(xccdf_version.name, 'version',
                         'version tag name does not match')

        self.assertEqual(xccdf_version.text, version,
                         'version does not match')

        self.assertFalse(hasattr(xccdf_version, 'xml_element'))

    def test_init_empty_instance(self):
        """
        Tests the class constructor with an empty instance
        """

        error_msg = 'either xml_element or version are required'
        with self.assertRaisesRegex(ValueError,
                                    error_msg):
            Version()

    def test_print_object(self):
        """
        Tests the string representation of an Version object
        """

        xccdf_version = self.create_version_object('ok')

        string_value = 'version {version}'.format(version=xccdf_version.text)
        self.assertEqual(str(xccdf_version), string_value,
                         'String representation does not match')

    def test_print_object_empty_instance(self):
        """
        Tests the string representation of an Version object
        from an empty instance
        """

        version = '1.0.0'
        xccdf_version = Version(version=version)

        string_value = 'version {version}'.format(version=version)
        self.assertEqual(str(xccdf_version), string_value,
                         'String representation does not match')


def suite():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTest(loader.loadTestsFromTestCase(VersionTestCase))
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
