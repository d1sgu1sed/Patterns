import unittest
import os
import json
from datetime import datetime
from Src.start_service import start_service
from Src.reposity import reposity
from Src.Models.osv_model import osv_model
from Src.Models.storage_model import storage_model


class Test_start_service(unittest.TestCase):
    __start_service = start_service()

    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        if self.__start_service.reposity.data[reposity.recipes_key()] == []:
            self.__start_service.start()

    """
    Проверка создания данных при помощи сервиса
    """
    def test_start_service_measure_not_empty(self):
        # подготовка
        data = self.__start_service.reposity.data

        # действие

        # проверка
        assert len(data[reposity.measure_key()]) != 0
        assert data[reposity.groups_key()][0] is not None

    """
    Проверка равенства созданных базовых единиц
    """
    def test_equal_instances(self):
        # подготовка
        data = self.__start_service.reposity.data
        
        # действие

        # проверка
        assert data[reposity.measure_key()][0] == data[reposity.measure_key()][2].base_measure

    """
    Тест проверки создания ОСВ
    """
    def test_create_osv(self):
        # подготовка
        start_date = datetime(2023, 1, 1, 0, 0, 0)
        end_date = datetime(2023, 12, 31, 23, 59, 59)
        
        # Получаем первый склад из репозитория
        storages = self.__start_service.reposity.data[reposity.storage_key()]
        assert len(storages) > 0, "Нет складов в репозитории"
        storage = storages[0]
        
        # действие
        osv = self.__start_service.create_osv(start_date, end_date, storage.unique_code)
        
        # проверка
        assert isinstance(osv, osv_model)
        assert osv.start_date == start_date
        assert osv.finish_date == end_date
        assert osv.storage == storage
        assert isinstance(osv.units, list)

    """
    Тест проверки создания ОСВ с несуществующим складом
    """
    def test_create_osv_with_invalid_storage(self):
        # подготовка
        start_date = datetime(2023, 1, 1, 0, 0, 0)
        end_date = datetime(2023, 12, 31, 23, 59, 59)
        invalid_storage_id = "non_existent_storage_id"
        
        # действие и проверка
        try:
            self.__start_service.create_osv(start_date, end_date, invalid_storage_id)
            self.fail("Ожидалось исключение argument_exception")
        except Exception as e:
            # Может быть argument_exception или другое исключение из validator
            assert "Пустой аргумент" in str(e) or "None" in str(e)

    """
    Тест проверки создания ОСВ с правильными датами
    """
    def test_create_osv_date_validation(self):
        # подготовка
        end_date = datetime(2023, 12, 31, 23, 59, 59)
        start_date = datetime(2023, 1, 1, 0, 0, 0)  # start_date раньше end_date
        
        storages = self.__start_service.reposity.data[reposity.storage_key()]
        storage = storages[0]
        
        # действие
        osv = self.__start_service.create_osv(start_date, end_date, storage.unique_code)
        
        # проверка
        assert osv.start_date == start_date
        assert osv.finish_date == end_date
        assert osv.start_date < osv.finish_date

    """
    Тест проверки дампа данных в файл
    """
    def test_dump_data_to_file(self):
        # подготовка
        test_filename = "test_dump.json"
        
        # Убедимся, что файл не существует перед тестом
        if os.path.exists(test_filename):
            os.remove(test_filename)
        
        # действие
        result = self.__start_service.dump(test_filename)
        
        # проверка
        assert result == True
        assert os.path.exists(test_filename)
        
        # Проверяем содержимое файла
        with open(test_filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
            assert isinstance(data, dict)
            # Проверяем, что все ключи репозитория присутствуют
            for key in reposity().keys:
                assert key in data
                assert isinstance(data[key], list)
        
        # Очистка
        if os.path.exists(test_filename):
            os.remove(test_filename)

    """
    Тест проверки дампа с невалидным именем файла
    """
    def test_dump_with_invalid_filename(self):
        # подготовка
        invalid_filename = ""
        
        # действие и проверка
        try:
            result = self.__start_service.dump(invalid_filename)
            self.fail("Ожидалось исключение argument_exception")
        except Exception as e:
            assert "Пустой аргумент" in str(e)

    """
    Тест проверки корректности данных после дампа
    """
    def test_dump_data_correctness(self):
        # подготовка
        test_filename = "test_dump_correctness.json"
        
        # действие
        result = self.__start_service.dump(test_filename)
        
        # проверка
        assert result == True
        
        # Загружаем данные из файла и проверяем структуру
        with open(test_filename, 'r', encoding='utf-8') as file:
            dumped_data = json.load(file)
            
            # Проверяем основные ключи
            expected_keys = reposity().keys
            for key in expected_keys:
                assert key in dumped_data
                assert isinstance(dumped_data[key], list)
            
            # Проверяем, что данные не пустые
            assert len(dumped_data[reposity.measure_key()]) > 0
            assert len(dumped_data[reposity.nomenclature_key()]) > 0
            assert len(dumped_data[reposity.storage_key()]) > 0
        
        # Очистка
        if os.path.exists(test_filename):
            os.remove(test_filename)

    """
    Тест проверки создания ОСВ с транзакциями
    """
    def test_create_osv_with_transactions(self):
        # подготовка
        start_date = datetime(2023, 1, 1, 0, 0, 0)
        end_date = datetime(2023, 12, 31, 23, 59, 59)
        
        storages = self.__start_service.reposity.data[reposity.storage_key()]
        storage = storages[0]
        
        # действие
        osv = self.__start_service.create_osv(start_date, end_date, storage.unique_code)
        
        # проверка
        assert len(osv.units) > 0  # Должны быть созданы элементы ОСВ
        
        # Проверяем структуру элементов ОСВ
        for unit in osv.units:
            assert hasattr(unit, 'nomenclature')
            assert hasattr(unit, 'measure')
            assert hasattr(unit, 'start_amount')
            assert hasattr(unit, 'finish_amount')
            assert hasattr(unit, 'add')
            assert hasattr(unit, 'sub')

    """
    Тест проверки интеграции создания ОСВ и дампа
    """
    def test_osv_and_dump_integration(self):
        # подготовка
        start_date = datetime(2023, 1, 1, 0, 0, 0)
        end_date = datetime(2023, 12, 31, 23, 59, 59)
        test_filename = "test_integration.json"
        
        storages = self.__start_service.reposity.data[reposity.storage_key()]
        storage = storages[0]
        
        # действие - создаем ОСВ и делаем дамп
        osv = self.__start_service.create_osv(start_date, end_date, storage.unique_code)
        dump_result = self.__start_service.dump(test_filename)
        
        # проверка
        assert isinstance(osv, osv_model)
        assert dump_result == True
        assert os.path.exists(test_filename)
        
        # Очистка
        if os.path.exists(test_filename):
            os.remove(test_filename)


if __name__ == '__main__':
    unittest.main()