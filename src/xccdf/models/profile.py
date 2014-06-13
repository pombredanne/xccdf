# -*- coding: utf-8 -*-

# XCCDF
from xccdf.models.element import Element
from xccdf.exceptions import RequiredAttributeException
from xccdf.constants import cardinality


class Profile(Element):

    """
    Class to implement <xccdf:Profile> element
    """

    skeleton = {
        'status': cardinality.CARDINALITY_0_N,
        'version': cardinality.CARDINALITY_0_1,
        'title': cardinality.CARDINALITY_1_N,
        'description': cardinality.CARDINALITY_0_N,
        'platform': cardinality.CARDINALITY_0_N,
        'select': cardinality.CARDINALITY_0_N
    }

    def __init__(self, xml_element):
        """
        Initializes the attrs attribute to serialize the attributes

        :param xml.etree.ElementTree xml_element: XML element to load_xml_attrs
        """

        super().__init__(xml_element)

        if (not hasattr(self, 'idref')
                or self.idref == ''
                or self.idref is None):
            raise RequiredAttributeException('idref attribute required')

    def __str__(self):
        string_value = '{idref}'.format(idref=self.idref)
        return string_value
