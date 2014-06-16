# -*- coding: utf-8 -*-

# XCCDF
from xccdf.models.html_element import HTMLElement
from xccdf.exceptions import RequiredAttributeException


class Notice(HTMLElement):

    """
    Class to implement <xccdf:notice> element
    """

    def __init__(self, xml_element=None, id=None):
        """
        Initializes the attrs attribute to serialize the attributes

        :param xml.etree.ElementTree xml_element: XML element to load_xml_attrs
        """

        if xml_element is None and id is None:
            raise ValueError('either xml_element or id are required')

        tag_name = 'notice' if xml_element is None else None
        self.id = id
        super().__init__(xml_element, tag_name)

        if not hasattr(self, 'id') or self.id == '' or self.id is None:
            raise RequiredAttributeException('id attribute required')

    def __str__(self):
        """
        String representation of Notice object
        """

        string_value = 'notice {id}'.format(id=self.id)
        if hasattr(self, 'lang'):
            string_value += ' ({lang})'.format(lang=self.lang)
        return string_value
