# -*- coding: utf-8 -*-

# Python stdlib
from datetime import datetime
import re

# lxml
from lxml import etree

# XCCDF
from xccdf.models.element import Element
from xccdf.exceptions import RequiredAttributeException
from xccdf.constants import NSMAP


class Version(Element):

    """
    Class to implement <xccdf:version> element
    """

    def __init__(self, xml_element=None, version=None):
        """
        Initializes the Version class and loads its attributes

        :param lxml.etree._Element xml_element: XML element to load
        :param str version: Version string
        """

        if xml_element is None and version is None:
            raise ValueError('either xml_element or version are required')

        tag_name = 'version' if xml_element is None else None
        self.text = version
        super().__init__(xml_element, tag_name)

        if (not hasattr(self, 'text') or
                self.text == '' or self.text is None):
            raise RequiredAttributeException('version content is required')

        if hasattr(self, 'time') and isinstance(self.time, str):
            self.time = self.str_to_time()

    def __str__(self):
        """
        String representation of Version object
        """

        string_value = 'version {version}'.format(version=self.text)
        return string_value

    def time_to_str(self):
        """
        Formats time attribute to the XCCDF dateTime format

        :returns: time formatted string
        :rtype: str
        """

        return '{time:%Y-%m-%dT%H:%M:%S}'.format(time=self.time)

    def str_to_time(self):
        """
        Formats a XCCDF dateTime string to a datetime object

        :returns: datetime object
        :rtype: datetime.datetime
        """

        return datetime(*list(map(int, re.split(r'-|:|T', self.time))))

    def update_xml_element(self):
        """
        Updates the xml element contents to matches the instance contents
        """

        if not hasattr(self, 'xml_element'):
            self.xml_element = etree.Element(self.name, nsmap=NSMAP)

        if hasattr(self, 'time'):
            self.xml_element.set('time', self.time_to_str())
        if hasattr(self, 'update'):
            self.xml_element.set('update', str(self.update))
        self.xml_element.text = self.text

    def to_xml_string(self):
        """
        Exports the element in XML format

        :returns: element in XML format
        :rtype: str
        """

        self.update_xml_element()
        xml = self.xml_element

        return etree.tostring(xml, pretty_print=True).decode('utf-8')


class TailoringVersion(Version):

    """
    Class to implement <xccdf:version> element
    specific to the <xccdf:Tailoring> element
    """

    def __init__(self, xml_element=None, version=None,
                 time=None):
        """
        Initializes the TailoringVersion class and loads its attributes

        :param lxml.etree._Element xml_element: XML element to load
        :param str version: Version string
        :param datetime.datetime time: Timestamp of this version
        """

        self.time = time
        super().__init__(xml_element, version)

        if (not hasattr(self, 'time') or
                self.time == '' or self.time is None):
            raise RequiredAttributeException('time is required')
