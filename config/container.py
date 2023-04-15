from containers import Container


def create_container():
    container = Container()

    container.config.env.from_env("ENV")

    # Server
    container.config.services.jwt_secret.from_env("JWT_SECRET")

    # Client
    container.config.services.client.url.from_env("CLIENT_URL")

    # Databases
    container.config.gateways.database.mongo.from_env("MONGO_URI")

    # SMTP
    container.config.services.smtp.server.from_env("SMTP_SERVER")
    container.config.services.smtp.username.from_env("SMTP_USERNAME")
    container.config.services.smtp.password.from_env("SMTP_PASSWORD")

    # External services
    container.config.services.geolocator_api.from_env("GEOLOCATOR_API")

    container.check_dependencies()

    return container
