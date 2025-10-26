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
    Генератор данных в формате CSV с улучшенным форматированием
    """

    """
    Генерирует CSV строку

    Параметры:
        data: Данные для преобразования в CSV
    """
    def generate(self, data: Any) -> str:
        # Получаем базовый текст и преобразуем данные в словари
        super().generate(data)
        dict_models = self.generate_dict(data)
        
        if not dict_models:
            return ""
            
        # Получаем названия колонок из первого элемента
        first_item = dict_models[0]
        column_names = first_item.keys()
        
        # Создаем строковый буфер для построения CSV
        output = io.StringIO()
        
        # Создаем CSV writer с настройками для лучшей читаемости
        csv_writer = csv.writer(
            output, 
            delimiter=';',
            quoting=csv.QUOTE_ALL,  # Все значения в кавычках для единообразия
            quotechar='"',
            lineterminator='\n'
        )
        
        # Записываем заголовок с понятными названиями колонок
        csv_writer.writerow(column_names)
        
        # Записываем данные
        for item in dict_models:
            row = []
            for column in column_names:
                value = item[column]
                # Преобразуем значение в строку с правильным форматированием
                if value is None:
                    row.append("")  # Пустые значения вместо None
                elif isinstance(value, (int, float)):
                    row.append(str(value))
                elif isinstance(value, str):
                    # Экранируем кавычки и убираем лишние пробелы
                    cleaned_value = value.strip().replace('"', '""')
                    if value != "":
                        row.append(cleaned_value)
                else:
                    # Для других типов используем строковое представление
                    row.append(str(value))
            
            csv_writer.writerow(row)
        
        # Получаем результат и закрываем буфер
        result = output.getvalue()
        output.close()
        
        return result