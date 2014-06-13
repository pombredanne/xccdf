# -*- coding: utf-8 -*-

# Python stdlib
import unittest
import os
import io
from xml.etree import ElementTree

# XCCDF
from xccdf.models.notice import Notice
from xccdf.exceptions import RequiredAttributeException


class NoticeTestCase(unittest.TestCase):

    """
    Test cases for Title class
    """

    def load_example_element(self, xml_file_type='ok'):
        """
        Helper method to load an XML element
        """

        file_name = 'example_xccdf_notice_{type}.xml'.format(
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

    def create_notice_object(self, object_type='ok'):
        """
        Helper method to create the Notice object

        :returns: Notice object
        :rtype: xccdf.models.notice.Notice
        """

        xml_element = self.load_example_element(object_type)

        return Notice(xml_element)

    def test_init_all_ok(self):
        """
        Tests the class constructor
        """

        xccdf_notice = self.create_notice_object('ok')

        self.assertEqual(xccdf_notice.tag_name, 'notice',
                         'notice tag name does not match')

        self.assertTrue(hasattr(xccdf_notice, 'id'))

    def test_init_no_id(self):
        """
        Tests the class constructor without an id
        """

        error_msg = 'id attribute required'
        with self.assertRaisesRegex(RequiredAttributeException,
                                    error_msg):
            self.create_notice_object('no_id')

    def test_print_object(self):
        """
        Tests the string representation of an Notice object
        """

        xccdf_notice = self.create_notice_object('ok')

        string_value = 'notice {id} ({lang})'.format(id=xccdf_notice.id,
                                                     lang=xccdf_notice.lang)
        self.assertEqual(str(xccdf_notice), string_value,
                         'String representation does not match')

    def test_print_object_no_lang(self):
        """
        Tests the string representation of an Notice object without a lang
        """

        xccdf_notice = self.create_notice_object('no_lang')

        string_value = 'notice {id}'.format(id=xccdf_notice.id)
        self.assertEqual(str(xccdf_notice), string_value,
                         'String representation does not match')


def suite():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTest(loader.loadTestsFromTestCase(NoticeTestCase))
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
