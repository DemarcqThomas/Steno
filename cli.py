#!/usr/bin/env python3
import curses
import os
import sys
from typing import List

ROOT = os.path.dirname(__file__)

from main import encode_image
from decode import decode_image
from encoders import available_encoders


def encoder_names() -> list:
    return [enc.name for enc in available_encoders()]


IMAGE_EXTS = ('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.webp')


OPTIONS = [
    ("Encode (steganographie)", "encode"),
    ("Decode (steganographie)", "decode"),
    ("Quitter", "quit"),
]


def draw_menu(stdscr, selected_idx: int) -> None:
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    title = "Steno - menu (use arrows, Enter to select)"

    def safe_addstr(y, x, s, attr=0):
        if y < 0 or y >= h:
            return
        maxlen = max(0, w - x - 1)
        try:
            out = s[:maxlen]
        except Exception:
            out = str(s)[:maxlen]
        try:
            if attr:
                stdscr.addstr(y, x, out, attr)
            else:
                stdscr.addstr(y, x, out)
        except curses.error:
            try:
                out2 = out.encode('ascii', 'replace').decode('ascii')[:maxlen]
                if attr:
                    stdscr.addstr(y, x, out2, attr)
                else:
                    stdscr.addstr(y, x, out2)
            except Exception:
                pass

    safe_addstr(1, max(0, (w - len(title)) // 2), title, curses.A_BOLD)

    for i, (label, _) in enumerate(OPTIONS):
        x = 4
        y = 3 + i
        if y >= h - 2:
            break
        if i == selected_idx:
            stdscr.attron(curses.color_pair(1))
            safe_addstr(y, x, label)
            stdscr.attroff(curses.color_pair(1))
        else:
            safe_addstr(y, x, label)

    stdscr.refresh()


def choose_from_list(stdscr, title: str, items: List[str]) -> int:
    selected = 0
    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()

        def safe_addstr(y, x, s, attr=0):
            if y < 0 or y >= h:
                return
            maxlen = max(0, w - x - 1)
            out = str(s)[:maxlen]
            try:
                if attr:
                    stdscr.addstr(y, x, out, attr)
                else:
                    stdscr.addstr(y, x, out)
            except curses.error:
                try:
                    out2 = out.encode('ascii', 'replace').decode('ascii')[:maxlen]
                    if attr:
                        stdscr.addstr(y, x, out2, attr)
                    else:
                        stdscr.addstr(y, x, out2)
                except Exception:
                    pass

        safe_addstr(1, 2, title, curses.A_BOLD)
        for i, it in enumerate(items):
            y = 3 + i
            x = 4
            if y >= h - 2:
                break
            if i == selected:
                stdscr.attron(curses.color_pair(1))
                safe_addstr(y, x, it)
                stdscr.attroff(curses.color_pair(1))
            else:
                safe_addstr(y, x, it)
        stdscr.refresh()

        key = stdscr.getch()
        if key in (curses.KEY_UP, ord('k')):
            selected = (selected - 1) % len(items)
        elif key in (curses.KEY_DOWN, ord('j')):
            selected = (selected + 1) % len(items)
        elif key in (curses.KEY_ENTER, ord('\n'), ord('\r')):
            return selected
        elif key in (27,):
            return -1


def curses_input(stdscr, prompt: str) -> str:
    curses.echo()
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    maxlen = max(0, w - 6)
    try:
        stdscr.addstr(1, 2, str(prompt)[:maxlen], curses.A_BOLD)
    except curses.error:
        try:
            stdscr.addstr(1, 2, str(prompt).encode('ascii', 'replace').decode('ascii')[:maxlen])
        except Exception:
            pass
    stdscr.refresh()
    inp = stdscr.getstr(3, 4).decode('utf-8', errors='ignore')
    curses.noecho()
    return inp


def show_message(stdscr, title: str, text: str) -> None:
    import textwrap

    stdscr.clear()
    h, w = stdscr.getmaxyx()
    max_lines = h - 5

    raw_lines = text.splitlines() or [text]
    wrapped = []
    for rl in raw_lines:
        wrapped.extend(textwrap.wrap(rl, width=max(1, w - 8)) or [""])

    pos = 0
    while True:
        stdscr.clear()
        try:
            stdscr.addstr(1, 2, title, curses.A_BOLD)
        except curses.error:
            try:
                stdscr.addstr(1, 2, title.encode('ascii', 'replace').decode('ascii'))
            except Exception:
                pass

        for i in range(max_lines):
            if pos + i >= len(wrapped):
                break
            try:
                stdscr.addstr(3 + i, 4, wrapped[pos + i])
            except curses.error:
                try:
                    stdscr.addstr(3 + i, 4, wrapped[pos + i].encode('ascii', 'replace').decode('ascii'))
                except Exception:
                    pass

        footer = "↑/↓ PgUp/PgDn pour naviguer — q ou ESC pour revenir"
        try:
            stdscr.addstr(h - 2, 2, footer[: w - 4])
        except curses.error:
            try:
                stdscr.addstr(h - 2, 2, footer.encode('ascii', 'replace').decode('ascii')[: w - 4])
            except Exception:
                pass

        stdscr.refresh()

        if len(wrapped) <= max_lines:
            try:
                key = stdscr.getch()
            except KeyboardInterrupt:
                return
            return

        try:
            key = stdscr.getch()
        except KeyboardInterrupt:
            return

        if key in (curses.KEY_DOWN, ord('j')):
            if pos + max_lines < len(wrapped):
                pos += 1
        elif key in (curses.KEY_UP, ord('k')):
            if pos > 0:
                pos -= 1
        elif key == curses.KEY_NPAGE:
            pos = min(pos + max_lines, max(0, len(wrapped) - max_lines))
        elif key == curses.KEY_PPAGE:
            pos = max(0, pos - max_lines)
        elif key in (ord('q'), 27):
            return


def main(stdscr):
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_CYAN)

    selected = 0
    while True:
        draw_menu(stdscr, selected)
        key = stdscr.getch()

        if key in (curses.KEY_UP, ord('k')):
            selected = (selected - 1) % len(OPTIONS)
        elif key in (curses.KEY_DOWN, ord('j')):
            selected = (selected + 1) % len(OPTIONS)
        elif key in (curses.KEY_ENTER, ord('\n'), ord('\r')):
            _, action = OPTIONS[selected]
            if action == 'quit':
                break

            fichiers = [f for f in os.listdir('.') if f.lower().endswith(IMAGE_EXTS)]
            if not fichiers:
                show_message(stdscr, "Erreur", "Aucune image trouvée dans le dossier courant (formats supportés: {} ).".format(
                    ", ".join(IMAGE_EXTS)))
                continue

            idx = choose_from_list(stdscr, "Choisissez une image:", fichiers)
            if idx == -1:
                continue
            nom_img = fichiers[idx]

            if action == 'encode':
                text = curses_input(stdscr, "Entrez votre message :")
                encode_image(nom_img, text)
                show_message(stdscr, "OK", "Message encodé dans l'image.")
            elif action == 'decode':
                decoded = decode_image(nom_img)
                show_message(stdscr, "Message décodé", decoded)


if __name__ == "__main__":
    curses.wrapper(main)
