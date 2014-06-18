# -*- coding: utf-8 -*-

# lxml
from lxml import etree

# XCCDF
from xccdf.models.element import Element
from xccdf.models.version import Version
from xccdf.models.status import Status
from xccdf.models.title import Title
from xccdf.models.description import Description
from xccdf.models.front_matter import FrontMatter
from xccdf.models.rear_matter import RearMatter
from xccdf.models.platform import Platform
from xccdf.models.profile import Profile
from xccdf.models.group import Group
from xccdf.models.rule import Rule
from xccdf.constants import NSMAP
from xccdf.exceptions import RequiredAttributeException
from xccdf.exceptions import CardinalityException


class Benchmark(Element):

    """
    Class to parse <xccdf:Benchmark> element
    """

    def __init__(self, xml_element=None, id=None):
        """
        Initializes the attrs attribute to serialize the attributes

        :param lxml.etree._Element xml_element: XML element to load
        :param str id: Unique ID of the Benchmark.
                       If xml_element is present, this parameter is ignored
        """

        if xml_element is None and id is None:
            raise ValueError('either xml_element or id are required')

        self.id = id
        tag_name = 'Benchmark' if xml_element is None else None
        super(Benchmark, self).__init__(xml_element, tag_name)

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
        String representation of Benchmark object
        """

        string_value = 'Benchmark {id}'.format(id=self.id)
        return string_value

    def load_children(self):
        """
        Load the subelements from the xml_element in its correspondent classes
        """
        # Containers
        children = list()
        statuses = list()
        titles = list()
        descriptions = list()
        front_matters = list()
        rear_matters = list()
        platforms = list()
        version = None
        profiles = list()
        groups = list()
        rules = list()

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
            elif tag == 'front-matter':
                front_matters.append(FrontMatter(element))
            elif tag == 'rear-matter':
                rear_matters.append(RearMatter(element))
            elif tag == 'platform':
                platforms.append(Platform(element))
            elif tag == 'Profile':
                profiles.append(Profile(element))
            elif tag == 'Group':
                groups.append(Group(element))
            # elif tag == 'Rule':
            #     rules.append(Rule(element))

        # Element validation
        if version is None:
            error_msg = 'a Benchmark must contain a version element'
            raise CardinalityException(error_msg)
        elif len(groups) <= 0 and len(rules) <= 0:
            error_msg = 'a Benchmark must contain at least a group or a rule'
            raise CardinalityException(error_msg)
        elif len(statuses) <= 0:
            error_msg = 'a Benchmark must contain at least a status element'
            raise CardinalityException(error_msg)

        # List construction
        children.extend(statuses)
        children.extend(titles)
        children.extend(descriptions)
        children.extend(front_matters)
        children.extend(rear_matters)
        children.extend(platforms)
        if version is not None:
            children.append(version)
        children.extend(profiles)
        children.extend(groups)
        children.extend(rules)

        return children

    def update_xml_element(self):
        """
        Updates the xml element contents to matches the instance contents
        """

        if not hasattr(self, 'xml_element'):
            self.xml_element = etree.Element(self.name, nsmap=NSMAP)

        self.xml_element.clear()

        if hasattr(self, 'resolved'):
            self.xml_element.set('resolved', self.resolved)
        if hasattr(self, 'style'):
            self.xml_element.set('style', self.style)
        if hasattr(self, 'style_href'):
            self.xml_element.set('style-href', self.style_href)
        if hasattr(self, 'lang'):
            self.xml_element.set(
                '{http://www.w3.org/XML/1998/namespace}lang', self.lang)
        self.xml_element.set('id', self.id)

        for child in self.children:
            if hasattr(child, 'update_xml_element'):
                child.update_xml_element()
                if hasattr(child, 'xml_element'):
                    self.xml_element.append(child.xml_element)

    def as_dict(self):
        """
        Serializes the object necessary data in a dictionary

        :returns: Serialized data in a dictionary
        :rtype: dict
        """

        result_dict = super(Benchmark, self).as_dict()

        statuses = list()
        titles = list()
        descriptions = list()
        front_matters = list()
        rear_matters = list()
        platforms = list()
        version = None
        profiles = list()
        groups = list()

        for child in self.children:
            if isinstance(child, Version):
                version = child.as_dict()
            elif isinstance(child, Status):
                statuses.append(child.as_dict())
            elif isinstance(child, Title):
                titles.append(child.as_dict())
            elif isinstance(child, Description):
                descriptions.append(child.as_dict())
            elif isinstance(child, FrontMatter):
                front_matters.append(child.as_dict())
            elif isinstance(child, RearMatter):
                rear_matters.append(child.as_dict())
            elif isinstance(child, Platform):
                platforms.append(child.as_dict())
            elif isinstance(child, Profile):
                profiles.append(child.as_dict())
            elif isinstance(child, Group):
                groups.append(child.as_dict())

        if version is not None:
            result_dict['version'] = version
        if len(statuses) > 0:
            result_dict['statuses'] = statuses
        if len(titles) > 0:
            result_dict['titles'] = titles
        if len(descriptions) > 0:
            result_dict['descriptions'] = descriptions
        if len(front_matters) > 0:
            result_dict['front_matters'] = front_matters
        if len(rear_matters) > 0:
            result_dict['rear_matters'] = rear_matters
        if len(platforms) > 0:
            result_dict['platforms'] = platforms
        if len(profiles) > 0:
            result_dict['profiles'] = profiles
        if len(groups) > 0:
            result_dict['groups'] = groups

        return result_dict
