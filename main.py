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
    parser.add_argument("--test", action="store_true", help="Run unit tests")
    args = parser.parse_args()

    # Run tests if --test flag is provided
    if args.test:
        # TO DO Run tests
        pass
    else:
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=args.port,
            reload=True,
        )
