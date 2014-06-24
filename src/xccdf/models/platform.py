# -*- coding: utf-8 -*-

"""
xccdf.models.notice includes the class Notice
to create or import a <xccdf:notice> element.

This module is part of the xccdf library.

Author: Rodrigo Núñez <rnunezmujica@icloud.com>
"""

# lxml
from lxml import etree

# XCCDF
from xccdf.models.element import Element
from xccdf.exceptions import RequiredAttributeException
from xccdf.constants import NSMAP


class Platform(Element):

    """
    Class to implement <xccdf:platform> element.
    """

    def __init__(self, xml_element=None, idref=None):
        """
        Initializes the attrs attribute to serialize the attributes.

        :param lxml.etree._Element xml_element: XML element to load.
        :param str idref: CPE string or identifier of CPEL expression.
        :raises ValueError: If no parameter is given.
        :raises RequiredAttributeException: If after importing the xml_element
                                            the idref attribute is missing.
        """
        if xml_element is None and idref is None:
            raise ValueError('either xml_element or idref are required')

        tag_name = 'platform' if xml_element is None else None
        self.idref = idref

        super(Platform, self).__init__(xml_element, tag_name)

        if (not hasattr(self, 'idref')
                or self.idref == ''
                or self.idref is None):
            raise RequiredAttributeException('idref attribute required')

    def __str__(self):
        """
        String representation of Platform object.

        :returns: Platform object as a string.
        :rtype: str
        """

        string_value = 'platform {idref}'.format(idref=self.idref)
        return string_value

    def update_xml_element(self):
        """
        Updates the xml element contents to matches the instance contents.

        :returns: Updated XML element.
        :rtype: lxml.etree._Element
        """

        if not hasattr(self, 'xml_element'):
            self.xml_element = etree.Element(self.name, nsmap=NSMAP)

        if hasattr(self, 'idref'):
            self.xml_element.set('idref', self.idref)

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
