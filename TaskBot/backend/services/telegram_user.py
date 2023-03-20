from backend.models import TelegramUser


def create_user(telegram_id: int, username: str, fio: str, phone_number:str) -> TelegramUser:
    return TelegramUser.objects.create(
        telegram_id=telegram_id,
        fio=fio,
        username=username,
        phone_number=phone_number
    )


def get_profile_by_telegram_id(telegram_id: int) -> TelegramUser:
    """Возвращает Profile пользователя по telegram_id"""
    return TelegramUser.objects.filter(telegram_id=telegram_id).first()
