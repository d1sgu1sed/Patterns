from Src.Core.validator import validator
from Src.Core.abstract import abstract
from Src.Models.nomenclature_group_model import nomenclature_group_model
from Src.Models.measure_model import measure_model

class nomenclature_model(abstract):
    __full_name: str
    __group: nomenclature_group_model
    __measure: measure_model

    def __init__(self, name: str, group: nomenclature_group_model, measure: measure_model):
        super().__init__(name)
        validator.validate(group, nomenclature_group_model)
        validator.validate(measure, measure_model)
        self.__group = group
        self.__measure = measure

    @property
    def full_name(self) -> str:
        return self.__full_name
    
    @property
    def group(self) -> nomenclature_group_model:
        return self.__group
    
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