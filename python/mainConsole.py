
from parkhaus.model import ParkhausModel as Model 
from parkhaus.presenter import ParkhausPresenter as Presenter 
from parkhaus.viewconsole import PresentationConsole as View 

# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    model = Model(10)
    view = View()
    presenter = Presenter(model, view)
    presenter.start_console()
