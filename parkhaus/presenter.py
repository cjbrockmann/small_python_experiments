

# ============================================================
# PRESENTER
# ============================================================

class ParkhausPresenter:
    def __init__(self, model, view):
        self.model = model
        self.ui = view

    def start_console(self):
        self.ui.clear()
        self.ui.show_gui(self.model.plaetze)

        while True:
            self.ui.show_menu()
            wahl = self.ui.ask("Auswahl: ").strip()

            if wahl == "1":
                typ = self.ui.ask("Fahrzeugtyp: ").strip() or "PKW"
                self.handle_einfahrt(typ)

            elif wahl == "2":
                try:
                    platz = int(self.ui.ask("Platznummer: "))
                except ValueError:
                    self.ui.message("Ungültige Eingabe!", "rot")
                    continue
                self.handle_ausfahrt(platz)

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

    def start_gui(self):
        self.ui.show_gui(self.model.plaetze)

    def handle_einfahrt(self, typ):
        result = self.model.einfahrt(typ)
        if result is None:
            self.ui.message("Keine freien Plätze!", "rot")
        else:
            platz, auto = result
            self.ui.message(f"Einfahrt: {auto} auf Platz {platz+1}", "gruen")
        self.ui.refresh_gui(self.model.plaetze)

    def handle_ausfahrt(self, platz):
        result = self.model.ausfahrt(platz)
        if result == "ungueltig":
            self.ui.message("Ungültiger Platz!", "rot")
        elif result == "frei":
            self.ui.message("Dieser Platz ist bereits frei!", "rot")
        else:
            self.ui.message(f"Ausfahrt: {result}", "gruen")
        self.ui.refresh_gui(self.model.plaetze)

    def refresh(self):
        self.ui.refresh_gui(self.model.plaetze)
