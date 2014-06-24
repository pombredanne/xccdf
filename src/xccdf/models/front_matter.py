# -*- coding: utf-8 -*-

"""
xccdf.models.front_matter includes the class FrontMatter
to create or import a <xccdf:front-matter> element.

This module is part of the xccdf library.

Author: Rodrigo Núñez <rnunezmujica@icloud.com>
"""

# XCCDF
from xccdf.models.html_element import HTMLElement


class FrontMatter(HTMLElement):

    """
    Class to implement <xccdf:front-matter> element.
    """

    def __init__(self, xml_element=None):
        """
         Initializes the attrs attribute to serialize the attributes.

        :param lxml.etree._Element xml_element: XML element to load.
        """

        tag_name = 'front-matter' if xml_element is None else None

        super(FrontMatter, self).__init__(xml_element, tag_name)

    def __str__(self):
        """
        String representation of FrontMatter object.

        :returns: FrontMatter object as a string.
        :rtype: str
        """

        string_value = 'front-matter'
        if hasattr(self, 'content'):
            string_value += ' {ftmatter}'.format(ftmatter=self.content)
        if hasattr(self, 'lang'):
            string_value += ' ({lang})'.format(lang=self.lang)
        return string_value
