# -*- coding: utf-8 -*-

# Python stdlib
from xml.etree import ElementTree


class Element(object):

    """
    Generic class to implement a XCCDF element
    """

    def __init__(self, xml_element):
        """
        Initializes the attrs attribute to serialize the attributes

        :param xml.etree.ElementTree xml_element: XML element to load_xml_attrs
        """

        if not isinstance(xml_element, ElementTree.Element):
            error_msg = 'xml_element must be an instance of '\
                        'xml.etree.ElementTree.Element'
            raise TypeError(error_msg)

        self.xml_element = xml_element

        uri, tag = Element.get_namespace_and_tag(self.xml_element.tag)
        self.namespace = uri
        self.tag_name = tag

        self.load_xml_attrs()

        self.text = self.xml_element.text

    def __str__(self):
        return '<{namespace}>{tag}'.format(namespace=self.namespace,
                                           tag=self.tag_name)

    def as_dict(self):
        """
        Serializes the object necessary data in a dictionary

        :returns: Serialized data in a dictionary
        :rtype: dict
        """

        element_dict = dict()
        element_dict['namespace'] = self.namespace
        element_dict['name'] = self.tag_name
        element_dict['text'] = self.text

        attr_dict = dict()
        for attr in self.attrs:
            if hasattr(self, attr):
                attr_dict[attr] = getattr(self, attr)
        element_dict['attrs'] = attr_dict

        return element_dict

    def load_xml_attrs(self):
        """
        Load XML attributes as object attributes
        """

        xml_attrs = self.xml_element.attrib

        attrs_list = []

        for variable, value in iter(xml_attrs.items()):
            uri, tag = Element.get_namespace_and_tag(variable)
            attrs_list.append(tag)
            setattr(self, tag, value)

        self.attrs = attrs_list

    @staticmethod
    def get_namespace_and_tag(name):
        """
        Separates the namespace and tag from an element

        :param str name: Tag
        :returns: Namespace URI and Tag namespace
        :rtype: tuple
        """

        if name[0] == "{":
            uri, ignore, tag = name[1:].partition("}")
        else:
            uri = None
            tag = name
        return uri, tag
