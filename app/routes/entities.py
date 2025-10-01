from fastapi.responses import HTMLResponse
from fastapi import APIRouter, HTTPException, Query,Request
from app.services.scorpio_client import ScorpioClient
import logging
import json
from fastapi.templating import Jinja2Templates
import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
print(BASE_DIR)  # adjust based on your structure
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

templates = Jinja2Templates(directory=TEMPLATES_DIR)

router = APIRouter()
client = ScorpioClient()

TYPE_MAP = {
    "vessel": "https://smartdatamodels.org/dataModel.MarineTransport/Vessel",
    "port": "https://smartdatamodels.org/dataModel.MarineTransport/Port"
}

# @router.get("/")
# def list_entities():
#     return client.get_entities()

# @router.get("/{entity_id}")
# def get_entity(entity_id: str):
#     entity = client.get_entity(entity_id)
#     if not entity:
#         raise HTTPException(status_code=404, detail="Entity not found")
#     return entity

@router.get("/test")
def test_endpoint():
    return {"message": "Test endpoint works"}


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
    
@router.get("/{entity_type}", summary="Get all entity IDs for a given type")
def get_entity_ids(entity_type: str):
    try:
        full_type = TYPE_MAP.get(entity_type.lower())
        if not full_type:
            raise HTTPException(status_code=400, detail="Unknown entity type")

        entities = client.query_entities(
            params={"type": full_type, "attrs": "id"}
        )
        return {"ids": [e["id"] for e in entities]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

logger = logging.getLogger(__name__)


@router.get("/vessel/nearby_vessels", summary="Get vessels near a location")
def get_nearby_vessels(
    longitude: float = Query(..., description="Longitude of the point"),
    latitude: float = Query(..., description="Latitude of the point"),
    max_distance: int = Query(10000, description="Max distance in meters")
):
    #logger.info(f"Function called with longitude={longitude}, latitude={latitude}, max_distance={max_distance}")

    try:
        # Example: Your Scorpio query params — fix format
        params = {
            "type": "https://smartdatamodels.org/dataModel.MarineTransport/Vessel",
            "georel": f"near;maxDistance=={max_distance}",
            "geometry": "Point",
            "coordinates": json.dumps([longitude, latitude]),
            "geoproperty": "location"
        }

        #logger.info(f"Querying with params: {params}")

        vessels = client.query_entities(params=params)  # Your Scorpio client call
        #logger.info(f"Received vessels: {vessels}")

        result = []
        for v in vessels:
            try:
                coords = v["location"]["value"]["coordinates"]
                result.append({"id": v["id"], "coordinates": coords})
            except KeyError:
                logger.warning(f"Missing location for vessel {v.get('id')}")
                continue

        return {"count": len(result), "vessels": result}

    except Exception as e:
        logger.exception("Error fetching nearby vessels")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/vessel/history", summary="Get vessel travel path (only geopoints)")
def get_vessel_history(
    vessel_id: str = Query(..., description="URN ID of the vessel")
):
    try:
        logger.info(f"Fetching vessel history for {vessel_id}")

        history = client.query_temporal_entity(
            entity_id=vessel_id,
            params={"attrs": "location"}
        )

        #print(history)

        if isinstance(history, list) and history:
            history = history[0]

        
        path = []

        current_entity = client.get_entity(vessel_id)
        if current_entity:
            current_coords = (
                current_entity
                .get("location", {})
                .get("value", {})
                .get("coordinates")
            )
            if current_coords and current_coords not in path:
                path.append(current_coords)

        location_data = history.get("location")
        print(location_data)
        # if isinstance(location_data, list):
        #     # Multiple GeoProperty history entries
        #     for loc in location_data:
        #         coords = loc.get("value", {}).get("coordinates")
        #         if coords:
        #             path.append(coords)
        # elif isinstance(location_data, dict):
        #     # Single GeoProperty entry
        #     coords = location_data.get("value", {}).get("coordinates")
        #     if coords:
        #         path.append(coords)
        if isinstance(location_data, list):
            # Sort locations by observedAt (fallback to modifiedAt if missing)
            sorted_locations = sorted(
                location_data,
                key=lambda loc: loc.get("observedAt") or loc.get("modifiedAt") or "0000-01-01T00:00:00Z",
                reverse=True   # Newest first
            )

            for loc in sorted_locations:
                coords = loc.get("value", {}).get("coordinates")
                if coords:
                    path.append(coords)

        #print(path)

        return {"id": vessel_id, "path": path}

    except Exception as e:
        logger.exception("Error fetching vessel history")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/vessel/details", response_class=HTMLResponse)
def vessel_details(request: Request, vessel_id: str):
    return templates.TemplateResponse(
        "details.html",
        {"request": request, "vessel_id": vessel_id}
    )