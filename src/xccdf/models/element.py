# -*- coding: utf-8 -*-


class Element(object):

    """
    Generic class to implement a XCCDF element
    """

    def __init__(self, xml_element=None, tag_name=None):
        """
        Initializes the attrs attribute to serialize the attributes

        :param xml.etree.ElementTree xml_element: XML element to load_xml_attrs
        """

        if xml_element is None and tag_name is None:
            raise ValueError('either xml_element or tag_name are required')

        if xml_element is not None:
            self.import_element(xml_element)
        else:
            self.name = tag_name
            self.attrs = list()

    def __str__(self):
        """
        String representation of Element object
        """

        string_value = ''
        if hasattr(self, 'namespace'):
            string_value += '<{namespace}>'.format(namespace=self.namespace)
        string_value += '{tag}'.format(tag=self.name)
        return string_value

    def import_element(self, xml_element):
        """
        Imports the element from an lxml element and loads its content
        """

        self.xml_element = xml_element

        uri, tag = Element.get_namespace_and_tag(self.xml_element.tag)
        self.namespace = uri
        self.name = tag

        self.load_xml_attrs()

        self.text = self.xml_element.text

    def as_dict(self):
        """
        Serializes the object necessary data in a dictionary

        :returns: Serialized data in a dictionary
        :rtype: dict
        """

        element_dict = dict()
        if hasattr(self, 'namespace'):
            element_dict['namespace'] = self.namespace
        if hasattr(self, 'name'):
            element_dict['name'] = self.name
        if hasattr(self, 'text'):
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

        attrs_list = list()

        if hasattr(self, 'xml_element'):
            xml_attrs = self.xml_element.attrib

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

        if isinstance(name, str):
            if name[0] == "{":
                uri, ignore, tag = name[1:].partition("}")
            else:
                uri = None
                tag = name
        else:
            uri = None
            tag = None
        return uri, tag
