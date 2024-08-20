import curses

from auth.google_oauth_auth import GoogleOAuthAuth
from auth.google_service_auth import GoogleServiceAuth
from data_transfer.google_drive_handler import GoogleDriveHandler


def display_files(stdscr, files):
    """Display files in the curses window with pagination."""
    page_size = stdscr.getmaxyx()[0] - 2  # Вычитаем 2 для заголовка и строки продолжения
    pages = [files[i:i + page_size] for i in range(0, len(files), page_size)]
    for page in pages:
        stdscr.clear()
        stdscr.addstr(0, 0, "Files and folders in the root directory:")
        for idx, file in enumerate(page):
            stdscr.addstr(idx + 1, 0, f"{file['name']} (ID: {file['id']}, Type: {file['mimeType']})")
        stdscr.addstr(len(page) + 1, 0, "Press any key for next page...")
        stdscr.refresh()
        stdscr.getch()


def main(stdscr):
    curses.curs_set(0)
    stdscr.clear()

    h, w = stdscr.getmaxyx()
    status_win = curses.newwin(1, w, h-1, 0)  # Создаём окно для статуса внизу экрана
    status_message = "Ready. Select an option."

    def update_status_window(message):
        """Update the status message in the status window."""
        status_win.clear()  # Очищаем только статусное окно
        status_win.addstr(0, 0, message)
        status_win.refresh()

    update_status_window(status_message)  # Первоначальное обновление статусного сообщения

    auth = GoogleServiceAuth()
    drive_handler = GoogleDriveHandler(auth)
    menu = ["Authorize OAuth", "List Root Files", "Exit"]
    current_row = 0

    def print_menu():
        stdscr.clear()
        for idx, item in enumerate(menu):
            x = w // 2 - len(item) // 2
            y = h // 2 - len(menu) // 2 + idx
            if 0 <= y < h:
                if idx == current_row:
                    stdscr.attron(curses.color_pair(1))
                    stdscr.addstr(y, x, item)
                    stdscr.attroff(curses.color_pair(1))
                else:
                    stdscr.addstr(y, x, item)
        stdscr.refresh()
        update_status_window(status_message)

    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    auth2 = None

    while True:
        print_menu()
        key = stdscr.getch()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
            status_message = "Moving up in menu..."
        elif key == curses.KEY_DOWN and current_row < len(menu) - 1:
            current_row += 1
            status_message = "Moving down in menu..."
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if current_row == 0:  # Authorize OAuth
                status_message = "Authenticating with OAuth..."
                stdscr.clear()
                if auth2 is None:
                    auth2 = GoogleOAuthAuth()
                    auth2.authenticate()
                status_message = "OAuth authorization complete."
                stdscr.addstr(10, 10, "OAuth authorization complete. Press any key to continue...")
                stdscr.refresh()
                stdscr.getch()
            elif current_row == 1:  # List Root Files
                status_message = "Listing root files..."
                stdscr.clear()
                files = []
                if auth2 is not None:
                    drive_handler = GoogleDriveHandler(auth2)
                    files = drive_handler.get_root_files_list()
                else:
                    files = drive_handler.get_root_files_list()
                display_files(stdscr, files)
                status_message = "Displayed root files."
                stdscr.refresh()
                stdscr.getch()
            elif current_row == 2:  # Exit
                status_message = "Exiting..."
                break


if __name__ == "__main__":
    curses.wrapper(main)
