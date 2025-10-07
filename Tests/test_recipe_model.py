import os
from Src.Models.recipe_model import recipe_model
from Src.start_service import start_service
from Src.reposity import reposity
import unittest

from Src.Models.recipe_step_model import recipe_step_model

class Test_recipe_model(unittest.TestCase):
    __start_service = start_service()

    def __init__(self, methodName = "runTest"):
        super().__init__(methodName)
        self.__start_service.start()
        
    """
    Проверка создания рецепта
    """
    def test_create_recipe(self):
        # подготовка
        recipe = recipe_model()
        
        # действие
        
        # проверка
        assert recipe.name == ''
    
    """
    Проверка работы фабричного метода на примере создания рецепта вафель
    """
    def test_fabric_method(self):
        # подготовка
        recipe = self.__start_service.reposity.data[reposity.recipies_key]['Вафли']
        steps = self.__start_service.reposity.data[reposity.recipies_steps_key]['Вафли']
        
        # действие

        # проверка
        assert recipe.name == 'Вафли хрустящие в вафельнице'
        for i in range(len(recipe.steps)):
            assert recipe.steps[i].description == steps[i].description

        
if __name__ == 'name':
    unittest.main()