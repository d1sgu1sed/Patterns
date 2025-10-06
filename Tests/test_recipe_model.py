import os
from Src.Models.recipe_model import recipe_model
import unittest

from Src.Models.recipe_step_model import recipe_step_model

class Test_recipe_model(unittest.TestCase):
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
        recipe = recipe_model.create_waffles()
        steps = recipe_step_model.create_waffles_step_list()
        
        # действие

        # проверка
        assert recipe.name == 'Вафли хрустящие в вафельнице'
        for i in range(len(recipe.steps)):
            assert recipe.steps[i].description == steps[i].description
    
    """
    Проверка работы форматирования
    """
    def test_formatting(self):
        # подготовка
        recipe = recipe_model.create_waffles()
        expected_filename = "Docs/receipt.md"
        
        # удаляем файл если он существует
        if os.path.exists(expected_filename):
            os.unlink(expected_filename)
        
        try:
            # действие
            md_content = recipe.formatting()
            
            # проверка
            assert os.path.exists(expected_filename)
            
            # проверяем что содержимое корректное
            with open(expected_filename, 'r', encoding='utf-8') as f:
                file_content = f.read()
            
            assert md_content == file_content
            assert f"# {recipe.name.upper()}" in md_content
            
        except:
            # очистка
            if os.path.exists(expected_filename):
                os.unlink(expected_filename)

        
if __name__ == 'name':
    unittest.main()