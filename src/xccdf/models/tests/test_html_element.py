# -*- coding: utf-8 -*-

# Python stdlib
import unittest
import os
import io
import re
from xml.etree import ElementTree

# XCCDF
from xccdf.models.html_element import HTMLElement


class HTMLElementTestCase(unittest.TestCase):

    """
    Test cases for Title class
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

        element_tree = ElementTree.fromstring(xml_string)

        return element_tree[0]

    def create_description_object(self, object_type='ok'):
        """
        Helper method to create the Description object

        :returns: Description object
        :rtype: xccdf.models.description.Description
        """

        xml_element = self.load_example_element(object_type)

        return HTMLElement(xml_element)

    def test_init_all_ok(self):
        """
        Tests the class constructor
        """

        xccdf_html_element = self.create_description_object('ok')

        self.assertNotEqual(xccdf_html_element.content, '', 'Content is empty')
        self.assertIsNotNone(xccdf_html_element.content, 'Content is empty')

    def test_method_as_dict(self):
        """
        Tests the as_dict method
        """

        xccdf_html_element = self.create_description_object('ok')

        element_dict = xccdf_html_element.as_dict()

        self.assertEqual(element_dict['content'],
                         xccdf_html_element.content,
                         'HTML content does not match')

    def test_method_get_html_content(self):
        """
        Tests the get_html_content method
        """

        xccdf_html_element = self.create_description_object('ok')

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

        xccdf_html_element = self.create_description_object('ok')

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


def suite():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTest(loader.loadTestsFromTestCase(HTMLElementTestCase))
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
