# -*- coding: utf-8 -*-

# XCCDF
from xccdf.models.element import Element


class Title(Element):

    """
    Class to implement <xccdf:title> element
    """

    def __init__(self, xml_element):
        """
        Initializes the attrs attribute to serialize the attributes

        :param xml.etree.ElementTree xml_element: XML element to load_xml_attrs
        """

        super().__init__(xml_element)

    def __str__(self):
        string_value = '{title}'.format(title=self.text)
        if hasattr(self, 'lang'):
            string_value += ' ({lang})'.format(lang=self.lang)
        return string_value
