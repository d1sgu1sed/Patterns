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


    """
    Тест проверки корректности генерации ОСВ с приходными операциями
    """
    def test_generate_osv_with_income_transactions(self):
        # Подготовка
        start_date = datetime(2023, 1, 1, 0, 0, 0)
        finish_date = datetime(2023, 1, 31, 23, 59, 59)
        storage = storage_model.create("Склад 1")
        osv = osv_model.create(start_date, finish_date, storage)
        
        # Создаем номенклатуру и транзакции
        group = nomenclature_group_model("Продукты")
        measure = measure_model.create("кг")
        nomenclature = nomenclature_model.create("Мука", group, measure)
        
        # Приходные транзакции
        transactions = [
            transaction_model.create(datetime(2023, 1, 10, 10, 0, 0), nomenclature, storage, 100, measure),
            transaction_model.create(datetime(2023, 1, 15, 14, 0, 0), nomenclature, storage, 50, measure)
        ]
        
        # Действие
        osv.generate_units(transactions, [nomenclature])
        
        # Проверка
        assert len(osv.units) == 1
        unit = osv.units[0]
        assert unit.nomenclature == nomenclature
        assert unit.add == 150  # 100 + 50
        assert unit.sub == 0
        assert unit.start_amount == 0
        assert unit.finish_amount == 150

    """
    Тест проверки корректности генерации ОСВ с расходными операциями
    """
    def test_generate_osv_with_outcome_transactions(self):
        # Подготовка
        start_date = datetime(2023, 1, 1, 0, 0, 0)
        finish_date = datetime(2023, 1, 31, 23, 59, 59)
        storage = storage_model.create("Склад 1")
        osv = osv_model.create(start_date, finish_date, storage)
        
        # Создаем номенклатуру и транзакции
        group = nomenclature_group_model("Продукты")
        measure = measure_model.create("шт")
        nomenclature = nomenclature_model.create("Хлеб", group, measure)
        
        # Расходные транзакции
        transactions = [
            transaction_model.create(datetime(2023, 1, 5, 9, 0, 0), nomenclature, storage, -30, measure),
            transaction_model.create(datetime(2023, 1, 20, 16, 0, 0), nomenclature, storage, -20, measure)
        ]
        
        # Действие
        osv.generate_units(transactions, [nomenclature])
        
        # Проверка
        assert len(osv.units) == 1
        unit = osv.units[0]
        assert unit.nomenclature == nomenclature
        assert unit.add == 0
        assert unit.sub == 50  # 30 + 20
        assert unit.start_amount == 0
        assert unit.finish_amount == -50

    """
    Тест проверки корректности генерации ОСВ со смешанными операциями
    """
    def test_generate_osv_with_mixed_transactions(self):
        # Подготовка
        start_date = datetime(2023, 1, 1, 0, 0, 0)
        finish_date = datetime(2023, 1, 31, 23, 59, 59)
        storage = storage_model.create("Склад 1")
        osv = osv_model.create(start_date, finish_date, storage)
        
        # Создаем номенклатуру
        group = nomenclature_group_model("Продукты")
        measure = measure_model.create("л")
        nomenclature = nomenclature_model.create("Молоко", group, measure)
        
        # Смешанные транзакции
        transactions = [
            transaction_model.create(datetime(2023, 1, 10, 10, 0, 0), nomenclature, storage, 200, measure),  # Приход
            transaction_model.create(datetime(2023, 1, 15, 14, 0, 0), nomenclature, storage, -80, measure),   # Расход
            transaction_model.create(datetime(2023, 1, 20, 11, 0, 0), nomenclature, storage, 100, measure),  # Приход
            transaction_model.create(datetime(2023, 1, 25, 16, 0, 0), nomenclature, storage, -50, measure)    # Расход
        ]
        
        # Действие
        osv.generate_units(transactions, [nomenclature])
        
        # Проверка
        assert len(osv.units) == 1
        unit = osv.units[0]
        assert unit.nomenclature == nomenclature
        assert unit.add == 300  # 200 + 100
        assert unit.sub == 130  # 80 + 50
        assert unit.start_amount == 0
        assert unit.finish_amount == 170  # 300 - 130

    """
    Тест проверки генерации ОСВ для нескольких номенклатур
    """
    def test_generate_osv_with_multiple_nomenclatures(self):
        # Подготовка
        start_date = datetime(2023, 1, 1, 0, 0, 0)
        finish_date = datetime(2023, 1, 31, 23, 59, 59)
        storage = storage_model.create("Склад 1")
        osv = osv_model.create(start_date, finish_date, storage)
        
        # Создаем несколько номенклатур
        group = nomenclature_group_model("Продукты")
        measure_kg = measure_model.create("кг")
        measure_lt = measure_model.create("л")
        
        flour = nomenclature_model.create("Мука", group, measure_kg)
        milk = nomenclature_model.create("Молоко", group, measure_lt)
        
        # Транзакции для разных номенклатур
        transactions = [
            transaction_model.create(datetime(2023, 1, 10, 10, 0, 0), flour, storage, 100, measure_kg),
            transaction_model.create(datetime(2023, 1, 15, 14, 0, 0), milk, storage, 50, measure_lt),
            transaction_model.create(datetime(2023, 1, 20, 11, 0, 0), flour, storage, 30, measure_kg),
        ]
        
        # Действие
        osv.generate_units(transactions, [flour, milk])
        
        # Проверка
        assert len(osv.units) == 2
        
        # Проверяем муку
        flour_unit = osv.find_unit(flour)
        assert flour_unit.add == 130  # 100 + 30
        assert flour_unit.sub == 0
        assert flour_unit.finish_amount == 130
        
        # Проверяем молоко
        milk_unit = osv.find_unit(milk)
        assert milk_unit.add == 50
        assert milk_unit.sub == 0
        assert milk_unit.finish_amount == 50

    """
    Тест проверки фильтрации транзакций по дате и складу
    """
    def test_generate_osv_with_filtered_transactions(self):
        # Подготовка
        start_date = datetime(2023, 1, 10, 0, 0, 0)
        finish_date = datetime(2023, 1, 20, 23, 59, 59)
        storage1 = storage_model.create("Склад 1")
        storage2 = storage_model.create("Склад 2")
        osv = osv_model.create(start_date, finish_date, storage1)
        
        # Создаем номенклатуру
        group = nomenclature_group_model("Продукты")
        measure = measure_model.create("кг")
        nomenclature = nomenclature_model.create("Мука", group, measure)
        
        # Транзакции разных периодов и складов
        transactions = [
            # Транзакции до периода (должны игнорироваться)
            transaction_model.create(datetime(2023, 1, 5, 10, 0, 0), nomenclature, storage1, 50, measure),
            # Транзакции в периоде на нужном складе
            transaction_model.create(datetime(2023, 1, 15, 10, 0, 0), nomenclature, storage1, 100, measure),
            # Транзакции на другом складе (должны игнорироваться)
            transaction_model.create(datetime(2023, 1, 15, 14, 0, 0), nomenclature, storage2, 200, measure),
            # Транзакции после периода (должны игнорироваться)
            transaction_model.create(datetime(2023, 1, 25, 10, 0, 0), nomenclature, storage1, 150, measure),
        ]
        
        # Действие
        osv.generate_units(transactions, [nomenclature])
        
        # Проверка - должна учитываться только одна транзакция
        assert len(osv.units) == 1
        unit = osv.units[0]
        assert unit.add == 100
        assert unit.sub == 0
        assert unit.finish_amount == 150


if __name__ == '__main__':
    unittest.main()