# -*- coding: utf-8 -*-

# XCCDF
from xccdf.models.element import Element
from xccdf.exceptions import RequiredAttributeException


class Platform(Element):

    """
    Class to implement <xccdf:platform> element
    """

    def __init__(self, xml_element=None, idref=None):
        """
        Initializes the attrs attribute to serialize the attributes

        :param lxml.etree._Element xml_element: XML element to load
        """
        if xml_element is None and idref is None:
            raise ValueError('either xml_element or idref are required')

        tag_name = 'platform' if xml_element is None else None
        self.idref = idref
        super().__init__(xml_element, tag_name)

        if (not hasattr(self, 'idref')
                or self.idref == ''
                or self.idref is None):
            raise RequiredAttributeException('idref attribute required')

    def __str__(self):
        """
        String representation of Notice object
        """

        string_value = 'platform {idref}'.format(idref=self.idref)
        return string_value
