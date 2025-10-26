from Dtos.ingredient_dto import ingredient_dto
from Src.Core.abstract_dto import abstract_dto
from Src.Core.validator import validator
from Src.Core.abstract import abstract
from Src.Models.measure_model import measure_model
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
    __measure: measure_model

    def __init__(self, product: nomenclature_model, amount: float|int, measure: measure_model):
        super().__init__(product.name)
        validator.validate(product, nomenclature_model)
        validator.validate(amount, float|int)
        validator.validate(measure, measure_model)
        self.__amount = float(amount)
        self.__product = product 
        self.__measure = measure
    
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
    
    """
    Единица измерения 
    """
    @property
    def measure(self):
        return self.__measure
    
    @product.setter
    def product(self, value: nomenclature_model):
        validator.validate(value, nomenclature_model)
    
    @amount.setter
    def amount(self, value: float|int):
        validator.validate(value, float|int)
        self.__amount = float(value)

    @measure.setter
    def measure(self, value: measure_model):
        validator.validate(value, measure_model)

    """
    Фабричный метод для создания
    """
    @staticmethod
    def create(nomenclature: nomenclature_model, amount: float|int, measure: measure_model):
        validator.validate(nomenclature, nomenclature_model)
        validator.validate(amount, float|int)
        validator.validate(measure, measure_model)
        
        item = ingredient_model(nomenclature, amount, measure)
        return item
    
    """
    Фабричный метод из Dto
    """
    @staticmethod
    def from_dto(dto:ingredient_dto, cache:dict):
        validator.validate(dto, ingredient_dto)
        validator.validate(cache, dict)
        measure = cache.get(dto.measure_id, None)
        nomenclature = cache.get(dto.nomenclature_id, None)
        amount = dto.value
        item = ingredient_model.create(nomenclature, amount, measure)
        if dto.id == "":
            dto.id = item.unique_code
        return item
    

    """
    Функция перевода объекта в DTO
    """
    def to_dto(self):
        item = ingredient_dto()
        item.id = self.unique_code
        item.measure_id = self.__measure.unique_code
        item.value = self.__amount
        item.nomenclature_id = self.__product.unique_code
        return item