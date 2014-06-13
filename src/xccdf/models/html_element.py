# -*- coding: utf-8 -*-

# Python stdlib
from xml.etree import ElementTree
import re

# XCCDF
from xccdf.models.element import Element


class HTMLElement(Element):

    """
    Generic class to implement a XCCDF element
    """

    def __init__(self, xml_element):
        """
        Initializes the attrs attribute to serialize the attributes

        :param xml.etree.ElementTree xml_element: XML element to load_xml_attrs
        """

        super().__init__(xml_element)

        self.content = self.get_html_content()

    def as_dict(self):
        """
        Serializes the object necessary data in a dictionary

        :returns: Serialized data in a dictionary
        :rtype: dict
        """

        element_dict = super().as_dict()
        element_dict['content'] = self.content

        return element_dict

    def get_html_content(self):
        """
        Parses the element and subelements and parses any HTML enabled text to
        its original HTML form for rendering
        """

        # Extract full element node content (including subelements)
        xml = self.xml_element
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

        return html_content
