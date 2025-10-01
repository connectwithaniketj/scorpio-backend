from fastapi import APIRouter, Request
from app.services.scorpio_client import ScorpioClient

router = APIRouter()

@router.post("")
async def notify(request: Request):
    body = await request.json()
    print(" Notification received from Scorpio:")
    print(body)
    # You can add logic here (store in DB, trigger alert, etc.)
    return {"status": "received"}

@router.post("/location_change")
async def location_change(request: Request):
    body = await request.json()
    print("📍 Location change received from Scorpio:")
    print(body)
    # You can add logic here (store in DB, trigger alert, etc.)
    return {"status": "received"}

