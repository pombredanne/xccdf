# -*- coding: utf-8 -*-

# XCCDF
from xccdf.models.element import Element


class Title(Element):

    """
    Class to implement <xccdf:title> element
    """

    def __init__(self, xml_element=None):
        """
        Initializes the attrs attribute to serialize the attributes

        :param xml.etree.ElementTree xml_element: XML element to load_xml_attrs
        """
        tag_name = 'title' if xml_element is None else None
        super().__init__(xml_element, tag_name)

    def __str__(self):
        """
        String representation of Title object
        """

        string_value = 'title'
        if hasattr(self, 'text'):
            string_value += ' {title}'.format(title=self.text)
        if hasattr(self, 'lang'):
            string_value += ' ({lang})'.format(lang=self.lang)
        return string_value
