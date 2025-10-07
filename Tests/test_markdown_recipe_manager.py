import os
import unittest
from Src.Models.recipe_model import recipe_model
from Src.Models.recipe_step_model import recipe_step_model
from Src.markdown_recipe_manager import markdown_recipe_manager
from Src.reposity import reposity
from Src.start_service import start_service

class Test_markdown_recipe_manager(unittest.TestCase):
    __start_service = start_service()

    def __init__(self, methodName = "runTest"):
        super().__init__(methodName)
        self.__start_service.start()
    
    """
    Проверка работы генерации markdown
    """
    def test_generate_markdown(self):
        # подготовка
        recipe = self.__start_service.reposity.data[reposity.recipies_key]['Вафли']
        expected_filename = "Docs/waffles.md"
        manager = markdown_recipe_manager.create(expected_filename, recipe)
        
        # удаляем файл если он существует
        if os.path.exists(expected_filename):
            os.unlink(expected_filename)
        
        try:
            # действие
            md_content = manager.generate_markdown()
            
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

    """
    Проверка создания менеджера через фабричный метод
    """
    def test_create_factory_method(self):
        # подготовка
        recipe = self.__start_service.reposity.data[reposity.recipies_key]['Вафли']
        filename = "test_factory.md"
        manager1 = markdown_recipe_manager.create(filename, recipe)
        manager2 = markdown_recipe_manager.create(filename, recipe)
        # действие
        
        # проверка
        assert len(markdown_recipe_manager._instances) == 1
        assert filename in markdown_recipe_manager._instances
        assert manager1 is manager2
    
    """
    Проверка обработки ошибок форматирования
    """
    def test_formatting_errors(self):
        # подготовка
        recipe = recipe_model()
        recipe.name = "Рецепт с ошибками"
        
        # Шаг с несовпадающим количеством параметров
        error_step = recipe_step_model()
        error_step.description = "Шаг с {0} плейсхолдером"
        error_step.params = []
        
        recipe.steps = [error_step]
        recipe.ingredients = []
        
        filename = "test_errors.md"
        manager = markdown_recipe_manager(filename, recipe)
        
        try:
            # действие
            md_content = manager.generate_markdown()
            
            # проверка
            assert "[Ошибка форматирования шага:" in md_content
            
        finally:
            if os.path.exists(filename):
                os.unlink(filename)