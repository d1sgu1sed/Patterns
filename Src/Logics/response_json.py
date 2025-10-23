from Src.Core.abstract_response import abstract_response
from Src.Models.ingredient_model import ingredient_model
from Src.Models.measure_model import measure_model
from Src.Models.nomenclature_group_model import nomenclature_group_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.recipe_model import recipe_model
from Src.Models.recipe_step_model import recipe_step_model
import json
from typing import Any

"""
Исключение при сериализации в JSON
"""  
class json_serialization_error(Exception):
    pass


class response_json(abstract_response):
    """
    Генератор данных в формате JSON
    """
    __model_handlers: dict
    
    def __init__(self):
        # Регистрация специальных обработчиков для моделей
        self.__model_handlers = {
            nomenclature_model: self.__nomenclature_to_dict,
            nomenclature_group_model: self.__nomenclature_group_to_dict,
            ingredient_model: self.__ingredient_to_dict,
            measure_model: self.__measure_to_dict,
            recipe_model: self.__recipe_to_dict,
            recipe_step_model: self.__recipe_step_to_dict,
        }
    
    """
    Форматирует шаги в требуемый формат
    """
    def __format_steps(self, steps: list) -> list:
        if not steps:
            return []
        
        formatted_steps = []
        for step in steps:
            if step.params:
                step_entry = [
                    step.description,
                    step.params if isinstance(step.params, dict) else dict(enumerate(step.params))
                ]
            else:
                step_entry = step.description
            
            formatted_steps.append(step_entry)
        
        return formatted_steps

    """
    Форматирует ингредиенты в требуемый формат
    """
    def __format_ingredients(self, ingredients: list) -> list:
        if not ingredients:
            return []
        
        formatted_ingredients = []
        for ingredient in ingredients:
            ingredient_dict = {
                "nomenclature": ingredient.product.name,
                "measure": ingredient.product.measure.name,
                "value": ingredient.amount
            }
            formatted_ingredients.append(ingredient_dict)
        
        return formatted_ingredients

    """
    Преобразует модель рецепта в словарь для сериализации в JSON
    """
    def __recipe_to_dict(self, recipe: recipe_model) -> dict:
        try:
            recipe_dict = {
                "name": recipe.name,
                "remark": recipe.remark,
                "ingredients": self.__format_ingredients(recipe.ingredients),
                "steps": self.__format_steps(recipe.steps)
            }
            
            return recipe_dict
            
        except Exception as e:
            raise json_serialization_error(f"Ошибка при преобразовании рецепта в словарь: {e}")

    """
    Преобразует шаг рецепта в словарь
    """
    def __recipe_step_to_dict(self, step: recipe_step_model) -> dict:
        step_dict = {
            "description": step.description,
        }
        
        if step.params:
            step_dict["params"] = step.params
        
        return step_dict

    """
    Конвертирует объект в словарь для JSON-сериализации
    """
    def __convert_to_dict(self, obj: Any) -> dict:
        try:
            # Поиск специального обработчика для типа объекта
            obj_type = type(obj)
            handler = self.__model_handlers.get(obj_type)
            if handler:
                return handler(obj)
            
            # Обработка составных типов
            return self.__handle_complex_types(obj)
                
        except (TypeError, ValueError, AttributeError) as e:
            return {"error": f"Serialization error: {str(e)}"}

    """
    Обработка сложных типов данных
    """
    def __handle_complex_types(self, obj: Any) -> dict:
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
    def __handle_object(self, obj: Any) -> dict:
        result = {}
        for key, value in obj.__dict__.items():
            if key.startswith('_'):
                continue
            result[key] = self.__process_value(value)
        return result

    """
    Обработка списков
    """
    def __handle_list(self, obj: list) -> list:
        return [self.__process_value(item) for item in obj]

    """
    Обработка словарей
    """
    def __handle_dict(self, obj: dict) -> dict:
        return {str(k): self.__process_value(v) for k, v in obj.items()}

    """
    Обработка простых типов данных
    """
    def __handle_simple_type(self, obj: Any) -> Any:
        if obj is None:
            return None
        elif isinstance(obj, (str, int, float, bool)):
            return obj
        else:
            return str(obj)

    """
    Рекурсивная обработка значений для JSON-сериализации
    """
    def __process_value(self, value: Any) -> Any:
        if value is None:
            return None
        elif isinstance(value, (str, int, float, bool)):
            return value
        elif isinstance(value, list):
            return [self.__process_value(item) for item in value]
        elif isinstance(value, dict):
            return {str(k): self.__process_value(v) for k, v in value.items()}
        elif hasattr(value, '__dict__'):
            return self.__convert_to_dict(value)
        else:
            return str(value)

    """
    Преобразует nomenclature_model в словарь
    """
    def __nomenclature_to_dict(self, nomenclature: nomenclature_model) -> dict:
        result = {}
        
        self.__add_dict_value(result, 'name', getattr(nomenclature, 'name', None))
        self.__add_dict_value(result, 'description', getattr(nomenclature, 'description', None))
        self.__add_dict_value(result, 'group', getattr(nomenclature.group, 'name', None))
        self.__add_dict_value(result, 'measure', getattr(nomenclature.measure, 'name', None))
        
        return result

    """
    Преобразует nomenclature_group_model в словарь
    """
    def __nomenclature_group_to_dict(self, group: nomenclature_group_model) -> dict:
        result = {}
        
        self.__add_dict_value(result, 'name', getattr(group, 'name', None))
        self.__add_dict_value(result, 'description', getattr(group, 'description', None))
        
        return result

    """
    Преобразует ingredient_model в словарь
    """
    def __ingredient_to_dict(self, ingredient: ingredient_model) -> dict:
        result = {}
        
        self.__add_dict_value(result, 'product', getattr(ingredient.product, 'name', None))
        self.__add_dict_value(result, 'amount', getattr(ingredient, 'amount', None))
        self.__add_dict_value(result, 'measure', getattr(ingredient.measure, 'name', None))
        
        return result

    """
    Преобразует measure_model в словарь
    """
    def __measure_to_dict(self, measure: measure_model) -> dict:
        result = {}
        
        self.__add_dict_value(result, 'name', getattr(measure, 'name', None))
        self.__add_dict_value(result, 'description', getattr(measure, 'description', None))
        self.__add_dict_value(result, 'base_measure', getattr(measure.base_measure, 'name', None))
        
        return result

    """
    Добавление значения в словарь если оно не None
    """
    def __add_dict_value(self, dictionary: dict, key: str, value: Any) -> None:
        if value is not None:
            dictionary[key] = value

    """
    Генерирует JSON строку на основе данных
    """
    def generate(self, data: Any) -> str:
        try:
            json_compatible_data = self.__convert_to_dict(data)
            return json.dumps(json_compatible_data, ensure_ascii=False, indent=2)
            
        except Exception as e:
            raise json_serialization_error(f"Ошибка при генерации JSON: {e}")