from datetime import datetime
from Src.Core.abstract import abstract
from Src.Core.validator import validator
from Src.Models.measure_model import measure_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.storage_model import storage_model


class balance_model(abstract):
    """
    Модель остатка по номенклатуре на складе.

    Поля:
        nomenclature (nomenclature_model): Номенклатура продукта.
        storage (storage_model): Склад, на котором хранится продукт.
        measure (measure_model): Единица измерения остатка.
        amount (float): Количество продукта в указанной единице измерения.
        date (datetime): Дата, на которую рассчитан остаток.
    """

    __nomenclature: nomenclature_model
    __storage: storage_model
    __measure: measure_model
    __amount: float
    __date: datetime

    """
    Наследование функции инициализации
    """
    def __init__(self, name: str = ""):
        super().__init__(name)

    """
    measure (measure_model): Единица измерения остатка.
    """
    @property
    def measure(self) -> measure_model:
        return self.__measure
    
    @measure.setter
    def measure(self, value: measure_model):
        validator.validate(value, measure_model)
        self.__measure = value

    """
    amount (float): Количество продукта в указанной единице измерения.
    """
    @property
    def amount(self) -> float:
        return self.__amount
    
    @amount.setter
    def amount(self, value: float | int):
        validator.validate(value, (float, int))
        self.__amount = float(value)

    """
    nomenclature (nomenclature_model): Номенклатура продукта, для которого рассчитан остаток.
    """
    @property
    def nomenclature(self) -> nomenclature_model:
        return self.__nomenclature
    
    @nomenclature.setter
    def nomenclature(self, value: nomenclature_model):
        validator.validate(value, nomenclature_model)
        self.__nomenclature = value

    """
    storage (storage_model): Склад, на котором хранится продукт.
    """
    @property
    def storage(self) -> storage_model:
        return self.__storage
    
    @storage.setter
    def storage(self, value: storage_model):
        validator.validate(value, storage_model)
        self.__storage = value

    """
    date (datetime): Дата, на которую рассчитан остаток.
    """
    @property
    def date(self) -> datetime:
        return self.__date
    
    @date.setter
    def date(self, value: datetime):
        validator.validate(value, datetime)
        self.__date = value
