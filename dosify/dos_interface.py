import curses


class DOSInterface:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.status_win = None
        self.status_win2 = None

    def initialize_windows(self):
        """Initializes the main and status windows."""
        h, w = self.stdscr.getmaxyx()
        self.status_win = curses.newwin(1, w, h-1, 0)  # Статусное окно внизу экрана
        self.status_win2 = curses.newwin(2, 50, 0, 0)  # Дополнительное окно статуса

    def display_files(self, files):
        """Displays files in the curses window with pagination."""
        page_size = self.stdscr.getmaxyx()[0] - 2  # Вычитаем 2 для заголовка и строки продолжения
        pages = [files[i:i + page_size] for i in range(0, len(files), page_size)]
        for page in pages:
            self.stdscr.clear()
            self.stdscr.addstr(0, 0, "Files and folders in the root directory:")
            for idx, file in enumerate(page):
                self.stdscr.addstr(idx + 1, 0, f"{file['name']} (ID: {file['id']}, Type: {file['mimeType']})")
            self.stdscr.addstr(len(page) + 1, 0, "Press any key for next page...")
            self.stdscr.refresh()
            self.stdscr.getch()

    def update_status_window(self, message):
        """Updates the status message in the main status window."""
        self.status_win.clear()
        self.status_win.addstr(0, 0, message)
        self.status_win.refresh()

    def update_status_window2(self):
        """Updates the status message in the second status window."""
        self.status_win2.clear()
        self.status_win2.addstr(0, 0, "Hello\nWorld")
        self.status_win2.refresh()

    def display_menu(self, menu, current_row):
        """Displays the menu with highlighting the selected row."""
        self.stdscr.clear()
        h, w = self.stdscr.getmaxyx()
        for idx, item in enumerate(menu):
            x = w // 2 - len(item) // 2
            y = h // 2 - len(menu) // 2 + idx
            if 0 <= y < h:
                if idx == current_row:
                    self.stdscr.attron(curses.color_pair(1))
                    self.stdscr.addstr(y, x, item)
                    self.stdscr.attroff(curses.color_pair(1))
                else:
                    self.stdscr.addstr(y, x, item)
        self.stdscr.refresh()
