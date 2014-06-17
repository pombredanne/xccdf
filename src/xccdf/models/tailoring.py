# -*- coding: utf-8 -*-

# Python stdlib
import re

# lxml
from lxml import etree

# XCCDF
from xccdf.models.element import Element
from xccdf.models.version import TailoringVersion
from xccdf.models.status import Status
from xccdf.models.profile import Profile
from xccdf.exceptions import RequiredAttributeException
from xccdf.exceptions import InvalidValueException
from xccdf.exceptions import CardinalityException
from xccdf.constants import NSMAP


class Tailoring(Element):

    """
    Class to implement <xccdf:Tailoring> element
    """

    def __init__(self, xml_element=None, id=None):
        """
        Initializes the attrs attribute to serialize the attributes

        :param lxml.etree._Element xml_element: XML element to load
        :param str id: Unique ID of the Tailoring.
                       If xml_element is present, this parameter is ignored
        """

        if xml_element is None and id is None:
            raise ValueError('either xml_element or id are required')
        tag_name = 'Tailoring' if xml_element is None else None
        self.id = id
        super().__init__(xml_element, tag_name=tag_name)

        if (not hasattr(self, 'id')
                or self.id == ''
                or self.id is None):
            raise RequiredAttributeException('id attribute required')

        if re.fullmatch(r'xccdf_(\w+)_tailoring_(\w+)', self.id) is None:
            raise InvalidValueException('id invalid format')

        if xml_element is not None:
            self.children = self.load_children()
        else:
            self.children = list()

    def __str__(self):
        """
        String representation of Tailoring object
        """

        string_value = 'Tailoring {id}'.format(id=self.id)
        return string_value

    def load_children(self):
        """
        Load the subelements from the xml_element in its correspondent classes
        """
        # Containers
        children = list()
        statuses = list()
        version = None
        profiles = list()

        # Element load
        for element in self.xml_element:
            uri, tag = Element.get_namespace_and_tag(element.tag)
            if tag == 'version':
                if version is None:
                    version = TailoringVersion(element)
                else:
                    error_msg = 'version element found more than once'
                    raise CardinalityException(error_msg)
            elif tag == 'status':
                statuses.append(Status(element))
            elif tag == 'Profile':
                profiles.append(Profile(element))

        # Element validation
        if version is None:
            error_msg = 'version element is required'
            raise CardinalityException(error_msg)
        if len(profiles) <= 0:
            error_msg = 'Profile element is required at least once'
            raise CardinalityException(error_msg)

        # List construction
        children.extend(statuses)
        if version is not None:
            children.append(version)
        children.extend(profiles)

        return children

    def update_xml_element(self):
        """
        Updates the xml element contents to matches the instance contents
        """

        if not hasattr(self, 'xml_element'):
            self.xml_element = etree.Element(self.name, nsmap=NSMAP)

        self.xml_element.clear()
        self.xml_element.set('id', self.id)

        for child in self.children:
            child.update_xml_element()
            self.xml_element.append(child.xml_element)
