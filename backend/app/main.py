from fastapi import FastAPI
from app.routers.github_router import router as github_router

app = FastAPI()
app.include_router(github_router)

@app.get("/")
async def root():
    return {"message": "GitHub Explorer API"}