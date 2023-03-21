from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.auth.infrastructure import auth_controller
from app.user.infrastructure import user_controller
from app.flash.infrastructure import flash_controller

from config import create_container, initial_setup, ALLOWED_ORIGINS


def init():
    # App setup
    app = FastAPI()
    app.container = create_container()

    # Middlewares
    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    # Routes
    app.include_router(auth_controller.router)
    app.include_router(user_controller.router)
    app.include_router(flash_controller.router)

    @app.get("/")
    def root():
        return "Welcome to the API Lightspot!"

    @app.on_event("startup")
    def startup():
        initial_setup()

    return app
