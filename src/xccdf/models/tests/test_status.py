# -*- coding: utf-8 -*-

# Python stdlib
import unittest
import os
import io
import sys
from datetime import date

# lxml
from lxml import etree

# XCCDF
from xccdf.models.status import Status
from xccdf.constants.status import STATUS_VALUE_CHOICES
from xccdf.exceptions import InvalidValueException


class StatusTestCase(unittest.TestCase):

    """
    Test cases for Status class
    """

    def load_example_element(self, xml_file_type='ok'):
        """
        Helper method to load an XML element
        """

        file_name = 'example_xccdf_status_{type}.xml'.format(
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

    def create_status_object(self, object_type='ok'):
        """
        Helper method to create the Status object

        :returns: Status object
        :rtype: xccdf.models.status.Status
        """

        xml_element = self.load_example_element(object_type)

        return Status(xml_element)

    def test_init_all_ok(self):
        """
        Tests the class constructor
        """

        xccdf_status = self.create_status_object('ok')

        self.assertEqual(xccdf_status.name, 'status',
                         'Status tag name does not match')

        self.assertIn(xccdf_status.text, STATUS_VALUE_CHOICES)

    def test_init_wrong_state(self):
        """
        Tests the class constructor with a wrong state
        """
        xml_element = self.load_example_element('ko')

        error_msg = 'is not valid. Must be one of this'

        if sys.version_info[0] >= 3 and sys.version_info[1] >= 2:
            with self.assertRaisesRegex(InvalidValueException,
                                        error_msg):
                Status(xml_element)
        else:
            with self.assertRaisesRegexp(InvalidValueException,
                                         error_msg):
                Status(xml_element)

    def test_init_no_date(self):
        """
        Tests the class constructor without a date
        """

        xccdf_status = self.create_status_object('no_date')

        self.assertFalse(hasattr(xccdf_status, 'date'))

    def test_init_no_xml_element(self):
        """
        Tests the class constructor with an empty instance
        """

        xccdf_status = Status(state=STATUS_VALUE_CHOICES[0])

        self.assertEqual(xccdf_status.name, 'status',
                         'Status tag name does not match')

        self.assertEqual(xccdf_status.text, STATUS_VALUE_CHOICES[0],
                         'State does not match')

    def test_init_empty_instance(self):
        """
        Tests the class constructor with an empty instance
        """

        error_msg = 'either xml_element or state are required'

        if sys.version_info[0] >= 3 and sys.version_info[1] >= 2:
            with self.assertRaisesRegex(ValueError,
                                        error_msg):
                Status()
        else:
            with self.assertRaisesRegexp(ValueError,
                                         error_msg):
                Status()

    def test_print_object(self):
        """
        Tests the string representation of an Status object
        """

        xccdf_status = self.create_status_object('ok')

        string_value = 'status {state} ({date})'.format(
            state=xccdf_status.text,
            date=xccdf_status.date)
        self.assertEqual(str(xccdf_status), string_value,
                         'String representation does not match')

    def test_print_object_no_date(self):
        """
        Tests the string representation of an Status object without a date
        """

        xccdf_status = self.create_status_object('no_date')

        string_value = 'status {state}'.format(state=xccdf_status.text)
        self.assertEqual(str(xccdf_status), string_value,
                         'String representation does not match')

    def test_print_object_empty_instance(self):
        """
        Tests the string representation of an Status object
        from an empty instance
        """

        xccdf_status = Status(state=STATUS_VALUE_CHOICES[0])

        string_value = 'status {state}'.format(state=STATUS_VALUE_CHOICES[0])
        self.assertEqual(str(xccdf_status), string_value,
                         'String representation does not match')

    def test_method_str_to_date(self):
        """
        Tests the str_to_date method
        """

        xccdf_status = self.create_status_object('ok')

        self.assertIsInstance(xccdf_status.str_to_date(), date,
                              'Returned date is not a date object')

    def test_method_str_to_date_no_date(self):
        """
        Tests the str_to_date method on a status without date
        """

        xccdf_status = self.create_status_object('no_date')

        self.assertIsNone(xccdf_status.str_to_date(),
                          'Expected None due to empty date')

    def test_method_update_xml_element(self):
        """
        Tests the update_xml_element method
        """

        xccdf_status = self.create_status_object('ok')

        new_state = 'test_state'

        self.assertNotEqual(xccdf_status.text, new_state,
                            'New state is equal to original')

        xccdf_status.text = new_state
        xccdf_status.update_xml_element()

        self.assertEqual(xccdf_status.xml_element.text, new_state,
                         'XML state does not match new state')
        self.assertEqual(xccdf_status.text, new_state,
                         'Title state does not match new state')

    def test_method_update_xml_element_empty_instance(self):
        """
        Tests the update_xml_element method with an empty instance
        """

        xccdf_status = Status(state=STATUS_VALUE_CHOICES[0])

        self.assertFalse(hasattr(xccdf_status, 'xml_element'),
                         'XML element is defined')

        xccdf_status.update_xml_element()

        self.assertTrue(hasattr(xccdf_status, 'xml_element'),
                        'XML element is not defined')

    def test_method_to_xml_string(self):
        """
        Tests the to_xml_string method
        """

        xccdf_status = self.create_status_object('ok')

        xml_content = xccdf_status.to_xml_string()

        new_xccdf_select = Status(
            etree.fromstring(xml_content.encode('utf-8')))

        self.assertEqual(xccdf_status.text, new_xccdf_select.text,
                         'Status state does not match')


def suite():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTest(loader.loadTestsFromTestCase(StatusTestCase))
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
