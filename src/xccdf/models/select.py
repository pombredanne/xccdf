# -*- coding: utf-8 -*-

# XCCDF
from xccdf.models.element import Element
from xccdf.exceptions import RequiredAttributeException, InvalidValueException


class Select(Element):

    """
    Class to implement <xccdf:version> element
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

        if (not hasattr(self, 'selected')
                or self.selected == ''
                or self.selected is None):
            raise RequiredAttributeException('selected attribute required')

        if self.selected not in ['true', '1', 'false', '0']:
            raise InvalidValueException(
                'selected attribute has a invalid value')

    def __str__(self):
        string_value = '{idref} {selected}'.format(
            idref=self.idref, selected=str(self.is_selected()))
        return string_value

    def is_selected(self):
        if self.selected in ['true', '1']:
            return True
        else:
            return False
