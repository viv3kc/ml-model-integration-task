# main.py
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.endpoints import router
from app.core.manager import model_manager
from app.models.openai import OpenAIProvider


def register_providers():
    """Register all model providers"""
    model_manager.register_provider(
        "openai",
        OpenAIProvider(),
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    register_providers()
    yield
    # Shutdown
    pass


app = FastAPI(title="Code Analysis Tool", lifespan=lifespan)

# Include routes
app.include_router(router)

if __name__ == "__main__":
    import argparse

    import uvicorn

    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=args.port,
        reload=True,
    )
