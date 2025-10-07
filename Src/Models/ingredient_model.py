from Src.Core.validator import validator
from Src.Core.abstract import abstract
from Src.Models.nomenclature_model import nomenclature_model

class ingredient_model(abstract):
    """
    Модель ингриедента для рецепта

    Поля:
        product (nomenclature_model): Продукт из номенклатуры.
        amount (float): Количество продукта
    """
    __amount: float
    __product: nomenclature_model
    _instances = {}

    def __init__(self, product: nomenclature_model, amount: float|int):
        super().__init__(product.name)
        validator.validate(product, nomenclature_model)
        validator.validate(amount, float|int)
        self.__amount = float(amount)
        self.__product = product 
    
    """
    Продукт
    """
    @property
    def product(self):
        return self.__product
    
    """
    Количество продукта
    """
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

    """
    Фабричный метод для создания
    """
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
    