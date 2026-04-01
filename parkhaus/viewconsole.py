import os
import time

# ============================================================
# CONSOLE VIEW
# ============================================================

class PresentationConsole:
    def __init__(self):
        self.gui_lines = 0
        self.non_gui_lines = 0

    # ------------------------------------------------------------
    # Low-Level Console
    # ------------------------------------------------------------
    def clear(self):
        os.system("cls" if os.name == "nt" else "clear")
        self.gui_lines = 0
        self.non_gui_lines = 0

    def print_gui_line(self, text=""):
        print(text)
        self.gui_lines += 1

    def print_line(self, text=""):
        print(text)
        self.non_gui_lines += 1

    def clear_non_gui(self):
        for _ in range(self.non_gui_lines):
            print("\033[1A\033[2K", end="")
        self.non_gui_lines = 0

    # ------------------------------------------------------------
    # GUI
    # ------------------------------------------------------------
    def show_gui(self, plaetze):
        self.gui_lines = 0

        self.print_gui_line("╔══════════════════════════════════════╗")
        self.print_gui_line("║            PARKHAUS STATUS           ║")
        self.print_gui_line("╚══════════════════════════════════════╝")

        for i, auto in enumerate(plaetze):
            if auto is None:
                self.print_gui_line(f"[{i+1:02}] ─────────────── frei" + " " * 20)
            else:
                self.print_gui_line(f"[{i+1:02}] {auto.typ:<15} {auto.id}")

        self.print_gui_line("────────────────────────────────────────")

    def refresh_gui(self, plaetze):
        print(f"\033[{self.gui_lines}F", end="")
        self.show_gui(plaetze)

    # ------------------------------------------------------------
    # Menü
    # ------------------------------------------------------------
    def show_menu(self):
        self.print_line("1 = Einfahrt")
        self.print_line("2 = Ausfahrt")
        self.print_line("3 = Anzeigen Refresh")
        self.print_line("0 = Beenden")
        self.print_line("────────────────────────────────────────")

    # ------------------------------------------------------------
    # Interaktion
    # ------------------------------------------------------------
    def message(self, text, color=None):
        farben = {
            "rot": "\033[31m",
            "gruen": "\033[32m",
            "gelb": "\033[33m"
        }
        if color:
            self.print_line(f"{farben[color]}{text}\033[0m")
        else:
            self.print_line(text)
        time.sleep(1)

    def ask(self, text):
        self.non_gui_lines += 1
        return input(text)
