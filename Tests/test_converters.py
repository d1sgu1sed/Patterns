import os
import unittest
from datetime import datetime
from Src.Converters.basic_converter import basic_converter
from Src.Converters.datetime_converter import datetime_converter
from Src.Converters.reference_converter import reference_converter
from Src.Core.abstract import abstract
from Src.Core.abstract_dto import abstract_dto
from Src.Core.common import common
from Src.Core.validator import argument_exception
from Src.Models.ingredient_model import ingredient_model
from Src.Models.recipe_step_model import recipe_step_model
from Src.Converters.convert_factory import convert_factory


class Test_convert_factory(unittest.TestCase):
    """
    Тесты для проверки работы фабрики конвертеров и методов конвертации
    """

    """
    Тест проверки конвертации базовых типов
    """
    def test_basic_types_conversion(self):
        # Подготовка
        factory = convert_factory()
        
        # Действие и Проверка
        # Строка
        result = factory.convert("test_string")
        assert result == "test_string"
        
        # Целое число
        result = factory.convert(123)
        assert result == 123
        
        # Дробное число
        result = factory.convert(45.67)
        assert result == 45.67
        
        # None
        result = factory.convert(None)
        assert result is None

    """
    Тест проверки конвертации даты и времени
    """
    def test_datetime_conversion(self):
        # Подготовка
        factory = convert_factory()
        test_date = datetime(2023, 12, 25, 14, 30, 45)
        expected_format = "2023-12-25 14:30:45"
        
        # Действие
        result = factory.convert(test_date)
        
        # Проверка
        assert result == expected_format
        assert isinstance(result, str)

    """
    Тест проверки конвертации списков
    """
    def test_list_conversion(self):
        # Подготовка
        factory = convert_factory()
        test_list = ["item1", 123, 45.67, datetime(2023, 1, 1, 10, 0, 0)]
        
        # Действие
        result = factory.convert(test_list)
        
        # Проверка
        assert isinstance(result, list)
        assert len(result) == 4
        assert result[0] == "item1"
        assert result[1] == 123
        assert result[2] == 45.67
        assert result[3] == "2023-01-01 10:00:00"

    """
    Тест проверки конвертации словарей
    """
    def test_dict_conversion(self):
        # Подготовка
        factory = convert_factory()
        test_dict = {
            "string_key": "string_value",
            "int_key": 123,
            "float_key": 45.67,
            "date_key": datetime(2023, 1, 1, 10, 0, 0)
        }
        
        # Действие
        result = factory.convert(test_dict)
        
        # Проверка
        assert isinstance(result, dict)
        assert result["string_key"] == "string_value"
        assert result["int_key"] == 123
        assert result["float_key"] == 45.67
        assert result["date_key"] == "2023-01-01 10:00:00"

    """
    Тест проверки обработки ошибок для неподдерживаемых типов
    """
    def test_unsupported_type_error(self):
        # Подготовка
        factory = convert_factory()
        
        # Создаем класс, который не наследуется от поддерживаемых базовых классов
        class UnsupportedClass:
            def __init__(self):
                self.data = "test"
        
        unsupported_obj = UnsupportedClass()
        
        # Действие и Проверка
        try:
            factory.convert(unsupported_obj)
            self.fail("Ожидалось исключение argument_exception")
        except argument_exception as e:
            assert "Нет конвертера для данного класса" in str(e)

    """
    Тест проверки прямого использования basic_converter
    """
    def test_direct_basic_converter(self):
        # Подготовка
        test_data = "direct_test"
        
        # Действие
        result = basic_converter.convert(test_data)
        
        # Проверка
        assert result == test_data
        
        # Проверяем с числами
        assert basic_converter.convert(123) == 123
        assert basic_converter.convert(45.67) == 45.67

    """
    Тест проверки прямого использования datetime_converter
    """
    def test_direct_datetime_converter(self):
        # Подготовка
        test_date = datetime(2023, 10, 5, 15, 45, 30)
        expected_format = "2023-10-05 15:45:30"
        
        # Действие
        result = datetime_converter.convert(test_date)
        
        # Проверка
        assert result == expected_format
        assert isinstance(result, str)

if __name__ == '__main__':
    unittest.main()