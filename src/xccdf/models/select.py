# -*- coding: utf-8 -*-

# Python stdlib
import sys

# lxml
from lxml import etree

# XCCDF
from xccdf.models.element import Element
from xccdf.exceptions import RequiredAttributeException, InvalidValueException
from xccdf.constants import NSMAP


class Select(Element):

    """
    Class to implement <xccdf:select> element
    """

    def __init__(self, xml_element=None, idref=None, selected=False):
        """
        Initializes the attrs attribute to serialize the attributes

        :param lxml.etree._Element xml_element: XML element to load
        """
        if xml_element is None and idref is None:
            raise ValueError('either xml_element or idref are required')

        tag_name = 'select' if xml_element is None else None
        self.idref = idref
        if selected is True:
            self.selected = 'true'
        else:
            self.selected = 'false'

        if sys.version_info[0] >= 3:
            super().__init__(xml_element, tag_name)
        else:
            super(Select, self).__init__(xml_element, tag_name)

        if (not hasattr(self, 'idref')
                or self.idref == ''
                or self.idref is None):
            raise RequiredAttributeException('idref attribute required')

        if self.selected not in ['true', '1', 'false', '0']:
            raise InvalidValueException(
                'selected attribute has a invalid value')

    def __str__(self):
        """
        String representation of Select object
        """

        string_value = 'select {idref} {selected}'.format(
            idref=self.idref, selected=str(self.is_selected()))
        return string_value

    def is_selected(self):
        """
        Return if the select element is selected
        or None if selected is not defined

        :returns: True, False or None
        :rtype: bool or NoneType
        """

        if self.selected in ['true', '1']:
            return True
        else:
            return False

    def update_xml_element(self):
        """
        Updates the xml element contents to matches the instance contents
        """

        if not hasattr(self, 'xml_element'):
            self.xml_element = etree.Element(self.name, nsmap=NSMAP)

        self.xml_element.set('idref', str(self.idref))
        self.xml_element.set('selected', str(self.selected))

    def to_xml_string(self):
        self.update_xml_element()
        xml = self.xml_element

        return etree.tostring(xml, pretty_print=True).decode('utf-8')
