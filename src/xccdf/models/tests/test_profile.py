# -*- coding: utf-8 -*-

# Python stdlib
import unittest
import os
import io
import sys

# lxml
from lxml import etree

# XCCDF
from xccdf.models.profile import Profile
from xccdf.models.status import Status
from xccdf.models.version import Version
from xccdf.models.title import Title
from xccdf.models.description import Description
from xccdf.models.platform import Platform
from xccdf.models.select import Select
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

        if sys.version_info[0] >= 3 and sys.version_info[1] >= 2:
            with self.assertRaisesRegex(RequiredAttributeException,
                                        error_msg):
                self.create_profile_object('no_id')
        else:
            with self.assertRaisesRegexp(RequiredAttributeException,
                                         error_msg):
                self.create_profile_object('no_id')

    def test_init_with_empty_instance(self):
        """
        Tests the class constructor with an empty instance
        """

        error_msg = 'either xml_element or id are required'

        if sys.version_info[0] >= 3 and sys.version_info[1] >= 2:
            with self.assertRaisesRegex(ValueError,
                                        error_msg):
                Profile()
        else:
            with self.assertRaisesRegexp(ValueError,
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

        if sys.version_info[0] >= 3 and sys.version_info[1] >= 2:
            with self.assertRaisesRegex(CardinalityException,
                                        error_msg):
                self.create_profile_object('duplicated_version')
        else:
            with self.assertRaisesRegexp(CardinalityException,
                                         error_msg):
                self.create_profile_object('duplicated_version')

    def test_init_no_title(self):
        """
        Tests the class constructor with no title
        """

        error_msg = 'title element is required at least once'

        if sys.version_info[0] >= 3 and sys.version_info[1] >= 2:
            with self.assertRaisesRegex(CardinalityException,
                                        error_msg):
                self.create_profile_object('no_title')
        else:
            with self.assertRaisesRegexp(CardinalityException,
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
        xccdf_profile = Profile(id=id)

        string_value = 'Profile {id}'.format(
            id=id)
        self.assertEqual(str(xccdf_profile), string_value,
                         'String representation does not match')

    def test_method_update_xml_element(self):
        """
        Tests the update_xml_element method
        """

        xccdf_profile = self.create_profile_object('ok')

        new_id = 'new_profile_id_test'

        self.assertNotEqual(xccdf_profile.id, new_id,
                            'New id is equal to original')

        xccdf_profile.id = new_id
        xccdf_profile.update_xml_element()

        self.assertEqual(xccdf_profile.xml_element.attrib['id'], new_id,
                         'XML id does not match new id')
        self.assertEqual(xccdf_profile.id, new_id,
                         'Title id does not match new id')

    def test_method_update_xml_element_empty_instance(self):
        """
        Tests the update_xml_element method with an empty instance
        """

        id = 'united_states_government_configuration_baseline'
        xccdf_profile = Profile(id=id)

        self.assertFalse(hasattr(xccdf_profile, 'xml_element'),
                         'XML element is defined')

        xccdf_profile.update_xml_element()

        self.assertTrue(hasattr(xccdf_profile, 'xml_element'),
                        'XML element is not defined')

    def test_method_as_dict(self):
        """
        Tests the as_dict method
        """

        xccdf_profile = self.create_profile_object('ok')

        result_dict = xccdf_profile.as_dict()

        self.assertIsInstance(result_dict, dict,
                              'as_dict result is not a dictionary')

        statuses = list()
        version = None
        titles = list()
        descriptions = list()
        platforms = list()
        selects = list()

        for child in xccdf_profile.children:
            if isinstance(child, Version):
                version = child.as_dict()
            elif isinstance(child, Status):
                statuses.append(child.as_dict())
            elif isinstance(child, Title):
                titles.append(child.as_dict())
            elif isinstance(child, Description):
                descriptions.append(child.as_dict())
            elif isinstance(child, Platform):
                platforms.append(child.as_dict())
            elif isinstance(child, Select):
                selects.append(child.as_dict())

        if version is not None:
            result_version = result_dict.get('version', None)
            self.assertIsNotNone(result_version,
                                 'Version not defined in dict result')
            self.assertEqual(result_version, version, 'Version does not match')
        if len(statuses) > 0:
            result_statuses = result_dict.get('statuses', None)
            self.assertIsNotNone(result_statuses,
                                 'Statuses list not defined in dict result')
            self.assertIsInstance(result_statuses, list,
                                  'Statuses list is not a list')
            for status in statuses:
                self.assertIn(status, result_statuses,
                              'Status not found in statuses result list')
        if len(titles) > 0:
            result_titles = result_dict.get('titles', None)
            self.assertIsNotNone(result_titles,
                                 'Titles list not defined in dict result')
            self.assertIsInstance(result_titles, list,
                                  'Titles list is not a list')
            for title in titles:
                self.assertIn(title, result_titles,
                              'Title not found in titles result list')
        if len(descriptions) > 0:
            result_descriptions = result_dict.get('descriptions', None)
            error_msg = 'Descriptions list not defined in dict result'
            self.assertIsNotNone(result_descriptions, error_msg)
            self.assertIsInstance(result_descriptions, list,
                                  'Descriptions list is not a list')
            error_msg = 'Description not found in descriptions result list'
            for description in descriptions:
                self.assertIn(description, result_descriptions, error_msg)

        if len(platforms) > 0:
            result_platforms = result_dict.get('platforms', None)
            self.assertIsNotNone(result_platforms,
                                 'Platforms list not defined in dict result')
            self.assertIsInstance(result_platforms, list,
                                  'Platforms list is not a list')
            for platform in platforms:
                self.assertIn(platform, result_platforms,
                              'Platform not found in platforms result list')

        if len(selects) > 0:
            result_selects = result_dict.get('selects', None)
            self.assertIsNotNone(result_selects,
                                 'Selects list not defined in dict result')
            self.assertIsInstance(result_selects, list,
                                  'Selects list is not a list')
            for select in selects:
                self.assertIn(select, result_selects,
                              'Select not found in selects result list')


def suite():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTest(loader.loadTestsFromTestCase(ProfileTestCase))
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
