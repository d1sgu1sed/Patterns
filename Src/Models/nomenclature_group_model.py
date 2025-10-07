from Src.Core.abstract import abstract
from Src.Core.validator import validator

class nomenclature_group_model(abstract):
    """
    Модель группа номенклатуры. 
    Предназначена для классификации номенклатуры по группам и категориям.
    """
    _instances = {}
    
    """
    Наследование функции инициализации
    """
    def __init__(self, name = ""):
        super().__init__(name)

    @staticmethod
    def create(name: str):
        validator.validate(name, str, 50)
        if name in nomenclature_group_model._instances.keys():
            return nomenclature_group_model._instances[name]
        item = nomenclature_group_model(name)
        nomenclature_group_model._instances[name] = item
        return item
