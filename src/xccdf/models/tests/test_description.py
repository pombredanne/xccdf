# -*- coding: utf-8 -*-

# Python stdlib
import unittest
import os
import io

# lxml
from lxml import etree

# XCCDF
from xccdf.models.description import Description


class DescriptionTestCase(unittest.TestCase):

    """
    Test cases for Title class
    """

    def load_example_element(self, xml_file_type='ok'):
        """
        Helper method to load an XML element
        """

        file_name = 'example_xccdf_description_{type}.xml'.format(
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

    def create_description_object(self, object_type='ok'):
        """
        Helper method to create the Description object

        :returns: Description object
        :rtype: xccdf.models.description.Description
        """

        xml_element = self.load_example_element(object_type)

        return Description(xml_element)

    def test_init_with_xml_element(self):
        """
        Tests the class constructor with a xml element
        """

        xccdf_description = self.create_description_object('ok')

        self.assertEqual(xccdf_description.name, 'description',
                         'Description tag name does not match')

    def test_init_with_emtpy_instance(self):
        """
        Tests the class constructor with an empty instance
        """

        xccdf_description = Description()

        self.assertEqual(xccdf_description.name, 'description',
                         'Description tag name does not match')

    def test_print_object(self):
        """
        Tests the string representation of an Description object
        """

        xccdf_description = self.create_description_object('ok')

        string_value = 'description {desc} ({lang})'.format(
            desc=xccdf_description.content,
            lang=xccdf_description.lang)
        self.assertEqual(str(xccdf_description), string_value,
                         'String representation does not match')

    def test_print_object_empty_instance(self):
        """
        Tests the string representation of an Description object
        from an empty instance
        """

        xccdf_description = Description()

        string_value = 'description'
        self.assertEqual(str(xccdf_description), string_value,
                         'String representation does not match')

    def test_print_object_no_lang(self):
        """
        Tests the string representation of an Description object without a lang
        """

        xccdf_description = self.create_description_object('no_lang')

        string_value = 'description {desc}'.format(
            desc=xccdf_description.content)
        self.assertEqual(str(xccdf_description), string_value,
                         'String representation does not match')

    def test_method_update_xml_element(self):
        """
        Tests the update_xml_element method
        """

        xccdf_description = self.create_description_object('ok')

        new_content = 'Test content'

        self.assertNotEqual(xccdf_description.content, new_content,
                            'New content is equal to original')

        xccdf_description.content = new_content
        xccdf_description.update_xml_element()

        self.assertEqual(xccdf_description.xml_element.text, new_content,
                         'XML content does not match new content')
        self.assertEqual(xccdf_description.content, new_content,
                         'Description content does not match new content')

    def test_method_to_xml_string(self):
        """
        Tests the to_xml_string method
        """

        xccdf_description = self.create_description_object('ok')

        xml_content = xccdf_description.to_xml_string()

        new_xccdf_description = Description(
            etree.fromstring(xml_content.encode('utf-8')))

        self.assertEqual(xccdf_description.text, new_xccdf_description.text,
                         'Title text does not match')
        self.assertEqual(xccdf_description.lang, new_xccdf_description.lang,
                         'Title lang does not match')
        self.assertEqual(xccdf_description.override,
                         new_xccdf_description.override,
                         'Title override does not match')


def suite():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTest(loader.loadTestsFromTestCase(DescriptionTestCase))
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
