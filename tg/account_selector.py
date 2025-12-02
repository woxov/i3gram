"""Account selection screen"""

import curses
import logging
from typing import Optional

log = logging.getLogger(__name__)


class AccountSelector:
    """Interactive account selection UI"""

    def __init__(self, accounts: list) -> None:
        self.accounts = accounts
        self.selected = 0

    def draw(self, stdscr: "curses.window") -> None:
        """Draw account list on screen"""
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        # Header
        header = "Select Telegram Account"
        stdscr.addstr(0, (width - len(header)) // 2, header, curses.A_BOLD)
        stdscr.addstr(1, 0, "=" * width)

        # Account list
        start_y = 3
        for i, phone in enumerate(self.accounts):
            prefix = "▶ " if i == self.selected else "  "
            line = f"{prefix}{phone}"
            
            if i == self.selected:
                stdscr.addstr(start_y + i, 0, line, curses.A_REVERSE)
            else:
                stdscr.addstr(start_y + i, 0, line)

        # Footer
        footer_y = height - 2
        footer = "↑/↓ or j/k: Navigate | Enter: Select | n: New Account | q: Quit"
        stdscr.addstr(footer_y, 0, footer[:width], curses.A_DIM)

        stdscr.refresh()

    def handle_input(self, ch: int) -> Optional[str]:
        """Handle user input, return selected phone or None"""
        if ch == ord('q'):
            return "quit"
        elif ch == ord('n'):
            return "new"
        elif ch == ord('\n') or ch == ord('\r'):
            return self.accounts[self.selected]
        elif ch == ord('j') or ch == curses.KEY_DOWN:
            self.selected = (self.selected + 1) % len(self.accounts)
        elif ch == ord('k') or ch == curses.KEY_UP:
            self.selected = (self.selected - 1) % len(self.accounts)
        return None

    def run(self, stdscr: "curses.window") -> Optional[str]:
        """Run interactive selection loop"""
        curses.curs_set(0)
        stdscr.nodelay(True)

        while True:
            self.draw(stdscr)
            try:
                ch = stdscr.getch()
                if ch == -1:
                    continue
                result = self.handle_input(ch)
                if result:
                    curses.curs_set(1)
                    return result
            except KeyboardInterrupt:
                curses.curs_set(1)
                return "quit"
