from fastapi import APIRouter, Query
from app.services.scorpio_client import ScorpioClient

router = APIRouter()
client = ScorpioClient()

@router.get("/{entity_id}")
def get_history(entity_id: str, attr: str = None):
    return client.get_entity_history(entity_id, attr)
