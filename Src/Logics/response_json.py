import json
from typing import Any
from Src.Core.abstract_response import abstract_response

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


class response_json(abstract_response):
    """
    Генератор данных в формате JSON с красивым форматированием
    """

    """
    Конвертирует данные в JSON
    
    Параметры:
        data: Данные для преобразования
    """
    def generate(self, data: list) -> str:
        super().generate(data)
        dict_obj = self.generate_dict(data)
        
        result = {}
        result["data"] = dict_obj

        
        # JSON с отступами и поддержкой кириллицы
        try:
            formatted_json = json.dumps(
                result,
                ensure_ascii=False,  # Для корректного отображения кириллицы
                indent=2,            # Отступы в 2 пробела
                sort_keys=False,     # Сохраняем порядок ключей
            )
            return formatted_json
        except Exception as e:
            raise formatting_error(f"Ошибка при форматировании JSON: {str(e)}")
