import curses

from dosify.dos_application import DOSApplication


def main(stdscr):
    app = DOSApplication(stdscr)
    app.run()


if __name__ == "__main__":
    curses.wrapper(main)
