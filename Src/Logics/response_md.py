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
    Генератор данных в формате Markdown
    """
    __model_handlers: dict
    
    def __init__(self):
        # Регистрация специальных обработчиков для моделей
        self.__model_handlers = {
            nomenclature_model: self.__nomenclature_to_md,
            nomenclature_group_model: self.__nomenclature_group_to_md,
            ingredient_model: self.__ingredient_to_md,
            measure_model: self.__measure_to_md,
            recipe_model: self.__recipe_to_md,
            recipe_step_model: self.__recipe_step_to_md,
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
    Преобразует модель рецепта в Markdown строку
    """
    def __recipe_to_md(self, recipe: recipe_model) -> str:
        md_content = f"# {recipe.name.upper()}\n\n"
        
        # Таблица ингредиентов
        md_content += self.__format_ingredients_table(recipe.ingredients)
        
        # Добавляем ремарку после таблицы
        if recipe.remark:
            md_content += f"{recipe.remark}\n\n"
        
        md_content += "## ПОШАГОВОЕ ПРИГОТОВЛЕНИЕ\n\n"
        
        # Шаги приготовления
        md_content += self.__format_steps(recipe.steps)
        
        return md_content

    """
    Форматирует таблицу ингредиентов
    """
    def __format_ingredients_table(self, ingredients: list) -> str:
        if not ingredients:
            return ""
        
        table = "| Ингредиенты | Количество |\n"
        table += "|-------------|------------|\n"
        
        for ingredient in ingredients:
            name = ingredient.product.name
            quantity = f"{ingredient.amount} {ingredient.measure.name}"
            table += f"| {name} | {quantity} |\n"
        
        table += "\n"
        return table

    """
    Форматирует шаги приготовления
    """
    def __format_steps(self, steps: list) -> str:
        if not steps:
            return ""
        
        steps_text = ""
        for i, step in enumerate(steps, 1):
            try:
                formatted_step = self.__formatting(step)
                steps_text += f"{i}. {formatted_step}\n"
            except Exception as e:
                steps_text += f"{i}. [Ошибка форматирования шага: {e}]\n"
        
        return steps_text

    """
    Преобразует шаг рецепта в Markdown
    """
    def __recipe_step_to_md(self, step: recipe_step_model) -> str:
        md_content = "## Шаг рецепта\n\n"
        
        try:
            formatted_step = self.__formatting(step)
            md_content += f"**Описание**: {formatted_step}\n\n"
        except Exception as e:
            md_content += f"**Ошибка**: {e}\n\n"
        
        if step.params:
            md_content += "**Параметры**:\n"
            if isinstance(step.params, dict):
                for key, value in step.params.items():
                    md_content += f"- {key}: {value}\n"
            else:
                for i, param in enumerate(step.params):
                    md_content += f"- Параметр {i}: {param}\n"
            md_content += "\n"
        
        return md_content

    """
    Конвертирует объект в Markdown строку
    """
    def __convert_to_md(self, obj: Any) -> str:
        try:
            # Если объект - список, обрабатываем каждый элемент отдельно
            if isinstance(obj, list):
                return self.__handle_list(obj)
            
            # Поиск специального обработчика для типа объекта
            obj_type = type(obj)
            handler = self.__model_handlers.get(obj_type)
            if handler:
                return handler(obj)
            
            # Обработка составных типов
            return self.__handle_complex_types(obj)
                
        except (TypeError, ValueError, AttributeError) as e:
            return f"# Ошибка сериализации\n\n{str(e)}"

    """
    Обработка сложных типов данных
    """
    def __handle_complex_types(self, obj: Any) -> str:
        if hasattr(obj, '__dict__'):
            return self.__handle_object(obj)
        elif isinstance(obj, dict):
            return self.__handle_dict(obj)
        else:
            return self.__handle_simple_type(obj)

    """
    Обработка объектов с __dict__
    """
    def __handle_object(self, obj: Any) -> str:
        md_content = f"# {obj.__class__.__name__}\n\n"
        
        for key, value in obj.__dict__.items():
            if key.startswith('_'):
                continue
            processed_value = self.__process_value(value)
            md_content += f"**{key}**: {processed_value}\n\n"
        
        return md_content

    """
    Обработка списков
    """
    def __handle_list(self, obj: list) -> str:
        if not obj:
            return "Пустой список"
        
        # Если в списке один элемент, возвращаем его представление
        if len(obj) == 1:
            return self.__convert_to_md(obj[0])
        
        md_content = f"# Список ({len(obj)} элементов)\n\n"
        
        # Для списков объектов используем компактное представление
        for i, item in enumerate(obj):
            item_content = self.__convert_to_md(item)
            # Убираем лишние заголовки если они есть
            if item_content.startswith('# '):
                lines = item_content.split('\n')
                if len(lines) > 1:
                    # Берем первую строку без заголовка и добавляем номер
                    first_line = lines[0].replace('# ', '')
                    md_content += f"{i + 1}. **{first_line}**\n"
                    # Добавляем остальное содержимое
                    if len(lines) > 2:
                        md_content += '\n'.join(lines[2:]) + '\n'
                else:
                    md_content += f"{i + 1}. {item_content}\n"
            else:
                md_content += f"{i + 1}. {item_content}\n"
            md_content += "\n"
        
        return md_content

    """
    Обработка словарей
    """
    def __handle_dict(self, obj: dict) -> str:
        if not obj:
            return "Пустой словарь"
        
        md_content = "# Словарь\n\n"
        for key, value in obj.items():
            processed_value = self.__process_value(value)
            md_content += f"**{key}**: {processed_value}\n\n"
        
        return md_content

    """
    Обработка простых типов данных
    """
    def __handle_simple_type(self, obj: Any) -> str:
        return str(obj) if obj is not None else "None"

    """
    Рекурсивная обработка значений для Markdown
    """
    def __process_value(self, value: Any) -> str:
        if value is None:
            return "None"
        elif isinstance(value, (str, int, float, bool)):
            return str(value)
        elif isinstance(value, list):
            if not value:
                return "[]"
            # Для вложенных списков используем компактное представление
            if len(value) <= 3:
                items = ", ".join([self.__process_value(item) for item in value])
                return f"[{items}]"
            else:
                return f"список из {len(value)} элементов"
        elif isinstance(value, dict):
            if not value:
                return "{}"
            return f"словарь из {len(value)} элементов"
        elif hasattr(value, '__dict__'):
            # Для вложенных объектов возвращаем краткое описание
            return self.__get_object_summary(value)
        else:
            return str(value)

    """
    Получение краткого описания объекта
    """
    def __get_object_summary(self, obj: Any) -> str:
        if hasattr(obj, 'name'):
            return getattr(obj, 'name', str(obj))
        elif hasattr(obj, '__class__'):
            return obj.__class__.__name__
        else:
            return str(obj)

    """
    Преобразует nomenclature_model в Markdown
    """
    def __nomenclature_to_md(self, nomenclature: nomenclature_model) -> str:
        md_content = "# Номенклатура\n\n"
        
        md_content = self.__add_md_field(md_content, "Название", getattr(nomenclature, 'name', None))
        md_content = self.__add_md_field(md_content, "Группа", getattr(nomenclature.group, 'name', None))
        md_content = self.__add_md_field(md_content, "Мера", getattr(nomenclature.measure, 'name', None))
        
        return md_content

    """
    Преобразует nomenclature_group_model в Markdown
    """
    def __nomenclature_group_to_md(self, group: nomenclature_group_model) -> str:
        md_content = "# Группа номенклатуры\n\n"
        
        md_content = self.__add_md_field(md_content, "Название", getattr(group, 'name', None))
        md_content = self.__add_md_field(md_content, "Описание", getattr(group, 'description', None))
        
        return md_content

    """
    Преобразует ingredient_model в Markdown
    """
    def __ingredient_to_md(self, ingredient: ingredient_model) -> str:
        md_content = "# Ингредиент\n\n"
        
        md_content = self.__add_md_field(md_content, "Продукт", getattr(ingredient.product, 'name', None))
        md_content = self.__add_md_field(md_content, "Количество", getattr(ingredient, 'amount', None))
        md_content = self.__add_md_field(md_content, "Мера", getattr(ingredient.measure, 'name', None))
        
        return md_content

    """
    Преобразует measure_model в Markdown
    """
    def __measure_to_md(self, measure: measure_model) -> str:
        md_content = "# Единица измерения\n\n"
        
        md_content = self.__add_md_field(md_content, "Название", getattr(measure, 'name', None))
        md_content = self.__add_md_field(md_content, "Описание", getattr(measure, 'description', None))
        md_content = self.__add_md_field(md_content, "Базовая мера", getattr(measure.base_measure, 'name', None))
        
        return md_content

    """
    Добавление поля в Markdown если значение не None
    """
    def __add_md_field(self, md_content: str, field: str, value: Any) -> str:
        if value is not None:
            md_content += f"**{field}**: {value}\n\n"
        return md_content

    """
    Генерирует Markdown строку на основе данных
    """
    def generate(self, data: Any) -> str:
        try:
            md_content = self.__convert_to_md(data)
            return md_content
            
        except Exception as e:
            raise formatting_error(f"Ошибка при генерации Markdown: {e}")