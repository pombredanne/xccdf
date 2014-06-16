# -*- coding: utf-8 -*-

# Python stdlib
import unittest
import os
import io

# lxml
from lxml import etree

# XCCDF
from xccdf.models.rear_matter import RearMatter


class RearMatterTestCase(unittest.TestCase):

    """
    Test cases for RearMatter class
    """

    def load_example_element(self, xml_file_type='ok'):
        """
        Helper method to load an XML element
        """

        file_name = 'example_xccdf_rear_matter_{type}.xml'.format(
            type=xml_file_type)

        xml_path = os.path.abspath(os.path.dirname(__file__))
        xml_file = io.open(os.path.join(
            xml_path,
            'examples',
            file_name))

        xml_string = xml_file.read()
        xml_file.close()

        element_tree = etree.fromstring(xml_string.encode('utf-8'))

        return element_tree[1]

    def create_rear_matter_object(self, object_type='ok'):
        """
        Helper method to create the RearMatter object

        :returns: RearMatter object
        :rtype: xccdf.models.rear_matter.RearMatter
        """

        xml_element = self.load_example_element(object_type)

        return RearMatter(xml_element)

    def test_init_all_ok(self):
        """
        Tests the class constructor
        """

        xccdf_rear_matter = self.create_rear_matter_object('ok')

        self.assertEqual(xccdf_rear_matter.name, 'rear-matter',
                         'RearMatter tag name does not match')

    def test_init_empty_instance(self):
        """
        Tests the class constructor with an empty instance
        """

        xccdf_rear_matter = RearMatter()

        self.assertEqual(xccdf_rear_matter.name, 'rear-matter',
                         'RearMatter tag name does not match')

    def test_print_object(self):
        """
        Tests the string representation of an RearMatter object
        """

        xccdf_rear_matter = self.create_rear_matter_object('ok')

        string_value = 'rear-matter {rrmatter} ({lang})'.format(
            rrmatter=xccdf_rear_matter.content,
            lang=xccdf_rear_matter.lang)
        self.assertEqual(str(xccdf_rear_matter), string_value,
                         'String representation does not match')

    def test_print_object_no_lang(self):
        """
        Tests the string representation of an RearMatter object without a lang
        """

        xccdf_rear_matter = self.create_rear_matter_object('no_lang')

        string_value = 'rear-matter {rrmatter}'.format(
            rrmatter=xccdf_rear_matter.content)
        self.assertEqual(str(xccdf_rear_matter), string_value,
                         'String representation does not match')

    def test_print_object_empty_instance(self):
        """
        Tests the string representation of an RearMatter object
        """

        xccdf_rear_matter = RearMatter()

        string_value = 'rear-matter'
        self.assertEqual(str(xccdf_rear_matter), string_value,
                         'String representation does not match')


def suite():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTest(loader.loadTestsFromTestCase(RearMatterTestCase))
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
