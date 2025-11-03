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
from typing import Any, List, Optional

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
        field_order: Опциональный список с порядком полей. Если передан - используются только указанные поля
    """
    def generate(self, data: Any, field_order: Optional[List[str]] = None) -> str:
        # Получаем базовый текст и преобразуем данные в словари
        super().generate(data)
        dict_models = self.generate_dict(data)
        
        if not dict_models:
            return ""
            
        # Получаем доступные поля из первого элемента
        first_item = dict_models[0]
        available_fields = list(first_item.keys())
        
        # Определяем порядок полей
        if field_order is None or len(field_order) == 0:
            # Используем порядок по умолчанию (исходный порядок полей)
            final_field_order = available_fields
        else:
            # Используем ТОЛЬКО поля из field_order, которые существуют в данных
            final_field_order = []
            for field in field_order:
                if field in available_fields:
                    final_field_order.append(field)
            # НЕ добавляем остальные поля - исключаем их полностью
        
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
        
        # Записываем заголовок с нужными полями в нужном порядке
        csv_writer.writerow(final_field_order)
        
        # Записываем данные
        for item in dict_models:
            row = []
            for column in final_field_order:
                value = item.get(column, "")  # Используем get для безопасности
                # Преобразуем значение в строку с правильным форматированием
                if value is None:
                    row.append("")  # Пустые значения вместо None
                elif isinstance(value, (int, float)):
                    row.append(str(value))
                elif isinstance(value, str):
                    # Экранируем кавычки и убираем лишние пробелы
                    cleaned_value = value.strip().replace('"', '""')
                    row.append(cleaned_value)
                else:
                    # Для других типов используем строковое представление
                    row.append(str(value))
            
            csv_writer.writerow(row)
        
        # Получаем результат и закрываем буфер
        result = output.getvalue()
        output.close()
        
        return result