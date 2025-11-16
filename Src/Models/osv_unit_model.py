from datetime import datetime
from Dtos.osv_unit_dto import osv_unit_dto
from Dtos.storage_dto import storage_dto
from Src.Core.abstract import abstract
from Src.Core.validator import validator
from Src.Models.measure_model import measure_model
from Src.Models.nomenclature_model import nomenclature_model

class osv_unit_model(abstract):
    """
    Модель элемента ОСВ.
    Представляет информацию об изменении количества конкретного продукта.
    """
    __nomenclature: nomenclature_model
    __measure: measure_model
    __start_amount: float
    __finish_amount: float
    __add: float
    __sub: float


    """
    Наследование функции инициализации
    """
    def __init__(self, name = ""):
        super().__init__(name)

    """
    Единица измерения
    """
    @property
    def measure(self) -> measure_model:
        return self.__measure
    
    """
    Продукт номенклатуры
    """
    @property
    def nomenclature(self) -> nomenclature_model:
        return self.__nomenclature
    
    """
    Начальное количество
    """
    @property
    def start_amount(self) -> float:
        return self.__start_amount
    
    """
    Конечное количество
    """
    @property
    def finish_amount(self) -> float:
        return self.__finish_amount
    
    """
    Приход
    """
    @property
    def add(self) -> float:
        return self.__add
    
    """
    Расход
    """
    @property
    def sub(self) -> float:
        return self.__sub

    @nomenclature.setter
    def nomenclature(self, value: nomenclature_model):
        self.__nomenclature = value
    
    @measure.setter
    def measure(self, value: measure_model):
        self.__measure = value

    @start_amount.setter
    def start_amount(self, value: float):
        self.__start_amount = value

    @finish_amount.setter
    def finish_amount(self, value: float):
        self.__finish_amount = value
    
    @add.setter
    def add(self, value: float):
        self.__add = value
    
    @sub.setter
    def sub(self, value: float):
        self.__sub = value

    """
    Фабричный метод создания модели элемента ОСВ
    """
    @staticmethod
    def create(nomenclature:nomenclature_model, measure: measure_model, 
               start_amount: float, finish_amount: float,
               add: float, sub: float):
        item = osv_unit_model()
        item.measure = measure
        item.nomenclature = nomenclature
        item.start_amount = start_amount
        item.finish_amount = finish_amount
        item.add = add
        item.sub = sub
        return item
    
    """
    Создание дефолтной модели элемента ОСВ
    """
    @staticmethod
    def create_default(name: str,
                       nomenclature:nomenclature_model,
                       measure: measure_model):
        item = osv_unit_model(name)
        item.measure = measure
        item.nomenclature = nomenclature
        item.start_amount = 0.0
        item.finish_amount = 0.0
        item.add = 0.0
        item.sub = 0.0
        return item

    """
    Фабричный метод из Dto
    """
    @staticmethod
    def from_dto(dto:osv_unit_dto, cache:dict):
        validator.validate(dto, osv_unit_dto)
        item = osv_unit_model()
        item.name = dto.name
        item.unique_code = dto.id
        item.nomenclature = cache.get(dto.nomenclature_id, None)
        item.measure = cache.get(dto.measure_id, None)
        item.sub = dto.sub
        item.add = dto.add
        item.finish_amount = dto.finish_amount
        item.start_amount = dto.start_amount
        return item

    """
    Функция перевода объекта в DTO
    """
    def to_dto(self):
        item = osv_unit_dto()
        item.name = self.__nomenclature.name
        item.id = self.unique_code
        item.nomenclature_id = self.__nomenclature.unique_code
        item.measure_id = self.__measure.unique_code
        item.sub = self.__sub
        item.add = self.__add
        item.finish_amount = self.__finish_amount
        item.start_amount = self.__start_amount

        return item