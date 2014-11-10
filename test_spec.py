#!/usr/bin/python
import unittest
import os
import json

from entei import render

SPECS_PATH = os.path.join('spec', 'specs')
SPECS = [path for path in os.listdir(SPECS_PATH) if path.endswith('.json')]
STACHE = render


def _test_case_from_path(json_path):
    json_path = '%s.json' % json_path

    class MustacheTestCase(unittest.TestCase):
        """A simple yaml based test case"""

        def _test_from_object(obj):
            """Generate a unit test from a test object"""

            def test_case(self):
                result = STACHE(obj['template'], obj['data'],
                                partials_dict=obj.get('partials', {}))

                self.assertEqual(result, obj['expected'])

            test_case.__doc__ = 'suite: {}    desc: {}'.format(spec,
                                                               obj['desc'])
            return test_case

        with open(json_path, 'r') as f:
            yaml = json.load(f)

        # Generates a unit test for each test object
        for i, test in enumerate(yaml['tests']):
            vars()['test_%s' % i] = _test_from_object(test)

    # Return the built class
    return MustacheTestCase

# Create TestCase for each json file
for spec in SPECS:
    # Ignore optional tests
    if spec[0] is not '~':
        spec = spec.split('.')[0]
        globals()[spec] = _test_case_from_path(os.path.join(SPECS_PATH, spec))

# Run unit tests from command line
if __name__ == "__main__":
    unittest.main()
