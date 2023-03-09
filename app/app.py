from fastapi import FastAPI

from app.auth.infrastructure import auth_controller
from app.user.infrastructure import user_controller

from config import create_container, initial_setup


def init():
    # App setup
    app = FastAPI()
    app.container = create_container()

    # Routes
    app.include_router(auth_controller.router)
    app.include_router(user_controller.router)

    @app.get("/")
    def root():
        return "Welcome to the API Lightspot!"

    @app.on_event("startup")
    def startup():
        initial_setup()

    return app
