# -*- coding: utf-8 -*-

# Python stdlib
import unittest
import os
import io
import sys

# lxml
from lxml import etree

# XCCDF
from xccdf.models.tailoring import Tailoring
from xccdf.exceptions import RequiredAttributeException
from xccdf.exceptions import CardinalityException
from xccdf.exceptions import InvalidValueException


class ProfileTestCase(unittest.TestCase):

    """
    Test cases for Profile class
    """

    def load_example_element(self, xml_file_type='ok'):
        """
        Helper method to load an XML element
        """

        file_name = 'example_xccdf_tailoring_{type}.xml'.format(
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

    def create_tailoring_element(self, object_type='ok'):
        """
        Helper method to create the Profile object

        :returns: Profile object
        :rtype: xccdf.models.description.Profile
        """

        xml_element = self.load_example_element(object_type)

        return Tailoring(xml_element)

    def test_init_with_xml_element(self):
        """
        Tests the class constructor with a xml element
        """

        xccdf_tailoring = self.create_tailoring_element('ok')

        self.assertEqual(xccdf_tailoring.name, 'Tailoring',
                         'Tailoring tag name does not match')
        self.assertTrue(hasattr(xccdf_tailoring, 'id'),
                        'Tailoring ID must be defined')

    def test_init_no_id(self):
        """
        Tests the class constructor with a xml element
        """

        error_msg = 'id attribute required'

        if sys.version_info[0] >= 3 and sys.version_info[1] >= 2:
            with self.assertRaisesRegex(RequiredAttributeException,
                                        error_msg):
                self.create_tailoring_element('no_id')
        else:
            with self.assertRaisesRegexp(RequiredAttributeException,
                                         error_msg):
                self.create_tailoring_element('no_id')

    def test_init_invalid_id(self):
        """
        Tests the class constructor with a xml element
        """

        error_msg = 'id invalid format'
        if sys.version_info[0] >= 3 and sys.version_info[1] >= 2:
            with self.assertRaisesRegex(InvalidValueException,
                                        error_msg):
                self.create_tailoring_element('invalid_id')
        else:
            with self.assertRaisesRegexp(InvalidValueException,
                                         error_msg):
                self.create_tailoring_element('invalid_id')

    def test_init_with_empty_instance(self):
        """
        Tests the class constructor with an empty instance
        """

        error_msg = 'either xml_element or id are required'
        if sys.version_info[0] >= 3 and sys.version_info[1] >= 2:
            with self.assertRaisesRegex(ValueError,
                                        error_msg):
                Tailoring()
        else:
            with self.assertRaisesRegexp(ValueError,
                                         error_msg):
                Tailoring()

    def test_init_no_xml_element(self):
        """
        Tests the class constructor with no xml_element
        """

        id = 'xccdf_test_tailoring_test'
        xccdf_tailoring = Tailoring(id=id)

        self.assertEqual(xccdf_tailoring.name, 'Tailoring',
                         'Tailoring tag name does not match')
        self.assertEqual(xccdf_tailoring.id, id,
                         'Tailoring id does not match')
        self.assertEqual(xccdf_tailoring.children, list(),
                         'Tailoring children list must be empty')

    def test_init_duplicated_version(self):
        """
        Tests the class constructor with more than one version
        """

        error_msg = 'version element found more than once'

        if sys.version_info[0] >= 3 and sys.version_info[1] >= 2:
            with self.assertRaisesRegex(CardinalityException,
                                        error_msg):
                self.create_tailoring_element('duplicated_version')
        else:
            with self.assertRaisesRegexp(CardinalityException,
                                         error_msg):
                self.create_tailoring_element('duplicated_version')

    def test_init_no_version(self):
        """
        Tests the class constructor with no version
        """

        error_msg = 'version element is required'

        if sys.version_info[0] >= 3 and sys.version_info[1] >= 2:
            with self.assertRaisesRegex(CardinalityException,
                                        error_msg):
                self.create_tailoring_element('no_version')
        else:
            with self.assertRaisesRegexp(CardinalityException,
                                         error_msg):
                self.create_tailoring_element('no_version')

    def test_init_no_title(self):
        """
        Tests the class constructor with no title
        """

        error_msg = 'Profile element is required at least once'

        if sys.version_info[0] >= 3 and sys.version_info[1] >= 2:
            with self.assertRaisesRegex(CardinalityException,
                                        error_msg):
                self.create_tailoring_element('no_profile')
        else:
            with self.assertRaisesRegexp(CardinalityException,
                                         error_msg):
                self.create_tailoring_element('no_profile')

    def test_print_object(self):
        """
        Tests the string representation of an Tailoring object
        """

        xccdf_tailoring = self.create_tailoring_element('ok')

        string_value = 'Tailoring {id}'.format(
            id=xccdf_tailoring.id)
        self.assertEqual(str(xccdf_tailoring), string_value,
                         'String representation does not match')

    def test_print_object_empty_instance(self):
        """
        Tests the string representation of an Tailoring object
        from an empty instance
        """

        id = 'xccdf_test_tailoring_test'
        xccdf_tailoring = Tailoring(id=id)

        string_value = 'Tailoring {id}'.format(
            id=id)
        self.assertEqual(str(xccdf_tailoring), string_value,
                         'String representation does not match')

    def test_method_update_xml_element(self):
        """
        Tests the update_xml_element method
        """

        xccdf_tailoring = self.create_tailoring_element('ok')

        new_id = 'new_profile_id_test'

        self.assertNotEqual(xccdf_tailoring.id, new_id,
                            'New id is equal to original')

        xccdf_tailoring.id = new_id
        xccdf_tailoring.update_xml_element()

        self.assertEqual(xccdf_tailoring.xml_element.attrib['id'], new_id,
                         'XML id does not match new id')
        self.assertEqual(xccdf_tailoring.id, new_id,
                         'Title id does not match new id')

    def test_method_update_xml_element_empty_instance(self):
        """
        Tests the update_xml_element method with an empty instance
        """

        id = 'xccdf_test_tailoring_test'
        xccdf_profile = Tailoring(id=id)

        self.assertFalse(hasattr(xccdf_profile, 'xml_element'),
                         'XML element is defined')

        xccdf_profile.update_xml_element()

        self.assertTrue(hasattr(xccdf_profile, 'xml_element'),
                        'XML element is not defined')


def suite():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTest(loader.loadTestsFromTestCase(ProfileTestCase))
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
