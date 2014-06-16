# -*- coding: utf-8 -*-

# Python stdlib
from xml.etree import ElementTree
import re

# XCCDF
from xccdf.models.element import Element


class HTMLElement(Element):

    """
    Generic class to implement a XCCDF element with HTML enabled text
    """

    def __init__(self, xml_element=None, tag_name=None):
        """
        Initializes the attrs attribute to serialize the attributes

        :param xml.etree.ElementTree xml_element: XML element to load_xml_attrs
        """

        super().__init__(xml_element, tag_name)
        if xml_element is not None:
            self.import_element(xml_element)

    def import_element(self, xml_element):
        """
        Imports the element from an ElementTree element and loads its content
        """

        super().import_element(xml_element)

        self.content = self.get_html_content()

    def as_dict(self):
        """
        Serializes the object necessary data in a dictionary

        :returns: Serialized data in a dictionary
        :rtype: dict
        """

        element_dict = super().as_dict()
        if hasattr(self, 'content'):
            element_dict['content'] = self.content

        return element_dict

    def get_html_content(self):
        """
        Parses the element and subelements and parses any HTML enabled text to
        its original HTML form for rendering
        """

        # Extract full element node content (including subelements)
        html_content = ''
        if hasattr(self, 'xml_element'):
            xml = self.xml_element
            content_list = ["" if xml.text is None else xml.text]

            def to_string(xml):
                return ElementTree.tostring(xml).decode('utf-8')

            content_list += [to_string(e) for e in xml.getchildren()]

            full_xml_content = "".join(content_list)

            # Parse tags to generate HTML valid content
            first_regex = r'html:'
            second_regex = r' xmlns:html=(["\'])(?:(?=(\\?))\2.)*?\1'
            html_content = re.sub(first_regex, '',
                                  re.sub(second_regex, '', full_xml_content))

        return html_content
