"""Catch missing frontend elements before demo day (stdlib-only static check)."""
from html.parser import HTMLParser
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]


class IdCollector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.labels_for = []
        self.scripts = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if "id" in values:
            self.ids.append(values["id"])
        if tag == "label" and "for" in values:
            self.labels_for.append(values["for"])
        if tag == "script" and "src" in values:
            self.scripts.append(values["src"])


class FrontendContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = IdCollector()
        cls.html.feed((ROOT / "index.html").read_text(encoding="utf-8"))
        cls.javascript = (ROOT / "app.js").read_text(encoding="utf-8")

    def test_all_dom_id_references_exist(self):
        names = set(re.findall(r"\$\('([^']+)'\)", self.javascript))
        missing = sorted(names - set(self.html.ids))
        self.assertFalse(missing, "JS references missing DOM ids: " + ", ".join(missing))

    def test_no_duplicate_ids_or_invalid_label_targets(self):
        self.assertEqual(len(self.html.ids), len(set(self.html.ids)), "Duplicate HTML id attributes")
        self.assertFalse(set(self.html.labels_for) - set(self.html.ids))

    def test_source_js_is_loaded(self):
        self.assertIn("/app.js", self.html.scripts)

    def test_external_recommendations_are_safe_link_targets(self):
        self.assertIn("link.rel='noopener noreferrer'", self.javascript)
        self.assertIn("link.textContent=item.resource", self.javascript)


if __name__ == "__main__":
    unittest.main()
