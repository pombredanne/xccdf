# -*- coding: utf-8 -*-

# Python stdlib
import unittest
import os
import io
from xml.etree import ElementTree
from datetime import date

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

        element_tree = ElementTree.fromstring(xml_string)

        return element_tree[0]

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
        with self.assertRaisesRegex(InvalidValueException,
                                    error_msg):
            Status(xml_element)

    def test_init_no_date(self):
        """
        Tests the class constructor without a date
        """

        xccdf_status = self.create_status_object('no_date')

        self.assertFalse(hasattr(xccdf_status, 'date'))

    def test_print_object(self):
        """
        Tests the string representation of an Status object
        """

        xccdf_status = self.create_status_object('ok')

        string_value = '{state} ({date})'.format(state=xccdf_status.text,
                                                 date=xccdf_status.date)
        self.assertEqual(str(xccdf_status), string_value,
                         'String representation does not match')

    def test_print_object_no_date(self):
        """
        Tests the string representation of an Status object without a date
        """

        xccdf_status = self.create_status_object('no_date')

        string_value = '{state}'.format(state=xccdf_status.text)
        self.assertEqual(str(xccdf_status), string_value,
                         'String representation does not match')

    def test_method_get_date(self):
        """
        Tests the get_date method
        """

        xccdf_status = self.create_status_object('ok')

        self.assertIsInstance(xccdf_status.get_date(), date,
                              'Returned date is not a date object')

    def test_method_get_date_no_date(self):
        """
        Tests the get_date method on a status without date
        """

        xccdf_status = self.create_status_object('no_date')

        self.assertIsNone(xccdf_status.get_date(),
                          'Expected None due to empty date')


def suite():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTest(loader.loadTestsFromTestCase(StatusTestCase))
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
