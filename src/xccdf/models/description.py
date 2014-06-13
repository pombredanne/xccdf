# -*- coding: utf-8 -*-

# XCCDF
from xccdf.models.html_element import HTMLElement


class Description(HTMLElement):

    """
    Class to implement <xccdf:description> element
    """

    def __init__(self, xml_element):
        """
        Initializes the attrs attribute to serialize the attributes

        :param xml.etree.ElementTree xml_element: XML element to load_xml_attrs
        """

        super().__init__(xml_element)

    def __str__(self):
        string_value = '{desc}'.format(desc=self.content)
        if hasattr(self, 'lang'):
            string_value += ' ({lang})'.format(lang=self.lang)
        return string_value
