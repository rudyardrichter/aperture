from fastapi import FastAPI

from server.routers import match


def create_app() -> FastAPI:
    api_v0 = FastAPI()
    api_v0.include_router(match.router, prefix="/match")
    app = FastAPI()
    app.mount("/v0", api_v0)
    return app
