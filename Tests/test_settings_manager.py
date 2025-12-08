import os
from Src.Models.settings_model import settings_model
from Src.settings_manager import settings_manager
import unittest

class Test_settings_manager(unittest.TestCase):
    """
    Проверка загрузки данных в менеджер настроек
    Они должны быть не пустыми
    """
    def test_load(self):
        # подготовка
        filename = '/home/ivan/Desktop/Patterns/settings.json'
        load_config = settings_manager(filename)

        # действие
        result = load_config.load()

        # проверка
        assert result
        assert load_config.settings.company.name != ''
    
    """
    Проверка загрузки данных в 2 менеджера настроек
    Они должны равными
    """
    def test_class_equals(self):
        # подготовка
        filename = '/home/ivan/Desktop/Patterns/settings.json'
        load_config1 = settings_manager(filename)
        load_config2 = settings_manager(filename)

        # действие
        load_config1.load()
        load_config2.load()

        # проверка
        for key in settings_model().company_attrs():
            assert getattr(load_config2.settings.company, key) == getattr(load_config1.settings.company, key)
    
    """
    Проверка загрузки данных в менеджер настроек из файла по абс. пути
    Они должны быть равными шаблону raw_data 
    """
    def test_loading_dict_settings(self):
        # подготовка
        filename = '/home/ivan/Desktop/Patterns/settings.json'
        load_config: settings_manager = settings_manager(filename)
        sett: settings_model

        # действие
        load_result = load_config.load()
        sett = load_config.settings
        raw_data = {
            "name": "Рога и копыта",
            "INN": 129741029322,
            "account": 12309184024,
            "correspondent_acc": 93029318292,
            "BIK": 129031229,
            "type_of_property": "33333"
        }

        # проверка
        assert load_result
        for key in raw_data.keys():
            assert raw_data[key] == getattr(sett.company, key)
    
    """
    Проверка загрузки данных в менеджер настроек из файла по отн. пути 
    Они должны равными
    """
    def test_loading_dict_settings_from_uncommon_config(self):
        # подготовка
        filename = os.path.join('Tests', 'config.json')
        load_config: settings_manager = settings_manager(filename)
        sett: settings_model

        # действие
        assert load_config.load()
        sett = load_config.settings
        raw_data = {
            "name": "ООО не приходите",
            "INN": 129741029388,
            "account": 12309184028,
            "correspondent_acc": 93029318288,
            "BIK": 129031289,
            "type_of_property": "99999"
        }
        
        # проверка
        for key in raw_data.keys():
            assert raw_data[key] == getattr(sett.company, key)


if __name__ == 'name':
    unittest.main()