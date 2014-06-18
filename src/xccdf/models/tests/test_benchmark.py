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


def suite():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTest(loader.loadTestsFromTestCase(BenchmarkTestCase))
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())