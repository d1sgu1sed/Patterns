import os
import unittest
from datetime import datetime
from Src.Core.validator import argument_exception, operation_exception
from Src.Models.transaction_model import transaction_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.storage_model import storage_model
from Src.Models.measure_model import measure_model
from Src.Models.nomenclature_group_model import nomenclature_group_model
from Dtos.transaction_dto import transaction_dto


class Test_transaction_model(unittest.TestCase):
    """
    Тесты для проверки работы модели транзакции
    """

    """
    Тест проверки создания модели транзакции фабричным методом
    """
    def test_create_transaction_model(self):
        # Подготовка
        test_date = datetime(2023, 12, 15, 14, 30, 0)
        group = nomenclature_group_model("Бакалея")
        measure = measure_model.create("кг")
        product = nomenclature_model.create("Мука", group, measure)
        storage = storage_model.create("Основной склад")
        amount = 150.5
        
        # Действие
        transaction = transaction_model.create(test_date, product, storage, amount, measure)
        
        # Проверка
        assert transaction.date == test_date
        assert transaction.product == product
        assert transaction.storage == storage
        assert transaction.amount == amount
        assert transaction.measure == measure

    """
    Тест проверки сеттеров модели транзакции
    """
    def test_transaction_model_setters(self):
        # Подготовка
        transaction = transaction_model()
        test_date = datetime(2023, 11, 20, 10, 0, 0)
        group = nomenclature_group_model("Напитки")
        measure = measure_model.create("л")
        product = nomenclature_model.create("Вода", group, measure)
        storage = storage_model.create("Склад напитков")
        amount = 75.25
        
        # Действие
        transaction.date = test_date
        transaction.product = product
        transaction.storage = storage
        transaction.amount = amount
        transaction.measure = measure
        
        # Проверка
        assert transaction.date == test_date
        assert transaction.product == product
        assert transaction.storage == storage
        assert transaction.amount == amount
        assert transaction.measure == measure

    """
    Тест проверки конвертации в DTO
    """
    def test_to_dto_conversion(self):
        # Подготовка
        test_date = datetime(2023, 10, 5, 9, 15, 30)
        group = nomenclature_group_model("Молочные продукты")
        measure = measure_model.create("шт")
        product = nomenclature_model.create("Молоко", group, measure)
        storage = storage_model.create("Холодильный склад")
        amount = 25.0
        
        transaction = transaction_model.create(test_date, product, storage, amount, measure)
        
        # Действие
        dto = transaction.to_dto()
        
        # Проверка
        assert dto.id == transaction.unique_code
        assert dto.nomenclature_id == product.unique_code
        assert dto.measure_id == measure.unique_code
        assert dto.storage_id == storage.unique_code
        assert dto.date == test_date
        assert dto.amount == amount

    """
    Тест проверки создания из DTO
    """
    def test_from_dto_conversion(self):
        # Подготовка
        test_date = datetime(2023, 9, 12, 16, 45, 0)
        group = nomenclature_group_model("Овощи")
        measure = measure_model.create("кг")
        product = nomenclature_model.create("Картофель", group, measure)
        storage = storage_model.create("Овощной склад")
        amount = 300.0
        
        # Создаем DTO
        dto = transaction_dto()
        dto.id = "test_transaction_id"
        dto.date = test_date
        dto.amount = amount
        
        # Создаем кэш с объектами
        cache = {
            product.unique_code: product,
            measure.unique_code: measure,
            storage.unique_code: storage
        }
        
        # Устанавливаем ID в DTO для поиска в кэше
        dto.nomenclature_id = product.unique_code
        dto.measure_id = measure.unique_code
        dto.storage_id = storage.unique_code
        
        # Действие
        transaction = transaction_model.from_dto(dto, cache)
        
        # Проверка
        assert transaction.unique_code == "test_transaction_id"
        assert transaction.date == test_date
        assert transaction.product == product
        assert transaction.storage == storage
        assert transaction.amount == amount
        assert transaction.measure == measure

    """
    Тест проверки создания из DTO с отсутствующими объектами в кэше
    """
    def test_from_dto_with_missing_cache_objects(self):
        # Подготовка
        dto = transaction_dto()
        dto.id = "test_missing_objects_id"
        dto.date = datetime(2023, 8, 1, 12, 0, 0)
        dto.amount = 100.0
        dto.nomenclature_id = "non_existent_nomenclature_id"
        dto.measure_id = "non_existent_measure_id"
        dto.storage_id = "non_existent_storage_id"
        
        cache = {}  # Пустой кэш
        
        # Действие
        transaction = transaction_model.from_dto(dto, cache)
        
        # Проверка - объекты должны быть None
        assert transaction.unique_code == "test_missing_objects_id"
        assert transaction.date == datetime(2023, 8, 1, 12, 0, 0)
        assert transaction.amount == 100.0
        assert transaction.product is None
        assert transaction.measure is None
        assert transaction.storage is None

    """
    Тест проверки работы с отрицательными значениями количества
    """
    def test_negative_amount(self):
        # Подготовка
        test_date = datetime(2023, 7, 25, 8, 0, 0)
        group = nomenclature_group_model("Мясо")
        measure = measure_model.create("кг")
        product = nomenclature_model.create("Говядина", group, measure)
        storage = storage_model.create("Мясной склад")
        amount = -50.0  # Отрицательное количество (расход)
        
        # Действие
        transaction = transaction_model.create(test_date, product, storage, amount, measure)
        
        # Проверка
        assert transaction.amount == -50.0

    """
    Тест проверки работы с нулевым количеством
    """
    def test_zero_amount(self):
        # Подготовка
        test_date = datetime(2023, 6, 10, 14, 0, 0)
        group = nomenclature_group_model("Фрукты")
        measure = measure_model.create("кг")
        product = nomenclature_model.create("Яблоки", group, measure)
        storage = storage_model.create("Фруктовый склад")
        amount = 0.0
        
        # Действие
        transaction = transaction_model.create(test_date, product, storage, amount, measure)
        
        # Проверка
        assert transaction.amount == 0.0

    """
    Тест проверки работы с дробными значениями количества
    """
    def test_fractional_amount(self):
        # Подготовка
        test_date = datetime(2023, 5, 15, 11, 30, 0)
        group = nomenclature_group_model("Специи")
        measure = measure_model.create("гр")
        product = nomenclature_model.create("Соль", group, measure)
        storage = storage_model.create("Склад специй")
        amount = 0.125  # Дробное значение
        
        # Действие
        transaction = transaction_model.create(test_date, product, storage, amount, measure)
        
        # Проверка
        assert transaction.amount == 0.125

    """
    Тест проверки последовательного изменения значений через сеттеры
    """
    def test_sequential_value_modification(self):
        # Подготовка
        transaction = transaction_model()
        initial_date = datetime(2023, 1, 1, 10, 0, 0)
        updated_date = datetime(2023, 1, 2, 15, 0, 0)
        
        group1 = nomenclature_group_model("Группа 1")
        group2 = nomenclature_group_model("Группа 2")
        measure1 = measure_model.create("шт")
        measure2 = measure_model.create("кг")
        product1 = nomenclature_model.create("Продукт 1", group1, measure1)
        product2 = nomenclature_model.create("Продукт 2", group2, measure2)
        storage1 = storage_model.create("Склад 1")
        storage2 = storage_model.create("Склад 2")
        
        # Действие - последовательное изменение всех свойств
        transaction.date = initial_date
        transaction.product = product1
        transaction.storage = storage1
        transaction.amount = 100.0
        transaction.measure = measure1
        
        # Изменение значений
        transaction.date = updated_date
        transaction.product = product2
        transaction.storage = storage2
        transaction.amount = 200.0
        transaction.measure = measure2
        
        # Проверка
        assert transaction.date == updated_date
        assert transaction.product == product2
        assert transaction.storage == storage2
        assert transaction.amount == 200.0
        assert transaction.measure == measure2

    """
    Тест проверки работы с разными типами единиц измерения
    """
    def test_different_measure_types(self):
        # Подготовка
        test_date = datetime(2023, 4, 20, 9, 0, 0)
        group = nomenclature_group_model("Разные единицы")
        
        # Тестируем разные единицы измерения
        measures = [
            measure_model.create("кг"),
            measure_model.create("л"),
            measure_model.create("шт"),
            measure_model.create("м"),
            measure_model.create("упаковка")
        ]
        
        for measure in measures:
            product = nomenclature_model.create(f"Продукт для {measure.name}", group, measure)
            storage = storage_model.create(f"Склад для {measure.name}")
            amount = 10.5
            
            # Действие
            transaction = transaction_model.create(test_date, product, storage, amount, measure)
            
            # Проверка
            assert transaction.measure == measure
            assert transaction.amount == amount
            assert transaction.product == product
            assert transaction.storage == storage


if __name__ == '__main__':
    unittest.main()