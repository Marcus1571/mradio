#!/usr/bin/env python3
"""Unit tests for mradio's pure helpers (extract_json_item, split_title).

Loads the single-file `mradio` script as a module via importlib so no
installation is required. Run with: make test  (or python3 test_mradio.py)
"""

import importlib.machinery
import importlib.util
import os
import unittest

_HERE = os.path.dirname(os.path.abspath(__file__))
_loader = importlib.machinery.SourceFileLoader("mradio", os.path.join(_HERE, "mradio"))
_spec = importlib.util.spec_from_loader("mradio", _loader)
_mradio = importlib.util.module_from_spec(_spec)
_loader.exec_module(_mradio)

extract_json_item = _mradio.extract_json_item
split_title = _mradio.split_title
latest_release_version = _mradio.latest_release_version
ver_key = _mradio.ver_key


class TestExtractJsonItem(unittest.TestCase):
    def test_clean_object(self):
        raw = ('{"movement": 1, "work": "Sonata No. 21 (Clementi)", '
               '"wiki": "Piano Sonata (Clementi)", "trivia": "Plain text."}')
        item = extract_json_item(raw)
        self.assertEqual(item["movement"], 1)
        self.assertEqual(item["work"], "Sonata No. 21 (Clementi)")
        self.assertEqual(item["wiki"], "Piano Sonata (Clementi)")
        self.assertEqual(item["trivia"], "Plain text.")

    def test_missing_fields(self):
        item = extract_json_item('"trivia": "Only trivia is here"')
        self.assertEqual(item["trivia"], "Only trivia is here")
        self.assertEqual(item["wiki"], "")
        self.assertEqual(item["work"], "")

    def test_trailing_prose_after_json(self):
        raw = ('{"movement": 0, "work": "", "wiki": "", '
               '"trivia": "A note."}\n\nHope that helps, but ignore this.')
        item = extract_json_item(raw)
        self.assertEqual(item["movement"], 0)
        self.assertEqual(item["trivia"], "A note.")

    def test_nested_braces(self):
        raw = ('{"movement": 1, "work": "W", "wiki": "X", '
               '"trivia": "Text with {braces} and a trailing detail."}')
        item = extract_json_item(raw)
        self.assertEqual(item["trivia"], "Text with {braces} and a trailing detail.")
        self.assertEqual(item["work"], "W")

    def test_markdown_fence(self):
        raw = ('```json\n{"movement": 0, "work": "", "wiki": "", '
               '"trivia": "Fenced trivia"}\n```')
        item = extract_json_item(raw)
        self.assertEqual(item["trivia"], "Fenced trivia")
        self.assertEqual(item["movement"], 0)

    def test_escaped_quote(self):
        raw = '{"movement": 0, "work": "", "wiki": "", "trivia": "Says \\"hi\\"."}'
        item = extract_json_item(raw)
        self.assertEqual(item["trivia"], 'Says "hi".')

    def test_garbage_with_keywords_returns_empty(self):
        item = extract_json_item("movement json schema nothing usable")
        self.assertEqual(item["trivia"], "")
        self.assertEqual(item["movement"], 0)

    def test_plain_prose_becomes_trivia(self):
        item = extract_json_item("This is just free prose from the model.")
        self.assertEqual(item["trivia"], "This is just free prose from the model.")


class TestSplitTitle(unittest.TestCase):
    def test_artist_dash_title(self):
        artist, title, performer = split_title("Mozart - Eine kleine Nachtmusik, KV 525")
        self.assertEqual(artist, "Mozart")
        self.assertEqual(title, "Eine kleine Nachtmusik, KV 525")
        self.assertEqual(performer, "")

    def test_no_dash(self):
        artist, title, performer = split_title("Symphony No. 9")
        self.assertEqual(artist, "")
        self.assertEqual(title, "Symphony No. 9")

    def test_parenthesized_performer(self):
        artist, title, performer = split_title(
            "Albéniz - Iberia: Book 1: Evocación (Alicia de Larrocha)")
        self.assertEqual(artist, "Albéniz")
        self.assertEqual(title, "Iberia: Book 1: Evocación")
        self.assertEqual(performer, "(Alicia de Larrocha)")

    def test_mojibake_repair_cp1252(self):
        artist, title, performer = split_title("Saint-SaÃ«ns - Danse macabre")
        self.assertEqual(artist, "Saint-Saëns")
        self.assertEqual(title, "Danse macabre")
        self.assertEqual(performer, "")

    def test_trailing_metadata_block_stripped(self):
        artist, title, performer = split_title(
            "Brahms - 1. Allegro {some icecast annotation}")
        self.assertEqual(artist, "Brahms")
        self.assertEqual(title, "1. Allegro")
        self.assertEqual(performer, "")


class TestReleaseFeed(unittest.TestCase):
    def test_latest_release_version(self):
        body = (
            '<entry><link href="https://github.com/Marcus1571/mradio/'
            'releases/tag/v0.7.15"/></entry>'
            '<entry><link href="https://github.com/Marcus1571/mradio/'
            'releases/tag/v0.7.14"/></entry>'
        )
        self.assertEqual(latest_release_version(body), "0.7.15")

    def test_release_version_no_tag(self):
        self.assertIsNone(latest_release_version("<entry>no releases</entry>"))

    def test_ver_key(self):
        self.assertEqual(ver_key("v0.7.15"), [0, 7, 15])
        self.assertEqual(ver_key("0.7.15-beta"), [0, 7, 15])
        self.assertGreater(ver_key("0.7.15"), ver_key("0.7.14"))
        self.assertLess(ver_key("0.7.2"), ver_key("0.7.10"))


if __name__ == "__main__":
    unittest.main()