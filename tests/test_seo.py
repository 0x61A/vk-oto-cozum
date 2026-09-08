"""Site-wide SEO contract checks using only the Python standard library."""

import json
import unittest
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = "https://vkotocozum.com"


class SeoDocument(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.title = ""
        self._in_title = False
        self.metas = []
        self.links = []
        self.h1_count = 0
        self.json_ld = []
        self._json_script = None
        self.feed(source)
        self.close()

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "title":
            self._in_title = True
        elif tag == "meta":
            self.metas.append(attributes)
        elif tag == "link":
            self.links.append(attributes)
        elif tag == "h1":
            self.h1_count += 1
        elif tag == "script" and attributes.get("type") == "application/ld+json":
            self._json_script = ""

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        if self._json_script is not None:
            self._json_script += data

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        elif tag == "script" and self._json_script is not None:
            self.json_ld.append(self._json_script)
            self._json_script = None

    def meta(self, key, value):
        return [item.get("content", "") for item in self.metas if item.get(key) == value]


def public_pages():
    pages = list(ROOT.glob("*.html"))
    pages.extend((ROOT / "hizmetler").glob("*/index.html"))
    return sorted(pages)


class SiteSeoTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pages = public_pages()
        cls.documents = {
            page: SeoDocument(page.read_text(encoding="utf-8")) for page in cls.pages
        }
        sitemap = ET.parse(ROOT / "sitemap.xml")
        cls.sitemap_urls = {
            node.text for node in sitemap.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc")
        }

    def test_each_page_has_unique_title_description_and_canonical(self):
        titles = []
        descriptions = []
        canonicals = []
        for page, doc in self.documents.items():
            with self.subTest(page=page):
                self.assertTrue(doc.title.strip())
                self.assertEqual(doc.h1_count, 1)
                description = doc.meta("name", "description")
                self.assertEqual(len(description), 1)
                self.assertGreaterEqual(len(description[0]), 70)
                canonical = [link["href"] for link in doc.links if link.get("rel") == "canonical"]
                self.assertEqual(len(canonical), 1)
                self.assertTrue(canonical[0].startswith(BASE))
                self.assertIn(canonical[0], self.sitemap_urls)
                titles.append(doc.title.strip())
                descriptions.append(description[0])
                canonicals.append(canonical[0])
        self.assertEqual(len(titles), len(set(titles)))
        self.assertEqual(len(descriptions), len(set(descriptions)))
        self.assertEqual(len(canonicals), len(set(canonicals)))

    def test_social_titles_and_urls_are_present(self):
        for page, doc in self.documents.items():
            with self.subTest(page=page):
                self.assertEqual(len(doc.meta("property", "og:title")), 1)
                self.assertEqual(len(doc.meta("property", "og:description")), 1)
                self.assertEqual(len(doc.meta("property", "og:url")), 1)

    def test_all_structured_data_is_valid_json(self):
        for page, doc in self.documents.items():
            with self.subTest(page=page):
                for block in doc.json_ld:
                    json.loads(block)
        for page in (
            ROOT / "index.html",
            ROOT / "sincan-arac-yazilim.html",
            ROOT / "hizmetler" / "dpf" / "index.html",
            ROOT / "hizmetler" / "egr" / "index.html",
            ROOT / "hizmetler" / "adblue" / "index.html",
            ROOT / "hizmetler" / "dtc-ariza-kodu" / "index.html",
        ):
            self.assertTrue(self.documents[page].json_ld, page)

    def test_priority_pages_lead_with_local_search_intent(self):
        expected = {
            ROOT / "index.html": "Sincan Oto Servis",
            ROOT / "sincan-arac-yazilim.html": "Sincan Araç Yazılımı",
            ROOT / "hizmetler" / "dpf" / "index.html": "Sincan DPF Temizliği",
            ROOT / "hizmetler" / "egr" / "index.html": "Sincan EGR Valfi",
            ROOT / "hizmetler" / "adblue" / "index.html": "Sincan AdBlue Arızası",
            ROOT / "hizmetler" / "dtc-ariza-kodu" / "index.html": "Sincan Bilgisayarlı Arıza Tespiti",
        }
        for page, prefix in expected.items():
            with self.subTest(page=page):
                self.assertTrue(self.documents[page].title.startswith(prefix))

    def test_vehicle_software_page_covers_primary_terms(self):
        source = (ROOT / "sincan-arac-yazilim.html").read_text(encoding="utf-8").casefold()
        for term in ("sincan araç", "stage 1", "ecu", "tcu", "şanzıman", "dsg"):
            self.assertIn(term, source)


if __name__ == "__main__":
    unittest.main(verbosity=2)
