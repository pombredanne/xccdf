# -*- coding: utf-8 -*-

# Python stdlib
import unittest
import os
import io
from xml.etree import ElementTree

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

        element_tree = ElementTree.fromstring(xml_string)

        return element_tree[0]

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


def suite():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTest(loader.loadTestsFromTestCase(DescriptionTestCase))
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
