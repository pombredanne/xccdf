# -*- coding: utf-8 -*-

# XCCDF
from xccdf.models.element import Element
from xccdf.exceptions import RequiredAttributeException


class Version(Element):

    """
    Class to implement <xccdf:version> element
    """

    def __init__(self, xml_element=None, version=None):
        """
        Initializes the attrs attribute to serialize the attributes

        :param xml.etree.ElementTree xml_element: XML element to load_xml_attrs
        """

        if xml_element is None and version is None:
            raise ValueError('either xml_element or version are required')

        tag_name = 'version' if xml_element is None else None
        self.text = version
        super().__init__(xml_element, tag_name)

        if (not hasattr(self, 'text') or
                self.text == '' or self.text is None):
            raise RequiredAttributeException('version content is required')

    def __str__(self):
        """
        String representation of Version object
        """

        string_value = 'version {version}'.format(version=self.text)
        return string_value
