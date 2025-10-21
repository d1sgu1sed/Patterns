import unittest
from Src.Models.model_data_route import model_data_route
from Src.reposity import reposity
from flask import jsonify

class Test_model_data_route(unittest.TestCase):
    """
    Проверка получения сырых данных модели
    Должен вернуть корректные данные для существующего типа модели
    """
    def test_get_raw_model_data_success(self):
        # подготовка
        test_data = {
            reposity.nomenclature_key(): ['nomenclature1', 'nomenclature2'],
            reposity.recipes_key(): ['recipe1', 'recipe2', 'recipe3'],
            reposity.measure_key(): ['measure1']
        }
        model_type = 'nomenclature'
        
        # действие
        result = model_data_route.get_raw_model_data(model_type, test_data)
        
        # проверка
        assert result == ['nomenclature1', 'nomenclature2']
        assert len(result) == 2

    """
    Проверка получения сырых данных модели
    Должен вернуть пустой список для существующего типа с отсутствующими данными
    """
    def test_get_raw_model_data_empty(self):
        # подготовка
        test_data = {
            reposity.nomenclature_key(): ['nomenclature1'],
            reposity.recipes_key(): []  # пустой список рецептов
        }
        model_type = 'recipe'
        
        # действие
        result = model_data_route.get_raw_model_data(model_type, test_data)
        
        # проверка
        assert result == []
        assert len(result) == 0


    """
    Проверка всех поддерживаемых типов моделей
    Должен корректно обрабатывать все зарегистрированные типы
    """
    def test_all_supported_model_types(self):
        # подготовка
        test_data = {
            reposity.nomenclature_key(): ['nomenclature_data'],
            reposity.groups_key(): ['group_data'],
            reposity.ingredients_key(): ['ingredient_data'],
            reposity.measure_key(): ['measure_data'],
            reposity.recipes_key(): ['recipe_data'],
            reposity.recipies_steps_key(): ['step_data']
        }
        
        supported_types = ['nomenclature', 'nomenclature_group', 'ingredient', 'measure', 'recipe', 'recipe_step']
        
        for model_type in supported_types:
            with self.subTest(model_type=model_type):
                # действие
                result = model_data_route.get_raw_model_data(model_type, test_data)
                
                # проверка
                assert result is not None
                assert len(result) == 1

if __name__ == '__main__':
    unittest.main()