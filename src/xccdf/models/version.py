# -*- coding: utf-8 -*-

# XCCDF
from xccdf.models.element import Element
from xccdf.exceptions import RequiredAttributeException


class Version(Element):

    """
    Class to implement <xccdf:version> element
    """

    def __init__(self, xml_element):
        """
        Initializes the attrs attribute to serialize the attributes

        :param xml.etree.ElementTree xml_element: XML element to load_xml_attrs
        """

        super().__init__(xml_element)

        if not hasattr(self, 'text') or self.text == '' or self.text is None:
            raise RequiredAttributeException('version content is required')

    def __str__(self):
        string_value = '{version}'.format(version=self.text)
        return string_value
