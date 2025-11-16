from Src.Core.abstract_dto import abstract_dto
from Src.Core.validator import argument_exception, validator


"""
DTO для представления фильтра.
Содержит название поля, значение и условие для фильтрации.
"""
class filter_dto(abstract_dto):
    __field_name: str = ""
    __value = ""
    __condition: str = ""
    __conditions_dict: dict
    
    def __init__(self):
        super().__init__()
        # Словарь условий: ключ - название условия, значение - лямбда-функция, принимающая два аргумента
        self.__conditions_dict: dict = {
            "LIKE": lambda field, pattern: pattern in field,
            "EQUALS": lambda field, expected: field == expected,
            "NOT EQUALS": lambda field, expected: field != expected,
            # Для числовых и датовых полей:
            "MORE": lambda field, bound: field > bound,
            "LESS": lambda field, bound: field < bound,
            # Диапазон: bound — кортеж (left, right)
            "IN RANGE": lambda field, bound: bound[0] < field < bound[1]
        }
    
    """
    Название поля фильтрации
    """
    @property
    def field_name(self) -> str:
        return self.__field_name
    
    @field_name.setter
    def field_name(self, value: str):
        validator.validate(value, str)
        self.__field_name = value
    
    """
    Значение для фильтрации
    """
    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value):
        self.__value = value
    
    """
    Модификатор условия
    """
    @property
    def condition(self) -> str:
        return self.__condition
        
    @condition.setter
    def condition(self, value: str):
        validator.validate(value, str)
        if value not in self.__conditions_dict.keys():
            raise argument_exception("Такого модификатора условия нет!")    
        self.__condition = value
    
    """
    Возвращает функцию-условие по его названию.
    """
    def get_condition(self, value: str):
        return self.__conditions_dict[value]
    
    """
    Создает и инициализирует DTO из словаря с данными.

    Ожидаемый словарь:
    {
        "filter_name": "название_поля",
        "value": "значение", 
        "condition": "тип_условия"
    }
    """
    @staticmethod
    def create(data) -> "filter_dto":
        validator.validate(data, dict)
        item = filter_dto()
        item.field_name = data.get("filter_name", "")
        item.value = data.get("value")
        op = data.get("type") or data.get("condition")
        if op:
            item.condition = op
        return item