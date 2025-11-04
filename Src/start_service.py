from datetime import datetime
import json
import os
from Dtos.ingredient_dto import ingredient_dto
from Dtos.measure_dto import measure_dto
from Dtos.nomenclature_group_dto import nomenclature_group_dto
from Dtos.nomeclature_dto import nomenclature_dto
from Dtos.storage_dto import storage_dto
from Dtos.transaction_dto import transaction_dto
from Src.Converters.convert_factory import convert_factory
from Src.Core.validator import argument_exception, operation_exception, validator
from Src.Models.osv_model import osv_model
from Src.Models.storage_model import storage_model
from Src.Models.transaction_model import transaction_model
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

                first_start = settings.get("first_start", False)
                if not first_start:
                    return True
                if "default_receipt" in settings.keys():
                    data = settings["default_receipt"]
                    if not(self.convert(data) and\
                        self.__convert_storages(settings) and\
                        self.__convert_transactions(settings)
                        ):
                        return False
                    return True

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
    
    # Загрузить склады
    def __convert_storages(self, data: dict) -> bool:
        validator.validate(data, dict)
        storages = data.get("storages", None)
        if storages is None or len(storages) == 0:
            return False
        for storage in storages:
            dto = storage_dto().create(storage)
            item = storage_model.from_dto(dto, self.__cache)
            self.__save_item(reposity.storage_key(), dto, item)

        return True       

    # Загрузить транзакции
    def __convert_transactions(self, data: dict) -> bool:
        validator.validate(data, dict)      
        transactions = data.get("transactions", None) 
        if transactions is None or len(transactions) == 0:
            return False
        for transaction in transactions:
            dto = transaction_dto().create(transaction)
            item = transaction_model.from_dto(dto, self.__cache)
            self.__save_item(reposity.transaction_key(), dto, item )

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
    Создание ОСВ
    """
    def create_osv(self, start: datetime, end: datetime, storage_id: str):
        data = self.__reposity.data
        transactions = data[reposity.transaction_key()]
        nomenclatures = data[reposity.nomenclature_key()]
        storage = self.__cache.get(storage_id, None)
        validator.validate(storage, storage_model)
        osv = osv_model.create(start, end, storage)
        osv.generate_units(transactions, nomenclatures)
        return osv
    
    """
    Вывод данных в файл
    """
    def dump(self, filename: str) -> bool:
        validator.validate(filename, str)
        try:
            data = {}
            converter = convert_factory()
            for key in reposity().keys:
                data[key] = []
                for i in self.__reposity.data[key]:
                    data[key].append(converter.convert(i))
            with open(filename, 'w', encoding="UTF-8") as file_instance:
                json.dump(data, file_instance, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            error_message = str(e)
            return False

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
