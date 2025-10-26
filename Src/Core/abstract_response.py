import abc
from Src.Converters.convert_factory import convert_factory
from Src.Core.abstract import abstract
from Src.Core.validator import validator, operation_exception

class abstract_response(abc.ABC):
    """
    Абстрактный класс для формирования ответов
    """
    
    """
    Сформировать нужный ответ
    """
    @abc.abstractmethod
    def generate(self, data: list) -> str:
        validator.validate(data, list)

        if len(data) == 0:
            raise operation_exception("Нет данных!")

        return ""
    
    """
    Создание словаря из объекта
    """
    def generate_dict(self, data: list[abstract]):
        validator.validate(data, list)
        validator.validate(data[0], abstract)
        converter = convert_factory()
        return converter.convert(data)

