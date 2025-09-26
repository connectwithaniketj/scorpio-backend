from fastapi import APIRouter, HTTPException
from app.services.scorpio_client import ScorpioClient


router = APIRouter()
client = ScorpioClient()

# @router.get("/")
# def list_entities():
#     return client.get_entities()

@router.get("/{entity_id}")
def get_entity(entity_id: str):
    entity = client.get_entity(entity_id)
    if not entity:
        raise HTTPException(status_code=404, detail="Entity not found")
    return entity

@router.get("/", summary="Get all entity types in Scorpio")
def get_entity_types():
    """
    Fetch all entity types currently present in the Scorpio Context Broker.
    Returns a list of unique entity type URIs.
    """
    try:
        types = client.get_entity_types()  # Calls method in ScorpioClient
        if not types:
            raise HTTPException(status_code=404, detail="No entity types found")
        return {"typeList": types}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))