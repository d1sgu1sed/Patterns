from Dtos.storage_dto import storage_dto
from Src.Core.abstract import abstract
from Src.Core.validator import validator

class storage_model(abstract):
    """
    Модель склад.
    Представляет место хранения продуктов по номенклатуре.
    """
    
    """
    Наследование функции инициализации
    """
    def __init__(self, name = ""):
        super().__init__(name)

    """
    Фабричный метод из Dto
    """
    @staticmethod
    def from_dto(dto:storage_dto, cache:dict):
        validator.validate(dto, storage_dto)
        item = storage_model()
        item.name = dto.name
        item.unique_code = dto.id
        return item

    """
    Функция перевода объекта в DTO
    """
    def to_dto(self):
        item = storage_dto()
        item.name = self.name
        item.id = self.unique_code
        return item
    
    """
    
    """
    @staticmethod
    def create(name):
        return storage_model(name)