# -*- coding: utf-8 -*-

# lxml
from lxml import etree

# XCCDF
from xccdf.models.element import Element
from xccdf.exceptions import RequiredAttributeException
from xccdf.constants import NSMAP


class Ident(Element):

    """
    Class to implement <xccdf:version> element
    """

    def __init__(self, xml_element=None, ident=None, system=None):
        """
        Initializes the Ident class and loads its attributes

        :param lxml.etree._Element xml_element: XML element to load
        :param str ident: Ident string
        """

        if xml_element is None and (ident is None and system is None):
            raise ValueError(
                'either xml_element or ident and system are required')

        tag_name = 'ident' if xml_element is None else None
        self.text = ident
        self.system = system

        super(Ident, self).__init__(xml_element, tag_name)

        if (not hasattr(self, 'text') or
                self.text == '' or self.text is None):
            raise RequiredAttributeException('ident is required')

        if (not hasattr(self, 'system') or
                self.system == '' or self.system is None):
            raise RequiredAttributeException('system attribute is required')

    def __str__(self):
        """
        String representation of Version object
        """

        string_value = 'ident {ident}'.format(ident=self.text)
        return string_value

    def update_xml_element(self):
        """
        Updates the xml element contents to matches the instance contents
        """

        if not hasattr(self, 'xml_element'):
            self.xml_element = etree.Element(self.name, nsmap=NSMAP)

        self.xml_element.set('system', str(self.system))
        self.xml_element.text = self.text

    def to_xml_string(self):
        """
        Exports the element in XML format

        :returns: element in XML format
        :rtype: str
        """

        self.update_xml_element()
        xml = self.xml_element

        return etree.tostring(xml, pretty_print=True).decode('utf-8')
