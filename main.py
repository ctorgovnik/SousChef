from fastapi import FastAPI
from src.api.routes import router
from src.config.settings import Settings

app = FastAPI()
settings = Settings()

app.include_router(router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 