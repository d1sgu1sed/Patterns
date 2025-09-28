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
    __unique_code:str
    __name: str

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
    Имя
    """
    @property
    def name(self) -> str:
        return self.__name
    
    @unique_code.setter
    def unique_code(self, value: str):
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
