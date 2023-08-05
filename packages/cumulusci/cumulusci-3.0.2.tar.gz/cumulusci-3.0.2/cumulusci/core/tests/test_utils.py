import datetime
import os
import unittest

import pytz

from .. import utils

from cumulusci.core.exceptions import ConfigMergeError
from cumulusci.utils import temporary_dir, touch

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


class TestUtils(unittest.TestCase):
    def test_parse_datetime(self):
        dt = utils.parse_datetime("2018-07-30", "%Y-%m-%d")
        self.assertEqual(dt, datetime.datetime(2018, 7, 30, 0, 0, 0, 0, pytz.UTC))

    def test_process_bool_arg(self):
        for arg in (True, "True", "true", "1"):
            self.assertTrue(utils.process_bool_arg(arg))

        for arg in (False, "False", "false", "0"):
            self.assertFalse(utils.process_bool_arg(arg))

        for arg in (None, datetime.datetime.now()):
            self.assertIsNone(utils.process_bool_arg(arg))

    def test_process_list_arg(self):
        self.assertEqual([1, 2], utils.process_list_arg([1, 2]))
        self.assertEqual(["a", "b"], utils.process_list_arg("a, b"))
        self.assertEqual(None, utils.process_list_arg(None))

    def test_process_glob_list_arg(self):
        with temporary_dir():
            touch("foo.py")
            touch("bar.robot")

            # Expect passing arg as list works.
            self.assertEqual(
                ["foo.py", "bar.robot"],
                utils.process_glob_list_arg(["foo.py", "bar.robot"]),
            )

            # Falsy arg should return an empty list
            self.assertEqual([], utils.process_glob_list_arg(None))
            self.assertEqual([], utils.process_glob_list_arg(""))
            self.assertEqual([], utils.process_glob_list_arg([]))

            # Expect output to be in order given
            self.assertEqual(
                ["foo.py", "bar.robot"],
                utils.process_glob_list_arg("foo.py, bar.robot"),
            )

            # Expect sorted output of glob results
            self.assertEqual(["bar.robot", "foo.py"], utils.process_glob_list_arg("*"))

            # Patterns that don't match any files
            self.assertEqual(
                ["*.bar", "x.y.z"], utils.process_glob_list_arg("*.bar, x.y.z")
            )

            # Recursive
            os.mkdir("subdir")
            filename = os.path.join("subdir", "baz.resource")
            touch(filename)
            self.assertEqual([filename], utils.process_glob_list_arg("**/*.resource"))

    def test_decode_to_unicode(self):
        self.assertEqual(u"\xfc", utils.decode_to_unicode(b"\xfc"))
        self.assertEqual(u"\u2603", utils.decode_to_unicode(u"\u2603"))
        self.assertEqual(None, utils.decode_to_unicode(None))


class TestMergedConfig(unittest.TestCase):
    def test_init(self):
        config = utils.merge_config(
            {"global_config": {"hello": "world"}, "user_config": {"hello": "christian"}}
        )
        self.assertEqual(config["hello"], "christian")

    def test_merge_failure(self):
        with self.assertRaises(ConfigMergeError) as cm:
            utils.merge_config(
                {
                    "global_config": {"hello": "world", "test": {"sample": 1}},
                    "user_config": {"hello": "christian", "test": [1, 2]},
                }
            )
        exception = cm.exception
        self.assertEqual(exception.config_name, "user_config")


class TestDictMerger(unittest.TestCase):
    """ some stuff that didnt get covered by usual usage  """

    def test_merge_into_list(self):
        combo = utils.dictmerge([1, 2], 3)
        self.assertSequenceEqual(combo, [1, 2, 3])

    def test_cant_merge_into_dict(self):
        with self.assertRaises(ConfigMergeError):
            utils.dictmerge({"a": "b"}, 2)

    def test_cant_merge_nonsense(self):
        with self.assertRaises(ConfigMergeError):
            utils.dictmerge(pytz, 2)


class TestYamlUtils(unittest.TestCase):
    yaml = """first: 1
second: 2
third:
  first: 1
  second: 2
"""

    def test_ordered_yaml_dump(self):
        ordered_data = {}
        ordered_data["first"] = 1
        ordered_data["second"] = 2
        ordered_data["third"] = {}
        ordered_data["third"]["first"] = 1
        ordered_data["third"]["second"] = 2

        result = StringIO()
        utils.ordered_yaml_dump(ordered_data, result)
        self.assertEqual(self.yaml, result.getvalue())

    def test_ordered_yaml_load(self):
        result = utils.ordered_yaml_load(self.yaml)
        self.assertIsInstance(result, dict)
        self.assertIsInstance(result["third"], dict)
