from fastapi import FastAPI
from app.routes import entities, history,notify
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.requests import Request

app = FastAPI(title="Scorpio Data Viewer API", version="0.1.0")
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")


app.include_router(entities.router, prefix="/entities", tags=["Entities"])
app.include_router(history.router, prefix="/history", tags=["History"])
app.include_router(notify.router, prefix="/notify", tags=["notify"])

@app.get("/", summary="Show map page")
async def map_page(request: Request):
    return templates.TemplateResponse("map.html", {"request": request})