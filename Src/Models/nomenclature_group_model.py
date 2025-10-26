from Dtos.nomenclature_group_dto import nomenclature_group_dto
from Src.Core.abstract import abstract
from Src.Core.abstract_dto import abstract_dto
from Src.Core.validator import validator

class nomenclature_group_model(abstract):
    """
    Модель группа номенклатуры. 
    Предназначена для классификации номенклатуры по группам и категориям.
    """
    
    """
    Наследование функции инициализации
    """
    def __init__(self, name = ""):
        super().__init__(name)

    @staticmethod
    def create(name: str):
        validator.validate(name, str, 50)
        item = nomenclature_group_model(name)
        
        return item
    
    """
    Фабричный метод из Dto
    """
    @staticmethod
    def from_dto(dto:abstract_dto, cache:dict):
        item = nomenclature_group_model()
        item.name = dto.name
        item.unique_code = dto.id
        return item

    """
    Функция перевода объекта в DTO
    """
    def to_dto(self):
        item = nomenclature_group_dto()
        item.name = self.name
        item.id = self.unique_code
        return item