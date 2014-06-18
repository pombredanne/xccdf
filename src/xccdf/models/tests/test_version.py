# -*- coding: utf-8 -*-

# Python stdlib
import unittest
import os
import io
import sys

# lxml
from lxml import etree

# XCCDF
from xccdf.models.version import Version, TailoringVersion
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

        element_tree = etree.fromstring(xml_string.encode('utf-8'))

        return element_tree[1]

    def create_version_object(self, object_type='ok'):
        """
        Helper method to create the Version object

        :returns: Version object
        :rtype: xccdf.models.version.Version
        """

        xml_element = self.load_example_element(object_type)

        return Version(xml_element)

    def create_tailoring_version_object(self, object_type='ok'):
        """
        Helper method to create the Version object

        :returns: Version object
        :rtype: xccdf.models.version.Version
        """

        xml_element = self.load_example_element(object_type)

        return TailoringVersion(xml_element)

    def test_init_all_ok(self):
        """
        Tests the class constructor
        """

        xccdf_version = self.create_version_object('ok')

        self.assertEqual(xccdf_version.name, 'version',
                         'version tag name does not match')

        self.assertTrue(hasattr(xccdf_version, 'text'))

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

        if sys.version_info[0] >= 3 and sys.version_info[1] >= 2:
            with self.assertRaisesRegex(ValueError,
                                        error_msg):
                Version()
        else:
            with self.assertRaisesRegexp(ValueError,
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

    def test_method_time_to_str(self):
        """
        Tests the time_to_str method
        """

        xccdf_version = self.create_version_object('ok')

        self.assertEqual(xccdf_version.time_to_str(),
                         xccdf_version.xml_element.attrib['time'],
                         'time_to_str timestamp string does not match')

    def test_method_update_xml_element(self):
        """
        Tests the update_xml_element method
        """

        xccdf_version = self.create_version_object('ok')

        new_text = '2.0.0.0'

        self.assertNotEqual(xccdf_version.text, new_text,
                            'New text is equal to original')

        xccdf_version.text = new_text
        xccdf_version.update_xml_element()

        self.assertEqual(xccdf_version.xml_element.text, new_text,
                         'XML text does not match new text')
        self.assertEqual(xccdf_version.text, new_text,
                         'Title text does not match new text')

    def test_method_update_xml_element_empty_instance(self):
        """
        Tests the update_xml_element method
        """

        version = '2.0.0.1'
        xccdf_version = Version(version=version)

        self.assertFalse(hasattr(xccdf_version, 'xml_element'),
                         'XML element is defined')

        xccdf_version.update_xml_element()

        self.assertTrue(hasattr(xccdf_version, 'xml_element'),
                        'XML element is not defined')

    def test_method_to_xml_string(self):
        """
        Tests the to_xml_string method
        """

        xccdf_version = self.create_version_object('ok')

        xml_content = xccdf_version.to_xml_string()

        new_xccdf_version = Version(
            etree.fromstring(xml_content.encode('utf-8')))

        self.assertEqual(xccdf_version.text, new_xccdf_version.text,
                         'Version text does not match')

    def test_tailoring_version_init_all_ok(self):
        """
        Tests the class constructor of TailoringVersion
        """

        xccdf_version = self.create_tailoring_version_object('ok')

        self.assertEqual(xccdf_version.name, 'version',
                         'version tag name does not match')

        self.assertEqual(xccdf_version.text, xccdf_version.xml_element.text,
                         'version text does not match')

        self.assertTrue(hasattr(xccdf_version, 'time'))

    def test_tailoring_version_init_no_time(self):
        """
        Tests the class constructor of TailoringVersion without time attr
        """

        error_msg = 'time is required'
        if sys.version_info[0] >= 3 and sys.version_info[1] >= 2:
            with self.assertRaisesRegex(RequiredAttributeException,
                                        error_msg):
                self.create_tailoring_version_object('no_time')
        else:
            with self.assertRaisesRegexp(RequiredAttributeException,
                                         error_msg):
                self.create_tailoring_version_object('no_time')


def suite():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTest(loader.loadTestsFromTestCase(VersionTestCase))
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
