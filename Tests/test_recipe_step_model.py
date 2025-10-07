import unittest
from Src.Models.recipe_step_model import recipe_step_model

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
    
if __name__ == 'name':
    unittest.main()
