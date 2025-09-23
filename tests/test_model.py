import os
from src.models.CompanyModel import CompanyModel
from src.models.Settings import Settings
from src.SettingsManager import SettingsManager
import unittest
import json

class TestCompanyModel(unittest.TestCase):
    """
    Проверка создания основной модели
    Данные после создания должны быть пустыми
    """
    def test_createmodel_company_model(self):
        # подготовка
        model = CompanyModel()
        
        # действие

        # проверка
        assert model.name == ""


    """
    Проверка создания основной модели
    Данные после создания должны быть не пустыми
    """
    def test_createmodel_company_model_notEmpty(self):
        # подготовка
        model = CompanyModel()
        
        # действие
        model.name = 'test'
        
        # проверка
        assert model.name != ""
    

    def test_load_createmodel_companymodel(self):
        # подготовка
        filename = '/home/ivan/Рабочий стол/Patterns/settings.json'
        load_config = SettingsManager(filename)

        # действие
        result = load_config.load()

        # проверка
        assert result
        assert load_config.settings.model.name != ''
    
    def test_class_equals(self):
        # подготовка
        filename = '/home/ivan/Рабочий стол/Patterns/settings.json'
        load_config1 = SettingsManager(filename)
        load_config2 = SettingsManager(filename)

        # действие
        load_config1.load()
        load_config2.load()

        # проверка
        assert load_config1.settings == load_config2.settings
        assert load_config1.settings.model == load_config2.settings.model
    
    def test_loading_dict_settings(self):
        # подготовка
        filename = '/home/ivan/Рабочий стол/Patterns/settings.json'
        load_config: SettingsManager = SettingsManager(filename)
        settings: Settings

        # действие
        load_result = load_config.load()
        settings = load_config.settings
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
            assert raw_data[key] == getattr(settings.model, key)
    
    def test_loading_dict_settings_from_uncommon_config(self):
        # подготовка
        filename = os.path.join('tests', 'config.json')
        load_config: SettingsManager = SettingsManager(filename)
        settings: Settings

        # действие
        assert load_config.load()
        settings = load_config.settings
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
            assert raw_data[key] == getattr(settings.model, key)
    


if __name__ == 'name':
    unittest.main()