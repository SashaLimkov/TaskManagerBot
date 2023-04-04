from backend.models import TelegramUser


def create_user(telegram_id: int, username: str, fio: str, phone_number: str) -> TelegramUser:
    return TelegramUser.objects.create(
        telegram_id=telegram_id,
        fio=fio,
        username=username,
        phone_number=phone_number
    )


def get_profile_by_telegram_id(telegram_id: int) -> TelegramUser:
    """Возвращает Profile пользователя по telegram_id"""
    return TelegramUser.objects.filter(telegram_id=telegram_id).first()


def get_profile_by_pk(user_pk: int) -> TelegramUser:
    """Возвращает Profile пользователя по telegram_id"""
    print(user_pk)
    return TelegramUser.objects.filter(pk=user_pk).first()


def get_profile_by_username(username: str) -> TelegramUser:
    """Возвращает Profile пользователя по telegram_id"""
    return TelegramUser.objects.filter(username=username).first()
