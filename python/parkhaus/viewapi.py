from fastapi import APIRouter
from pydantic import BaseModel


class EinfahrtRequest(BaseModel):
    fahrzeugtyp: str = "PKW"


class ParkhausApiView:
    def __init__(self, presenter):
        self.presenter = presenter
        self.router = APIRouter(prefix="/parkhaus", tags=["Parkhaus"])
        self.router.add_api_route("/status", self.get_status, methods=["GET"])
        self.router.add_api_route("/einfahrt", self.post_einfahrt, methods=["POST"])
        self.router.add_api_route("/ausfahrt/{platz}", self.post_ausfahrt, methods=["POST"])

    def _serialize_plaetze(self, plaetze):
        response = []
        for i, auto in enumerate(plaetze, start=1):
            if auto is None:
                response.append(
                    {
                        "platz": i,
                        "belegt": False,
                        "fahrzeugtyp": None,
                        "auto_id": None,
                    }
                )
            else:
                response.append(
                    {
                        "platz": i,
                        "belegt": True,
                        "fahrzeugtyp": auto.typ,
                        "auto_id": auto.id,
                    }
                )
        return response

    async def get_status(self):
        plaetze = self.presenter.refresh()
        return {"plaetze": self._serialize_plaetze(plaetze)}

    async def post_einfahrt(self, payload: EinfahrtRequest):
        result = self.presenter.handle_einfahrt(payload.fahrzeugtyp)
        return {
            "status": result["status"],
            "message": result["message"],
            "platz": result.get("platz"),
            "auto_id": result.get("auto_id"),
            "fahrzeugtyp": result.get("fahrzeugtyp"),
            "plaetze": self._serialize_plaetze(result["plaetze"]),
        }

    async def post_ausfahrt(self, platz: int):
        result = self.presenter.handle_ausfahrt(platz)
        return {
            "status": result["status"],
            "message": result["message"],
            "auto_id": result.get("auto_id"),
            "fahrzeugtyp": result.get("fahrzeugtyp"),
            "plaetze": self._serialize_plaetze(result["plaetze"]),
        }
