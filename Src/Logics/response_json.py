from Src.Core.abstract_response import abstract_response
from Src.Core.validator import validator
from Src.Models.recipe_model import recipe_model
from Src.Models.recipe_step_model import recipe_step_model
import json

"""
Исключение при сериализации в JSON
"""  
class json_serialization_error(Exception):
    pass


class response_json(abstract_response):
    """
    Генератор рецепта в формате JSON

    Поля:
        filename (str): Название файла для загрузки конфига.
        recipe(recipe_model): Модель рецепта.
    """

    __filename: str
    __recipe: recipe_model

    def __init__(self, filename: str, recipe: recipe_model):
        validator.validate(filename, str)
        validator.validate(recipe, recipe_model)
        self.__filename = filename
        self.__recipe = recipe

    """
    Название файла
    """
    @property
    def filename(self):
        return self.__filename
    
    """
    Модель рецепта
    """
    @property
    def recipe(self):
        return self.__recipe

    @filename.setter
    def filename(self, value: str):
        validator.validate(value, str)
        self.__filename = value
    
    @recipe.setter
    def recipe(self, value: recipe_model):
        validator.validate(value, recipe_model)
        self.__recipe = value
    
    """
    Фабричный метод создания
    """
    @staticmethod
    def create(filename: str, recipe: recipe_model):
        validator.validate(filename, str)
        validator.validate(recipe, recipe_model)
        item = response_json(filename, recipe)
        return item
    
    """
    Форматирует шаги в требуемый формат
    """
    def __format_steps(self) -> list:
        if not self.__recipe.steps:
            return []
        
        formatted_steps = []
        for step in self.__recipe.steps:
            if step.params:
                # Шаг с параметрами - представляем как массив [описание, параметры]
                step_entry = [
                    step.description,
                    step.params if isinstance(step.params, dict) else dict(enumerate(step.params))
                ]
            else:
                # Шаг без параметров - просто строка с описанием
                step_entry = step.description
            
            formatted_steps.append(step_entry)
        
        return formatted_steps

    """
    Форматирует ингредиенты в требуемый формат
    """
    def __format_ingredients(self) -> list:
        if not self.__recipe.ingredients:
            return []
        
        formatted_ingredients = []
        for ingredient in self.__recipe.ingredients:
            ingredient_dict = {
                "nomenclature": ingredient.product.unique_code,  # предполагая, что id есть у продукта
                "measure": ingredient.product.measure.unique_code,  # предполагая, что id есть у меры
                "value": ingredient.amount
            }
            formatted_ingredients.append(ingredient_dict)
        
        return formatted_ingredients

    """
    Преобразует модель рецепта в словарь для сериализации в JSON
    """
    def __recipe_to_dict(self) -> dict:
        try:
            recipe_dict = {
                "name": self.__recipe.name,
                "remark": self.__recipe.remark,
                "ingredients": self.__format_ingredients(),
                "steps": self.__format_steps()
            }
            
            return recipe_dict
            
        except Exception as e:
            raise json_serialization_error(f"Ошибка при преобразовании рецепта в словарь: {e}")

    """
    Генерирует JSON строку и записывает в файл
    """
    def generate(self):
        try:
            # Преобразуем рецепт в словарь
            recipe_dict = self.__recipe_to_dict()
            
            # Сериализуем в JSON с красивым форматированием
            json_content = json.dumps(recipe_dict, ensure_ascii=False, indent=2)
            
            # Записываем в файл
            with open(self.__filename, 'w', encoding='utf-8') as f:
                f.write(json_content)
            
            return json_content
            
        except Exception as e:
            raise json_serialization_error(f"Ошибка при генерации JSON: {e}")