import unittest
import asyncio

from ...parsing import DictParser, handleAcceptHeader
from ...parsing.fields import StringField, DictField, PrefixDictField, IntegerField
from ..test_case import async_test


class TestParsing(unittest.TestCase):
    @async_test
    async def test_moo(self):
        class dp(DictParser):
            stringOne = StringField()
            stringTwo = StringField()
            dictOne = DictField(
                fields={
                    "stringThree": StringField(),
                    "stringFour": StringField(),
                    "dictTwo": DictField({}),
                }
            )

        parsed = await dp().parse({
            "stringOne": "moo",
            "stringTwo": "cow",
            "dictOne": {
                "stringThree": "moo",
                "stringFour": "cow",
                "dictTwo": {
                    "x": 1
                }
            }
        })

        self.assertEqual(parsed["stringOne"], "moo")
        self.assertEqual(parsed["stringTwo"], "cow")
        self.assertEqual(parsed["dictOne"]["stringThree"], "moo")
        self.assertEqual(parsed["dictOne"]["stringFour"], "cow")
        self.assertEqual(parsed["dictOne"]["dictTwo"]["x"], 1)


class TestParseFrom(unittest.TestCase):
    @async_test
    async def test_parse_from(self):
        class dp(DictParser):
            stringOne = StringField()
            stringTwo = StringField(parseFrom="notStringTwo")

        parsed = await dp().parse({
            "stringOne": "moo",
            "notStringTwo": "cow",
            "stringTwo": "something else",
        })

        self.assertEqual(parsed["stringOne"], "moo")
        self.assertEqual(parsed["stringTwo"], "cow")


class TestPrefixDict(unittest.TestCase):
    @async_test
    async def test_prefix_dict(self):
        class dp(DictParser):
            dictOne = PrefixDictField(
                prefix="moo.",
                fields={
                    "one": StringField(),
                    "two": IntegerField(),
                },
            )

        parsed = await dp().parse({
            "one": "moo",
            "two": "cow",
            "dictOne": "something else",
            "moo.one": "theOne",
            "moo.two": 2,
        })

        self.assertEqual(parsed["dictOne"]["one"], "theOne")
        self.assertEqual(parsed["dictOne"]["two"], 2)


class TestAcceptHeaderParsing(unittest.TestCase):
    def test_simple_parsing(self):
        contentType, parameters = handleAcceptHeader(
            "text/*;q=0.3, text/html;q=0.7, text/html;level=1, text/html;level=2;q=0.4, */*;q=0.5",
            ["text/html", "text/plain"],
        )
        self.assertEqual(contentType, "text/html")
        self.assertEqual(parameters["level"], "1")


if __name__ == '__main__':
    unittest.main()