from app.common.infrastructure import SendEmail, Body, JwtAdapter
from app.user.domain import UserOut


class SendEmailToNewUser:
    def __init__(self, send_email: SendEmail, client_url: str, jwt: JwtAdapter):
        self.send_email = send_email
        self.client_url = client_url
        self.jwt = jwt

    def __call__(self, user: UserOut):
        token = self.jwt.encrypt(f"user_id:{user.id}")

        subject = "¡Ha sido registrado en Lightspot!"
        body = f"""
            Hola, {user.fullname}<br><br>
            Un administrador ha creado una cuenta para usted. Para acceder haga clic 
            <a href='{self.client_url}?registration_token={token}'>aquí</a>.<br>
            Posteriormente será dirigido al aplicativo para asignar su contraseña.
            """

        self.send_email(
            subject=subject,
            body=body,
            to=user.email,
            body_type=Body.HTML
        )
