# -*- coding: utf-8 -*-

# Python stdlib
import unittest
import os
import io

# lxml
from lxml import etree

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

        element_tree = etree.fromstring(xml_string.encode('utf-8'))

        return element_tree[1]

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

        self.assertEqual(xccdf_platform.name, 'platform',
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

    def test_init_no_xml_element(self):
        """
        Tests the class constructor with an empty instance
        """
        idref = 'cpe:/o:redhat:enterprise_linux:5'
        xccdf_platform = Platform(idref=idref)

        self.assertEqual(xccdf_platform.name, 'platform',
                         'platform tag name does not match')

        self.assertEqual(xccdf_platform.idref, idref,
                         'platform idref does not match')

    def test_init_empty_instance(self):
        """
        Tests the class constructor with an empty instance
        """

        error_msg = 'either xml_element or idref are required'
        with self.assertRaisesRegex(ValueError,
                                    error_msg):
            Platform()

    def test_print_object(self):
        """
        Tests the string representation of an Platform object
        """

        xccdf_platform = self.create_platform_object('ok')

        string_value = 'platform {idref}'.format(idref=xccdf_platform.idref)
        self.assertEqual(str(xccdf_platform), string_value,
                         'String representation does not match')

    def test_method_update_xml_element(self):
        """
        Tests the update_xml_element method
        """

        xccdf_platform = self.create_platform_object('ok')

        new_idref = 'cpe:test:test:test'

        self.assertNotEqual(xccdf_platform.idref, new_idref,
                            'New idref is equal to original')

        xccdf_platform.idref = new_idref
        xccdf_platform.update_xml_element()

        self.assertEqual(xccdf_platform.xml_element.attrib['idref'], new_idref,
                         'XML idref does not match new idref')
        self.assertEqual(xccdf_platform.idref, new_idref,
                         'Title idref does not match new idref')

    def test_method_update_xml_element_empty_instance(self):
        """
        Tests the update_xml_element method
        """

        idref = 'cpe:/o:redhat:enterprise_linux:5'
        xccdf_platform = Platform(idref=idref)

        self.assertFalse(hasattr(xccdf_platform, 'xml_element'),
                         'XML element is defined')

        xccdf_platform.update_xml_element()

        self.assertTrue(hasattr(xccdf_platform, 'xml_element'),
                        'XML element is not defined')

    def test_method_to_xml_string(self):
        """
        Tests the to_xml_string method
        """

        xccdf_platform = self.create_platform_object('ok')

        xml_content = xccdf_platform.to_xml_string()

        new_xccdf_platform = Platform(
            etree.fromstring(xml_content.encode('utf-8')))

        self.assertEqual(xccdf_platform.idref, new_xccdf_platform.idref,
                         'Platform idref does not match')


def suite():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTest(loader.loadTestsFromTestCase(PlatformTestCase))
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
