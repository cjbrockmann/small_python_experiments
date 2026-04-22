

# ============================================================
# PRESENTER
# ============================================================

class ParkhausPresenter:
    def __init__(self, model, view=None):
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
                result = self.handle_einfahrt(typ)
                self._show_console_result(result)

            elif wahl == "2":
                try:
                    platz = int(self.ui.ask("Platznummer: "))
                except ValueError:
                    self.ui.message("Ungültige Eingabe!", "rot")
                    continue
                result = self.handle_ausfahrt(platz)
                self._show_console_result(result)

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
            return {
                "status": "error",
                "message": "Keine freien Plätze!",
                "color": "rot",
                "plaetze": self.model.plaetze
            }

        platz, auto = result
        return {
            "status": "ok",
            "message": f"Einfahrt: {auto} auf Platz {platz+1}",
            "color": "gruen",
            "platz": platz + 1,
            "auto_id": auto.id,
            "fahrzeugtyp": auto.typ,
            "plaetze": self.model.plaetze
        }

    def handle_ausfahrt(self, platz):
        result = self.model.ausfahrt(platz)
        if result == "ungueltig":
            return {
                "status": "error",
                "message": "Ungültiger Platz!",
                "color": "rot",
                "plaetze": self.model.plaetze
            }
        if result == "frei":
            return {
                "status": "error",
                "message": "Dieser Platz ist bereits frei!",
                "color": "rot",
                "plaetze": self.model.plaetze
            }

        return {
            "status": "ok",
            "message": f"Ausfahrt: {result}",
            "color": "gruen",
            "auto_id": result.id,
            "fahrzeugtyp": result.typ,
            "plaetze": self.model.plaetze
        }

    def refresh(self):
        return self.model.plaetze

    def _show_console_result(self, result):
        self.ui.message(result["message"], result["color"])
        self.ui.refresh_gui(self.model.plaetze)
