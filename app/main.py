from fastapi import FastAPI
from app.routes import entities, history,notify


app = FastAPI(title="Scorpio Data Viewer API", version="0.1.0")

app.include_router(entities.router, prefix="/entities", tags=["Entities"])
app.include_router(history.router, prefix="/history", tags=["History"])
app.include_router(notify.router, prefix="/notify", tags=["notify"])