# -*- coding: utf-8 -*-

"""
xccdf.models.title includes the class Title
to create or import a <xccdf:title> element.

This module is part of the xccdf library.

Author: Rodrigo Núñez <rnunezmujica@icloud.com>
"""

# lxml
from lxml import etree

# XCCDF
from xccdf.models.element import Element
from xccdf.constants import NSMAP


class Title(Element):

    """
    Class to implement <xccdf:title> element.
    """

    def __init__(self, xml_element=None):
        """
        Initializes the attrs attribute to serialize the attributes.

        :param lxml.etree._Element xml_element: XML element to load_xml_attrs.
        """
        tag_name = 'title' if xml_element is None else None

        super(Title, self).__init__(xml_element, tag_name)

    def __str__(self):
        """
        String representation of Title object.

        :returns: Title object as a string
        :rtype: str
        """

        string_value = 'title'
        if hasattr(self, 'text'):
            string_value += ' {title}'.format(title=self.text)
        if hasattr(self, 'lang'):
            string_value += ' ({lang})'.format(lang=self.lang)
        return string_value

    def update_xml_element(self):
        """
        Updates the xml element contents to matches the instance contents.

        :returns: Updated XML element.
        :rtype: lxml.etree._Element
        """

        if not hasattr(self, 'xml_element'):
            self.xml_element = etree.Element(self.name, nsmap=NSMAP)

        if hasattr(self, 'lang'):
            self.xml_element.set(
                '{http://www.w3.org/XML/1998/namespace}lang', self.lang)
        if hasattr(self, 'override'):
            self.xml_element.set('override', str(self.override))
        if hasattr(self, 'text'):
            self.xml_element.text = self.text

        return self.xml_element

    def to_xml_string(self):
        """
        Exports the element in XML format.

        :returns: element in XML format.
        :rtype: str
        """

        self.update_xml_element()
        xml = self.xml_element

        return etree.tostring(xml, pretty_print=True).decode('utf-8')
