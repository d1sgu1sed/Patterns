import os
import unittest
from datetime import datetime
from Src.Core.validator import argument_exception, operation_exception
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.osv_unit_model import osv_unit_model
from Src.Models.storage_model import storage_model
from Src.Models.transaction_model import transaction_model
from Src.Models.measure_model import measure_model
from Src.Models.osv_model import osv_model
from Src.Models.nomenclature_group_model import nomenclature_group_model


class Test_osv_model(unittest.TestCase):
    """
    Тесты для проверки работы модели ОСВ (оборотно-сальдовой ведомости)
    """

    """
    Тест проверки создания модели ОСВ фабричным методом
    """
    def test_create_osv_model(self):
        # Подготовка
        start_date = datetime(2023, 1, 1, 0, 0, 0)
        finish_date = datetime(2023, 1, 31, 23, 59, 59)
        storage = storage_model.create("Склад 1")
        
        # Действие
        osv = osv_model.create(start_date, finish_date, storage)
        
        # Проверка
        assert osv.start_date == start_date
        assert osv.finish_date == finish_date
        assert osv.storage == storage
        assert osv.units == []

    """
    Тест проверки сеттеров с валидацией
    """
    def test_setters_validation(self):
        # Подготовка
        osv = osv_model()
        test_date = datetime(2023, 1, 1, 0, 0, 0)
        test_storage = storage_model.create("Склад 1")
        
        # Создаем необходимые объекты для osv_unit_model
        group = nomenclature_group_model("Тестовая группа")
        measure = measure_model.create("кг")
        nomenclature = nomenclature_model.create("Тестовая номенклатура", group, measure)
        test_units = [osv_unit_model.create_default("",nomenclature, measure)]
        
        # Действие
        osv.start_date = test_date
        osv.finish_date = test_date
        osv.storage = test_storage
        osv.units = test_units
        
        # Проверка
        assert osv.start_date == test_date
        assert osv.finish_date == test_date
        assert osv.storage == test_storage
        assert osv.units == test_units

    """
    Тест проверки ошибок валидации в сеттерах
    """
    def test_setters_validation_errors(self):
        # Подготовка
        osv = osv_model()
        
        # Действие и Проверка - неверный тип для даты
        try:
            osv.start_date = "invalid_date"
            self.fail("Ожидалось исключение argument_exception")
        except argument_exception as e:
            assert "Некорректный тип!" in str(e)
        
        # Действие и Проверка - неверный тип для склада
        try:
            osv.storage = "invalid_storage"
            self.fail("Ожидалось исключение argument_exception")
        except argument_exception as e:
            assert "Некорректный тип!" in str(e)
        
        # Действие и Проверка - неверный тип для units
        try:
            osv.units = "invalid_units"
            self.fail("Ожидалось исключение argument_exception")
        except argument_exception as e:
            assert "Некорректный тип!" in str(e)

    """
    Тест проверки конвертации в DTO
    """
    def test_to_dto_conversion(self):
        # Подготовка
        start_date = datetime(2023, 1, 1, 0, 0, 0)
        finish_date = datetime(2023, 1, 31, 23, 59, 59)
        storage = storage_model.create("Склад 1")
        osv = osv_model.create(start_date, finish_date, storage)
        
        # Действие
        dto = osv.to_dto()
        
        # Проверка
        assert dto.start_date == start_date
        assert dto.finish_date == finish_date
        assert dto.storage_id == storage.unique_code
        assert dto.units == []
        assert dto.id == osv.unique_code

    """
    Тест проверки поиска элемента ОСВ по номенклатуре
    """
    def test_find_unit_by_nomenclature(self):
        # Подготовка
        osv = osv_model()
        group = nomenclature_group_model("Тестовая группа")
        measure = measure_model.create("кг")
        nomenclature = nomenclature_model.create("Тестовая номенклатура", group, measure)
        unit = osv_unit_model.create_default("",nomenclature, measure)
        osv.units = [unit]
        
        # Действие
        found_unit = osv.find_unit(nomenclature)
        
        # Проверка
        assert found_unit == unit

    """
    Тест проверки ошибки при поиске несуществующей номенклатуры
    """
    def test_find_unit_not_found_error(self):
        # Подготовка
        osv = osv_model()
        group = nomenclature_group_model("Тестовая группа")
        measure = measure_model.create("кг")
        existing_nomenclature = nomenclature_model.create("Существующая", group, measure)
        non_existing_nomenclature = nomenclature_model.create("Несуществующая", group, measure)
        unit = osv_unit_model.create_default("",existing_nomenclature, measure)
        osv.units = [unit]
        
        # Действие и Проверка
        try:
            osv.find_unit(non_existing_nomenclature)
            self.fail("Ожидалось исключение operation_exception")
        except operation_exception as e:
            assert "Элемент ОСВ не найден" in str(e)

    """
    Тест проверки работы с пустыми данными
    """
    def test_empty_data_handling(self):
        # Подготовка
        osv = osv_model()
        
        # Действие - генерация с пустыми списками
        osv.generate_units([], [])
        
        # Проверка
        assert osv.units == []


if __name__ == '__main__':
    unittest.main()