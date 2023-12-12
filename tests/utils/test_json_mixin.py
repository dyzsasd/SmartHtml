import unittest

from datetime import datetime

from smart_html.utils.mixin import JsonMixin, JsonFormat


class TestValueClass(JsonMixin):
    def __init__(self, h, i, j, k, l):
        self.h = h
        self.i = i
        self.j = j
        self.k = k
        self.l = l


class Test(JsonMixin):
    def __init__(self, a, b, c, d):
        self.a = a
        self.b = b
        self.c = c
        self.d = d


class TestDateTimeJson(unittest.TestCase):
    def test_write(self):
        dt = datetime(2023, 5, 23, 5, 43, 21, 739384)
        dt_json = JsonFormat.get_format(dt).write(dt)
        self.assertEqual(dt_json['__type'], "datetime")
        self.assertEqual(dt_json['value'], "2023-05-23T05:43:21.739384")

    def test_read(self):
        dt_json = {'__type': 'datetime', 'value': '2023-05-23T05:43:21.739384'}
        dt_parsed = JsonFormat.get_format(dt_json).read(dt_json)
        self.assertEqual(dt_parsed, datetime(2023, 5, 23, 5, 43, 21, 739384))


class TestJsonMixin(unittest.TestCase):
    def test_write_to_json(self):
        dt = datetime(2023, 5, 23, 5, 43, 21, 739384)
        value = TestValueClass(h=1, i="test value", j=dt, k=False, l=1.5)

        test_instance = Test(
            a=[value, value, 9, {3: "test33"}],
            b={"test": 1, "test2": "test2 value",
                4: 5, 6: "test9", "test12": True},
            c=value,
            d={"test_value": value},
        )

        test_instance_json = test_instance.to_json()

        target_json = {
            "__type": "Test",
            "a": [
                {
                    "__type": "TestValueClass",
                    "h": 1,
                    "i": "test value",
                    "j": {
                        "__type": "datetime",
                        "value": "2023-05-23T05:43:21.739384"
                    },
                    "k": False,
                    "l": 1.5
                },
                {
                    "__type": "TestValueClass",
                    "h": 1,
                    "i": "test value",
                    "j": {
                        "__type": "datetime",
                        "value": "2023-05-23T05:43:21.739384"
                    },
                    "k": False,
                    "l": 1.5
                },
                9,
                {
                    3: "test33",
                    "__type": "dict"
                }
            ],
            "b": {
                "test": 1,
                "test2": "test2 value",
                4: 5,
                6: "test9",
                "test12": True,
                "__type": "dict"
            },
            "c": {
                "__type": "TestValueClass",
                "h": 1,
                "i": "test value",
                "j": {
                    "__type": "datetime",
                    "value": "2023-05-23T05:43:21.739384"
                },
                "k": False,
                "l": 1.5
            },
            "d": {
                "test_value": {
                    "__type": "TestValueClass",
                    "h": 1,
                    "i": "test value",
                    "j": {
                        "__type": "datetime",
                        "value": "2023-05-23T05:43:21.739384"
                    },
                    "k": False,
                    "l": 1.5
                },
                "__type": "dict"
            }
        }
        self.assertDictEqual(test_instance_json, target_json)

    def test_read_from_json(self):
        dt = datetime(2023, 5, 23, 5, 43, 21, 739384)
        value = TestValueClass(h=1, i="test value", j=dt, k=False, l=1.5)

        target_instance = Test(
            a=[value, value, 9, {3: "test33"}],
            b={"test": 1, "test2": "test2 value",
                4: 5, 6: "test9", "test12": True},
            c=value,
            d={"test_value": value},
        )

        raw_json = {
            "__type": "Test",
            "a": [
                {
                    "__type": "TestValueClass",
                    "h": 1,
                    "i": "test value",
                    "j": {
                        "__type": "datetime",
                        "value": "2023-05-23T05:43:21.739384"
                    },
                    "k": False,
                    "l": 1.5
                },
                {
                    "__type": "TestValueClass",
                    "h": 1,
                    "i": "test value",
                    "j": {
                        "__type": "datetime",
                        "value": "2023-05-23T05:43:21.739384"
                    },
                    "k": False,
                    "l": 1.5
                },
                9,
                {
                    3: "test33",
                    "__type": "dict"
                }
            ],
            "b": {
                "test": 1,
                "test2": "test2 value",
                4: 5,
                6: "test9",
                "test12": True,
                "__type": "dict"
            },
            "c": {
                "__type": "TestValueClass",
                "h": 1,
                "i": "test value",
                "j": {
                    "__type": "datetime",
                    "value": "2023-05-23T05:43:21.739384"
                },
                "k": False,
                "l": 1.5
            },
            "d": {
                "test_value": {
                    "__type": "TestValueClass",
                    "h": 1,
                    "i": "test value",
                    "j": {
                        "__type": "datetime",
                        "value": "2023-05-23T05:43:21.739384"
                    },
                    "k": False,
                    "l": 1.5
                },
                "__type": "dict"
            }
        }

        parsed_instance = Test.from_json(raw_json)
        self.assertEqual(parsed_instance.a[0].j, target_instance.a[0].j)
        self.assertDictEqual(parsed_instance.b, target_instance.b)
