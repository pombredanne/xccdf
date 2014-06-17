# -*- coding: utf-8 -*-

# Python stdlib
from datetime import date

# lxml
from lxml import etree

# XCCDF
from xccdf.exceptions import InvalidValueException
from xccdf.models.element import Element
from xccdf.constants.status import STATUS_VALUE_CHOICES
from xccdf.constants import NSMAP


class Status(Element):

    """
    Class to implement <xccdf:status> element
    """

    def __init__(self, xml_element=None, state=None):
        """
        Initializes the attrs attribute to serialize the attributes

        :param lxml.etree._Element xml_element: XML element to load_xml_attrs
        """

        if xml_element is None and state is None:
            raise ValueError('either xml_element or state are required')

        self.text = state
        tag_name = 'status' if xml_element is None else None

        super(Status, self).__init__(xml_element, tag_name)

        if self.text not in STATUS_VALUE_CHOICES:
            val = '{val} is not valid. Must '\
                  'be one of this: {choices}'.format(
                      val=self.text, choices=repr(STATUS_VALUE_CHOICES))
            raise InvalidValueException(val)

    def __str__(self):
        """
        String representation of Status object
        """

        string_value = 'status {state}'.format(state=self.text)
        if hasattr(self, 'date'):
            string_value += ' ({date})'.format(date=self.date)
        return string_value

    def str_to_date(self):
        """
        Returns the date attribute as a date object

        :returns: Date of the status if it exists
        :rtype: date or NoneType
        """

        if hasattr(self, 'date'):
            return date(*list(map(int, self.date.split('-'))))
        else:
            return None

    def update_xml_element(self):
        """
        Updates the xml element contents to matches the instance contents
        """

        if not hasattr(self, 'xml_element'):
            self.xml_element = etree.Element(self.name, nsmap=NSMAP)

        if hasattr(self, 'date'):
            self.xml_element.set('date', self.date)
        self.xml_element.text = self.text

    def to_xml_string(self):
        self.update_xml_element()
        xml = self.xml_element

        return etree.tostring(xml, pretty_print=True).decode('utf-8')
