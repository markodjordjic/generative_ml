from fastapi import FastAPI
from app.routers import color_palette

app = FastAPI()

app.include_router(color_palette.router)

@app.get("/")
async def root():
    
    return {"message": "Hello Wild!"}