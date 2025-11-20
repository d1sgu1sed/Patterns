import abc
from Dtos.filter_dto import filter_dto
from Src.Core.common import common
from Src.Core.validator import argument_exception, validator

"""
Абстрактный класс прототипа для работы с коллекциями данных.
Реализует паттерн Прототип и предоставляет методы для фильтрации данных.
"""
class prototype(abc.ABC):
    __data = []

    def __init__(self, data: list):
        validator.validate(data, list)
        self.__data = data
    
    """
    Данные, над которыми будет проводиться фильтрация
    """
    @property
    def data(self):
        return self.__data
    
    """
    Абстрактный метод клонирования прототипа.
    """
    @abc.abstractmethod
    def clone(self, data: list = None):
        inner_data = data
        if inner_data is None:
            inner_data = self.__data
        instance = prototype(inner_data)
        return instance

    """
    Получает значение из объекта по цепочке полей (включая вложенные).
    """
    def get_value_from_field(value, field: str):
        compl_fields = field.split(".")
        for field in compl_fields:
            # Берём внутренние поля объекта
            fields_in = common.get_fields(value)
            if field in fields_in:
                # Берём значение у поля объетка
                value = getattr(value, field)
            else:
                raise argument_exception(f"Неверное поле {field} в объекте {value}!")
        return value

    """
    Статический метод для фильтрации данных в прототипе по заданному фильтру.
    """
    @staticmethod
    def filter(proto: 'prototype', filter: filter_dto) -> 'prototype':
        data = proto.data
        if len(data) == 0:
            return proto.clone(data)
        result = []
        for item in data:
            # Берём значение из обычного/составного поля
            value = prototype.get_value_from_field(item, filter.field_name)
            # Получаем функцию условия ("LIKE", "EQUALS" и т.д.) и проверяем значение
            # Первый аргумент — значение поля, второй — значение фильтра
            condition_fn = filter.get_condition(filter.condition)
            if condition_fn(value, filter.value):
                result.append(item)
        return proto.clone(result)