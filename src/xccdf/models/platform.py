# -*- coding: utf-8 -*-

# XCCDF
from xccdf.models.element import Element
from xccdf.exceptions import RequiredAttributeException


class Platform(Element):

    """
    Class to implement <xccdf:platform> element
    """

    def __init__(self, xml_element):
        """
        Initializes the attrs attribute to serialize the attributes

        :param xml.etree.ElementTree xml_element: XML element to load_xml_attrs
        """

        super().__init__(xml_element)

        if (not hasattr(self, 'idref')
                or self.idref == ''
                or self.idref is None):
            raise RequiredAttributeException('idref attribute required')

    def __str__(self):
        string_value = '{idref}'.format(idref=self.idref)
        return string_value
