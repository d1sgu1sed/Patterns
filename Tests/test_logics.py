import os
import unittest
import json
import xml.etree.ElementTree as ET
from Src.Logics.response_csv import response_csv
from Src.Logics.response_json import response_json
from Src.Logics.response_md import response_md
from Src.Logics.response_xml import response_xml
from Src.Models.nomenclature_group_model import nomenclature_group_model
from Src.Logics.factory_entities import factory_entities
from Src.Core.response_format import response_formats
from Src.Core.validator import validator
from Src.Core.abstract_response import abstract_response
from Src.Models.recipe_step_model import recipe_step_model
from Src.reposity import reposity
from Src.start_service import start_service

class Test_factory(unittest.TestCase):
    """
    Тесты для проверки работы фабрики и методов response_*
    """
    __start_service = start_service()

    """
    Тест проверки создания markdown рецепта
    """
    def test_md_factory_create(self):
        # Подготовка
        factory = factory_entities()
        data = self.__start_service.reposity.data[reposity.recipes_key()][0]
        expected_filename = "Docs/waffles.md"

        # Действие
        logic = factory.create(response_formats.md())
        # удаляем файл если он существует
        if os.path.exists(expected_filename):
            os.unlink(expected_filename)

        # Проверка
        assert logic is not None
        instance = logic()
        validator.validate(instance, response_md)
        text = instance.generate(data)
        with open(expected_filename, 'w', encoding='utf-8') as f:
            f.write(text)
        assert os.path.exists(expected_filename)
        
        # проверяем что содержимое корректное
        with open(expected_filename, 'r', encoding='utf-8') as f:
            file_content = f.read()
        
        assert text == file_content
        assert f"# {data.name.upper()}" in text
    
    """
    Тест проверки создания json рецепта
    """
    def test_json_factory_create(self):
    # Подготовка
        factory = factory_entities()
        data = self.__start_service.reposity.data[reposity.recipes_key()][0]
        expected_filename = "Docs/waffles.json"

        # Действие
        logic = factory.create(response_formats.json())
        
        # удаляем файл если он существует
        if os.path.exists(expected_filename):
            os.unlink(expected_filename)

        # Проверка
        assert logic is not None
        instance = logic()
        validator.validate(instance, response_json)
        text = instance.generate(data)
        # Записываем в файл
        with open(expected_filename, 'w', encoding='utf-8') as f:
            f.write(text)
        assert os.path.exists(expected_filename)
        
        # проверяем что содержимое корректное
        with open(expected_filename, 'r', encoding='utf-8') as f:
            file_content = f.read()
        
        assert text == file_content
        
        # проверяем что JSON валидный и содержит основные поля
        json_data = json.loads(text)
        assert "name" in json_data
        assert "ingredients" in json_data
        assert "steps" in json_data
        assert json_data["name"] == data.name
    
    """
    Тест проверки создания csv рецепта
    """
    def test_csv_factory_create(self):
        # Подготовка
        factory = factory_entities()
        data = self.__start_service.reposity.data[reposity.recipes_key()][0]
        expected_filename = "Docs/waffles.csv"

        # Действие
        logic = factory.create(response_formats.csv())
        
        # удаляем файл если он существует
        if os.path.exists(expected_filename):
            os.unlink(expected_filename)

        # Проверка
        assert logic is not None
        instance = logic()
        validator.validate(instance, response_csv)
        text = instance.generate(data)
        with open(expected_filename, 'w', newline='', encoding='utf-8') as f:
            f.write(text)
        assert os.path.exists(expected_filename)
        
        # проверяем что содержимое корректное
        with open(expected_filename, 'r', encoding='utf-8') as f:
            file_content = f.read()
        
        # Нормализуем переносы строк перед сравнением
        text_normalized = text.replace('\r\n', '\n').replace('\r', '\n')
        file_content_normalized = file_content.replace('\r\n', '\n').replace('\r', '\n')
        
        assert text_normalized == file_content_normalized
        
        # проверяем что CSV содержит основные данные
        assert data.name.upper() in text_normalized
        assert "ИНГРЕДИЕНТЫ" in text_normalized
        assert "ПОШАГОВОЕ ПРИГОТОВЛЕНИЕ" in text_normalized
    
    """
    Тест проверки создания csv рецепта
    """
    def test_csv_factory_steps_create(self):
        # Подготовка
        factory = factory_entities()
        data = self.__start_service.reposity.data[reposity.recipes_key()][0]
        expected_filename = "Docs/waffles.csv"

        # Действие
        logic = factory.create(response_formats.csv())
        
        # удаляем файл если он существует
        if os.path.exists(expected_filename):
            os.unlink(expected_filename)

        # Проверка
        assert logic is not None
        instance = logic()
        validator.validate(instance, response_csv)
        text = instance.generate(data)
        with open(expected_filename, 'w', newline='', encoding='utf-8') as f:
            f.write(text)
        assert os.path.exists(expected_filename)
        
        # проверяем что содержимое корректное
        with open(expected_filename, 'r', encoding='utf-8') as f:
            file_content = f.read()
        
        # Нормализуем переносы строк перед сравнением
        text_normalized = text.replace('\r\n', '\n').replace('\r', '\n')
        file_content_normalized = file_content.replace('\r\n', '\n').replace('\r', '\n')
        
        assert text_normalized == file_content_normalized

    """
    Тест проверки создания xml рецепта
    """
    def test_xml_factory_create(self):
        # Подготовка
        factory = factory_entities()
        data = self.__start_service.reposity.data[reposity.recipes_key()][0]
        expected_filename = "Docs/waffles.xml"

        # Действие
        logic = factory.create(response_formats.xml())
        
        # удаляем файл если он существует
        if os.path.exists(expected_filename):
            os.unlink(expected_filename)

        # Проверка
        assert logic is not None
        instance = logic()
        validator.validate(instance, response_xml)
        text = instance.generate(data)
        
        # Записываем в файл
        with open(expected_filename, 'w', encoding='utf-8') as f:
            f.write(text)
        assert os.path.exists(expected_filename)
        
        # проверяем что содержимое корректное
        with open(expected_filename, 'r', encoding='utf-8') as f:
            file_content = f.read()
        
        assert text == file_content
        
        # проверяем что XML валидный и содержит основные поля
        try:
            root = ET.fromstring(text)
            
            # Проверяем основные элементы рецепта
            name_elem = root.find("name")
            assert name_elem is not None
            assert name_elem.text == data.name
            
            # Проверяем наличие ингредиентов
            ingredients_elem = root.find("ingredients")
            assert ingredients_elem is not None
            
            # Проверяем наличие шагов
            steps_elem = root.find("steps")
            assert steps_elem is not None
            
            # Проверяем что есть хотя бы один ингредиент и шаг
            ingredient_elems = ingredients_elem.findall("ingredient")
            assert len(ingredient_elems) > 0
            
            step_elems = steps_elem.findall("step")
            assert len(step_elems) > 0
            
        except ET.ParseError as e:
            self.fail(f"Сгенерированный XML невалиден: {e}")
    
    """
    Тест проверки создания xml для различных типов данных
    """
    def test_xml_factory_various_data(self):
        # Подготовка
        factory = factory_entities()
        
        # Тестируем с различными типами данных
        test_cases = [
            ("simple_dict", {"key": "value", "number": 123}),
            ("list_data", [1, 2, 3, "test"]),
            ("nested_data", {
                "recipe_name": "Test Recipe",
                "ingredients": ["flour", "sugar"],
                "metadata": {"author": "Test", "time": 30}
            })
        ]
        
        for test_name, test_data in test_cases:
            with self.subTest(test_name=test_name):
                # Действие
                logic = factory.create(response_formats.xml())
                instance = logic()
                text = instance.generate(test_data)
                
                # Проверка
                assert text is not None
                assert len(text) > 0
                
                # Проверяем что XML валиден
                try:
                    root = ET.fromstring(text)
                    assert root is not None
                except ET.ParseError as e:
                    self.fail(f"XML для {test_name} невалиден: {e}")
    
    """
    Тест проверки создания markdown для различных типов данных
    """
    def test_md_factory_various_data(self):
        # Подготовка
        factory = factory_entities()
        
        # Тестируем с различными типами данных
        test_cases = [
            ("simple_dict", {"key": "value", "number": 123}),
            ("list_data", [1, 2, 3, "test"]),
            ("nested_data", {
                "recipe_name": "Test Recipe",
                "ingredients": ["flour", "sugar"],
                "metadata": {"author": "Test", "time": 30}
            }),
            ("simple_object", type('SimpleObject', (), {
                'name': 'Test Object',
                'value': 42,
                'description': 'Test description'
            })())
        ]
        
        for test_name, test_data in test_cases:
            with self.subTest(test_name=test_name):
                # Действие
                logic = factory.create(response_formats.md())
                instance = logic()
                text = instance.generate(test_data)
                
                # Проверка
                assert text is not None
                assert len(text) > 0
                
                # Проверяем что Markdown содержит основные элементы
                if isinstance(test_data, dict):
                    for key in test_data.keys():
                        assert str(key) in text
                elif hasattr(test_data, '__dict__'):
                    for key in test_data.__dict__.keys():
                        if not key.startswith('_'):
                            assert key in text

    """
    Тест проверки создания csv для различных типов данных
    """
    def test_csv_factory_various_data(self):
        # Подготовка
        factory = factory_entities()
        
        # Тестируем с различными типами данных
        test_cases = [
            ("simple_dict", {"key": "value", "number": 123}),
            ("list_data", [1, 2, 3, "test"]),
            ("nested_data", {
                "recipe_name": "Test Recipe",
                "ingredients": ["flour", "sugar"],
                "metadata": {"author": "Test", "time": 30}
            }),
            ("simple_object", type('SimpleObject', (), {
                'name': 'Test Object',
                'value': 42
            })())
        ]
        
        for test_name, test_data in test_cases:
            with self.subTest(test_name=test_name):
                # Действие
                logic = factory.create(response_formats.csv())
                instance = logic()
                text = instance.generate(test_data)
                
                # Проверка
                assert text is not None
                assert len(text) > 0
                
                # Проверяем что CSV содержит данные
                if isinstance(test_data, dict):
                    for key in test_data.keys():
                        assert str(key) in text
                    for value in test_data.values():
                        assert str(value) in text
                elif isinstance(test_data, list):
                    for item in test_data:
                        assert str(item) in text
                elif hasattr(test_data, '__dict__'):
                    for key, value in test_data.__dict__.items():
                        if not key.startswith('_'):
                            assert key in text
                            assert str(value) in text

    """
    Тест проверки создания json для различных типов данных
    """
    def test_json_factory_various_data(self):
        # Подготовка
        factory = factory_entities()
        
        # Тестируем с различными типами данных
        test_cases = [
            ("simple_dict", {"key": "value", "number": 123}),
            ("nested_data", {
                "recipe_name": "Test Recipe",
                "ingredients": ["flour", "sugar"],
                "metadata": {"author": "Test", "time": 30}
            }),
            ("simple_object", type('SimpleObject', (), {
                'name': 'Test Object',
                'value': 42
            })())
        ]
        
        for test_name, test_data in test_cases:
            with self.subTest(test_name=test_name):
                # Действие
                logic = factory.create(response_formats.json())
                instance = logic()
                text = instance.generate(test_data)
                
                # Проверка
                assert text is not None
                assert len(text) > 0
                
                # Проверяем что JSON валиден
                try:
                    json_data = json.loads(text)
                    assert json_data is not None
                    
                    # Для разных типов данных проверяем по-разному
                    if isinstance(test_data, dict):
                        # Для словаря проверяем ключи и значения
                        for key, value in test_data.items():
                            if key in json_data:
                                assert str(json_data[key]) == str(value)
                    elif isinstance(test_data, list):
                        # Для списка проверяем что JSON тоже список и содержит те же элементы
                        assert isinstance(json_data, list)
                        expected_str = [str(item) for item in test_data]
                        actual_str = [str(item) for item in json_data]
                        assert expected_str == actual_str
                    elif hasattr(test_data, '__dict__'):
                        # Для объектов проверяем наличие полей
                        for key in test_data.__dict__.keys():
                            if not key.startswith('_'):
                                if key in json_data:
                                    assert str(json_data[key]) == str(getattr(test_data, key))
                                
                except json.JSONDecodeError as e:
                    self.fail(f"JSON для {test_name} невалиден: {e}")
    
if __name__ == '__main__':
    unittest.main()