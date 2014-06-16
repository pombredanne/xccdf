# -*- coding: utf-8 -*-

# Python stdlib
import unittest
import os
import io

# lxml
from lxml import etree

# XCCDF
from xccdf.models.title import Title


class TitleTestCase(unittest.TestCase):

    """
    Test cases for Title class
    """

    def load_example_element(self, xml_file_type='ok'):
        """
        Helper method to load an XML element
        """

        file_name = 'example_xccdf_title_{type}.xml'.format(type=xml_file_type)

        xml_path = os.path.abspath(os.path.dirname(__file__))
        xml_file = io.open(os.path.join(
            xml_path,
            'examples',
            file_name))

        xml_string = xml_file.read()
        xml_file.close()

        element_tree = etree.fromstring(xml_string.encode('utf-8'))

        return element_tree[1]

    def create_title_object(self, object_type='ok'):
        """
        Helper method to create the Title object

        :returns: Title object
        :rtype: xccdf.models.title.Title
        """

        xml_element = self.load_example_element(object_type)

        return Title(xml_element)

    def test_init_all_with_xml_element(self):
        """
        Tests the class constructor with a xml element
        """

        xccdf_title = self.create_title_object('ok')

        self.assertEqual(xccdf_title.name, 'title',
                         'Title tag name does not match')

    def test_init_all_with_empty_instace(self):
        """
        Tests the class constructor with an empty instance
        """

        xccdf_title = Title()

        self.assertEqual(xccdf_title.name, 'title',
                         'Title tag name does not match')

    def test_print_object(self):
        """
        Tests the string representation of an Title object
        """

        xccdf_title = self.create_title_object('ok')

        string_value = 'title {title} ({lang})'.format(title=xccdf_title.text,
                                                       lang=xccdf_title.lang)
        self.assertEqual(str(xccdf_title), string_value,
                         'String representation does not match')

    def test_print_object_empty_instance(self):
        """
        Tests the string representation of an Title object
        from an empty instance
        """

        xccdf_title = Title()

        string_value = 'title'
        self.assertEqual(str(xccdf_title), string_value,
                         'String representation does not match')

    def test_print_object_no_lang(self):
        """
        Tests the string representation of an Title object without a lang
        """

        xccdf_title = self.create_title_object('no_lang')

        string_value = 'title {title}'.format(title=xccdf_title.text)
        self.assertEqual(str(xccdf_title), string_value,
                         'String representation does not match')


def suite():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTest(loader.loadTestsFromTestCase(TitleTestCase))
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
