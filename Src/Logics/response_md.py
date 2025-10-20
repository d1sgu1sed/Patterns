from Src.Core.abstract_response import abstract_response
from Src.Core.common import common
import re
from Src.Core.validator import validator
from Src.Models.recipe_model import recipe_model
from Src.Models.recipe_step_model import recipe_step_model

"""
Исключение при форматировании пустой строки
"""  
class empty_description_exception(Exception):
    pass

"""
Исключение при неравном количестве 
плейсхолдеров и параметров шага
"""  
class non_equal_params(Exception):
    pass

"""
Исключение при форматировании
"""  
class formatting_error(Exception):
    pass


class response_md(abstract_response):
    """
    Генератор рецепта в формате Markdown

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
        item = response_md(filename, recipe)

        return item
    
    """
    Форматирует строку description, подставляя параметры из params
    в плейсхолдеры в фигурных скобках.
    
    Проверяет соответствие количества плейсхолдеров и длины списка параметров.
    В дальнейшем можно добавить функционал для преобразования в различные форматы
    """
    def __formatting(self, step: recipe_step_model) -> str:  
        if not step.description:
            raise empty_description_exception("Пустое описание")
        
        if step.params is None:
            step.params = []
        
        placeholders = re.findall(r'\{([^}]+)\}', step.description)
        
        if len(placeholders) != len(step.params):
            raise non_equal_params(
                f"Количество плейсхолдеров {len(placeholders)} не соответствует количеству параметров {len(step.params)}"
            )
        
        try:
            if isinstance(step.params, dict):
                # Для dict-параметров
                formatted_description = step.description.format(**step.params)
            else:
                # Для list-параметров
                formatted_description = step.description.format(*step.params)
            return formatted_description
        except:
            raise formatting_error(
                f"Ошибка при форматировании строки. Плейсхолдеры: {placeholders}, Параметры: {step.params}"
            )

    """
    Форматирует таблицу ингредиентов
    """
    def __format_ingredients_table(self) -> str:
        if not self.__recipe.ingredients:
            return ""
        
        table = "| Ингредиенты | Количество |\n"
        table += "|-------------|------------|\n"
        
        for ingredient in self.__recipe.ingredients:
            name = ingredient.product.name
            quantity = f"{ingredient.amount} {ingredient.measure.name}"
            table += f"| {name} | {quantity} |\n"
        
        table += "\n"
        return table

    """
    Форматирует шаги приготовления
    """
    def __format_steps(self) -> str:
        if not self.__recipe.steps:
            return ""
        
        steps_text = ""
        for i, step in enumerate(self.__recipe.steps, 1):
            try:
                formatted_step = self.__formatting(step)
                steps_text += f"{i}. {formatted_step}\n"
            except Exception as e:
                steps_text += f"{i}. [Ошибка форматирования шага: {e}]\n"
        
        return steps_text

    """
    Форматирует рецепт в Markdown строку и записывает в файл
    """
    def generate(self):
        # Формируем заголовок
        md_content = f"# {self.__recipe.name.upper()}\n\n"
        
        # Таблица ингредиентов
        md_content += self.__format_ingredients_table()
        
        # Добавляем ремарку после таблицы
        if self.__recipe.remark:
            md_content += f"{self.recipe.remark}\n\n"
        
        md_content += "## ПОШАГОВОЕ ПРИГОТОВЛЕНИЕ\n\n"
        
        # Шаги приготовления
        md_content += self.__format_steps()
        
        with open(self.__filename, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        return md_content
    
