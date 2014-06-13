# -*- coding: utf-8 -*-

# Python stdlib
from datetime import date

# XCCDF
from xccdf.exceptions import InvalidValueException
from xccdf.models.element import Element
from xccdf.constants.status import STATUS_VALUE_CHOICES


class Status(Element):

    """
    Class to implement <xccdf:status> element
    """

    def __init__(self, xml_element):
        """
        Initializes the attrs attribute to serialize the attributes

        :param xml.etree.ElementTree xml_element: XML element to load_xml_attrs
        """

        super().__init__(xml_element)

        if self.text not in STATUS_VALUE_CHOICES:
            val = '{val} is not valid. Must be one of this: {choices}'.format(
                val=self.text, choices=repr(STATUS_VALUE_CHOICES))
            raise InvalidValueException(val)

    def __str__(self):
        string_value = '{state}'.format(state=self.text)
        if hasattr(self, 'date'):
            string_value += ' ({date})'.format(date=self.date)
        return string_value

    def get_date(self):
        """
        Returns the date attribute as a date object

        :returns: Date of the status if it exists
        :rtype: date or NoneType
        """

        if hasattr(self, 'date'):
            return date(*list(map(int, self.date.split('-'))))
        else:
            return None
