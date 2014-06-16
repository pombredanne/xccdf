# -*- coding: utf-8 -*-

# XCCDF
from xccdf.models.html_element import HTMLElement


class Description(HTMLElement):

    """
    Class to implement <xccdf:description> element
    """

    def __init__(self, xml_element=None):
        """
        Initializes the attrs attribute to serialize the attributes

        :param xml.etree.ElementTree xml_element: XML element to load_xml_attrs
        """

        tag_name = 'description' if xml_element is None else None

        super().__init__(xml_element, tag_name)

    def __str__(self):
        """
        String representation of Description object
        """

        string_value = 'description'
        if hasattr(self, 'content'):
            string_value += ' {desc}'.format(desc=self.content)
        if hasattr(self, 'lang'):
            string_value += ' ({lang})'.format(lang=self.lang)
        return string_value
