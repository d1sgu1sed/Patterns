import unittest
from Src.Core.validator import argument_exception
from Dtos.filter_dto import filter_dto


class Test_filter_dto(unittest.TestCase):
    """
    Тесты для проверки работы DTO фильтра
    """

    """
    Тест проверки создания DTO фильтра фабричным методом
    """
    def test_create_filter_dto_success(self):
        # Подготовка
        data = {
            "filter_name": "name",
            "value": "test_value",
            "condition": "EQUALS"
        }
        
        # Действие
        dto = filter_dto.create(data)
        
        # Проверка
        assert dto.field_name == "name"
        assert dto.value == "test_value"
        assert dto.condition == "EQUALS"

    """
    Тест проверки создания DTO фильтра с псевдонимом type
    """
    def test_create_filter_dto_with_type_alias(self):
        # Подготовка
        data = {
            "filter_name": "measure.name",
            "value": "кг",
            "type": "LIKE"
        }
        
        # Действие
        dto = filter_dto.create(data)
        
        # Проверка
        assert dto.field_name == "measure.name"
        assert dto.value == "кг"
        assert dto.condition == "LIKE"

    """
    Тест проверки создания DTO фильтра без условия
    """
    def test_create_filter_dto_without_condition(self):
        # Подготовка
        data = {
            "filter_name": "name",
            "value": "test"
        }
        
        # Действие
        dto = filter_dto.create(data)
        
        # Проверка
        assert dto.field_name == "name"
        assert dto.value == "test"
        assert dto.condition == ""

    """
    Тест проверки валидации названия поля
    """
    def test_field_name_validation_error(self):
        # Подготовка
        dto = filter_dto()
        
        # Действие и Проверка
        try:
            dto.field_name = 123
            self.fail("Ожидалось исключение argument_exception")
        except argument_exception as e:
            assert "Некорректный тип!" in str(e)

    """
    Тест проверки валидации условия фильтра
    """
    def test_condition_validation_error(self):
        # Подготовка
        dto = filter_dto()
        
        # Действие и Проверка
        try:
            dto.condition = "INVALID_CONDITION"
            self.fail("Ожидалось исключение argument_exception")
        except argument_exception as e:
            assert "Такого модификатора условия нет!" in str(e)

    """
    Тест проверки получения функций условий
    """
    def test_get_condition_functions(self):
        # Подготовка
        dto = filter_dto()
        
        # Действие
        equals_func = dto.get_condition("EQUALS")
        like_func = dto.get_condition("LIKE")
        more_func = dto.get_condition("MORE")
        
        # Проверка
        assert equals_func("test", "test") == True
        assert equals_func("test", "different") == False
        assert like_func("hello world", "world") == True
        assert like_func("hello world", "test") == False
        assert more_func(10, 5) == True
        assert more_func(5, 10) == False

    """
    Тест проверки условия диапазона
    """
    def test_in_range_condition(self):
        # Подготовка
        dto = filter_dto()
        
        # Действие
        range_func = dto.get_condition("IN RANGE")
        
        # Проверка
        assert range_func(5, (1, 10)) == True
        assert range_func(15, (1, 10)) == False
        assert range_func(1, (1, 10)) == False


if __name__ == '__main__':
    unittest.main()