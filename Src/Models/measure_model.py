from Src.Core.validator import validator
from Src.Core.abstract import abstract

class measure_model(abstract):
    """
    Модель единица измерения.

    Поля:
        base_measure (measure_model | None): Базовая единица измерения.
        coef (float): Числовое отношение к базовой единице измерения.
    """
    __base_measure = None
    __coef: float

    def __init__(self, name: str, coef: float | int, base_measure = None):
        super().__init__(name)
        if base_measure is not None:
            validator.validate(base_measure, measure_model)
        validator.validate(coef, float | int)
        self.__base_measure = base_measure
        self.__coef = float(coef)

    """
    base_measure (measure_model | None): Базовая единица измерения.
    """
    @property
    def base_measure(self):
        return self.__base_measure
    
    """
    coef (float): Числовое отношение к базовой единице измерения.
    """
    @property
    def coef(self):
        return self.__coef
    
    @coef.setter
    def coef(self, value: float | int):
        validator.validate(value, float | int)
        self.__coef = float(value)
    
    @base_measure.setter
    def base_measure(self, value:str):
        validator.validate(value, str, 50)
        self.__base_measure = value
    
