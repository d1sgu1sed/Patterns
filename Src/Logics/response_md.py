from Src.Core.abstract_response import abstract_response
from Src.Models.ingredient_model import ingredient_model
from Src.Models.measure_model import measure_model
from Src.Models.nomenclature_group_model import nomenclature_group_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.recipe_model import recipe_model
from Src.Models.recipe_step_model import recipe_step_model
import re
from typing import Any

"""
Исключение при форматировании
"""  
class formatting_error(Exception):
    pass


class response_md(abstract_response):
    """
    Генератор данных в формате Markdown
    """

    """
    Генерирует Markdown таблицу на основе данных
    
    Параметры:
        data: Данные для преобразования
    """
    def generate(self, data: list) -> str:
        super().generate(data)
        dict_obj = self.generate_dict(data)
        
        try:
            if not dict_obj:
                return "Нет данных для отображения"
            
            item = dict_obj[0]
            fields = item.keys()
            
            # Шапка таблицы
            text = f"|{'|'.join(fields)}|\n"
            text += f"|{'|'.join(['---' for _ in fields])}|\n"
            
            # Данные таблицы
            for item in dict_obj:
                table_line = []
                for field in fields:
                    attr = item[field]
                    if isinstance(attr, str):
                        table_line.append(f"\"{attr}\"")
                    else:
                        table_line.append(f"{attr}")
                text += f"|{'|'.join(table_line)}|\n"
            
            return text
            
        except Exception as e:
            raise formatting_error(f"Ошибка при форматировании Markdown: {str(e)}")