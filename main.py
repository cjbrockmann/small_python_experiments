from fastapi import FastAPI

from parkhaus.model import ParkhausModel
from parkhaus.presenter import ParkhausPresenter
from parkhaus.viewapi import ParkhausApiView


model = ParkhausModel(10)
presenter = ParkhausPresenter(model=model)
api_view = ParkhausApiView(presenter=presenter)

app = FastAPI(title="Parkhaus API", version="1.0.0")
app.include_router(api_view.router)


@app.get("/")
async def root():
    return {
        "message": "Parkhaus API laeuft",
        "docs": "/docs",
        "status_endpoint": "/parkhaus/status",
    }
