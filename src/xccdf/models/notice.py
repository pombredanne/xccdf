# -*- coding: utf-8 -*-

# XCCDF
from xccdf.models.html_element import HTMLElement
from xccdf.exceptions import RequiredAttributeException


class Notice(HTMLElement):

    """
    Class to implement <xccdf:notice> element
    """

    def __init__(self, xml_element):
        """
        Initializes the attrs attribute to serialize the attributes

        :param xml.etree.ElementTree xml_element: XML element to load_xml_attrs
        """

        super().__init__(xml_element)

        if not hasattr(self, 'id') or self.id == '' or self.id is None:
            raise RequiredAttributeException('id attribute required')

    def __str__(self):
        string_value = 'notice {id}'.format(id=self.id)
        if hasattr(self, 'lang'):
            string_value += ' ({lang})'.format(lang=self.lang)
        return string_value
