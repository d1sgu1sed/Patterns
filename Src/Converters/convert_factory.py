from datetime import date, datetime
from Src.Converters.basic_converter import basic_converter
from Src.Converters.datetime_converter import datetime_converter
from Src.Converters.reference_converter import reference_converter
from Src.Core.abstract import abstract
from Src.Core.abstract_dto import abstract_dto
from Src.Core.common import common
from Src.Core.validator import argument_exception
from Src.Models.ingredient_model import ingredient_model
from Src.Models.recipe_step_model import recipe_step_model
from typing import Any


class convert_factory:
    """
    Класс-фабрика для конвертации объектов в словарь
    """    

    __converters={
        str:basic_converter,
        int:basic_converter,
        float:basic_converter,
        date:datetime_converter,
        abstract:reference_converter,
        abstract_dto:basic_converter,
        object:basic_converter
    }

    """
    Функция конвертации объекта в словарь
    """
    def convert(self, obj: Any):
        # Базовые типы и None
        if type(obj) in [str, int, float] or obj is None:
            return self.__converters[type(obj).__bases__[0]].convert(obj)
        
        # Дата
        if isinstance(obj, date):
            return self.__converters[type(obj).__bases__[0]].convert(obj)

        # Списки
        if isinstance(obj, list):
            return [self.convert(item) for item in obj]
        
        # Словари
        if isinstance(obj, dict):
            return {key: self.convert(value) for key, value in obj.items()}
        
        # Объекты с конвертерами
        try:
            cls_name = type(obj).__bases__[0]
            convert_obj = self.__converters[cls_name].convert(obj)
            fields = common.get_fields(convert_obj)
            return {key: self.convert(getattr(convert_obj, key)) for key in fields}
        except Exception as e:
            message = str(e)
            raise argument_exception("Нет конвертера для данного класса")