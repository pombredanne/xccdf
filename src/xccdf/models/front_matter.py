# -*- coding: utf-8 -*-

# XCCDF
from xccdf.models.html_element import HTMLElement


class FrontMatter(HTMLElement):

    """
    Class to implement <xccdf:front-matter> element
    """

    def __init__(self, xml_element=None):
        """
        Initializes the attrs attribute to serialize the attributes

        :param xml.etree.ElementTree xml_element: XML element to load_xml_attrs
        """

        tag_name = 'front-matter' if xml_element is None else None
        super().__init__(xml_element, tag_name)

    def __str__(self):
        """
        String representation of FrontMatter object
        """

        string_value = 'front-matter'
        if hasattr(self, 'content'):
            string_value += ' {ftmatter}'.format(ftmatter=self.content)
        if hasattr(self, 'lang'):
            string_value += ' ({lang})'.format(lang=self.lang)
        return string_value
