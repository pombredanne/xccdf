# -*- coding: utf-8 -*-

# lxml
from lxml import etree

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

    def update_xml_element(self):
        """
        Updates the xml element contents to matches the instance contents
        """

        super().update_xml_element()

        if hasattr(self, 'lang'):
            self.xml_element.set(
                '{http://www.w3.org/XML/1998/namespace}lang', self.lang)
        if hasattr(self, 'override'):
            self.xml_element.set('override', str(self.override))

    def to_xml_string(self):
        self.update_xml_element()
        xml = self.xml_element

        return etree.tostring(xml, pretty_print=True).decode('utf-8')
