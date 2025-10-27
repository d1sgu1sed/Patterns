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
    
    """
    Генерирует XML строку на основе данных
    
    Параметр:
        data: Данные для преобразования
        
    Возвращает:
        str: Отформатированная XML строка
    """
    def generate(self, data: list) -> str:
        super().generate(data)
        dict_obj = self.generate_dict(data)
        
        try:
            xml_content = "<data>"
            xml_content += self.__build_xml_from_dict(dict_obj, "obj")
            xml_content += "</data>"
            return xml_content
            
        except Exception as e:
            raise xml_serialization_error(f"Ошибка при сериализации в XML: {str(e)}")
    
    """
    Рекурсивно преобразует словарь или список в XML формат
        
    Параметры:
        obj: Объект для преобразования
        tag: Базовый тег для элементов
            
    Возвращает:
        str: XML строка
    """
    def __build_xml_from_dict(self, obj, tag: str) -> str:
        text = ""
        if isinstance(obj, list):
            for item in obj:
                text += f"<{tag}>" + self.__build_xml_from_dict(item, "") + f"</{tag}>"
        elif isinstance(obj, dict):
            for key in obj.keys():
                if isinstance(obj[key], dict) or isinstance(obj[key], list):
                    text += f"<{key}>{self.__build_xml_from_dict(obj[key], key + '_obj')}</{key}>"
                else:
                    text += f"<{key}>{obj[key]}</{key}>"
        else:
            text += str(obj)
        return text