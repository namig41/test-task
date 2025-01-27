"""
Модель работы с датами.
"""

import datetime


def ts_now() -> datetime.datetime:
    """
    Возвращает текущий timestamp по GTM.

    :return: Значение даты
    """
    return datetime.datetime.now(datetime.timezone.utc)
