# -*- coding: utf-8 -*-

# lxml
from lxml import etree

# XCCDF
from xccdf.models.element import Element
from xccdf.models.version import Version
from xccdf.models.status import Status
from xccdf.models.title import Title
from xccdf.models.description import Description
from xccdf.models.platform import Platform
from xccdf.models.ident import Ident
from xccdf.constants import NSMAP
from xccdf.exceptions import RequiredAttributeException
from xccdf.exceptions import CardinalityException


class Rule(Element):

    """
    Class to parse <xccdf:Rule> element
    """

    def __init__(self, xml_element=None, id=None):
        """
        Initializes the attrs attribute to serialize the attributes

        :param lxml.etree._Element xml_element: XML element to load
        :param str id: Unique ID of the Rule.
                       If xml_element is present, this parameter is ignored
        """

        if xml_element is None and id is None:
            raise ValueError('either xml_element or id are required')

        self.id = id
        tag_name = 'Rule' if xml_element is None else None
        super(Rule, self).__init__(xml_element, tag_name)

        if (not hasattr(self, 'id')
                or self.id == ''
                or self.id is None):
            raise RequiredAttributeException('id attribute required')

        if xml_element is not None:
            self.children = self.load_children()
        else:
            self.children = list()

    def __str__(self):
        """
        String representation of Rule object
        """

        string_value = 'Rule {id}'.format(id=self.id)
        return string_value

    def load_children(self):
        """
        Load the subelements from the xml_element in its correspondent classes
        """
        # Containers
        children = list()
        statuses = list()
        version = None
        titles = list()
        descriptions = list()
        platforms = list()
        idents = list()

        # Element load
        for element in self.xml_element:
            uri, tag = Element.get_namespace_and_tag(element.tag)
            if tag == 'version':
                if version is None:
                    version = Version(element)
                else:
                    error_msg = 'version element found more than once'
                    raise CardinalityException(error_msg)
            elif tag == 'status':
                statuses.append(Status(element))
            elif tag == 'title':
                titles.append(Title(element))
            elif tag == 'description':
                descriptions.append(Description(element))
            elif tag == 'platform':
                platforms.append(Platform(element))
            elif tag == 'ident':
                idents.append(Ident(element))

        # List construction
        children.extend(statuses)
        if version is not None:
            children.append(version)
        children.extend(titles)
        children.extend(descriptions)
        children.extend(platforms)
        children.extend(idents)

        return children

    def as_dict(self):
        """
        Serializes the object necessary data in a dictionary

        :returns: Serialized data in a dictionary
        :rtype: dict
        """

        result_dict = super(Rule, self).as_dict()

        statuses = list()
        version = None
        titles = list()
        descriptions = list()
        platforms = list()
        idents = list()

        for child in self.children:
            if isinstance(child, Version):
                version = child.as_dict()
            elif isinstance(child, Status):
                statuses.append(child.as_dict())
            elif isinstance(child, Title):
                titles.append(child.as_dict())
            elif isinstance(child, Description):
                descriptions.append(child.as_dict())
            elif isinstance(child, Platform):
                platforms.append(child.as_dict())
            elif isinstance(child, Ident):
                idents.append(child.as_dict())

        if version is not None:
            result_dict['version'] = version
        if len(statuses) > 0:
            result_dict['statuses'] = statuses
        if len(titles) > 0:
            result_dict['titles'] = titles
        if len(descriptions) > 0:
            result_dict['descriptions'] = descriptions
        if len(platforms) > 0:
            result_dict['platforms'] = platforms
        if len(idents) > 0:
            result_dict['idents'] = idents

        return result_dict

    def update_xml_element(self):
        """
        Updates the xml element contents to matches the instance contents
        """

        if not hasattr(self, 'xml_element'):
            self.xml_element = etree.Element(self.name, nsmap=NSMAP)

        self.xml_element.clear()

        if hasattr(self, 'abstract'):
            self.xml_element.set('abstract', self.abstract)
        if hasattr(self, 'prohibitChanges'):
            self.xml_element.set('prohibitChanges', self.prohibitChanges)
        if hasattr(self, 'hidden'):
            self.xml_element.set('hidden', self.hidden)
        if hasattr(self, 'role'):
            self.xml_element.set('severity', self.hidden)
        if hasattr(self, 'selected'):
            self.xml_element.set('selected', self.selected)
        if hasattr(self, 'weight'):
            self.xml_element.set('weight', self.weight)
        self.xml_element.set('id', self.id)

        for child in self.children:
            if hasattr(child, 'update_xml_element'):
                child.update_xml_element()
                if hasattr(child, 'xml_element'):
                    self.xml_element.append(child.xml_element)
