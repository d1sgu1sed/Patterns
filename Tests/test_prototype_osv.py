from datetime import datetime
import unittest

from Dtos.filter_dto import filter_dto
from Src.Logics.prototype_osv import prototype_osv
from Src.Models.measure_model import measure_model
from Src.Models.nomenclature_group_model import nomenclature_group_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.storage_model import storage_model
from Src.Models.transaction_model import transaction_model


class Test_prototype_osv(unittest.TestCase):
    """
    Тесты для проверки работы прототипа ОСВ
    """

    """
    Тест проверки фильтрации по номенклатуре
    """
    def test_filter_by_nomenclature(self):
        # Подготовка
        group = nomenclature_group_model("Продукты")
        measure = measure_model.create("кг")
        nomenclature = nomenclature_model.create("Мука", group, measure)
        storage = storage_model.create("Склад 1")
        
        transactions = [
            transaction_model.create(datetime(2023, 1, 10, 10, 0, 0), nomenclature, storage, 100, measure),
            transaction_model.create(datetime(2023, 1, 15, 14, 0, 0), nomenclature, storage, 50, measure),
        ]
        proto = prototype_osv(transactions)
        
        # Действие
        filtered_proto = prototype_osv.filter_by_nomenclature(proto, nomenclature)
        
        # Проверка
        assert len(filtered_proto.data) == 2
        for item in filtered_proto.data:
            assert item.product == nomenclature

    """
    Тест проверки фильтрации по единице измерения
    """
    def test_filter_by_measure(self):
        # Подготовка
        group = nomenclature_group_model("Продукты")
        measure_kg = measure_model.create("кг")
        measure_lt = measure_model.create("л")
        nomenclature = nomenclature_model.create("Мука", group, measure_kg)
        storage = storage_model.create("Склад 1")
        
        transactions = [
            transaction_model.create(datetime(2023, 1, 10, 10, 0, 0), nomenclature, storage, 100, measure_kg),
            transaction_model.create(datetime(2023, 1, 15, 14, 0, 0), nomenclature, storage, 50, measure_kg),
        ]
        proto = prototype_osv(transactions)
        
        # Действие
        filtered_proto = prototype_osv.filter_by_measure(proto, measure_kg)
        
        # Проверка
        assert len(filtered_proto.data) == 2
        for item in filtered_proto.data:
            assert item.measure == measure_kg

    """
    Тест проверки фильтрации по диапазону дат
    """
    def test_filter_by_date_in_range(self):
        # Подготовка
        group = nomenclature_group_model("Продукты")
        measure = measure_model.create("кг")
        nomenclature = nomenclature_model.create("Мука", group, measure)
        storage = storage_model.create("Склад 1")
        
        transactions = [
            transaction_model.create(datetime(2023, 1, 10, 10, 0, 0), nomenclature, storage, 100, measure),
            transaction_model.create(datetime(2023, 1, 20, 14, 0, 0), nomenclature, storage, 50, measure),
            transaction_model.create(datetime(2023, 2, 5, 9, 0, 0), nomenclature, storage, 75, measure),
        ]
        proto = prototype_osv(transactions)
        start_date = datetime(2023, 1, 12, 0, 0, 0)
        end_date = datetime(2023, 2, 1, 0, 0, 0)
        
        # Действие
        filtered_proto = prototype_osv.filter_by_date_in_range(proto, start_date, end_date)
        
        # Проверка
        assert len(filtered_proto.data) == 1
        for item in filtered_proto.data:
            assert start_date < item.date < end_date

    """
    Тест проверки фильтрации по складу
    """
    def test_filter_by_storage(self):
        # Подготовка
        group = nomenclature_group_model("Продукты")
        measure = measure_model.create("кг")
        nomenclature = nomenclature_model.create("Мука", group, measure)
        storage1 = storage_model.create("Склад 1")
        storage2 = storage_model.create("Склад 2")
        
        transactions = [
            transaction_model.create(datetime(2023, 1, 10, 10, 0, 0), nomenclature, storage1, 100, measure),
            transaction_model.create(datetime(2023, 1, 15, 14, 0, 0), nomenclature, storage2, 50, measure),
        ]
        proto = prototype_osv(transactions)
        
        # Действие
        filtered_proto = prototype_osv.filter_by_storage(proto, storage1)
        
        # Проверка
        assert len(filtered_proto.data) == 1
        for item in filtered_proto.data:
            assert item.storage == storage1

    """
    Тест проверки универсальной фильтрации
    """
    def test_universal_filter(self):
        # Подготовка
        group = nomenclature_group_model("Продукты")
        measure = measure_model.create("кг")
        nomenclature = nomenclature_model.create("Мука", group, measure)
        storage = storage_model.create("Склад 1")
        
        transactions = [
            transaction_model.create(datetime(2023, 1, 10, 10, 0, 0), nomenclature, storage, 100, measure),
            transaction_model.create(datetime(2023, 1, 15, 14, 0, 0), nomenclature, storage, 50, measure),
        ]
        proto = prototype_osv(transactions)
        
        filter_obj = filter_dto()
        filter_obj.field_name = "amount"
        filter_obj.value = 75
        filter_obj.condition = "MORE"
        
        # Действие
        filtered_proto = prototype_osv.filter(proto, filter_obj)
        
        # Проверка
        assert len(filtered_proto.data) == 1
        assert filtered_proto.data[0].amount == 100


if __name__ == '__main__':
    unittest.main()