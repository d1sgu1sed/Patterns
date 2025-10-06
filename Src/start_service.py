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

    def __init__(self):
        self.__reposity.data[reposity.measure_key] = {}
        self.__reposity.data[reposity.groups_key] = {}
        self.__reposity.data[reposity.nomenclature_key] = {}
        self.__reposity.data[reposity.recipies_steps_key] = {}
        self.__reposity.data[reposity.ingredients_key] = {}
        self.__reposity.data[reposity.recipies_key] = {}

    """
    Реализация Singleton
    """
    def __new__(cls):
        if not cls.__instance:
            cls.__instance = super(start_service, cls).__new__(cls)
        return cls.__instance
    
    @property
    def reposity(self):
        return self.__reposity
    
    def default_create_measure(self):
        measures = reposity.measure_key
        self.__reposity.data[measures]['гр'] = measure_model.create_gr()
        self.__reposity.data[measures]['кг'] = measure_model.create_kg()
        self.__reposity.data[measures]['шт'] = measure_model.create_pcs()
        self.__reposity.data[measures]['л'] = measure_model.create_l()
        self.__reposity.data[measures]['мл'] = measure_model.create_ml()

    def default_create_groups(self):
        groups = reposity.groups_key

        # Животного происхождения
        self.__reposity.data[groups]['Животного происхождения'] = \
            nomenclature_group_model.create_animal_product()
        # Бакалея
        self.__reposity.data[groups]['Бакалея'] = \
            nomenclature_group_model.create_grocery()
        # Пищевые добавки
        self.__reposity.data[groups]['Пищевые добавки'] = \
            nomenclature_group_model.create_supplements()
    
    def default_create_nomenclature(self):
        nomenclature = reposity.nomenclature_key
        
        # Сахар
        self.__reposity.data[nomenclature]['Сахар'] = \
            nomenclature_model.create_sugar()
        # Масло
        self.__reposity.data[nomenclature]['Сливочное масло'] = \
            nomenclature_model.create_butter()
        # Яйца
        self.__reposity.data[nomenclature]['Яйцо куриное'] = \
            nomenclature_model.create_egg()
        # Мука
        self.__reposity.data[nomenclature]['Мука пшеничная'] = \
            nomenclature_model.create_flour()
        # Ванилин
        self.__reposity.data[nomenclature]['Ванилин'] = \
            nomenclature_model.create_vanilin()
    
    def create_default_ingredients(self):
        ingredients = reposity.ingredients_key
        
        # Сахар
        self.__reposity.data[ingredients]['Сахар'] = \
            ingredient_model.create_sugar(80)
        # Сливочное масло 
        self.__reposity.data[ingredients]['Сливочное масло'] = \
            ingredient_model.create_butter(70)
        # Пшеничная мука
        self.__reposity.data[ingredients]['Пшеничная мука'] = \
            ingredient_model.create_flour(100)
        # Яйцо куриное
        self.__reposity.data[ingredients]['Яйцо куриное'] = \
            ingredient_model.create_egg(1)
        # Ванилин
        self.__reposity.data[ingredients]['Ванилин'] = \
            ingredient_model.create_vanilin(5)

    def create_default_receipt_steps(self):
        steps = reposity.recipies_steps_key
        self.__reposity.data[steps]['Вафли'] = recipe_step_model.create_waffles_step_list()
        
    def create_default_receipt(self):
        recipies_key = reposity.recipies_key
        self.__reposity.data[recipies_key]['Вафли'] = recipe_model.create_waffles()
        
    def start(self):
        self.default_create_measure()
        self.default_create_groups()
        self.default_create_nomenclature()
        self.create_default_ingredients()
        self.create_default_receipt_steps()
        self.create_default_receipt()