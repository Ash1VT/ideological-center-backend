from loguru import logger

from core.utils.email import send_email


async def send_application_created_email(user_email: str, event_name: str):
    await send_email(
        subject="Заявки на мероприятия",
        receiver_email=user_email,
        body=f"Ваша заявка на мероприятие {event_name} принята!"
    )

    logger.info(f"Application created email sent to {user_email}")


async def send_application_accepted_email(user_email: str, event_name: str):
    await send_email(
        subject="Заявки на мероприятия",
        receiver_email=user_email,
        body=f"Ваша заявка на мероприятие {event_name} подтверждена! Теперь вы участник мероприятия."
    )

    logger.info(f"Application accepted email sent to {user_email}")


async def send_application_rejected_email(user_email: str, event_name: str):
    await send_email(
        subject="Заявки на мероприятия",
        receiver_email=user_email,
        body=f"К сожалению, ваша заявка на мероприятие {event_name} была отклонена."
    )

    logger.info(f"Application declined email sent to {user_email}")
