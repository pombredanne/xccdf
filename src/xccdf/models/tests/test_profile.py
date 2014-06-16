# -*- coding: utf-8 -*-

# Python stdlib
import unittest
import os
import io

# lxml
from lxml import etree

# XCCDF
from xccdf.models.profile import Profile
from xccdf.exceptions import RequiredAttributeException
from xccdf.exceptions import CardinalityException


class ProfileTestCase(unittest.TestCase):

    """
    Test cases for Profile class
    """

    def load_example_element(self, xml_file_type='ok'):
        """
        Helper method to load an XML element
        """

        file_name = 'example_xccdf_profile_{type}.xml'.format(
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

    def create_profile_object(self, object_type='ok'):
        """
        Helper method to create the Profile object

        :returns: Profile object
        :rtype: xccdf.models.description.Profile
        """

        xml_element = self.load_example_element(object_type)

        return Profile(xml_element)

    def test_init_with_xml_element(self):
        """
        Tests the class constructor with a xml element
        """

        xccdf_profile = self.create_profile_object('ok')

        self.assertEqual(xccdf_profile.name, 'Profile',
                         'Profile tag name does not match')
        self.assertTrue(hasattr(xccdf_profile, 'id'),
                        'Profile ID must be defined')

    def test_init_no_id(self):
        """
        Tests the class constructor with a xml element
        """

        error_msg = 'id attribute required'
        with self.assertRaisesRegex(RequiredAttributeException,
                                    error_msg):
            self.create_profile_object('no_id')

    def test_init_with_empty_instance(self):
        """
        Tests the class constructor with an empty instance
        """

        error_msg = 'either xml_element or id are required'
        with self.assertRaisesRegex(ValueError,
                                    error_msg):
            Profile()

    def test_init_no_xml_element(self):
        """
        Tests the class constructor with no xml_element
        """

        id = 'united_states_government_configuration_baseline'
        xccdf_profile = Profile(id=id)

        self.assertEqual(xccdf_profile.name, 'Profile',
                         'Profile tag name does not match')
        self.assertEqual(xccdf_profile.id, id,
                         'Profile id does not match')
        self.assertEqual(xccdf_profile.children, list(),
                         'Profile children list must be empty')

    def test_init_duplicated_version(self):
        """
        Tests the class constructor with more than one version
        """

        error_msg = 'version element found more than once'
        with self.assertRaisesRegex(CardinalityException,
                                    error_msg):
            self.create_profile_object('duplicated_version')

    def test_init_no_title(self):
        """
        Tests the class constructor with no title
        """

        error_msg = 'title element is required at least once'
        with self.assertRaisesRegex(CardinalityException,
                                    error_msg):
            self.create_profile_object('no_title')

    def test_print_object(self):
        """
        Tests the string representation of an Profile object
        """

        xccdf_profile = self.create_profile_object('ok')

        string_value = 'Profile {id}'.format(
            id=xccdf_profile.id)
        self.assertEqual(str(xccdf_profile), string_value,
                         'String representation does not match')

    def test_print_object_empty_instance(self):
        """
        Tests the string representation of an Profile object
        from an empty instance
        """

        id = 'united_states_government_configuration_baseline'
        xccdf_description = Profile(id=id)

        string_value = 'Profile {id}'.format(
            id=id)
        self.assertEqual(str(xccdf_description), string_value,
                         'String representation does not match')

def suite():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTest(loader.loadTestsFromTestCase(ProfileTestCase))
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
