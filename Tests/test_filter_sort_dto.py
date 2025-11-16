import unittest

from Dtos.filter_sort_dto import filter_sort_dto
from Src.Core.validator import argument_exception


class Test_filter_sort_dto(unittest.TestCase):
    """
    Тесты для проверки работы DTO фильтров и сортировок
    """

    """
    Тест проверки создания DTO фильтров и сортировок
    """
    def test_create_filter_sort_dto_success(self):
        # Подготовка
        data = {
            "filters": [
                {
                    "filter_name": "name",
                    "value": "Пшеничная мука",
                    "type": "LIKE"
                },
                {
                    "filter_name": "measure.name",
                    "value": "кг",
                    "type": "EQUALS"
                }
            ],
            "sorting": ["name", "measure.name"]
        }
        
        # Действие
        dto = filter_sort_dto.create(data)
        
        # Проверка
        assert len(dto.filters) == 2
        assert dto.filters[0].field_name == "name"
        assert dto.filters[0].value == "Пшеничная мука"
        assert dto.filters[0].condition == "LIKE"
        assert dto.filters[1].field_name == "measure.name"
        assert dto.filters[1].value == "кг"
        assert dto.filters[1].condition == "EQUALS"
        assert dto.sorting == ["name", "measure.name"]

    """
    Тест проверки создания пустого DTO
    """
    def test_create_filter_sort_dto_empty(self):
        # Подготовка
        data = {}
        
        # Действие
        dto = filter_sort_dto.create(data)
        
        # Проверка
        assert len(dto.filters) == 0
        assert len(dto.sorting) == 0

    """
    Тест проверки создания DTO только с фильтрами
    """
    def test_create_filter_sort_dto_only_filters(self):
        # Подготовка
        data = {
            "filters": [
                {
                    "filter_name": "date",
                    "value": "2023-01-01",
                    "condition": "MORE"
                }
            ]
        }
        
        # Действие
        dto = filter_sort_dto.create(data)
        
        # Проверка
        assert len(dto.filters) == 1
        assert len(dto.sorting) == 0

    """
    Тест проверки создания DTO только с сортировками
    """
    def test_create_filter_sort_dto_only_sorting(self):
        # Подготовка
        data = {
            "sorting": ["date", "product.name"]
        }
        
        # Действие
        dto = filter_sort_dto.create(data)
        
        # Проверка
        assert len(dto.filters) == 0
        assert dto.sorting == ["date", "product.name"]

    """
    Тест проверки валидации списка фильтров
    """
    def test_filters_setter_validation(self):
        # Подготовка
        dto = filter_sort_dto()
        
        # Действие и Проверка
        try:
            dto.filters = "not_a_list"
            self.fail("Ожидалось исключение argument_exception")
        except argument_exception as e:
            assert "Некорректный тип!" in str(e)

    """
    Тест проверки валидации списка сортировок
    """
    def test_sorting_setter_validation(self):
        # Подготовка
        dto = filter_sort_dto()
        
        # Действие и Проверка
        try:
            dto.sorting = "not_a_list"
            self.fail("Ожидалось исключение argument_exception")
        except argument_exception as e:
            assert "Некорректный тип!" in str(e)
