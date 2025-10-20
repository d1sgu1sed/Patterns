import re
import io
import csv
from Src.Core.abstract_response import abstract_response
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


class response_csv(abstract_response):
    """
    Генератор рецепта в формате CSV

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
        item = response_csv(filename, recipe)
        return item
    
    """
    Форматирует строку description, подставляя параметры из params
    в плейсхолдеры в фигурных скобках.
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
    Форматирует таблицу ингредиентов для CSV
    """
    def __format_ingredients_table(self) -> list:
        if not self.__recipe.ingredients:
            return []
        
        ingredients_data = []
        # Заголовок таблицы ингредиентов
        ingredients_data.append(["Ингредиенты", "Количество"])
        
        for ingredient in self.__recipe.ingredients:
            name = ingredient.product.name
            quantity = f"{ingredient.amount} {ingredient.product.measure.name}"
            ingredients_data.append([name, quantity])
        
        return ingredients_data

    """
    Форматирует шаги приготовления для CSV
    """
    def __format_steps(self) -> list:
        if not self.__recipe.steps:
            return []
        
        steps_data = []
        # Заголовок таблицы шагов
        steps_data.append(["Шаг", "Описание"])
        
        for i, step in enumerate(self.__recipe.steps, 1):
            try:
                formatted_step = self.__formatting(step)
                steps_data.append([i, formatted_step])
            except Exception as e:
                steps_data.append([i, f"[Ошибка форматирования шага: {e}]"])
        
        return steps_data

    """
    Форматирует рецепт в CSV и записывает в файл
    """
    def generate(self) -> str:
        csv_content = []
        
        # Заголовок рецепта
        csv_content.append(["РЕЦЕПТ", self.__recipe.name.upper()])
        csv_content.append([])  # Пустая строка
        
        # Таблица ингредиентов
        ingredients_data = self.__format_ingredients_table()
        if ingredients_data:
            csv_content.append(["ИНГРЕДИЕНТЫ"])
            csv_content.extend(ingredients_data)
            csv_content.append([])  # Пустая строка
        
        # Ремарка
        if self.__recipe.remark:
            csv_content.append(["РЕМАРКА", self.__recipe.remark])
            csv_content.append([])  # Пустая строка
        
        # Шаги приготовления
        steps_data = self.__format_steps()
        if steps_data:
            csv_content.append(["ПОШАГОВОЕ ПРИГОТОВЛЕНИЕ"])
            csv_content.extend(steps_data)
        
        # Записываем в файл и одновременно формируем строку для возврата
        output = io.StringIO()
        writer = csv.writer(output, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        writer.writerows(csv_content)
        result_string = output.getvalue()
        
        # Записываем в файл
        with open(self.__filename, 'w', newline='', encoding='utf-8') as f:
            f.write(result_string)
        
        return result_string