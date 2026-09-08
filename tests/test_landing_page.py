"""Static checks for the vehicle-software landing page; no network or packages."""

import json
import re
import subprocess
import unittest
import xml.etree.ElementTree as ET
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import parse_qs, urlsplit


ROOT = Path(__file__).resolve().parents[1]
ROUTE = "/sincan-arac-yazilim"
CANONICAL = "https://vkotocozum.com" + ROUTE
PHONE = "+905518652667"
MAP = "https://maps.app.goo.gl/xVXFtiYD74qMrL4h7"


class Document(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.elements = []
        self.scripts = []
        self._script = None
        self.feed(source)
        self.close()

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        self.elements.append((tag, attributes))
        if tag == "script":
            self._script = {"attrs": attributes, "content": ""}

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)

    def handle_data(self, data):
        if self._script is not None:
            self._script["content"] += data

    def handle_endtag(self, tag):
        if tag == "script" and self._script is not None:
            self.scripts.append(self._script)
            self._script = None

    def tags(self, name):
        return [attrs for tag, attrs in self.elements if tag == name]


class LandingPageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = (ROOT / "sincan-arac-yazilim.html").read_text(encoding="utf-8")
        cls.doc = Document(cls.source)

    def test_turkish_metadata_and_one_heading(self):
        self.assertEqual(self.doc.tags("html")[0]["lang"], "tr")
        self.assertEqual(len(self.doc.tags("h1")), 1)
        self.assertNotIn("\ufffd", self.source)
        self.assertIn("Ahmet Bircan Kaya", self.source)
        self.assertTrue(any(a.get("name") == "viewport" for a in self.doc.tags("meta")))

    def test_canonical_and_social_url(self):
        canonical = [a["href"] for a in self.doc.tags("link") if a.get("rel") == "canonical"]
        self.assertEqual(canonical, [CANONICAL])
        og = [a["content"] for a in self.doc.tags("meta") if a.get("property") == "og:url"]
        self.assertEqual(og, [CANONICAL])

    def test_all_new_phone_links_call_ahmet(self):
        phones = [a["href"] for a in self.doc.tags("a") if a.get("href", "").startswith("tel:")]
        self.assertEqual(len(phones), 1)
        self.assertEqual(set(phones), {"tel:" + PHONE})
        self.assertNotIn("Ahmet Bircan Kaya’yı ara", self.source)

    def test_whatsapp_recipient_and_draft_message(self):
        links = [a for a in self.doc.tags("a") if a.get("data-lead-action") == "whatsapp"]
        self.assertEqual(len(links), 3)
        for anchor in links:
            with self.subTest(location=anchor.get("data-lead-location")):
                url = urlsplit(anchor["href"])
                self.assertEqual(url.scheme, "https")
                self.assertEqual(url.path, "/" + PHONE.lstrip("+"))
                text = parse_qs(url.query)["text"][0]
                for prompt in ("Marka/model:", "Yıl:", "Motor:", "Şanzıman:", "işlem veya şikayet:"):
                    self.assertIn(prompt, text)
                self.assertEqual(anchor["data-lead-action"], "whatsapp")

    def test_tracking_hooks_have_distinct_positions(self):
        hooks = [a for a in self.doc.tags("a") if "data-lead-action" in a]
        pairs = [(a["data-lead-action"], a["data-lead-location"]) for a in hooks]
        self.assertEqual(len(pairs), len(set(pairs)))
        self.assertEqual(set(a for a, _ in pairs), {"phone", "whatsapp", "directions"})
        self.assertEqual([location for action, location in pairs if action == "phone"], ["contact"])

    def test_no_active_marketing_scripts_or_forms(self):
        self.assertEqual(len(self.doc.scripts), 2)
        self.assertEqual(self.doc.scripts[0]["attrs"].get("type"), "application/ld+json")
        self.assertEqual(self.doc.scripts[1]["attrs"].get("src"), "/assets/js/software-menu.js")
        menu_source = (ROOT / "assets/js/software-menu.js").read_text(encoding="utf-8")
        self.assertFalse(self.doc.tags("form"))
        for term in ("googletagmanager", "connect.facebook.net", "fbq(", "gtag(", "localStorage", "sessionStorage"):
            self.assertNotIn(term, self.source + menu_source)

    def test_structured_data_and_hours(self):
        graph = json.loads(self.doc.scripts[0]["content"])["@graph"]
        service = next(item for item in graph if item["@type"] == "Service")
        provider = service["provider"]
        self.assertEqual(provider["@id"], "https://vkotocozum.com/#business")
        contact = provider["contactPoint"]
        self.assertEqual(contact["telephone"], PHONE)
        self.assertEqual(contact["hoursAvailable"]["opens"], "09:00")
        self.assertEqual(contact["hoursAvailable"]["closes"], "19:30")
        self.assertEqual(len(contact["hoursAvailable"]["dayOfWeek"]), 6)
        self.assertIn("09.00–19.30", self.source)

    def test_local_resources_and_navigation_exist(self):
        ids = [attrs["id"] for _, attrs in self.doc.elements if "id" in attrs]
        self.assertEqual(len(ids), len(set(ids)))
        for tag, attrs in self.doc.elements:
            for key in ("href", "src"):
                ref = attrs.get(key, "")
                parsed = urlsplit(ref)
                if parsed.scheme or parsed.netloc or not ref:
                    continue
                if parsed.fragment:
                    if parsed.path:
                        fragment_page = ROOT / (parsed.path.lstrip("/") + ".html")
                        fragment_doc = Document(fragment_page.read_text(encoding="utf-8"))
                        self.assertIn(parsed.fragment, [a.get("id") for _, a in fragment_doc.elements])
                    else:
                        self.assertIn(parsed.fragment, ids)
                if parsed.path.startswith("/"):
                    target = ROOT / parsed.path.lstrip("/")
                    choices = (target, Path(str(target) + ".html"), target / "index.html")
                    self.assertTrue(any(path.is_file() for path in choices), f"Missing {tag} {ref}")
        for img in self.doc.tags("img"):
            self.assertTrue(img.get("alt"))
            self.assertGreater(int(img["width"]), 0)
            self.assertGreater(int(img["height"]), 0)

    def test_external_tab_safety_and_known_map(self):
        for anchor in self.doc.tags("a"):
            if anchor.get("target") == "_blank":
                self.assertIn("noopener", anchor.get("rel", "").split())
        self.assertEqual([a["href"] for a in self.doc.tags("a") if a.get("data-lead-action") == "directions"], [MAP])

    def test_sitemap_includes_canonical_once(self):
        sitemap = ET.parse(ROOT / "sitemap.xml")
        locations = [node.text for node in sitemap.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc")]
        self.assertEqual(locations.count(CANONICAL), 1)
        self.assertEqual(len(locations), len(set(locations)))

    def test_new_page_is_inside_software_services_not_footer(self):
        source = (ROOT / "hizmetler.html").read_text(encoding="utf-8")
        section = re.search(r'<section id="yazilim-cozumleri"[\s\S]*?</section>', source).group(0)
        self.assertIn("Yazılım Hizmetlerini İncele", section)
        self.assertEqual([a.get("href") for a in Document(section).tags("a")].count(ROUTE), 2)
        for route in ("adblue", "egr", "dpf", "dtc-ariza-kodu"):
            self.assertIn(f'href="/hizmetler/{route}"', section)
        footer = re.search(r'<footer\b[\s\S]*?</footer>', source).group(0)
        self.assertNotIn(ROUTE, footer)

    def test_home_page_navigation_is_preserved(self):
        original = subprocess.check_output(["git", "show", "HEAD:index.html"], cwd=ROOT).decode("utf-8")
        current = (ROOT / "index.html").read_text(encoding="utf-8")
        def navigation(source):
            return source.split("<!-- TopNavBar -->", 1)[1].split("<!-- Hero Section -->", 1)[0].replace("\r\n", "\n")
        self.assertEqual(navigation(current), navigation(original))

    def test_original_service_header_is_reused_exactly(self):
        original = subprocess.check_output(["git", "show", "HEAD:hizmetler.html"], cwd=ROOT).decode("utf-8")
        current_services = (ROOT / "hizmetler.html").read_text(encoding="utf-8")
        def header(source):
            return re.search(r'<header\b[\s\S]*?</header>', source).group(0).replace("\r\n", "\n")
        self.assertEqual(header(current_services), header(original))
        self.assertEqual(header(self.source), header(original))
        self.assertNotIn("header-call", self.source)
        self.assertNotIn("page-nav", self.source)
        self.assertIn('href="/assets/css/site.css"', self.source)

    def test_breadcrumb_places_page_under_services(self):
        graph = json.loads(self.doc.scripts[0]["content"])["@graph"]
        breadcrumb = next(item for item in graph if item["@type"] == "BreadcrumbList")
        self.assertEqual([item["name"] for item in breadcrumb["itemListElement"]],
                         ["Ana Sayfa", "Hizmetler", "Yazılım Çözümleri"])

    def test_mechanical_service_section_unchanged(self):
        original = subprocess.check_output(["git", "show", "HEAD:hizmetler.html"], cwd=ROOT).decode("utf-8")
        current = (ROOT / "hizmetler.html").read_text(encoding="utf-8")
        def mechanical(source):
            return source.split("<!-- Category 1:", 1)[1].split("<!-- Category 2:", 1)[0].replace("\r\n", "\n")
        self.assertEqual(mechanical(current), mechanical(original))

    def test_existing_contact_destinations_unchanged(self):
        def contacts(source):
            return Counter(a["href"] for a in Document(source).tags("a")
                           if a.get("href", "").startswith("tel:") or "wa.me/" in a.get("href", ""))

        for filename in ("index.html", "hizmetler.html"):
            original = subprocess.check_output(["git", "show", f"HEAD:{filename}"], cwd=ROOT).decode("utf-8")
            current = (ROOT / filename).read_text(encoding="utf-8")
            self.assertEqual(contacts(current), contacts(original), f"Contact links changed: {filename}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
