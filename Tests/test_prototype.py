from Dtos.filter_dto import filter_dto
from Src.Logics.prototype_osv import prototype_osv
import unittest
from datetime import datetime
from Src.reposity import reposity
from Src.start_service import start_service

class Test_prototype(unittest.TestCase):
    __start_service = start_service()
    
    def test_prototype_filter(self):
        # подготовка
        data = self.__start_service.reposity.data
        prototype_transaction = prototype_osv(data[reposity.transaction_key()])
        filter_nomenclature = data[reposity.nomenclature_key()][0]
        
        # действие
        test_prototype = prototype_transaction.filter_by_nomenclature(prototype_transaction, filter_nomenclature)
        
        # проверка
        assert len(test_prototype.data) > 0
        assert len(prototype_transaction.data) > 0
        assert len(prototype_transaction.data) >= len(test_prototype.data)

    """
    Тест проверки фильтрации по единице измерения
    """
    def test_prototype_filter_by_measure(self):
        # подготовка
        data = self.__start_service.reposity.data
        prototype_transaction = prototype_osv(data[reposity.transaction_key()])
        filter_measure = data[reposity.measure_key()][0]
        
        # действие
        test_prototype = prototype_osv.filter_by_measure(prototype_transaction, filter_measure)
        
        # проверка
        assert len(test_prototype.data) > 0
        assert len(prototype_transaction.data) >= len(test_prototype.data)
        for item in test_prototype.data:
            assert item.measure == filter_measure

    """
    Тест проверки фильтрации по складу
    """
    def test_prototype_filter_by_storage(self):
        # подготовка
        data = self.__start_service.reposity.data
        prototype_transaction = prototype_osv(data[reposity.transaction_key()])
        filter_storage = data[reposity.storage_key()][0]
        
        # действие
        test_prototype = prototype_osv.filter_by_storage(prototype_transaction, filter_storage)
        
        # проверка
        assert len(test_prototype.data) > 0
        assert len(prototype_transaction.data) >= len(test_prototype.data)
        for item in test_prototype.data:
            assert item.storage == filter_storage

    """
    Тест проверки цепочки фильтров
    """
    def test_prototype_filter_chain(self):
        # подготовка
        data = self.__start_service.reposity.data
        prototype_transaction = prototype_osv(data[reposity.transaction_key()])
        filter_nomenclature = data[reposity.nomenclature_key()][0]
        filter_measure = data[reposity.measure_key()][0]
        
        # действие - цепочка фильтров
        filtered_by_nomenclature = prototype_osv.filter_by_nomenclature(prototype_transaction, filter_nomenclature)
        filtered_by_measure = prototype_osv.filter_by_measure(filtered_by_nomenclature, filter_measure)
        
        # проверка
        assert len(filtered_by_measure.data) > 0
        assert len(filtered_by_nomenclature.data) >= len(filtered_by_measure.data)
        for item in filtered_by_measure.data:
            assert item.product == filter_nomenclature
            assert item.measure == filter_measure

    """
    Тест проверки фильтрации с условием MORE через DTO
    """
    def test_filter_dto_more_condition(self):
        # подготовка
        data = self.__start_service.reposity.data
        prototype_transaction = prototype_osv(data[reposity.transaction_key()])
        
        dto = filter_dto()
        dto.field_name = "amount"
        dto.value = 10  # Фильтруем транзакции с количеством больше 10
        dto.condition = "MORE"
        
        # действие
        test_prototype = prototype_osv.filter(prototype_transaction, dto)
        
        # проверка
        if len(test_prototype.data) > 0:
            for item in test_prototype.data:
                assert item.amount > dto.value

    """
    Тест проверки фильтрации с условием LESS через DTO
    """
    def test_filter_dto_less_condition(self):
        # подготовка
        data = self.__start_service.reposity.data
        prototype_transaction = prototype_osv(data[reposity.transaction_key()])
        
        dto = filter_dto()
        dto.field_name = "amount"
        dto.value = 100  # Фильтруем транзакции с количеством меньше 100
        dto.condition = "LESS"
        
        # действие
        test_prototype = prototype_osv.filter(prototype_transaction, dto)
        
        # проверка
        if len(test_prototype.data) > 0:
            for item in test_prototype.data:
                assert item.amount < dto.value

    """
    Тест проверки фильтрации по вложенным полям через DTO
    """
    def test_filter_dto_nested_fields(self):
        # подготовка
        data = self.__start_service.reposity.data
        prototype_transaction = prototype_osv(data[reposity.transaction_key()])
        measure = data[reposity.measure_key()][0]
        
        dto = filter_dto()
        dto.field_name = "measure.name"
        dto.value = measure.name
        dto.condition = "EQUALS"
        
        # действие
        test_prototype = prototype_osv.filter(prototype_transaction, dto)
        
        # проверка
        assert len(test_prototype.data) > 0
        for item in test_prototype.data:
            assert item.measure.name == measure.name
            
    """
    Тест проверки сохранения исходных данных при фильтрации
    """
    def test_prototype_original_data_preservation(self):
        # подготовка
        data = self.__start_service.reposity.data
        original_transactions = data[reposity.transaction_key()]
        prototype_transaction = prototype_osv(original_transactions)
        original_count = len(prototype_transaction.data)
        
        filter_nomenclature = data[reposity.nomenclature_key()][0]
        
        # действие
        filtered_prototype = prototype_osv.filter_by_nomenclature(prototype_transaction, filter_nomenclature)
        
        # проверка - исходные данные не должны измениться
        assert len(prototype_transaction.data) == original_count
        assert len(filtered_prototype.data) <= original_count
        assert len(original_transactions) == original_count

    def test_prototype_filters(self):
        # подготовка
        data = self.__start_service.reposity.data
        prototype_transaction = prototype_osv(data[reposity.transaction_key()])
        filter_nomenclature = data[reposity.nomenclature_key()][0]
        filter_measure = data[reposity.measure_key()][0]
        test_prototype1 = prototype_transaction.filter_by_nomenclature(prototype_transaction, filter_nomenclature)
        
        # действие
        test_prototype2 = test_prototype1.filter_by_measure(test_prototype1, filter_measure)
        
        # проверка
        assert len(test_prototype2.data) > 0
        assert len(test_prototype1.data) > 0
        assert len(test_prototype1.data) >= len(test_prototype2.data)
    
    def test_filter_dto(self):
        # подготовка
        data = self.__start_service.reposity.data
        prototype_transaction = prototype_osv(data[reposity.transaction_key()])
        filter_nomenclature = data[reposity.nomenclature_key()][0]
        dto = filter_dto()
        dto.field_name = "name"
        dto.value = filter_nomenclature.name
        dto.condition = "EQUALS"
        
        # действие
        test_prototype = prototype_transaction.filter(prototype_transaction, dto)
        
        # проверка
        assert len(test_prototype.data) == 2
        assert len(prototype_transaction.data) >= len(test_prototype.data)
    

if __name__ == '__main__':
    unittest.main()