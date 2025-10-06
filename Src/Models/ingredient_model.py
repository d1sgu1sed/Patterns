from Src.Core.validator import validator
from Src.Core.abstract import abstract
from Src.Models.nomenclature_model import nomenclature_model

class ingredient_model(abstract):
    __amount: float
    __product: nomenclature_model
    _instances = {}

    def __init__(self, product: nomenclature_model, amount: float|int):
        super().__init__(product.name)
        validator.validate(product, nomenclature_model)
        validator.validate(amount, float|int)
        self.__amount = float(amount)
        self.__product = product 
    
    @property
    def product(self):
        return self.__product
    
    @property
    def amount(self):
        return self.__amount
    
    @product.setter
    def product(self, value: nomenclature_model):
        validator.validate(value, nomenclature_model)
    
    @amount.setter
    def amount(self, value: float|int):
        validator.validate(value, float|int)
        self.__amount = float(value)

    @staticmethod
    def create_sugar(amount: float|int):
        return ingredient_model.create(nomenclature_model.create_sugar(), amount)
    
    @staticmethod
    def create_butter(amount: float|int):
        return ingredient_model.create(nomenclature_model.create_butter(), amount)
    
    @staticmethod
    def create_flour(amount: float|int):
        return ingredient_model.create(nomenclature_model.create_flour(), amount)
    
    @staticmethod
    def create_egg(amount: float|int):
        return ingredient_model.create(nomenclature_model.create_egg(), amount)
    
    @staticmethod
    def create_vanilin(amount: float|int):
        return ingredient_model.create(nomenclature_model.create_vanilin(), amount)

    @staticmethod
    def create(nomenclature: nomenclature_model, amount: float|int):
        validator.validate(nomenclature, nomenclature_model)
        validator.validate(amount, float|int)
        name = nomenclature.name + '_' + str(float(amount))
        if name in ingredient_model._instances.keys():
            return ingredient_model._instances[name]
        item = ingredient_model(nomenclature, amount)
        ingredient_model._instances[name] = item
        return item
    