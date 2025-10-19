import json
import os
from Dtos.ingredient_dto import ingredient_dto
from Dtos.measure_dto import measure_dto
from Dtos.nomenclature_group_dto import nomenclature_group_dto
from Dtos.nomeclature_dto import nomenclature_dto
from Src.Core.validator import argument_exception, operation_exception, validator
from Src.reposity import reposity
from Src.Models.measure_model import measure_model
from Src.Models.nomenclature_group_model import nomenclature_group_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.ingredient_model import ingredient_model
from Src.Models.recipe_model import recipe_model
from Src.Models.recipe_step_model import recipe_step_model

class start_service:
    __reposity: reposity = reposity()
    __instance = None
    __default_recipe: recipe_model
    __filename: str = ""
    __cache = {}

    def __init__(self):
        self.__reposity.initalize()

    """
    Реализация Singleton
    """
    def __new__(cls):
        if not cls.__instance:
            cls.__instance = super(start_service, cls).__new__(cls)
        return cls.__instance
    
    """
    Хранилище
    """
    @property
    def reposity(self):
        return self.__reposity
    
    """
    Название файла
    """
    @property
    def filename(self) -> str:
        return self.__filename

    """
    Полный путь к файлу настроек
    """
    @filename.setter
    def filename(self, value:str):
        validator.validate(value, str)
        full_filename = os.path.abspath(value)        
        if os.path.exists(full_filename):
            self.__filename = full_filename.strip()
        else:
            raise argument_exception(f'Не найден файл настроек {full_filename}')
        
    """
    Функция загрузки рецепта из файла
    """
    def load(self) -> bool:
        if self.__filename == "":
            raise operation_exception("Не найден файл настроек!")

        try:
            with open(self.__filename, 'r') as file_instance:
                settings = json.load(file_instance)

                if "default_receipt" in settings.keys():
                    data = settings["default_receipt"]
                    return self.convert(data)

            return False
        except Exception as e:
            error_message = str(e)
            return False
    
    # Загрузить единицы измерений   
    def __convert_measures(self, data: dict) -> bool:
        validator.validate(data, dict)
        ranges = data.get('measures', [])
        if len(ranges) == 0:
            return False
         
        for range in ranges:
            dto = measure_dto().create(range)
            item = measure_model.from_dto(dto, self.__cache)
            self.__save_item(reposity.measure_key(), dto, item)

        return True

    # Загрузить группы номенклатуры
    def __convert_groups(self, data: dict) -> bool:
        validator.validate(data, dict)
        nomenclature_groups = data.get('nomenclature_groups', [])
        if len(nomenclature_groups) == 0:
            return False

        for groups in nomenclature_groups:
            dto = nomenclature_group_dto().create(groups)    
            item = nomenclature_group_model.from_dto(dto, self.__cache)
            self.__save_item(reposity.groups_key(), dto, item)

        return True

    # Загрузить номенклатуру
    def __convert_nomenclatures(self, data: dict) -> bool:
        validator.validate(data, dict)
        nomenclatures = data.get('nomenclatures', [])
        if len(nomenclatures) == 0:
            return False
         
        for nomenclature in nomenclatures:
            dto = nomenclature_dto().create(nomenclature)
            item = nomenclature_model.from_dto(dto, self.__cache)
            self.__save_item(reposity.nomenclature_key(), dto, item)

        return True
    
    # Загрузить ингредиенты
    def __convert_ingredients(self, data: dict) -> bool:
        validator.validate(data, dict)
        ingredients = data.get('ingredients', [])
        if len(ingredients) == 0:
            return False
         
        for ingredient in ingredients:
            dto = ingredient_dto().create(ingredient)
            item = ingredient_model.from_dto(dto, self.__cache)
            self.__save_item(reposity.ingredients_key(), dto, item)

        return True
    
    # Обработать полученный словарь    
    def convert(self, data: dict) -> bool:
        validator.validate(data, dict)

        # 1 Созданим рецепт
        name = data.get('name', 'Неизвестно')
        remark = data.get('remark', '')

        # Загрузим шаги приготовления
        steps = data.get('steps', [])
        validated_steps = []
        for step in steps:
            step_model = None
            if isinstance(step, list):
                step_model = recipe_step_model.create(step[0], step[1])
            else:
                step_model = recipe_step_model.create(step)
            
            validated_steps.append(step_model)
            self.__reposity.data[reposity.recipies_steps_key()].append(step_model)


        self.__convert_measures(data)
        self.__convert_groups(data)
        self.__convert_nomenclatures(data)
        self.__convert_ingredients(data)

        ingredients = self.__reposity.data[reposity.ingredients_key()]
        self.__default_recipe = recipe_model.create(name, validated_steps, ingredients, remark)
        # Сохраняем рецепт
        self.__reposity.data[reposity.recipes_key()].append(self.__default_recipe)
        return True
       
    """
    Сохранить элемент в репозитории
    """
    def __save_item(self, key:str, dto, item):
        validator.validate(key, str)
        item.unique_code = dto.id
        self.__cache.setdefault(dto.id, item)
        self.__reposity.data[key].append(item)

    def start(self):
        self.__filename = "settings.json"
        result = self.load()
        if not result:
            raise operation_exception("Невозможно сформировать стартовый набор данных!")
