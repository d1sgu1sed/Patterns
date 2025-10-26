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
        text = instance.generate([data])
        with open(expected_filename, 'w', encoding='utf-8') as f:
            f.write(text)
        assert os.path.exists(expected_filename)
        
        # проверяем что содержимое корректное
        with open(expected_filename, 'r', encoding='utf-8') as f:
            file_content = f.read()
        
        assert text == file_content
        assert data.name in text
    
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
        text = instance.generate([data])
        # Записываем в файл
        with open(expected_filename, 'w', encoding='utf-8') as f:
            f.write(text)
        assert os.path.exists(expected_filename)
        
        # проверяем что содержимое корректное
        with open(expected_filename, 'r', encoding='utf-8') as f:
            file_content = f.read()
        
        assert text == file_content
        
        # проверяем что JSON валидный и содержит основные поля
        json_data = json.loads(text)['data'][0]
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
        text = instance.generate([data])
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
        assert data.name in text_normalized
    
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
        text = instance.generate([data])
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
        text = instance.generate([data])
        
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
            
            # Проверяем корневой элемент
            assert root.tag == "data"
            
            # Проверяем что есть дочерние элементы
            children = list(root)
            assert len(children) > 0
            
            # Ищем первый объект с данными рецепта
            recipe_obj = None
            for child in root:
                if child.tag == "obj":
                    recipe_obj = child
                    break
            
            assert recipe_obj is not None, "Не найден элемент obj с данными рецепта"
            
            # Проверяем наличие связанных данных (ингредиенты, шаги)
            ingredients_found = False
            steps_found = False
            
            for elem in recipe_obj.iter():
                if "ingredient" in elem.tag.lower():
                    ingredients_found = True
                elif "step" in elem.tag.lower() or "steps" in elem.tag.lower():
                    steps_found = True
            
            # Проверяем что есть хотя бы один ингредиент и шаг
            assert ingredients_found, "Не найдены ингредиенты"
            assert steps_found, "Не найдены шаги приготовления"
            
        except ET.ParseError as e:
            self.fail(f"Сгенерированный XML невалиден: {e}")

if __name__ == '__main__':
    unittest.main()