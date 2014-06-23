# -*- coding: utf-8 -*-

# Python stdlib
import unittest
import os
import io
import sys

# lxml
from lxml import etree

# XCCDF
from xccdf.models.benchmark import Benchmark
from xccdf.models.version import Version
from xccdf.models.title import Title
from xccdf.models.status import Status
from xccdf.models.description import Description
from xccdf.models.front_matter import FrontMatter
from xccdf.models.rear_matter import RearMatter
from xccdf.models.platform import Platform
from xccdf.models.profile import Profile
from xccdf.models.group import Group
from xccdf.exceptions import RequiredAttributeException
from xccdf.exceptions import CardinalityException


class BenchmarkTestCase(unittest.TestCase):

    """
    Test cases for Benchmark class
    """

    def load_example_element(self, xml_file_type='ok'):
        """
        Helper method to load an XML element
        """

        file_name = 'example_xccdf_benchmark_{type}.xml'.format(
            type=xml_file_type)

        xml_path = os.path.abspath(os.path.dirname(__file__))
        xml_file = io.open(os.path.join(
            xml_path,
            'examples',
            file_name))

        xml_string = xml_file.read()
        xml_file.close()

        element_tree = etree.fromstring(xml_string.encode('utf-8'))

        return element_tree

    def create_benchmark_object(self, object_type='ok'):
        """
        Helper method to create the Benchmark object

        :returns: Benchmark object
        :rtype: xccdf.models.description.Benchmark
        """

        xml_element = self.load_example_element(object_type)

        return Benchmark(xml_element)

    def test_init_with_xml_element(self):
        """
        Tests the class constructor with a xml element
        """

        xccdf_benchmark = self.create_benchmark_object('ok')

        self.assertEqual(xccdf_benchmark.name, 'Benchmark',
                         'Benchmark tag name does not match')
        self.assertTrue(hasattr(xccdf_benchmark, 'id'),
                        'Benchmark ID must be defined')

    def test_init_no_id(self):
        """
        Tests the class constructor with a xml element
        """

        error_msg = 'id attribute required'

        if sys.version_info[0] >= 3 and sys.version_info[1] >= 2:
            with self.assertRaisesRegex(RequiredAttributeException,
                                        error_msg):
                self.create_benchmark_object('no_id')
        else:
            with self.assertRaisesRegexp(RequiredAttributeException,
                                         error_msg):
                self.create_benchmark_object('no_id')

    def test_init_with_empty_instance(self):
        """
        Tests the class constructor with an empty instance
        """

        error_msg = 'either xml_element or id are required'

        if sys.version_info[0] >= 3 and sys.version_info[1] >= 2:
            with self.assertRaisesRegex(ValueError,
                                        error_msg):
                Benchmark()
        else:
            with self.assertRaisesRegexp(ValueError,
                                         error_msg):
                Benchmark()

    def test_init_no_xml_element(self):
        """
        Tests the class constructor with no xml_element
        """

        id = "usgcb-rhel5desktop-benchmark-2.2.2.5.b"
        xccdf_benchmark = Benchmark(id=id)

        self.assertEqual(xccdf_benchmark.name, 'Benchmark',
                         'Benchmark tag name does not match')
        self.assertEqual(xccdf_benchmark.id, id,
                         'Benchmark id does not match')
        self.assertEqual(xccdf_benchmark.children, list(),
                         'Benchmark children list must be empty')

    def test_init_duplicated_version(self):
        """
        Tests the class constructor with more than one version
        """

        error_msg = 'version element found more than once'

        if sys.version_info[0] >= 3 and sys.version_info[1] >= 2:
            with self.assertRaisesRegex(CardinalityException,
                                        error_msg):
                self.create_benchmark_object('duplicated_version')
        else:
            with self.assertRaisesRegexp(CardinalityException,
                                         error_msg):
                self.create_benchmark_object('duplicated_version')

    def test_init_no_version(self):
        """
        Tests the class constructor with no version
        """

        error_msg = 'a Benchmark must contain a version element'

        if sys.version_info[0] >= 3 and sys.version_info[1] >= 2:
            with self.assertRaisesRegex(CardinalityException,
                                        error_msg):
                self.create_benchmark_object('no_version')
        else:
            with self.assertRaisesRegexp(CardinalityException,
                                         error_msg):
                self.create_benchmark_object('no_version')

    def test_init_no_status(self):
        """
        Tests the class constructor with no status
        """

        error_msg = 'a Benchmark must contain at least a status element'

        if sys.version_info[0] >= 3 and sys.version_info[1] >= 2:
            with self.assertRaisesRegex(CardinalityException,
                                        error_msg):
                self.create_benchmark_object('no_status')
        else:
            with self.assertRaisesRegexp(CardinalityException,
                                         error_msg):
                self.create_benchmark_object('no_status')

    def test_init_no_benchmarks_or_rules(self):
        """
        Tests the class constructor with no children benchmarks or rules
        """

        error_msg = 'a Benchmark must contain at least a group or a rule'

        if sys.version_info[0] >= 3 and sys.version_info[1] >= 2:
            with self.assertRaisesRegex(CardinalityException,
                                        error_msg):
                self.create_benchmark_object('no_groups_rules')
        else:
            with self.assertRaisesRegexp(CardinalityException,
                                         error_msg):
                self.create_benchmark_object('no_groups_rules')

    def test_print_object(self):
        """
        Tests the string representation of an Benchmark object
        """

        xccdf_benchmark = self.create_benchmark_object('ok')

        string_value = 'Benchmark {id}'.format(
            id=xccdf_benchmark.id)
        self.assertEqual(str(xccdf_benchmark), string_value,
                         'String representation does not match')

    def test_print_object_empty_instance(self):
        """
        Tests the string representation of an Benchmark object
        from an empty instance
        """

        id = "usgcb-rhel5desktop-benchmark-2.2.2.5.b"
        xccdf_benchmark = Benchmark(id=id)

        string_value = 'Benchmark {id}'.format(
            id=id)
        self.assertEqual(str(xccdf_benchmark), string_value,
                         'String representation does not match')

    def test_method_update_xml_element(self):
        """
        Tests the update_xml_element method
        """

        xccdf_benchmark = self.create_benchmark_object('ok')

        new_id = 'new_benchmark_id_test'

        self.assertNotEqual(xccdf_benchmark.id, new_id,
                            'New id is equal to original')

        xccdf_benchmark.id = new_id
        xccdf_benchmark.update_xml_element()

        self.assertEqual(xccdf_benchmark.xml_element.attrib['id'], new_id,
                         'XML id does not match new id')
        self.assertEqual(xccdf_benchmark.id, new_id,
                         'Title id does not match new id')

    def test_method_update_xml_element_empty_instance(self):
        """
        Tests the update_xml_element method with an empty instance
        """

        id = 'united_states_government_configuration_baseline'
        xccdf_benchmark = Benchmark(id=id)

        self.assertFalse(hasattr(xccdf_benchmark, 'xml_element'),
                         'XML element is defined')

        xccdf_benchmark.update_xml_element()

        self.assertTrue(hasattr(xccdf_benchmark, 'xml_element'),
                        'XML element is not defined')

    def test_method_as_dict(self):
        """
        Tests the as_dict method
        """

        xccdf_benchmark = self.create_benchmark_object('ok')

        result_dict = xccdf_benchmark.as_dict()

        self.assertIsInstance(result_dict, dict,
                              'as_dict result is not a dictionary')

        statuses = list()
        titles = list()
        descriptions = list()
        front_matters = list()
        rear_matters = list()
        platforms = list()
        version = None
        profiles = list()
        groups = list()

        for child in xccdf_benchmark.children:
            if isinstance(child, Version):
                version = child.as_dict()
            elif isinstance(child, Status):
                statuses.append(child.as_dict())
            elif isinstance(child, Title):
                titles.append(child.as_dict())
            elif isinstance(child, Description):
                descriptions.append(child.as_dict())
            elif isinstance(child, FrontMatter):
                front_matters.append(child.as_dict())
            elif isinstance(child, RearMatter):
                rear_matters.append(child.as_dict())
            elif isinstance(child, Platform):
                platforms.append(child.as_dict())
            elif isinstance(child, Profile):
                profiles.append(child.as_dict())
            elif isinstance(child, Group):
                groups.append(child.as_dict())

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

        if len(front_matters) > 0:
            result_fmatters = result_dict.get('front_matters', None)
            error_msg = 'Front matters list not defined in dict result'
            self.assertIsNotNone(result_fmatters, error_msg)
            self.assertIsInstance(result_fmatters, list,
                                  'Front matters list is not a list')
            error_msg = 'Front matter not found in front_matters result list'
            for fmatter in front_matters:
                self.assertIn(fmatter, result_fmatters, error_msg)

        if len(rear_matters) > 0:
            result_rmatters = result_dict.get('rear_matters', None)
            error_msg = 'Rear matters list not defined in dict result'
            self.assertIsNotNone(result_rmatters, error_msg)
            self.assertIsInstance(result_rmatters, list,
                                  'Rear matters list is not a list')
            error_msg = 'Rear matter not found in rear_matters result list'
            for rmatter in rear_matters:
                self.assertIn(rmatter, result_rmatters, error_msg)

        if len(platforms) > 0:
            result_platforms = result_dict.get('platforms', None)
            self.assertIsNotNone(result_platforms,
                                 'Platforms list not defined in dict result')
            self.assertIsInstance(result_platforms, list,
                                  'Platforms list is not a list')
            for platform in platforms:
                self.assertIn(platform, result_platforms,
                              'Platform not found in platforms result list')

        if len(profiles) > 0:
            result_profiles = result_dict.get('profiles', None)
            self.assertIsNotNone(result_profiles,
                                 'Profiles list not defined in dict result')
            self.assertIsInstance(result_profiles, list,
                                  'Profiles list is not a list')
            for profile in profiles:
                self.assertIn(profile, result_profiles,
                              'Profile not found in profiles result list')

        if len(groups) > 0:
            result_groups = result_dict.get('groups', None)
            self.assertIsNotNone(result_groups,
                                 'Groups list not defined in dict result')
            self.assertIsInstance(result_groups, list,
                                  'Groups list is not a list')
            for group in groups:
                self.assertIn(group, result_groups,
                              'Group not found in groups result list')


def suite():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTest(loader.loadTestsFromTestCase(BenchmarkTestCase))
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
