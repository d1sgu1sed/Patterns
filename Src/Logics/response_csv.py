import re
import io
import csv
from Src.Core.abstract_response import abstract_response
from Src.Models.ingredient_model import ingredient_model
from Src.Models.measure_model import measure_model
from Src.Models.nomenclature_group_model import nomenclature_group_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.recipe_model import recipe_model
from Src.Models.recipe_step_model import recipe_step_model
from typing import Any

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
    Генератор данных в формате CSV
    """
    __model_handlers: dict
    
    def __init__(self):
        # Регистрация специальных обработчиков для моделей
        self.__model_handlers = {
            nomenclature_model: self.__nomenclature_to_csv,
            nomenclature_group_model: self.__nomenclature_group_to_csv,
            ingredient_model: self.__ingredient_to_csv,
            measure_model: self.__measure_to_csv,
            recipe_model: self.__recipe_to_csv,
            recipe_step_model: self.__recipe_step_to_csv,
        }
    
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
                formatted_description = step.description.format(**step.params)
            else:
                formatted_description = step.description.format(*step.params)
            return formatted_description
        except:
            raise formatting_error(
                f"Ошибка при форматировании строки. Плейсхолдеры: {placeholders}, Параметры: {step.params}"
            )

    """
    Преобразует модель рецепта в CSV данные
    """
    def __recipe_to_csv(self, recipe: recipe_model) -> list:
        csv_content = []
        
        # Заголовок рецепта
        csv_content.append(["РЕЦЕПТ", recipe.name.upper()])
        csv_content.append([])  # Пустая строка
        
        # Таблица ингредиентов
        ingredients_data = self.__format_ingredients_table(recipe.ingredients)
        if ingredients_data:
            csv_content.append(["ИНГРЕДИЕНТЫ"])
            csv_content.extend(ingredients_data)
            csv_content.append([])  # Пустая строка
        
        # Ремарка
        if recipe.remark:
            csv_content.append(["РЕМАРКА", recipe.remark])
            csv_content.append([])  # Пустая строка
        
        # Шаги приготовления
        steps_data = self.__format_steps(recipe.steps)
        if steps_data:
            csv_content.append(["ПОШАГОВОЕ ПРИГОТОВЛЕНИЕ"])
            csv_content.extend(steps_data)
        
        return csv_content

    """
    Форматирует таблицу ингредиентов для CSV
    """
    def __format_ingredients_table(self, ingredients: list) -> list:
        if not ingredients:
            return []
        
        ingredients_data = []
        ingredients_data.append(["Ингредиенты", "Количество"])
        
        for ingredient in ingredients:
            name = ingredient.product.name
            quantity = f"{ingredient.amount} {ingredient.product.measure.name}"
            ingredients_data.append([name, quantity])
        
        return ingredients_data

    """
    Форматирует шаги приготовления для CSV
    """
    def __format_steps(self, steps: list) -> list:
        if not steps:
            return []
        
        steps_data = []
        steps_data.append(["Шаг", "Описание"])
        
        for i, step in enumerate(steps, 1):
            try:
                formatted_step = self.__formatting(step)
                steps_data.append([i, formatted_step])
            except Exception as e:
                steps_data.append([i, f"[Ошибка форматирования шага: {e}]"])
        
        return steps_data

    """
    Преобразует шаг рецепта в CSV
    """
    def __recipe_step_to_csv(self, step: recipe_step_model) -> list:
        csv_data = []
        csv_data.append(["recipe_step"])
        csv_data.append([])
        
        csv_data.append(["description", "params"])
        try:
            formatted_step = self.__formatting(step)
            params_str = str(step.params) if step.params else ""
            csv_data.append([formatted_step, params_str])
        except Exception as e:
            csv_data.append([f"Ошибка: {e}", ""])
        
        return csv_data

    """
    Конвертирует объект в CSV данные
    """
    def __convert_to_csv(self, obj: Any) -> list:
        try:
            # Поиск специального обработчика для типа объекта
            obj_type = type(obj)
            handler = self.__model_handlers.get(obj_type)
            if handler:
                return handler(obj)
            
            # Обработка составных типов
            return self.__handle_complex_types(obj)
                
        except (TypeError, ValueError, AttributeError) as e:
            return [["Ошибка сериализации"], [str(e)]]

    """
    Обработка сложных типов данных
    """
    def __handle_complex_types(self, obj: Any) -> list:
        if hasattr(obj, '__dict__'):
            return self.__handle_object(obj)
        elif isinstance(obj, list):
            return self.__handle_list(obj)
        elif isinstance(obj, dict):
            return self.__handle_dict(obj)
        else:
            return self.__handle_simple_type(obj)

    """
    Обработка объектов с __dict__
    """
    def __handle_object(self, obj: Any) -> list:
        csv_data = []
        csv_data.append([obj.__class__.__name__])
        csv_data.append([])
        
        headers = []
        values = []
        
        for key, value in obj.__dict__.items():
            if key.startswith('_'):
                continue
            headers.append(key)
            values.append(self.__process_value(value))
        
        csv_data.append(headers)
        csv_data.append(values)
        return csv_data

    """
    Обработка списков
    """
    def __handle_list(self, obj: list) -> list:
        csv_data = []
        for i, item in enumerate(obj):
            item_data = self.__convert_to_csv(item)
            if isinstance(item_data, list) and all(isinstance(row, list) for row in item_data):
                csv_data.extend(item_data)
            else:
                csv_data.append([self.__process_value(item_data)])
            csv_data.append([])
        return csv_data[:-1] if csv_data else []

    """
    Обработка словарей
    """
    def __handle_dict(self, obj: dict) -> list:
        csv_data = []
        csv_data.append(["dict"])
        csv_data.append([])
        
        csv_data.append(["Key", "Value"])
        for key, value in obj.items():
            csv_data.append([str(key), self.__process_value(value)])
        
        return csv_data

    """
    Обработка простых типов данных
    """
    def __handle_simple_type(self, obj: Any) -> list:
        return [[str(obj)]]

    """
    Рекурсивная обработка значений для CSV
    """
    def __process_value(self, value: Any) -> str:
        if value is None:
            return "None"
        elif isinstance(value, (str, int, float, bool)):
            return str(value)
        elif isinstance(value, list):
            return "; ".join([self.__process_value(item) for item in value])
        elif isinstance(value, dict):
            dict_items = [f"{k}: {self.__process_value(v)}" for k, v in value.items()]
            return "; ".join(dict_items)
        elif hasattr(value, '__dict__'):
            return self.__convert_to_csv_string(value)
        else:
            return str(value)

    """
    Конвертирует объект в CSV строку (для вложенных объектов)
    """
    def __convert_to_csv_string(self, obj: Any) -> str:
        try:
            csv_data = self.__convert_to_csv(obj)
            output = io.StringIO()
            writer = csv.writer(output, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
            writer.writerows(csv_data)
            return output.getvalue()
        except:
            return str(obj)

    """
    Преобразует nomenclature_model в CSV
    """
    def __nomenclature_to_csv(self, nomenclature: nomenclature_model) -> list:
        csv_data = []
        csv_data.append(["nomenclature"])
        csv_data.append([])
        
        csv_data.append(["Поле", "Значение"])
        self.__add_csv_row(csv_data, "Название", getattr(nomenclature, 'name', None))
        self.__add_csv_row(csv_data, "Группа", getattr(nomenclature.group, 'name', None))
        self.__add_csv_row(csv_data, "Мера", getattr(nomenclature.measure, 'name', None))
        
        return csv_data

    """
    Преобразует nomenclature_group_model в CSV
    """
    def __nomenclature_group_to_csv(self, group: nomenclature_group_model) -> list:
        csv_data = []
        csv_data.append(["nomenclature_group"])
        csv_data.append([])
        
        csv_data.append(["Поле", "Значение"])
        self.__add_csv_row(csv_data, "Название", getattr(group, 'name', None))
        self.__add_csv_row(csv_data, "Описание", getattr(group, 'description', None))
        
        return csv_data

    """
    Преобразует ingredient_model в CSV
    """
    def __ingredient_to_csv(self, ingredient: ingredient_model) -> list:
        csv_data = []
        csv_data.append(["ingredient"])
        csv_data.append([])
        
        csv_data.append(["Поле", "Значение"])
        self.__add_csv_row(csv_data, "Продукт", getattr(ingredient.product, 'name', None))
        self.__add_csv_row(csv_data, "Количество", getattr(ingredient, 'amount', None))
        self.__add_csv_row(csv_data, "Мера", getattr(ingredient.measure, 'name', None))
        
        return csv_data

    """
    Преобразует measure_model в CSV
    """
    def __measure_to_csv(self, measure: measure_model) -> list:
        csv_data = []
        csv_data.append(["measure"])
        csv_data.append([])
        
        csv_data.append(["Поле", "Значение"])
        self.__add_csv_row(csv_data, "Название", getattr(measure, 'name', None))
        self.__add_csv_row(csv_data, "Описание", getattr(measure, 'description', None))
        
        return csv_data

    """
    Добавление строки в CSV данные если значение не None
    """
    def __add_csv_row(self, csv_data: list, field: str, value: Any) -> None:
        if value is not None:
            csv_data.append([field, str(value)])

    """
    Генерирует CSV строку на основе данных
    """
    def generate(self, data: Any) -> str:
        try:
            csv_data = self.__convert_to_csv(data)
            
            output = io.StringIO()
            writer = csv.writer(output, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
            writer.writerows(csv_data)
            result_string = output.getvalue()
            
            return result_string
            
        except Exception as e:
            raise formatting_error(f"Ошибка при генерации CSV: {e}")