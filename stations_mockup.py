#!/usr/bin/env python3
"""mradio station-picker UI mockup (standalone, NOT part of mradio).

Run interactively:      python3 stations_mockup.py
Print main frame:       python3 stations_mockup.py --shot
Print picker frame:     python3 stations_mockup.py --shot-pick

Concept being explored: the now-playing screen stays as-is, and a letter key
`s` opens the "Preselected stations" menu; 1-9 or arrows+Enter pick a station,
Esc/s/q returns to the player.
Keys: s = stations menu · 1-9 = pick · arrows/Enter = pick · p = theme · q = quit
"""

import curses
import sys
import time

VERSION = "0.7.24"

STATIONS = [
    (True,  "WQXR",                  "128k MP3 · US, member-supported"),
    (True,  "Radio Swiss Classic",   "128k MP3 · CH, public (Italian feed)"),
    (False, "VCR Auditorium",        "128k MP3 · Venice Classic Radio"),
    (False, "VCR Classica+",         "128k MP3 · Venice Classic Radio"),
    (False, "Naim Classical",        "320k AAC · Naim Audio"),
    (False, "Classic FM",            "128k MP3 · UK, commercial (ads)"),
    (False, "Radio Paradise",        "128k MP3 · US, eclectic, ad-free"),
    (False, "Swiss Jazz",            "128k MP3 · CH, public"),
    (False, "radio klassik Stephansdom", "128k MP3 · AT, non-profit"),
    (False, "NPO Radio 4 / Klassiek", "192k MP3 · NL, public"),
    (False, "France Musique",        "128k MP3 · FR, public"),
    (False, "BBC Radio 3",           "HLS AAC+ · UK, public (no icy)"),
]

DARK_256 = {1: (117, -1), 2: (189, -1), 3: (0, 44), 4: (35, -1),
            5: (110, -1), 6: (216, -1), 7: (117, -1),
            8: (0, 121), 9: (0, 210), 10: (0, 208)}
LIGHT_256 = {1: (27, -1), 2: (239, -1), 3: (0, 32), 4: (29, -1),
             5: (242, -1), 6: (60, -1), 7: (172, -1),
             8: (15, 28), 9: (15, 124), 10: (0, 208)}
LIGHT_NAVY_256 = {1: (27, -1), 2: (18, -1), 3: (0, 32), 4: (29, -1),
                  5: (242, -1), 6: (130, -1), 7: (172, -1),
                  8: (15, 28), 9: (15, 124), 10: (0, 208)}
LIGHT_MAUVE_256 = {1: (27, -1), 2: (19, -1), 3: (0, 32), 4: (30, -1),
                   5: (242, -1), 6: (137, -1), 7: (99, -1),
                   8: (15, 28), 9: (15, 124), 10: (0, 208)}
SCHEMES = ("dark", "light", "light-navy", "light-mauve")
PALS = {"dark": DARK_256, "light": LIGHT_256,
        "light-navy": LIGHT_NAVY_256, "light-mauve": LIGHT_MAUVE_256}


def init_colors(theme):
    if getattr(curses, "COLORS", 0) >= 256:
        for n in range(1, 11):
            curses.init_pair(n, *PALS[theme][n])
    else:
        pal = {1: curses.COLOR_BLUE, 2: curses.COLOR_BLACK, 3: curses.COLOR_BLACK,
               4: curses.COLOR_GREEN, 5: curses.COLOR_BLACK, 6: curses.COLOR_MAGENTA,
               7: curses.COLOR_BLUE, 8: curses.COLOR_BLACK, 9: curses.COLOR_BLACK,
               10: curses.COLOR_BLACK}
        bg = {3: curses.COLOR_CYAN, 8: curses.COLOR_GREEN, 9: curses.COLOR_RED,
              10: curses.COLOR_YELLOW}
        for n in range(1, 11):
            curses.init_pair(n, pal[n], bg.get(n, -1))


def add(std, y, x, text, pair, attr=0):
    try:
        std.attron(curses.color_pair(pair) | attr)
        std.addstr(y, x, text)
        std.attroff(curses.color_pair(pair) | attr)
    except curses.error:
        pass


def render_main(std, theme, cur_st, msg, msg_t):
    std.erase()
    h, w = std.getmaxyx()
    tw = max(8, w - 2)

    badge = " ● RADIO "
    add(std, 0, 0, badge, 3)
    x = len(badge)
    add(std, 0, x, " ▸ ", 1)
    x += 3
    add(std, 0, x, " " + cur_st + " ", 2)
    x += len(cur_st) + 2
    add(std, 0, x, " ▸ ", 1)
    x += 3
    add(std, 0, x, " LIVE ", 8)
    x += 6
    add(std, 0, x, f" {theme} (p)", 1)

    y = 2
    add(std, y, 1, "Ludwig van Beethoven", 4, curses.A_BOLD); y += 1
    add(std, y, 1, "Symphony No. 9 in D minor, Op. 125", 2, curses.A_BOLD); y += 1
    add(std, y, 1, "Berliner Philharmoniker · Herbert von Karajan", 6); y += 1
    add(std, y, 1, "Work: Symphony No. 9 · IV. Presto", 7); y += 1
    y += 1

    blurb = ("Schiller's 'Ode to Joy' — the finale Beethoven never heard "
             "performed. Mock trivia line to show the dim subtext slot.")
    for line in ([] if h < 14 else [blurb]):
        add(std, y, 1, line[:tw], 5, curses.A_DIM); y += 1
    y += 1

    if h - y > 6:
        add(std, y, 1, " 128 kbps · 44.1 kHz · mp3 · cache 2.3s · "
                       "stream 00:42", 7); y += 1

    if h - y > 4:
        vw = max(10, w - 14)
        add(std, y, 1, " vol ", 1)
        add(std, y + 1, 1, " " + ("█" * 7 + "░" * (vw - 7))[:vw], 4)
        add(std, y + 1, 1 + vw + 2, " 72%", 2)

    right = "v" + VERSION + " · mock"
    add(std, h - 1, max(0, w - len(right) - 1), right, 1)

    if msg and time.time() - msg_t < 2.5:
        line = "► launching " + msg + " … (mock)"
    else:
        line = (" AI: 1=opencode  2=ollama  3=api   now:opencode   "
                "press to re-request")
    add(std, h - 2, 1, line, 3)
    add(std, h - 1, 1,
        (" q:quit  sp:pause  +/-:vol  m:mute  r:reconnect  s:stations")
        [:max(8, w - len(right) - 6)], 6)


def render_pick(std, theme, cur, msg, msg_t):
    std.erase()
    h, w = std.getmaxyx()

    badge = " ● RADIO "
    add(std, 0, 0, badge, 3)
    x = len(badge)
    add(std, 0, x, " ▸ ", 1)
    x += 3
    add(std, 0, x, " pick a station ", 2, curses.A_BOLD)
    x += 16
    add(std, 0, x, " ▸ ", 1)
    x += 3
    add(std, 0, x, " SELECT ", 8)
    x += 8
    add(std, 0, x, f" {theme} (p)", 1)

    y = 2
    add(std, y, 1, "Preselected stations", 1, curses.A_BOLD)
    y += 1
    for i in range(len(STATIONS)):
        if y >= h - 2:
            break
        vis = STATIONS[i]
        if i == cur:
            add(std, y, 1, "▶", 2, curses.A_BOLD)
        add(std, y, 4, f"{i+1}", 1)
        add(std, y, 7, "★" if vis[0] else " ", 8)
        add(std, y, 9, "·" if not vis[0] else " ", 5)
        add(std, y, 11, vis[1], 2 if vis[0] else 6, curses.A_BOLD if vis[0] else 0)
        subx = 11 + len(vis[1]) + 2
        if subx < w - 4:
            add(std, y, subx, vis[2], 5, curses.A_DIM)
        y += 1

    right = "v" + VERSION + " · mock"
    add(std, h - 1, max(0, w - len(right) - 1), right, 1)

    if msg and time.time() - msg_t < 2.5:
        add(std, h - 2, 1, "► launching " + msg + " … (mock)", 3)
    else:
        add(std, h - 2, 1, " pick a number — returns to the player", 3)
    add(std, h - 1, 1,
        (" q/Esc:back  ↑/↓:move  Enter:pick  1-9:pick  p:scheme")
        [:max(8, w - len(right) - 6)], 6)


def run(std):
    curses.curs_set(0)
    curses.start_color()
    curses.use_default_colors()
    theme = "dark"
    init_colors(theme)
    mode = "main"
    cur = 0
    cur_st = STATIONS[0][1]
    msg = None
    msg_t = 0.0
    while True:
        if mode == "pick":
            render_pick(std, theme, cur, msg, msg_t)
        else:
            render_main(std, theme, cur_st, msg, msg_t)
        std.refresh()
        c = std.getch()
        if c in (ord("q"), 27):
            if mode == "pick":
                mode = "main"
            else:
                break
        elif c == ord("s"):
            mode = "pick" if mode == "main" else "main"
        elif c == ord("p"):
            theme = SCHEMES[(SCHEMES.index(theme) + 1) % len(SCHEMES)]
            init_colors(theme)
        elif mode == "pick":
            if c in (curses.KEY_DOWN, ord("j")) and cur < len(STATIONS) - 1:
                cur += 1
            elif c in (curses.KEY_UP, ord("k")) and cur > 0:
                cur -= 1
            elif c in (10, 13, curses.KEY_ENTER):
                cur_st = STATIONS[cur][1]
                msg, msg_t = cur_st, time.time()
                mode = "main"
            elif ord("1") <= c <= ord("9"):
                i = c - ord("1")
                if i < len(STATIONS):
                    cur = i
                    cur_st = STATIONS[i][1]
                    msg, msg_t = cur_st, time.time()
                    mode = "main"


def shot(mode="main"):
    std = curses.initscr()
    try:
        curses.start_color()
        curses.use_default_colors()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        init_colors("dark")
        if mode == "pick":
            render_pick(std, "dark", 0, None, 0.0)
        else:
            render_main(std, "dark", STATIONS[0][1], None, 0.0)
        curses.doupdate()
        lines = []
        h, w = std.getmaxyx()
        for y in range(h):
            row = std.instr(y, 0, w)
            if isinstance(row, bytes):
                row = row.decode(errors="replace")
            lines.append(row.rstrip())
        curses.endwin()
        print("\n".join(lines))
    finally:
        curses.endwin()


if __name__ == "__main__":
    if "--shot-pick" in sys.argv:
        shot("pick")
    elif "--shot" in sys.argv:
        shot("main")
    else:
        curses.wrapper(run)