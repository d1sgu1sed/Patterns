import abc
import uuid

from Src.Core.validator import validator

"""
Исключение при подачи в __eq__ аргумента 
другого типа
"""   
class type_exception(Exception):
    pass  

class abstract(abc.ABC):
    """
    Абстрактная модель, содержит ID и имя.

    Поля:
        unique_code (str): Уникальный ID-код модели.
        name (str): Имя (не больше 50 симв).
    """
    __unique_code:str
    __name: str

    @abc.abstractmethod
    def __init__(self, name: str = "") -> None:
        super().__init__()
        self.__unique_code = uuid.uuid4().hex
        self.__name = name

    """
    Уникальный код
    """
    @property
    def unique_code(self) -> str:
        return self.__unique_code

    """
    Алиас для unique_code (для совместимости с DTO)
    """
    @property
    def id(self) -> str:
        return self.__unique_code

    """
    Имя
    """
    @property
    def name(self) -> str:
        return self.__name

    @unique_code.setter
    def unique_code(self, value: str):
        validator.validate(value, str)
        self.__unique_code = value.strip()

    @id.setter
    def id(self, value: str):
        # Setter для алиаса id - устанавливает unique_code
        validator.validate(value, str)
        self.__unique_code = value.strip()
    
    @name.setter
    def name(self, value: str):
        validator.validate(value, str)
        self.__name = value

    """
    Перегрузка штатного варианта сравнения
    """
    def __eq__(self, other) -> bool:
        if not isinstance(other, abstract):
            raise type_exception("Некорректный тип данных")
        return self.__unique_code == other.unique_code
