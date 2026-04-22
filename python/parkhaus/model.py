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
