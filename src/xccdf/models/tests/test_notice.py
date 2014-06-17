# -*- coding: utf-8 -*-

# Python stdlib
import unittest
import os
import io
import sys

# lxml
from lxml import etree

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

        element_tree = etree.fromstring(xml_string.encode('utf-8'))

        return element_tree[1]

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

        self.assertEqual(xccdf_notice.name, 'notice',
                         'notice tag name does not match')

        self.assertTrue(hasattr(xccdf_notice, 'id'))

    def test_init_empty_instance(self):
        """
        Tests the class constructor with an empty instance
        """

        error_msg = 'either xml_element or id are required'

        if sys.version_info[0] >= 3 and sys.version_info[1] >= 2:
            with self.assertRaisesRegex(ValueError,
                                        error_msg):
                Notice()
        else:
            with self.assertRaisesRegexp(ValueError,
                                         error_msg):
                Notice()

    def test_init_no_xml_element(self):
        """
        Tests the class constructor without an xml_element
        """

        id = 'terms_of_use'
        xccdf_notice = Notice(id=id)

        self.assertEqual(xccdf_notice.name, 'notice',
                         'notice tag name does not match')

        self.assertEqual(xccdf_notice.id, id, 'notice id does not match')

    def test_init_no_id(self):
        """
        Tests the class constructor without an id
        """

        error_msg = 'id attribute required'

        if sys.version_info[0] >= 3 and sys.version_info[1] >= 2:
            with self.assertRaisesRegex(RequiredAttributeException,
                                        error_msg):
                self.create_notice_object('no_id')
        else:
            with self.assertRaisesRegexp(RequiredAttributeException,
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

    def test_print_object_empty_instance(self):
        """
        Tests the string representation of an Notice object
        from an empty instance
        """

        id = 'terms_of_use'
        xccdf_notice = Notice(id=id)

        string_value = 'notice {id}'.format(id=id)
        self.assertEqual(str(xccdf_notice), string_value,
                         'String representation does not match')


def suite():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTest(loader.loadTestsFromTestCase(NoticeTestCase))
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
