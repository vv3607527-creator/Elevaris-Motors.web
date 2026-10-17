import re
import unittest
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "index.html"


class SiteParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.links = []
        self.images_without_alt = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.add(attrs["id"])
        if tag == "a" and "href" in attrs:
            self.links.append(attrs["href"])
        if tag == "img" and "alt" not in attrs:
            self.images_without_alt.append(attrs)


class SiteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = HTML.read_text(encoding="utf-8")
        cls.parser = SiteParser()
        cls.parser.feed(cls.source)

    def test_document_has_required_metadata(self):
        self.assertRegex(self.source, r"<title>[^<]+</title>")
        self.assertRegex(self.source, r'<meta name="description" content="[^"]+">')
        self.assertIn('<meta name="viewport"', self.source)

    def test_internal_links_resolve(self):
        for href in self.parser.links:
            if href.startswith("#") and href != "#":
                self.assertIn(href[1:], self.parser.ids, href)

    def test_images_are_accessible(self):
        self.assertEqual([], self.parser.images_without_alt)

    def test_booking_actions_are_real(self):
        self.assertIn("https://wa.me/918639865789", self.source)
        self.assertNotIn("hello@elevarismotors.example", self.source)

    def test_inline_javascript_is_present_and_strict(self):
        self.assertIn('"use strict"', self.source)
        self.assertGreaterEqual(len(re.findall(r"<script", self.source)), 3)


if __name__ == "__main__":
    unittest.main()
