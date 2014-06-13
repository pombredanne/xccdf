# -*- coding: utf-8 -*-

# Python stdlib
import unittest
import os
import io
from xml.etree import ElementTree

# XCCDF
from xccdf.models.front_matter import FrontMatter


class FrontMatterTestCase(unittest.TestCase):

    """
    Test cases for FrontMatter class
    """

    def load_example_element(self, xml_file_type='ok'):
        """
        Helper method to load an XML element
        """

        file_name = 'example_xccdf_front_matter_{type}.xml'.format(
            type=xml_file_type)

        xml_path = os.path.abspath(os.path.dirname(__file__))
        xml_file = io.open(os.path.join(
            xml_path,
            'examples',
            file_name))

        xml_string = xml_file.read()
        xml_file.close()

        element_tree = ElementTree.fromstring(xml_string)

        return element_tree[0]

    def create_front_matter_object(self, object_type='ok'):
        """
        Helper method to create the FrontMatter object

        :returns: FrontMatter object
        :rtype: xccdf.models.front_matter.FrontMatter
        """

        xml_element = self.load_example_element(object_type)

        return FrontMatter(xml_element)

    def test_init_all_ok(self):
        """
        Tests the class constructor
        """

        xccdf_front_matter = self.create_front_matter_object('ok')

        self.assertEqual(xccdf_front_matter.tag_name, 'front-matter',
                         'FrontMatter tag name does not match')

    def test_print_object(self):
        """
        Tests the string representation of an FrontMatter object
        """

        xccdf_front_matter = self.create_front_matter_object('ok')

        string_value = '{ftmatter} ({lang})'.format(
            ftmatter=xccdf_front_matter.content,
            lang=xccdf_front_matter.lang)
        self.assertEqual(str(xccdf_front_matter), string_value,
                         'String representation does not match')

    def test_print_object_no_lang(self):
        """
        Tests the string representation of an FrontMatter object without a lang
        """

        xccdf_front_matter = self.create_front_matter_object('no_lang')

        string_value = '{ftmatter}'.format(ftmatter=xccdf_front_matter.content)
        self.assertEqual(str(xccdf_front_matter), string_value,
                         'String representation does not match')


def suite():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTest(loader.loadTestsFromTestCase(FrontMatterTestCase))
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
