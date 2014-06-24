# -*- coding: utf-8 -*-

"""
xccdf.models.notice includes the class Notice
to create or import a <xccdf:notice> element.

This module is part of the xccdf library.

Author: Rodrigo Núñez <rnunezmujica@icloud.com>
"""

# XCCDF
from xccdf.models.html_element import HTMLElement
from xccdf.exceptions import RequiredAttributeException


class Notice(HTMLElement):

    """
    Class to implement <xccdf:notice> element.
    """

    def __init__(self, xml_element=None, id=None):
        """
        Initializes the attrs attribute to serialize the attributes.

        :param lxml.etree._Element xml_element: XML element to load.
        :param str id: Id attribute.
        :raises ValueError: If no parameter is given.
        :raises RequiredAttributeException: If after importing the xml_element
                                            the id attribute is missing.
        """

        if xml_element is None and id is None:
            raise ValueError('either xml_element or id are required')

        tag_name = 'notice' if xml_element is None else None
        self.id = id

        super(Notice, self).__init__(xml_element, tag_name)

        if not hasattr(self, 'id') or self.id == '' or self.id is None:
            raise RequiredAttributeException('id attribute required')

    def __str__(self):
        """
        String representation of Notice object.

        :returns: Notice object as a string.
        :rtype: str
        """

        string_value = 'notice {id}'.format(id=self.id)
        if hasattr(self, 'lang'):
            string_value += ' ({lang})'.format(lang=self.lang)
        return string_value
