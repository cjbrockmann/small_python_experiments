
from parkhaus.model import ParkhausModel as Model 
from parkhaus.presenter import ParkhausPresenter as Presenter
from parkhaus.viewgui import PresentationGui as View 
import tkinter as tk
from tkinter import ttk

# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    model = Model(10)
    root = tk.Tk()
    view = View(root)
    presenter = Presenter(model, view)
    view.presenter = presenter  # Damit die GUI an den Presenter zugreifen kann... 
    presenter.start_gui()
    root.mainloop()

