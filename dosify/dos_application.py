import curses

from auth.google_oauth_auth import GoogleOAuthAuth
from auth.google_service_auth import GoogleServiceAuth
from data_transfer.google_drive_handler import GoogleDriveHandler
from dosify.dos_interface import DOSInterface


class DOSApplication:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.interface = DOSInterface(stdscr)
        self.auth = GoogleServiceAuth()
        self.drive_handler = GoogleDriveHandler(self.auth)
        self.auth2 = None
        self.menu = ["Authorize OAuth", "List Root Files", "Exit"]
        self.current_row = 0
        self.status_message = "Ready. Select an option."

    def run(self):
        """Main loop of the DOS application."""
        curses.curs_set(0)
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

        self.interface.initialize_windows()

        while True:
            self.interface.display_menu(self.menu, self.current_row)
            self.interface.update_status_window(self.status_message)
            self.interface.update_status_window2()
            key = self.stdscr.getch()

            if key == curses.KEY_UP and self.current_row > 0:
                self.current_row -= 1
                self.status_message = "Moving up in menu..."
            elif key == curses.KEY_DOWN and self.current_row < len(self.menu) - 1:
                self.current_row += 1
                self.status_message = "Moving down in menu..."
            elif key == curses.KEY_ENTER or key in [10, 13]:
                self.handle_menu_selection()

            if self.status_message == "Exiting...":
                break

    def handle_menu_selection(self):
        """Handle the current menu selection."""
        if self.current_row == 0:  # Authorize OAuth
            self.status_message = "Authenticating with OAuth..."
            self.stdscr.clear()
            if self.auth2 is None:
                self.auth2 = GoogleOAuthAuth()
                self.auth2.authenticate()
            self.status_message = "OAuth authorization complete."
            self.stdscr.addstr(10, 10, "OAuth authorization complete. Press any key to continue...")
            self.stdscr.refresh()
            self.stdscr.getch()
        elif self.current_row == 1:  # List Root Files
            self.status_message = "Listing root files..."
            self.stdscr.clear()
            files = self.drive_handler.get_root_files_list() if self.auth2 else []
            self.interface.display_files(files)
            self.status_message = "Displayed root files."
            self.stdscr.refresh()
            self.stdscr.getch()
        elif self.current_row == 2:  # Exit
            self.status_message = "Exiting..."
