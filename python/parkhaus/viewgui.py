
import tkinter as tk
from tkinter import ttk


# ============================================================
# TKINTER GUI VIEW
# ============================================================

class PresentationGui:
    def __init__(self, root):
        self.root = root
        self.presenter = None

        self.root.title("Parkhaus GUI")
        self.frame = tk.Frame(root, padx=20, pady=20)
        self.frame.pack()

        self.frame.grid_columnconfigure(0, minsize=180)
        self.frame.grid_columnconfigure(1, minsize=260)

        # Überschrift (groß & fett)
        self.title_label = tk.Label(
            self.frame,
            text="PARKHAUS VERWALTUNG",
            font=("Arial", 18, "bold"),
            anchor="center"
        )
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(0, 15))        

        # Parkplatzliste
        self.platz_frame = tk.Frame(self.frame)
        self.platz_frame.grid(row=1, column=1, rowspan=10, padx=20, sticky="n")

        # Frame für Label + Combobox
        self.input_frame = tk.Frame(self.frame)
        self.input_frame.grid(row=2, column=0, pady=5, sticky="w")

        # Label
        tk.Label(self.input_frame, text="Fahrzeugtyp:").pack(side="left")

        # Combobox
        self.entry = ttk.Combobox(
            self.input_frame,
            values=["PKW", "SUV", "Elektro", "Motorrad"],
            width=15
        )
        self.entry.bind("<<ComboboxSelected>>", lambda e: self.root.focus())
        self.entry.set("PKW")
        self.entry.pack(side="left", padx=5)

        # Buttons links
        self.btn_einfahrt = tk.Button(self.frame, text="Einfahrt", width=20, command=self.on_einfahrt)
        self.btn_beenden = tk.Button(self.frame, text="Beenden", width=20, command=root.quit)

        self.btn_einfahrt.grid(row=1, column=0, pady=5)

        # Statuszeile
        self.status = tk.Label(
            self.frame,
            text="",
            fg="black",
            width=30,
            height=3,
            anchor="w",
            justify="left",
            wraplength=200,
            relief="flat",
            bd=0
        )
        self.status.grid(row=3, column=0, pady=10, sticky="we")
        self.colors = {
            "rot": "#cc0000",
            "gruen": "#008800",
            "gelb": "#cc8800",
            None: "black"
        }
        self._status_hide_id = None
        self.btn_beenden.grid(row=4, column=0, pady=5)

        self.window_locked = False

    def lock_window_size(self):
        if not self.window_locked:
            self.root.update_idletasks()
            self.root.minsize(self.root.winfo_width(), self.root.winfo_height())
            self.root.maxsize(self.root.winfo_width(), self.root.winfo_height())
            self.window_locked = True

    def show_gui(self, plaetze):
        for widget in self.platz_frame.winfo_children():
            widget.destroy()

        for i, auto in enumerate(plaetze):
            row = tk.Frame(self.platz_frame)
            row.pack(fill="x")

            if auto is None:
                text = f"[{i+1:02}] frei"
            else:
                text = f"[{i+1:02}] {auto.typ} ({auto.id})"

            lbl = tk.Label(row, text=text, anchor="w", width=25, font=("Consolas", 11))
            lbl.pack(side="left")

            btn = tk.Button(
                row,
                text="X",
                fg="red",
                width=3,
                command=lambda p=i+1: self.on_ausfahrt_platz(p)
            )
            btn.pack(side="right")

        self.lock_window_size()

    def refresh_gui(self, plaetze):
        self.show_gui(plaetze)

    def message(self, text, color=None):
        self.message_timed(text, color)
        # self.status.configure(fg=self.colors.get(color, "black"))
        # self.status.configure(text=text)

    def on_einfahrt(self):
        typ = self.entry.get().strip() or "PKW"
        result = self.presenter.handle_einfahrt(typ)
        self.message(result["message"], result["color"])
        self.refresh_gui(result["plaetze"])
        self.entry.set("PKW")   # Combobox zurücksetzen

    def on_ausfahrt(self):
        try:
            platz = int(self.entry.get().strip())
        except ValueError:
            self.message("Bitte eine gültige Zahl eingeben!", "rot")
            return
        result = self.presenter.handle_ausfahrt(platz)
        self.message(result["message"], result["color"])
        self.refresh_gui(result["plaetze"])

    def on_refresh(self):
        self.refresh_gui(self.presenter.refresh())

    def on_ausfahrt_platz(self, platz):
        result = self.presenter.handle_ausfahrt(platz)
        self.message(result["message"], result["color"])
        self.refresh_gui(result["plaetze"])

    def message_timed(self, text, color=None, timeout_ms=2000):
        if self._status_hide_id is not None:
            self.root.after_cancel(self._status_hide_id)
        self.status.configure(fg=self.colors.get(color, "black"), text=text)
        self._status_hide_id = self.root.after(timeout_ms, self._hide_status)

    def _hide_status(self):
        self.status.configure(text="")
        self._status_hide_id = None        
