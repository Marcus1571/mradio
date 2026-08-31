#!/usr/bin/env python3
"""Unit tests for mradio's pure helpers (extract_json_item, split_title).

Loads the single-file `mradio` script as a module via importlib so no
installation is required. Run with: make test  (or python3 test_mradio.py)
"""

import importlib.machinery
import importlib.util
import json
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
        self.assertEqual(pairs[5], (59, -1), "grey subtext color")
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
            self.assertEqual(sorted(pairs), list(range(1, 12)),
                             f"{scheme} must define all 10 pairs + popup input pair")
            self.assertEqual(len(pairs), 11)


class TestProviderRules(unittest.TestCase):
    def test_api_provider_gets_sincerity_rules(self):
        prompt = "base prompt"
        out = _mradio.apply_provider_rules(prompt, "openai")
        self.assertTrue(out.startswith(prompt))
        for token in ("Never invent facts", "premiere date", "wiki",
                       "is better than a padded one"):
            self.assertIn(token, out)

    def test_other_providers_keep_stock_prompt(self):
        for provider in ("opencode", "ollama", "bogus"):
            self.assertEqual(_mradio.apply_provider_rules("X", provider), "X")

    def test_sincerity_rules_cover_the_big_hallucinations(self):
        rules = _mradio.SINCERITY_RULES
        for phrase in (
            "Never invent facts",
            "premiere date",
            "film, TV show, or commercial",
            "composer, performer, or work other than",
            "is better than a padded one",
        ):
            self.assertTrue(phrase.lower() in rules.lower(),
                            f"missing anti-hallucination phrase: {phrase!r}")


class TestReleaseFeed(unittest.TestCase):
    def test_latest_release_version(self):
        body = (
            '<entry><link href="https://github.com/Marcus1571/mradio/'
            'releases/tag/v0.7.15"/></entry>'
            '<entry><link href="https://github.com/Marcus1571/mradio/'
            'releases/tag/v0.7.14"/></entry>'
        )
        self.assertEqual(latest_release_version(body), "0.7.15")

    def test_latest_release_version_out_of_order(self):
        body = (
            '<entry><link href="https://github.com/Marcus1571/mradio/'
            'releases/tag/v0.7.15"/></entry>'
            '<entry><link href="https://github.com/Marcus1571/mradio/'
            'releases/tag/v0.7.55"/></entry>'
        )
        self.assertEqual(latest_release_version(body), "0.7.55")
        self.assertEqual(latest_release_tag(body), "v0.7.55")

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

    def test_check_on_v_answers_from_cache_instantly(self):
        _old = _mradio._latest
        _mradio._latest = dict(_old)
        _mradio._latest["note"] = "up to date (v0.7.99)"
        saved = _mradio.force_check
        calls = []
        _mradio.force_check = lambda s: calls.append(s)
        try:
            s = {"update_msg": "", "update_msg_t": 0}
            _mradio.check_on_v(s)
            self.assertIn("up to date", s["update_msg"])
            # every `v` press refreshes, even with a fresh cached answer
            self.assertEqual(len(calls), 1)
        finally:
            _mradio.force_check = saved
            _mradio._latest = _old

    def test_check_on_v_falls_back_to_force_check_without_cache(self):
        _old = _mradio._latest
        _mradio._latest = dict(_old)
        _mradio._latest["note"] = ""
        saved = _mradio.force_check
        calls = []
        _mradio.force_check = lambda s: calls.append(s)
        try:
            s = {"update_msg": "", "update_msg_t": 0}
            _mradio.check_on_v(s)
            self.assertEqual(len(calls), 1)
        finally:
            _mradio.force_check = saved
            _mradio._latest = _old

    def test_check_on_v_pending_restart_note(self):
        _old = _mradio._latest
        _mradio._latest = dict(_old)
        _mradio._latest["note"] = "up to date"
        _mradio._latest["version"] = "0.7.99"
        saved = _mradio.force_check
        _mradio.force_check = lambda s: None
        try:
            s = {"update_msg": "", "update_msg_t": 0, "update_pending": True}
            _mradio.check_on_v(s)
            self.assertIn("restart to apply", s["update_msg"])
        finally:
            _mradio.force_check = saved
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

    def test_304_refetches_for_newer_release(self):
        _old = _mradio._latest
        _mradio._latest = dict(_old)
        _mradio._latest["etag"] = '"old"'
        _mradio._latest["version"] = "0.9.0"
        _mradio._latest["tag"] = "v0.9.0"
        _mradio._latest["note"] = ""
        saved = _mradio.urllib.request.urlopen
        calls = []

        class _Resp:
            headers = {"ETag": '"t"'}
            def __enter__(self): return self
            def __exit__(self, *a): return False
            def read(self):
                return (b'<entry><link href="https://github.com/Marcus1571/'
                        b'mradio/releases/tag/v0.9.0"/></entry>')

        def sim(req, timeout=6):
            calls.append(req)
            if len(calls) == 1:
                raise _mradio.urllib.error.HTTPError(
                    "", 304, "Not Modified", {}, None)
            return _Resp()

        _mradio.urllib.request.urlopen = sim
        try:
            _mradio.check_update()
            self.assertEqual(len(calls), 2)
            self.assertEqual(_mradio._latest["version"], "0.9.0")
            self.assertIn("press U", _mradio._latest["note"])
        finally:
            _mradio.urllib.request.urlopen = saved
            _mradio._latest = _old

    def test_update_interval_default_hourly(self):
        self.assertEqual(_mradio.UPDATE_INTERVAL, 3600)

    def test_update_interval_floor(self):
        self.assertGreaterEqual(_mradio.UPDATE_INTERVAL, 60)

    def test_oc_port_auto_detects_binary(self):
        saved_oc = _mradio.OC
        saved_onpath = _mradio._OC_ONPATH
        saved_which = _mradio.shutil.which
        _mradio.OC = ""
        _mradio._OC_ONPATH = None
        _mradio.shutil.which = lambda n: "/usr/bin/opencode"
        try:
            self.assertEqual(_mradio.oc_port(), 4096)
        finally:
            _mradio.OC = saved_oc
            _mradio._OC_ONPATH = saved_onpath
            _mradio.shutil.which = saved_which

    def test_oc_port_zero_disables_even_with_binary(self):
        saved_oc = _mradio.OC
        saved_onpath = _mradio._OC_ONPATH
        saved_which = _mradio.shutil.which
        _mradio.OC = "0"
        _mradio._OC_ONPATH = None
        _mradio.shutil.which = lambda n: "/usr/bin/opencode"
        try:
            self.assertEqual(_mradio.oc_port(), 0)
        finally:
            _mradio.OC = saved_oc
            _mradio._OC_ONPATH = saved_onpath
            _mradio.shutil.which = saved_which

    def test_oc_port_off_without_binary(self):
        saved_oc = _mradio.OC
        saved_onpath = _mradio._OC_ONPATH
        saved_which = _mradio.shutil.which
        _mradio.OC = ""
        _mradio._OC_ONPATH = None
        _mradio.shutil.which = lambda n: None
        try:
            self.assertEqual(_mradio.oc_port(), 0)
        finally:
            _mradio.OC = saved_oc
            _mradio._OC_ONPATH = saved_onpath
            _mradio.shutil.which = saved_which


class TestStations(unittest.TestCase):
    def test_default_stations_shape(self):
        sts = _mradio.DEFAULT_STATIONS
        self.assertGreaterEqual(len(sts), 2)
        for ent in sts:
            self.assertIn("name", ent)
            self.assertIn("url", ent)
            self.assertTrue(ent["name"].strip())
            host = ent["url"].split("/")[2]
            self.assertIn(".", host)

    def test_fav_index_main_row(self):
        for d in range(1, 10):
            self.assertEqual(_mradio.fav_index(ord(str(d))), d - 1)
        self.assertEqual(_mradio.fav_index(ord("0")), 9)

    def test_fav_index_rejects_others(self):
        self.assertIsNone(_mradio.fav_index(ord("a")))
        self.assertIsNone(_mradio.fav_index(ord(" ")))
        self.assertIsNone(_mradio.fav_index(-1))

    def test_load_favorites_seeds_from_defaults(self):
        import tempfile
        saved = _mradio.STATIONS_FILE
        with tempfile.TemporaryDirectory() as td:
            _mradio.STATIONS_FILE = os.path.join(td, "stations.json")
            try:
                sts = _mradio.load_favorites()
                self.assertEqual(sts, list(_mradio.DEFAULT_STATIONS)[:10])
                self.assertTrue(os.path.exists(_mradio.STATIONS_FILE))
            finally:
                _mradio.STATIONS_FILE = saved

    def test_load_favorites_reads_user_file(self):
        import tempfile
        saved = _mradio.STATIONS_FILE
        with tempfile.TemporaryDirectory() as td:
            _mradio.STATIONS_FILE = os.path.join(td, "stations.json")
            _mradio.save_favorites([
                {"name": "Alpha", "url": "https://a.example/stream.mp3"},
                {"name": "Beta", "url": "https://b.example/stream.aac"},
            ])
            try:
                sts = _mradio.load_favorites()
                self.assertEqual(len(sts), 2)
                self.assertEqual(sts[0]["name"], "Alpha")
                self.assertEqual(sts[1]["url"], "https://b.example/stream.aac")
            finally:
                _mradio.STATIONS_FILE = saved

    def test_load_favorites_honors_empty_user_file(self):
        import tempfile
        saved = _mradio.STATIONS_FILE
        with tempfile.TemporaryDirectory() as td:
            _mradio.STATIONS_FILE = os.path.join(td, "stations.json")
            with open(_mradio.STATIONS_FILE, "w") as fh:
                json.dump({"favorites": []}, fh)
            try:
                self.assertEqual(_mradio.load_favorites(), [])
            finally:
                _mradio.STATIONS_FILE = saved

    def test_load_favorites_migrates_legacy_cfg(self):
        import tempfile
        saved_cfg, saved_st = _mradio.CFG_FILE, _mradio.STATIONS_FILE
        with tempfile.TemporaryDirectory() as td:
            _mradio.CFG_FILE = os.path.join(td, "config.json")
            _mradio.STATIONS_FILE = os.path.join(td, "stations.json")
            with open(_mradio.CFG_FILE, "w") as fh:
                json.dump({"stations": [
                    {"name": "Alpha", "url": "https://a.example/stream.mp3"},
                ]}, fh)
            try:
                sts = _mradio.load_favorites()
                self.assertEqual(sts[0]["name"], "Alpha")
                self.assertTrue(os.path.exists(_mradio.STATIONS_FILE))
            finally:
                _mradio.CFG_FILE = saved_cfg
                _mradio.STATIONS_FILE = saved_st


class TestNimSetup(unittest.TestCase):
    def test_provider_display_mapping(self):
        self.assertEqual(_mradio._PROVIDER_DISPLAY["openai"], "NIM")
        self.assertEqual(_mradio._PROVIDER_DISPLAY["opencode"], "opencode")
        self.assertEqual(_mradio._PROVIDER_DISPLAY["ollama"], "ollama")

    def test_save_api_key(self):
        import tempfile
        saved = _mradio.SETTINGS_FILE
        saved_key = _mradio.API_KEY
        with tempfile.TemporaryDirectory() as td:
            _mradio.SETTINGS_FILE = os.path.join(td, "settings.json")
            _mradio.API_KEY = ""
            try:
                self.assertTrue(_mradio.save_api_key("nvapi-test123"))
                self.assertEqual(_mradio.API_KEY, "nvapi-test123")
                d = _mradio.load_settings()
                self.assertEqual(d["api_key"], "nvapi-test123")
            finally:
                _mradio.SETTINGS_FILE = saved
                _mradio.API_KEY = saved_key

    def test_save_api_key_validates_prefix(self):
        self.assertTrue(callable(_mradio.prompt_api_key))

    def test_save_ollama_url(self):
        import tempfile
        saved = _mradio.SETTINGS_FILE
        saved_url = _mradio.OLLAMA
        with tempfile.TemporaryDirectory() as td:
            _mradio.SETTINGS_FILE = os.path.join(td, "settings.json")
            _mradio.OLLAMA = ""
            try:
                self.assertTrue(_mradio.save_ollama_url("http://192.168.1.12:11434"))
                self.assertEqual(_mradio.OLLAMA, "http://192.168.1.12:11434")
                d = _mradio.load_settings()
                self.assertEqual(d["ollama_url"], "http://192.168.1.12:11434")
            finally:
                _mradio.SETTINGS_FILE = saved
                _mradio.OLLAMA = saved_url

    def test_prompt_ollama_validates_url(self):
        self.assertTrue(callable(_mradio.prompt_ollama))


class TestGenres(unittest.TestCase):
    def test_genre_of_classical(self):
        for n in ("Venice Classic Radio", "Naim Classical", "radio klassik",
                  "France Musique", "NPO Klassiek"):
            self.assertEqual(_mradio.genre_of(n), "classical")

    def test_genre_of_jazz(self):
        for n in ("Swiss Jazz", "WBGO Jazz 88.3", "Swing Coconut"):
            self.assertEqual(_mradio.genre_of(n), "jazz")

    def test_genre_of_blues(self):
        for n in ("Jazz Radio Blues", "181.FM True Blues", "Chicago Blues"):
            self.assertEqual(_mradio.genre_of(n), "blues")

    def test_genre_of_other(self):
        self.assertEqual(_mradio.genre_of("Radio Paradise"), "other")
        self.assertEqual(_mradio.genre_of(""), "other")
        self.assertEqual(_mradio.genre_of("BBC Radio 3"), "other")

    def test_genre_buckets_preserves_order_and_buckets(self):
        stations = [
            {"name": "A", "url": "u://a", "genre": "classical"},
            {"name": "B", "url": "u://b", "genre": "jazz"},
            {"name": "C", "url": "u://c", "genre": "classical"},
            {"name": "D", "url": "u://d", "genre": "other"},
        ]
        b = _mradio.genre_buckets(stations)
        self.assertEqual([e["name"] for e in b["classical"]], ["A", "C"])
        self.assertEqual([e["name"] for e in b["jazz"]], ["B"])
        self.assertEqual([e["name"] for e in b["other"]], ["D"])
        self.assertEqual(b["blues"], [])

    def test_genre_stations_for_jazz_aggregates_curated(self):
        favs = [{"name": "Swiss Jazz", "url": "http://s.example/j.mp3",
                 "genre": "jazz"}]
        sts = _mradio.genre_stations_for(favs, "jazz")
        names = [e["name"] for e in sts]
        self.assertIn("Swiss Jazz", names)
        for curated in ("WBGO", "WWOZ", "KCSM 91.1", "KJAZZ 88.1",
                        "Adroit Jazz Underground", "SomaFM Secret Agent"):
            self.assertIn(curated, names)

    def test_genre_stations_for_blues_aggregates_curated(self):
        sts = _mradio.genre_stations_for([], "blues")
        names = [e["name"] for e in sts]
        for curated in ("1.FM Blues", "181.FM True Blues", "WDCB 90.9"):
            self.assertIn(curated, names)

    def test_genre_stations_for_classical_stays_favorites_only(self):
        favs = [{"name": "WQXR", "url": "u://wqxr", "genre": "classical"}]
        sts = _mradio.genre_stations_for(favs, "classical")
        self.assertEqual([e["name"] for e in sts], ["WQXR"])

    def test_genre_stations_for_dedups_favorite_matching_curated(self):
        favs = [{"name": "Swiss Jazz",
                 "url": "http://stream.srg-ssr.ch/m/rsj/mp3_128",
                 "genre": "jazz"}]
        sts = _mradio.genre_stations_for(favs, "jazz")
        seen = [e["name"] for e in sts]
        self.assertEqual(len(seen), len(set(seen)))
        self.assertEqual(seen.count("Swiss Jazz"), 1)

    def test_genre_station_counts_includes_curated_jazz_blues(self):
        favs = [{"name": "Swiss Jazz", "url": "u://j", "genre": "jazz"},
                {"name": "WQXR", "url": "u://w", "genre": "classical"}]
        counts = _mradio.genre_station_counts(favs)
        self.assertGreaterEqual(counts["jazz"], 7)
        self.assertGreaterEqual(counts["blues"], 3)
        self.assertEqual(counts["classical"], 1)

    def test_load_favorites_backfills_genre_on_legacy_entries(self):
        import tempfile
        saved = _mradio.STATIONS_FILE
        with tempfile.TemporaryDirectory() as td:
            _mradio.STATIONS_FILE = os.path.join(td, "stations.json")
            _mradio.save_favorites([
                {"name": "Swiss Jazz", "url": "https://s.example/stream.mp3"},
            ])
            try:
                sts = _mradio.load_favorites()
                self.assertEqual(sts[0]["genre"], "jazz")
            finally:
                _mradio.STATIONS_FILE = saved

    def test_back_target_genre_goes_to_genres(self):
        self.assertEqual(_mradio.back_target("genre", True), "genres")
        self.assertEqual(_mradio.back_target("genre", False), "genres")

    def test_back_target_playing_leaves_menu(self):
        self.assertIsNone(_mradio.back_target("fav", True))
        self.assertIsNone(_mradio.back_target("genres", True))

    def test_back_target_bare_launch_quits(self):
        self.assertEqual(_mradio.back_target("fav", False), "QUIT")
        self.assertEqual(_mradio.back_target("genres", False), "QUIT")


if __name__ == "__main__":
    unittest.main()