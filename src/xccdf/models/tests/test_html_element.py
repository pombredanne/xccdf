# -*- coding: utf-8 -*-

# Python stdlib
import unittest
import os
import io
import re
from xml.etree import ElementTree

# lxml
from lxml import etree

# XCCDF
from xccdf.models.html_element import HTMLElement


class HTMLElementTestCase(unittest.TestCase):

    """
    Test cases for HTMLElement class
    """

    def load_example_element(self, xml_file_type='ok'):
        """
        Helper method to load an XML element
        """

        file_name = 'example_xccdf_html_element_{type}.xml'.format(
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

    def create_html_object(self, object_type='ok'):
        """
        Helper method to create the HTMLElement object

        :returns: HTMLElement object
        :rtype: xccdf.models.description.HTMLElement
        """

        xml_element = self.load_example_element(object_type)

        return HTMLElement(xml_element)

    def test_init_with_xml_element(self):
        """
        Tests the class constructor with an xml element
        """

        xccdf_html_element = self.create_html_object('ok')

        self.assertNotEqual(xccdf_html_element.content, '', 'Content is empty')
        self.assertIsNotNone(xccdf_html_element.content, 'Content is empty')

    def test_init_empty(self):
        """
        Tests the class constructor empty
        """

        tag_name = 'html-element'
        xccdf_html_element = HTMLElement(tag_name=tag_name)

        self.assertEqual(xccdf_html_element.name, tag_name,
                         'Tag name does not match')
        self.assertFalse(hasattr(xccdf_html_element, 'content'),
                         'Content is defined in an empty instance')

    def test_method_as_dict(self):
        """
        Tests the as_dict method
        """

        xccdf_html_element = self.create_html_object('ok')

        element_dict = xccdf_html_element.as_dict()

        self.assertEqual(element_dict['content'],
                         xccdf_html_element.content,
                         'HTML content does not match')

    def test_method_as_dict_empty(self):
        """
        Tests the as_dict method from an empty object
        """

        tag_name = 'html-element'
        xccdf_html_element = HTMLElement(tag_name=tag_name)

        element_dict = xccdf_html_element.as_dict()

        self.assertEqual(element_dict.get('name', None),
                         xccdf_html_element.name,
                         'Name is not defined inside dictionary')
        self.assertIsNone(element_dict.get('content', None),
                          'Content is defined for an empty instance')

    def test_method_get_html_content(self):
        """
        Tests the get_html_content method
        """

        xccdf_html_element = self.create_html_object('ok')

        xml = xccdf_html_element.xml_element
        content_list = ["" if xml.text is None else xml.text]

        def to_string(xml):
            return ElementTree.tostring(xml).decode('utf-8')

        content_list += [to_string(e) for e in xml.getchildren()]

        full_xml_content = "".join(content_list)

        # Parse tags to generate HTML valid content
        html_content = re.sub(r'html:', '',
                              re.sub(
                                  r' xmlns:html=(["\'])(?:(?=(\\?))\2.)*?\1',
                                  '',
                                  full_xml_content))

        self.assertEqual(xccdf_html_element.content, html_content,
                         'Parsed HTML content does not match')

    def test_method_get_html_content_no_html(self):
        """
        Tests the get_html_content method without HTML content
        """

        xccdf_html_element = self.create_html_object('ok')

        xml = xccdf_html_element.xml_element
        content_list = ["" if xml.text is None else xml.text]

        def to_string(xml):
            return ElementTree.tostring(xml).decode('utf-8')

        content_list += [to_string(e) for e in xml.getchildren()]

        full_xml_content = "".join(content_list)

        # Parse tags to generate HTML valid content
        html_content = re.sub(r'html:', '',
                              re.sub(
                                  r' xmlns:html=(["\'])(?:(?=(\\?))\2.)*?\1',
                                  '',
                                  full_xml_content))

        self.assertEqual(xccdf_html_element.content, html_content,
                         'Parsed plain content does not match')

    def test_method_get_html_content_empty_instance(self):
        """
        Tests the get_html_content method in an empty instance
        """

        tag_name = 'html-element'
        xccdf_html_element = HTMLElement(tag_name=tag_name)

        self.assertEqual(xccdf_html_element.get_html_content(),
                         '',
                         'HTML content from empty instance is not empty')

    def test_method_convert_html_to_xml(self):
        """
        Tests the convert_html_to_xml method
        """

        xccdf_html_element = self.create_html_object('ok')

        xml_content = xccdf_html_element.convert_html_to_xml()

        test_xml_content = re.sub(r'<(?!/)', '<xhtml:',
                                  xccdf_html_element.content)

        self.assertEqual(xml_content, test_xml_content,
                         'Converted xml content does not match')

    def test_method_convert_html_to_xml_empty_instance(self):
        """
        Tests the convert_html_to_xml method in an empty instance
        """

        tag_name = 'html-element'
        xccdf_html_element = HTMLElement(tag_name=tag_name)

        self.assertEqual(xccdf_html_element.convert_html_to_xml(),
                         '',
                         'XML content from empty instance is not empty')

    def test_method_update_xml_element(self):
        """
        Tests the update_xml_element method
        """

        xccdf_html_element = self.create_html_object('ok')

        xccdf_html_element.update_xml_element()

        self.assertEqual(xccdf_html_element.xml_element.text,
                         xccdf_html_element.convert_html_to_xml(),
                         'Updated XML element text does not match')

    def test_method_update_xml_element_empty_instance(self):
        """
        Tests the update_xml_element method from an empty instance
        """

        tag_name = 'html-element'
        xccdf_html_element = HTMLElement(tag_name=tag_name)

        self.assertFalse(hasattr(xccdf_html_element, 'xml_element'),
                         'XML element is defined')

        xccdf_html_element.update_xml_element()

        self.assertTrue(hasattr(xccdf_html_element, 'xml_element'),
                        'XML element is not defined')


def suite():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTest(loader.loadTestsFromTestCase(HTMLElementTestCase))
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
