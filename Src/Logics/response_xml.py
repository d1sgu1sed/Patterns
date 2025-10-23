import re
import xml.etree.ElementTree as ET
from xml.dom import minidom
from Src.Core.abstract_response import abstract_response
from Src.Models.ingredient_model import ingredient_model
from Src.Models.measure_model import measure_model
from Src.Models.nomenclature_group_model import nomenclature_group_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.recipe_model import recipe_model
from Src.Models.recipe_step_model import recipe_step_model
from typing import Any

"""
Исключение при сериализации в XML
"""  
class xml_serialization_error(Exception):
    pass


class response_xml(abstract_response):
    """
    Генератор данных в формате XML
    """
    __model_handlers: dict
    
    def __init__(self):
        # Регистрация специальных обработчиков для моделей
        self.__model_handlers = {
            nomenclature_model: self.__nomenclature_to_xml,
            nomenclature_group_model: self.__nomenclature_group_to_xml,
            ingredient_model: self.__ingredient_to_xml,
            measure_model: self.__measure_to_xml,
            recipe_model: self.__recipe_to_xml,
            recipe_step_model: self.__recipe_step_to_xml,
        }
    
    """
    Форматирует строку description, подставляя параметры из params
    в плейсхолдеры в фигурных скобках.
    """
    def __formatting(self, step: recipe_step_model) -> str:  
        if not step.description:
            return ""
        
        if step.params is None:
            step.params = []
        
        placeholders = re.findall(r'\{([^}]+)\}', step.description)
        
        if len(placeholders) != len(step.params):
            return step.description
        
        try:
            if isinstance(step.params, dict):
                formatted_description = step.description.format(**step.params)
            else:
                formatted_description = step.description.format(*step.params)
            return formatted_description
        except:
            return step.description

    """
    Преобразует модель рецепта в XML элемент
    """
    def __recipe_to_xml(self, recipe: recipe_model) -> ET.Element:
        try:
            recipe_elem = ET.Element("recipe")
            
            # Основные поля рецепта
            self.__add_text_element(recipe_elem, "name", recipe.name)
            self.__add_text_element(recipe_elem, "remark", recipe.remark)
            
            # Ингредиенты
            if recipe.ingredients:
                ingredients_elem = ET.SubElement(recipe_elem, "ingredients")
                for ingredient in recipe.ingredients:
                    ingredient_elem = self.__ingredient_to_xml(ingredient)
                    ingredients_elem.append(ingredient_elem)
            
            # Шаги приготовления
            if recipe.steps:
                steps_elem = ET.SubElement(recipe_elem, "steps")
                for i, step in enumerate(recipe.steps, 1):
                    step_elem = self.__recipe_step_to_xml(step)
                    step_elem.set("number", str(i))
                    steps_elem.append(step_elem)
            
            return recipe_elem
            
        except Exception as e:
            raise xml_serialization_error(f"Ошибка при преобразовании рецепта в XML: {e}")

    """
    Преобразует шаг рецепта в XML
    """
    def __recipe_step_to_xml(self, step: recipe_step_model) -> ET.Element:
        step_elem = ET.Element("step")
        
        formatted_description = self.__formatting(step)
        self.__add_text_element(step_elem, "description", formatted_description)
        
        if step.params:
            params_elem = ET.SubElement(step_elem, "parameters")
            if isinstance(step.params, dict):
                for key, value in step.params.items():
                    param_elem = ET.SubElement(params_elem, "parameter")
                    param_elem.set("key", str(key))
                    param_elem.text = str(value)
            else:
                for j, param in enumerate(step.params):
                    param_elem = ET.SubElement(params_elem, "parameter")
                    param_elem.set("index", str(j))
                    param_elem.text = str(param)
        
        return step_elem

    """
    Конвертирует объект в XML элемент
    """
    def __convert_to_xml(self, obj: Any, element_name: str = "root") -> ET.Element:
        try:
            # Поиск специального обработчика для типа объекта
            obj_type = type(obj)
            handler = self.__model_handlers.get(obj_type)
            if handler:
                return handler(obj)
            
            # Обработка составных типов
            return self.__handle_complex_types(obj, element_name)
                
        except (TypeError, ValueError, AttributeError) as e:
            return self.__create_error_element(element_name, f"Serialization error: {str(e)}")

    """
    Обработка сложных типов данных
    """
    def __handle_complex_types(self, obj: Any, element_name: str) -> ET.Element:
        if hasattr(obj, '__dict__'):
            return self.__handle_object(obj, element_name)
        elif isinstance(obj, list):
            return self.__handle_list(obj, element_name)
        elif isinstance(obj, dict):
            return self.__handle_dict(obj, element_name)
        else:
            return self.__handle_simple_type(obj, element_name)

    """
    Обработка объектов с __dict__
    """
    def __handle_object(self, obj: Any, element_name: str) -> ET.Element:
        elem = ET.Element(element_name)
        elem.set("type", obj.__class__.__name__)
        
        for key, value in obj.__dict__.items():
            if key.startswith('_'):
                continue
            child_elem = self.__convert_to_xml(value, key)
            elem.append(child_elem)
        
        return elem

    """
    Обработка списков
    """
    def __handle_list(self, obj: list, element_name: str) -> ET.Element:
        list_elem = ET.Element(element_name)
        list_elem.set("type", "list")
        
        for i, item in enumerate(obj):
            item_elem = self.__convert_to_xml(item, "item")
            item_elem.set("index", str(i))
            list_elem.append(item_elem)
        
        return list_elem

    """
    Обработка словарей
    """
    def __handle_dict(self, obj: dict, element_name: str) -> ET.Element:
        dict_elem = ET.Element(element_name)
        dict_elem.set("type", "dict")
        
        for key, value in obj.items():
            child_elem = self.__convert_to_xml(value, str(key))
            dict_elem.append(child_elem)
        
        return dict_elem

    """
    Обработка простых типов данных
    """
    def __handle_simple_type(self, obj: Any, element_name: str) -> ET.Element:
        elem = ET.Element(element_name)
        elem.set("type", type(obj).__name__)
        if obj is not None:
            elem.text = str(obj)
        return elem

    """
    Создание элемента с ошибкой
    """
    def __create_error_element(self, element_name: str, message: str) -> ET.Element:
        elem = ET.Element(element_name)
        elem.set("type", "error")
        elem.text = message
        return elem

    """
    Добавление текстового элемента если текст не пустой
    """
    def __add_text_element(self, parent: ET.Element, tag: str, text: Any) -> None:
        if text is not None:
            elem = ET.SubElement(parent, tag)
            # Конвертируем в строку если это не строка
            if not isinstance(text, str):
                text = str(text)
            elem.text = text

    """
    Преобразует nomenclature_model в XML
    """
    def __nomenclature_to_xml(self, nomenclature: nomenclature_model) -> ET.Element:
        elem = ET.Element("nomenclature")
        
        self.__add_text_element(elem, "name", getattr(nomenclature, 'name', None))
        self.__add_text_element(elem, "description", getattr(nomenclature, 'description', None))
        self.__add_text_element(elem, "group", getattr(nomenclature.group, 'name', None))
        self.__add_text_element(elem, "measure", getattr(nomenclature.measure, 'name', None))
        
        return elem

    """
    Преобразует nomenclature_group_model в XML
    """
    def __nomenclature_group_to_xml(self, group: nomenclature_group_model) -> ET.Element:
        elem = ET.Element("nomenclature_group")
        self.__add_text_element(elem, "name", getattr(group, 'name', None))
        self.__add_text_element(elem, "description", getattr(group, 'description', None))
        return elem

    """
    Преобразует ingredient_model в XML
    """
    def __ingredient_to_xml(self, ingredient: ingredient_model) -> ET.Element:
        elem = ET.Element("ingredient")
        
        self.__add_text_element(elem, "product", getattr(ingredient.product, 'name', None))
        self.__add_text_element(elem, "amount", ingredient.amount)
        self.__add_text_element(elem, "measure", getattr(ingredient.measure, 'name', None))
        
        return elem

    """
    Преобразует measure_model в XML
    """
    def __measure_to_xml(self, measure: measure_model) -> ET.Element:
        elem = ET.Element("measure")
        
        self.__add_text_element(elem, "name", getattr(measure, 'name', None))
        self.__add_text_element(elem, "description", getattr(measure, 'description', None))
        
        return elem

    """
    Форматирует XML в красивую строку с отступами
    """
    def __prettify_xml(self, elem: ET.Element) -> str:
        try:
            rough_string = ET.tostring(elem, encoding='unicode')
            reparsed = minidom.parseString(rough_string)
            return reparsed.toprettyxml(indent="  ")
        except:
            return ET.tostring(elem, encoding='unicode')

    """
    Генерирует XML строку на основе данных
    """
    def generate(self, data: Any) -> str:
        try:
            root_elem = self.__convert_to_xml(data, "data")
            xml_string = self.__prettify_xml(root_elem)
            return xml_string
            
        except Exception as e:
            raise xml_serialization_error(f"Ошибка при генерации XML: {e}")