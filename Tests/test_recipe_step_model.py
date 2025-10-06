import unittest
from Src.Models.recipe_step_model import empty_description_exception, formatting_error, non_equal_params, recipe_step_model
from Src.start_service import start_service
from Src.reposity import reposity

class Test_recipe_step_model(unittest.TestCase):
    """
    Проверка создания шага рецепта
    """
    def test_create_receipt_step(self):
        # подготовка
        receipt_step = recipe_step_model("l")
        
        # действие

        # проверка
        assert receipt_step.name == ""
        assert receipt_step.description == "l"
        assert receipt_step.params == None
    
    """
    Проверка функции форматирования
    """
    def test_formatting(self):
        # подготовка
        receipt_step = recipe_step_model("Добавьте {vanilin_name} {vanilin_n} {vanilin_measure}.")
        params_dict = {
            'vanilin_name' : 'ванилин',
            'vanilin_n': '50',
            'vanilin_measure': 'грамм'
        }
        format_str: str

        # действие
        receipt_step.params = params_dict
        format_str = receipt_step.formatting()

        # проверка
        assert receipt_step.description == "Добавьте {vanilin_name} {vanilin_n} {vanilin_measure}."
        assert receipt_step.params == params_dict
        assert format_str == "Добавьте ванилин 50 грамм."
    
    """
    Проверка исключений функции форматирования
    """
    def test_exception_formatting(self):
        # подготовка
        receipt_step_mismatch = recipe_step_model("Добавьте {ingredient} {amount}.")
        receipt_step_invalid = recipe_step_model("Добавьте {0} {1} {2}.")
        
        params_list_three = ["мука", "200", "грамм"]
        params_list_two = ["мука", "200"]
        params_dict_invalid = {'wrong_key': 'value', 'wrong_key2': 'value'}

        # действие/проверка
        receipt_step_mismatch.params = params_list_three
        try:
            receipt_step_mismatch.formatting()
            assert False
        except non_equal_params:
            assert True

        receipt_step_invalid.params = params_list_two
        try:
            receipt_step_invalid.formatting()
            assert False
        except non_equal_params:
            assert True 

        receipt_step_mismatch.params = params_dict_invalid
        try:
            receipt_step_mismatch.formatting()
            assert False
        except formatting_error:
            assert True 
    
if __name__ == 'name':
    unittest.main()
