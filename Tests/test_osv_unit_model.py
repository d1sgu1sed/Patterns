import os
import unittest
from datetime import datetime
from Src.Core.validator import argument_exception, operation_exception
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.osv_unit_model import osv_unit_model
from Src.Models.measure_model import measure_model
from Src.Models.nomenclature_group_model import nomenclature_group_model
from Dtos.osv_unit_dto import osv_unit_dto


class Test_osv_unit_model(unittest.TestCase):
    """
    Тесты для проверки работы модели элемента ОСВ
    """

    """
    Тест проверки создания модели элемента ОСВ фабричным методом
    """
    def test_create_osv_unit_model(self):
        # Подготовка
        group = nomenclature_group_model("Тестовая группа")
        measure = measure_model.create("кг")
        nomenclature = nomenclature_model.create("Тестовая номенклатура", group, measure)
        start_amount = 100.0
        finish_amount = 150.0
        add = 80.0
        sub = 30.0
        
        # Действие
        unit = osv_unit_model.create(nomenclature, measure, start_amount, finish_amount, add, sub)
        
        # Проверка
        assert unit.nomenclature == nomenclature
        assert unit.measure == measure
        assert unit.start_amount == start_amount
        assert unit.finish_amount == finish_amount
        assert unit.add == add
        assert unit.sub == sub

    """
    Тест проверки создания дефолтной модели элемента ОСВ
    """
    def test_create_default_osv_unit_model(self):
        # Подготовка
        group = nomenclature_group_model("Тестовая группа")
        measure = measure_model.create("шт")
        nomenclature = nomenclature_model.create("Тестовая номенклатура", group, measure)
        
        # Действие
        unit = osv_unit_model.create_default("",nomenclature, measure)
        
        # Проверка
        assert unit.nomenclature == nomenclature
        assert unit.measure == measure
        assert unit.start_amount == 0.0
        assert unit.finish_amount == 0.0
        assert unit.add == 0.0
        assert unit.sub == 0.0

    """
    Тест проверки сеттеров модели элемента ОСВ
    """
    def test_osv_unit_model_setters(self):
        # Подготовка
        unit = osv_unit_model()
        group = nomenclature_group_model("Тестовая группа")
        measure = measure_model.create("л")
        nomenclature = nomenclature_model.create("Тестовая номенклатура", group, measure)
        
        # Действие
        unit.nomenclature = nomenclature
        unit.measure = measure
        unit.start_amount = 50.0
        unit.finish_amount = 70.0
        unit.add = 25.0
        unit.sub = 5.0
        
        # Проверка
        assert unit.nomenclature == nomenclature
        assert unit.measure == measure
        assert unit.start_amount == 50.0
        assert unit.finish_amount == 70.0
        assert unit.add == 25.0
        assert unit.sub == 5.0

    """
    Тест проверки конвертации в DTO
    """
    def test_to_dto_conversion(self):
        # Подготовка
        group = nomenclature_group_model("Тестовая группа")
        measure = measure_model.create("кг")
        nomenclature = nomenclature_model.create("Мука", group, measure)
        unit = osv_unit_model.create(nomenclature, measure, 100.0, 120.0, 30.0, 10.0)
        
        # Действие
        dto = unit.to_dto()
        
        # Проверка
        assert dto.id == unit.unique_code
        assert dto.nomenclature_id == nomenclature.unique_code
        assert dto.measure_id == measure.unique_code
        assert dto.start_amount == 100.0
        assert dto.finish_amount == 120.0
        assert dto.add == 30.0
        assert dto.sub == 10.0

    """
    Тест проверки создания из DTO
    """
    def test_from_dto_conversion(self):
        # Подготовка
        group = nomenclature_group_model("Тестовая группа")
        measure = measure_model.create("гр")
        nomenclature = nomenclature_model.create("Соль", group, measure)
        
        # Создаем DTO
        dto = osv_unit_dto()
        dto.id = "test_id_123"
        dto.name = "Тестовый элемент ОСВ"
        dto.start_amount = 200.0
        dto.finish_amount = 180.0
        dto.add = 50.0
        dto.sub = 70.0
        
        # Создаем кэш с объектами
        cache = {
            nomenclature.unique_code: nomenclature,
            measure.unique_code: measure
        }
        
        # Устанавливаем ID в DTO для поиска в кэше
        dto.nomenclature_id = nomenclature.unique_code
        dto.measure_id = measure.unique_code
        
        # Действие
        unit = osv_unit_model.from_dto(dto, cache)
        
        # Проверка
        assert unit.unique_code == "test_id_123"
        assert unit.name == "Тестовый элемент ОСВ"
        assert unit.nomenclature == nomenclature
        assert unit.measure == measure
        assert unit.start_amount == 200.0
        assert unit.finish_amount == 180.0
        assert unit.add == 50.0
        assert unit.sub == 70.0

    """
    Тест проверки создания из DTO с отсутствующими объектами в кэше
    """
    def test_from_dto_with_missing_cache_objects(self):
        # Подготовка
        dto = osv_unit_dto()
        dto.id = "test_id_456"
        dto.name = "Элемент с отсутствующими объектами"
        dto.nomenclature_id = "non_existent_nomenclature_id"
        dto.measure_id = "non_existent_measure_id"
        dto.start_amount = 100.0
        dto.finish_amount = 100.0
        dto.add = 0.0
        dto.sub = 0.0
        
        cache = {}  # Пустой кэш
        
        # Действие
        unit = osv_unit_model.from_dto(dto, cache)
        
        # Проверка - объекты должны быть None
        assert unit.unique_code == "test_id_456"
        assert unit.name == "Элемент с отсутствующими объектами"
        assert unit.nomenclature is None
        assert unit.measure is None
        assert unit.start_amount == 100.0
        assert unit.finish_amount == 100.0
        assert unit.add == 0.0
        assert unit.sub == 0.0

    """
    Тест проверки работы с отрицательными значениями
    """
    def test_negative_values(self):
        # Подготовка
        group = nomenclature_group_model("Тестовая группа")
        measure = measure_model.create("шт")
        nomenclature = nomenclature_model.create("Тестовый продукт", group, measure)
        
        # Действие
        unit = osv_unit_model.create(nomenclature, measure, -50.0, -30.0, -20.0, -40.0)
        
        # Проверка
        assert unit.start_amount == -50.0
        assert unit.finish_amount == -30.0
        assert unit.add == -20.0
        assert unit.sub == -40.0

    """
    Тест проверки работы с нулевыми значениями
    """
    def test_zero_values(self):
        # Подготовка
        group = nomenclature_group_model("Тестовая группа")
        measure = measure_model.create("мл")
        nomenclature = nomenclature_model.create("Тестовый продукт", group, measure)
        
        # Действие
        unit = osv_unit_model.create(nomenclature, measure, 0.0, 0.0, 0.0, 0.0)
        
        # Проверка
        assert unit.start_amount == 0.0
        assert unit.finish_amount == 0.0
        assert unit.add == 0.0
        assert unit.sub == 0.0

    """
    Тест проверки работы с дробными значениями
    """
    def test_fractional_values(self):
        # Подготовка
        group = nomenclature_group_model("Тестовая группа")
        measure = measure_model.create("кг")
        nomenclature = nomenclature_model.create("Тестовый продукт", group, measure)
        
        # Действие
        unit = osv_unit_model.create(nomenclature, measure, 123.45, 678.90, 555.55, 0.05)
        
        # Проверка
        assert unit.start_amount == 123.45
        assert unit.finish_amount == 678.90
        assert unit.add == 555.55
        assert unit.sub == 0.05

    """
    Тест проверки изменения значений через сеттеры
    """
    def test_value_modification_through_setters(self):
        # Подготовка
        group = nomenclature_group_model("Тестовая группа")
        measure = measure_model.create("шт")
        nomenclature = nomenclature_model.create("Тестовый продукт", group, measure)
        unit = osv_unit_model.create_default("",nomenclature, measure)
        
        # Действие - последовательное изменение значений
        unit.start_amount = 100.0
        unit.add = 50.0
        unit.sub = 30.0
        unit.finish_amount = 120.0  # 100 + 50 - 30 = 120
        
        # Проверка
        assert unit.start_amount == 100.0
        assert unit.add == 50.0
        assert unit.sub == 30.0
        assert unit.finish_amount == 120.0


if __name__ == '__main__':
    unittest.main()