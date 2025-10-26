import abc
from typing import Any

class abstract_converter(abc.ABC):
    """
    Абстрактный класс для перевода объектов в словарь
    """

    """
    Конвертация объекта в словарь
    """
    @abc.abstractmethod
    def convert(self, data: Any) -> str:
        pass