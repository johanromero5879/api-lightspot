from containers import Container


def create_container():
    container = Container()
    container.config.env.from_env("ENV")
    container.config.services.jwt_secret.from_env("JWT_SECRET")
    container.config.services.geolocator_api.from_env("GEOLOCATOR_API")
    container.config.gateways.database.mongo.from_env("MONGO_URI")
    container.check_dependencies()

    return container
