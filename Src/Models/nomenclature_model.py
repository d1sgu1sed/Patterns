from Dtos.nomeclature_dto import nomenclature_dto
from Src.Core.validator import validator
from Src.Core.abstract import abstract
from Src.Models.nomenclature_group_model import nomenclature_group_model
from Src.Models.measure_model import measure_model

class nomenclature_model(abstract):
    """
    Модель номенклатура.
    
    Поля:
        full_name (str): Полное наименование, до 255 символов.
        group (nomenclature_group_model): Группа, к которой относится продукт.
        measure (measure_model): Единица измерения.
    """

    __full_name: str = ""
    __group: nomenclature_group_model
    __measure: measure_model

    def __init__(self, name: str, group: nomenclature_group_model, measure: measure_model):
        super().__init__(name)
        validator.validate(group, nomenclature_group_model)
        validator.validate(measure, measure_model)
        self.__group = group
        self.__measure = measure

    """
    full_name (str): Полное наименование, до 255 символов 
    """
    @property
    def full_name(self) -> str:
        return self.__full_name
    
    """
    group (nomenclature_group_model): Группа, к которой относится продукт.
    """
    @property
    def group(self) -> nomenclature_group_model:
        return self.__group
    
    """
    measure (measure_model): Единица измерения.
    """
    @property
    def measure(self) -> measure_model:
        return self.__measure
    
    @full_name.setter
    def full_name(self, value: str):
        # validator.validate(value, str, 255)
        self.__full_name = value
    
    @group.setter
    def group(self, value: nomenclature_group_model):
        validator.validate(value, nomenclature_group_model)
        self.__group = value

    @measure.setter
    def measure(self, value: measure_model):
        validator.validate(value, measure_model)
        self.__measure = value

    """
    Фабричный метод создания номенклатуры
    """
    @staticmethod
    def create(name: str, group: nomenclature_group_model, measure: measure_model):
        validator.validate(name, str, 50)
        item = nomenclature_model(name, group, measure)
        
        return item
    
    """
    Фабричный метод из Dto
    """
    @staticmethod
    def from_dto(dto:nomenclature_dto, cache:dict):
        validator.validate(dto, nomenclature_dto)
        validator.validate(cache, dict)
        measure = cache.get(dto.measure_id, None)
        group = cache.get(dto.group_id, None)
        item = nomenclature_model.create(dto.name, group, measure)
        item.unique_code = dto.id
        return item
    
    """
    Функция перевода объекта в DTO
    """
    def to_dto(self):
        item = nomenclature_dto()
        item.name = self.name
        item.group_id = self.__group.unique_code
        item.measure_id = self.__measure.unique_code
        item.id = self.unique_code
        return item