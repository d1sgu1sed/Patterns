import abc
from Src.Core.validator import validator, operation_exception
from Src.Models.recipe_model import recipe_model

class abstract_response(abc.ABC):
    """
    Абстрактный класс для формирования ответов
    """
    
    """
    Сформировать нужный ответ
    """
    @abc.abstractmethod
    def generate(self, format:str, data: list) -> str:
        validator.validate(format, str)
        validator.validate(data, list)

        if len(data) == 0:
            raise operation_exception("Нет данных!")

        return ""
