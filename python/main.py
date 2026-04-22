from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from parkhaus.model import ParkhausModel
from parkhaus.presenter import ParkhausPresenter
from parkhaus.viewapi import ParkhausApiView


model = ParkhausModel(10)
presenter = ParkhausPresenter(model=model)
api_view = ParkhausApiView(presenter=presenter)

app = FastAPI(title="Parkhaus API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_view.router)


@app.get("/")
async def root():
    return {
        "message": "Parkhaus API laeuft",
        "docs": "/docs",
        "status_endpoint": "/parkhaus/status",
    }
