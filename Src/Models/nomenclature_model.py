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

    __full_name: str
    __group: nomenclature_group_model
    __measure: measure_model
    _instances = {}

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
        validator.validate(value, str, 255)
        self.__full_name = value
    
    @group.setter
    def group(self, value: nomenclature_group_model):
        validator.validate(value, nomenclature_group_model)
        self.__group = value

    @measure.setter
    def measure(self, value: measure_model):
        validator.validate(value, measure_model)
        self.__measure = value

    @staticmethod
    def create_sugar():
        name = 'Сахар'
        group = nomenclature_group_model.create_grocery()
        measure = measure_model.create_gr()
        return nomenclature_model.create(name, group, measure)
    
    @staticmethod
    def create_butter():
        name = 'Сливочное масло'
        group = nomenclature_group_model.create_animal_product()
        measure = measure_model.create_gr()
        return nomenclature_model.create(name, group, measure)
    
    @staticmethod
    def create_egg():
        name = 'Яйцо куриное'
        group = nomenclature_group_model.create_animal_product()
        measure = measure_model.create_pcs()
        return nomenclature_model.create(name, group, measure)
    
    @staticmethod
    def create_flour():
        name = 'Мука пшеничная'
        group = nomenclature_group_model.create_grocery()
        measure = measure_model.create_gr()
        return nomenclature_model.create(name, group, measure)
    
    @staticmethod
    def create_vanilin():
        name = 'Ванилин'
        group = nomenclature_group_model.create_supplements()
        measure = measure_model.create_gr()
        return nomenclature_model.create(name, group, measure)

    """
    Фабричный метод создания номенклатуры
    """
    @staticmethod
    def create(name: str, group: nomenclature_group_model, measure: measure_model):
        validator.validate(name, str, 50)
        if name in nomenclature_model._instances.keys():
            return nomenclature_model._instances[name]
        item = nomenclature_model(name, group, measure)
        nomenclature_model._instances[name] = item
        return item