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
latest_release_tag = _mradio.latest_release_tag
ver_key = _mradio.ver_key
next_theme = _mradio.next_theme
init_colors = _mradio.init_colors
SCHEMES = _mradio.SCHEMES


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


class _FakeStd:
    def __init__(self, h, w):
        self._h, self._w, self.calls = h, w, []
    def erase(self): pass
    def attron(self, *a): pass
    def attroff(self, *a): pass
    def refresh(self): pass
    def getmaxyx(self): return self._h, self._w
    def addstr(self, y, x, text): self.calls.append((y, x, text))


class TestRightFooter(unittest.TestCase):
    def test_version_bottom_right(self):
        s = _mradio.make_state()
        f = _FakeStd(24, 100)
        _old = _mradio.curses.color_pair
        _mradio.curses.color_pair = lambda p: p
        try:
            _mradio.render(f, 12, s)
        finally:
            _mradio.curses.color_pair = _old
        ver = "v" + _mradio.VERSION
        matching = [c for c in f.calls if c[2] == ver and c[0] == f._h - 1]
        self.assertTrue(matching, "version not drawn on the bottom row")

    def test_update_pill_when_newer_release(self):
        s = _mradio.make_state()
        s["update_url"] = _mradio.UPDATE_URL
        f = _FakeStd(24, 100)
        _old = _mradio.curses.color_pair
        _mradio.curses.color_pair = lambda p: p
        try:
            _mradio.render(f, 12, s)
        finally:
            _mradio.curses.color_pair = _old
        self.assertTrue(any(c[2] == " UPDATE " and c[0] == f._h - 2
                            for c in f.calls), "UPDATE pill not drawn")
        self.assertIsNotNone(s.get("update_zone"))


class TestPalettes(unittest.TestCase):
    def test_next_theme_cycles_all_schemes(self):
        seen = []
        t = "dark"
        for _ in range(len(SCHEMES) + 1):
            seen.append(t)
            t = next_theme(t)
        self.assertEqual(seen[:len(SCHEMES)] + [seen[0]], seen,
                         "rotation must wrap back to the first scheme")

    def test_next_theme_unknown_falls_back_to_dark(self):
        self.assertEqual(next_theme("nope"), SCHEMES[1])

    def test_init_colors_256_sets_chip_bg_and_fg(self):
        pairs = {}
        _old_c = getattr(_mradio.curses, "COLORS", None)
        _old = _mradio.curses.init_pair
        _mradio.curses.COLORS = 256
        _mradio.curses.init_pair = lambda n, fg, bg: pairs.__setitem__(n, (fg, bg))
        try:
            init_colors("light-navy")
        finally:
            if _old_c is None:
                del _mradio.curses.COLORS
            else:
                _mradio.curses.COLORS = _old_c
            _mradio.curses.init_pair = _old
        self.assertEqual(pairs[2], (18, -1), "navy title color")
        self.assertEqual(pairs[5], (242, -1), "grey subtext color")
        self.assertEqual(pairs[6], (130, -1), "cinnamon performer color")
        self.assertEqual(pairs[8], (15, 28), "white on green LIVE chip")

    def test_init_colors_each_scheme_has_10_pairs(self):
        for scheme in SCHEMES:
            pairs = {}
            _old_c = getattr(_mradio.curses, "COLORS", None)
            _old = _mradio.curses.init_pair
            _mradio.curses.COLORS = 256
            _mradio.curses.init_pair = lambda n, fg, bg: pairs.__setitem__(n, (fg, bg))
            try:
                init_colors(scheme)
            finally:
                if _old_c is None:
                    del _mradio.curses.COLORS
                else:
                    _mradio.curses.COLORS = _old_c
                _mradio.curses.init_pair = _old
            self.assertEqual(sorted(pairs), list(range(1, 11)),
                             f"{scheme} must define all 10 pairs")


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

    def test_latest_release_tag(self):
        body = (
            '<entry><link href="https://github.com/Marcus1571/mradio/'
            'releases/tag/v0.7.17"/></entry>'
        )
        self.assertEqual(latest_release_tag(body), "v0.7.17")

    def test_apply_update_no_newer_release(self):
        saved = dict(_mradio._latest)
        _mradio._latest = {"version": "0.7.16", "etag": "", "tag": None}
        try:
            ok, _ = _mradio.apply_update()
            self.assertFalse(ok)
        finally:
            _mradio._latest = saved

    def test_force_check_reports_when_busy(self):
        _old = _mradio._latest
        _mradio._latest = dict(_old)
        lock = _mradio._forced_lock
        self.assertTrue(lock.acquire(blocking=False))
        try:
            s = {"update_msg": "", "update_msg_t": 0}
            _mradio.force_check(s)
            self.assertIn("already running", s["update_msg"])
        finally:
            lock.release()
            _mradio._latest = _old

    def test_check_update_note_when_current(self):
        _old = _mradio._latest
        _mradio._latest = dict(_old)
        _mradio._latest["etag"] = ""
        _mradio._latest["note"] = ""
        saved = _mradio.urllib.request.urlopen

        class _Resp:
            headers = {"ETag": '"t"'}
            def __enter__(self): return self
            def __exit__(self, *a): return False
            def read(self):
                return ('<entry><link href="https://github.com/Marcus1571/'
                        f'mradio/releases/tag/v{_mradio.VERSION}"/></entry>'
                        ).encode()

        _mradio.urllib.request.urlopen = lambda req, timeout=6: _Resp()
        try:
            _mradio.check_update()
            self.assertIn("up to date", _mradio._latest["note"])
        finally:
            _mradio.urllib.request.urlopen = saved
            _mradio._latest = _old

    def test_check_update_note_newer(self):
        _old = _mradio._latest
        _mradio._latest = dict(_old)
        _mradio._latest["etag"] = ""
        _mradio._latest["note"] = ""
        saved = _mradio.urllib.request.urlopen

        class _Resp:
            headers = {"ETag": '"t"'}
            def __enter__(self): return self
            def __exit__(self, *a): return False
            def read(self):
                return (b'<entry><link href="https://github.com/Marcus1571/'
                        b'mradio/releases/tag/v0.9.0"/></entry>')

        _mradio.urllib.request.urlopen = lambda req, timeout=6: _Resp()
        try:
            _mradio.check_update()
            self.assertIn("press U", _mradio._latest["note"])
            self.assertEqual(_mradio._latest["version"], "0.9.0")
        finally:
            _mradio.urllib.request.urlopen = saved
            _mradio._latest = _old

    def test_update_interval_default_hourly(self):
        self.assertEqual(_mradio.UPDATE_INTERVAL, 3600)

    def test_update_interval_floor(self):
        self.assertGreaterEqual(_mradio.UPDATE_INTERVAL, 60)


if __name__ == "__main__":
    unittest.main()