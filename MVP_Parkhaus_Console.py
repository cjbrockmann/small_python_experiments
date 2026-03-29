import os
import time
import random

# ============================================================
# MODEL
# ============================================================

class Auto:
    def __init__(self, typ, auto_id):
        self.typ = typ
        self.id = auto_id

    def __str__(self):
        return f"{self.typ} ({self.id})"


class ParkhausModel:
    def __init__(self, anzahl_plaetze):
        self.plaetze = [None] * anzahl_plaetze

    # -----------------------------
    # Hilfsfunktionen
    # -----------------------------
    def _erstelle_auto(self, fahrzeugtyp):
        return Auto(
            typ=fahrzeugtyp,
            auto_id="A" + str(random.randint(1000, 9999))
        )

    def finde_freien_platz(self):
        for i, p in enumerate(self.plaetze):
            if p is None:
                return i
        return None

    # -----------------------------
    # Geschäftslogik
    # -----------------------------
    def einfahrt(self, fahrzeugtyp):
        platz = self.finde_freien_platz()
        if platz is None:
            return None

        auto = self._erstelle_auto(fahrzeugtyp)
        self.plaetze[platz] = auto
        return platz, auto

    def ausfahrt(self, platznummer):
        nummer = platznummer - 1
        if nummer < 0 or nummer >= len(self.plaetze):
            return "ungueltig"

        auto = self.plaetze[nummer]
        if auto is None:
            return "frei"

        self.plaetze[nummer] = None
        return auto


# ============================================================
# VIEW (Presentation)
# ============================================================

class Presentation:
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


# ============================================================
# PRESENTER
# ============================================================

class ParkhausPresenter:
    def __init__(self, model, view):
        self.model = model
        self.ui = view

    def start(self):
        self.ui.clear()
        self.ui.show_gui(self.model.plaetze)

        while True:
            self.ui.show_menu()
            wahl = self.ui.ask("Auswahl: ").strip()

            if wahl == "1":
                typ = self.ui.ask("Fahrzeugtyp: ").strip() or "Normal"
                result = self.model.einfahrt(typ)

                if result is None:
                    self.ui.message("Keine freien Plätze!", "rot")
                else:
                    platz, auto = result
                    self.ui.message(f"Einfahrt: {auto} auf Platz {platz+1}", "gruen")

            elif wahl == "2":
                try:
                    platz = int(self.ui.ask("Platznummer: "))
                except ValueError:
                    self.ui.message("Ungültige Eingabe!", "rot")
                    continue

                result = self.model.ausfahrt(platz)

                if result == "ungueltig":
                    self.ui.message("Ungültiger Platz!", "rot")
                elif result == "frei":
                    self.ui.message("Dieser Platz ist bereits frei!", "rot")
                else:
                    self.ui.message(f"Ausfahrt: {result}", "gelb")

            elif wahl == "3":
                self.ui.ask("Weiter mit ENTER...")
                self.ui.clear()
                self.ui.show_gui(self.model.plaetze)
                continue

            elif wahl == "0":
                self.ui.message("Programm beendet.")
                self.ui.clear()
                break

            else:
                self.ui.message("Ungültige Auswahl!", "rot")

            self.ui.clear_non_gui()
            self.ui.refresh_gui(self.model.plaetze)


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    view = Presentation()
    model = ParkhausModel(10)
    presenter = ParkhausPresenter(model, view)
    presenter.start()
