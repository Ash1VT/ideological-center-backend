from fastapi_mail import MessageSchema
from setup.email import fm


async def send_email(receiver_email: str, subject: str, body: str):
    message = MessageSchema(
        subject=subject,
        recipients=[receiver_email],
        body=body,
        subtype="html",
    )

    await fm.send_message(message)
