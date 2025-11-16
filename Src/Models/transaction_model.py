from datetime import datetime
from Dtos.transaction_dto import transaction_dto
from Src.Core.abstract import abstract
from Src.Core.validator import validator
from Src.Models.measure_model import measure_model
from Src.Models.nomenclature_group_model import nomenclature_group_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.storage_model import storage_model

class transaction_model(abstract):
    """
    Модель транзакции.
    Представляет единицу оборота продукции на складе.
    """
    
    __date: datetime
    __product: nomenclature_model
    __storage: storage_model
    __amount: float
    __measure: measure_model

    """
    Наследование функции инициализации
    """
    def __init__(self, name = ""):
        super().__init__(name)

    """
    Дата проведения транзакции
    """
    @property
    def date(self) -> datetime:
        return self.__date
    
    """
    Продукт из номенклатуры
    """
    @property
    def product(self) -> nomenclature_model:
        return self.__product
    
    """
    Склад транзакции
    """
    @property
    def storage(self) -> storage_model:
        return self.__storage
    
    """
    Количество продукта
    """
    @property
    def amount(self) -> float:
        return self.__amount
    
    """
    Единица измерения продукта в транзакции
    """
    @property
    def measure(self) -> measure_model:
        return self.__measure
    
    @date.setter
    def date(self, value: datetime):
        self.__date = value

    @product.setter
    def product(self, value: nomenclature_model):
        self.__product = value

    @storage.setter
    def storage(self, value: storage_model):
        self.__storage = value
    
    @amount.setter
    def amount(self, value: float):
        self.__amount = value

    @measure.setter
    def measure(self, value: measure_model):
        self.__measure = value

    """
    Фабричный метод создания модели транзакции
    """
    @staticmethod
    def create(date: datetime, product: nomenclature_model, 
               storage: storage_model, amount: float, 
               measure: measure_model) -> 'transaction_model':
        item = transaction_model()
        item.date = date
        item.product = product
        item.storage = storage
        item.amount = amount
        item.measure = measure
        return item
    
    """
    Фабричный метод из Dto
    """
    @staticmethod
    def from_dto(dto: transaction_dto, cache: dict):
        validator.validate(dto, transaction_dto)
        validator.validate(cache, dict)
        measure = cache.get(dto.measure_id, None)
        product = cache.get(dto.nomenclature_id, None)
        storage = cache.get(dto.storage_id, None)

        item = transaction_model.create(dto.date, product, storage, dto.amount, measure)
        if product is not None:
            item.name = product.name
        item.unique_code = dto.id
        return item
    
    """
    Функция перевода объекта в DTO
    """
    def to_dto(self):
        item = transaction_dto()
        item.name = self.__product.name
        item.nomenclature_id = self.__product.unique_code
        item.measure_id = self.__measure.unique_code
        item.id = self.unique_code
        item.storage_id = self.__storage.unique_code
        item.date = self.__date
        item.amount = self.__amount
        return item