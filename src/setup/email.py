from fastapi_mail import ConnectionConfig, FastMail

from setup.settings.server import get_server_settings

settings = get_server_settings()

conf = ConnectionConfig(
    MAIL_USERNAME=settings.email_host_user,
    MAIL_PASSWORD=settings.email_host_password,
    MAIL_FROM=settings.email_from,
    MAIL_PORT=settings.email_port,
    MAIL_SERVER=settings.email_host,
    MAIL_FROM_NAME=settings.email_from_name,
    MAIL_SSL_TLS=settings.email_use_ssl,
    MAIL_STARTTLS=settings.email_use_tls,
    USE_CREDENTIALS=True,
)

fm = FastMail(conf)
