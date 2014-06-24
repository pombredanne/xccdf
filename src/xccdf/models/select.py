# -*- coding: utf-8 -*-

"""
xccdf.models.select includes the class Select
to create or import a <xccdf:select> element.

This module is part of the xccdf library.

Author: Rodrigo Núñez <rnunezmujica@icloud.com>
"""

# lxml
from lxml import etree

# XCCDF
from xccdf.models.element import Element
from xccdf.exceptions import RequiredAttributeException, InvalidValueException
from xccdf.constants import NSMAP


class Select(Element):

    """
    Class to implement <xccdf:select> element.
    """

    def __init__(self, xml_element=None, idref=None, selected=False):
        """
        Initializes the attrs attribute to serialize the attributes.

        :param lxml.etree._Element xml_element: XML element to load.
        :param str idref: Unique identifier of a Select element.
        :param bool selected: Mark the Select element as selected.
        :raises ValueError: If no parameter is given.
        :raises RequiredAttributeException: If after importing the xml_element
                                            the idref attribute is missing.
        :raises InvalidValueException: If the imported selected attribute has
                                       an invalid value.
        """
        if xml_element is None and idref is None:
            raise ValueError('either xml_element or idref are required')

        tag_name = 'select' if xml_element is None else None
        self.idref = idref
        if selected is True:
            self.selected = 'true'
        else:
            self.selected = 'false'

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
        String representation of Select object.

        :returns: Select object as a string.
        :rtype: str
        """

        string_value = 'select {idref} {selected}'.format(
            idref=self.idref, selected=str(self.is_selected()))
        return string_value

    def is_selected(self):
        """
        Return if the select element is selected
        or None if selected is not defined.

        :returns: If the element is marked as selected.
        :rtype: bool or NoneType
        """

        if self.selected in ['true', '1']:
            return True
        else:
            return False

    def update_xml_element(self):
        """
        Updates the xml element contents to matches the instance contents.

        :returns: Updated XML element
        :rtype: lxml.etree._Element
        """

        if not hasattr(self, 'xml_element'):
            self.xml_element = etree.Element(self.name, nsmap=NSMAP)

        self.xml_element.set('idref', str(self.idref))
        self.xml_element.set('selected', str(self.selected))

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
