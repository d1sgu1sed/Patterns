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
    _instances = {}

    def __init__(self, name: str, coef: float | int = 1, base_measure = None):
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
    def base_measure(self, value):
        validator.validate(value, measure_model)
        self.__base_measure = value
    
    @staticmethod
    def create_kg():
        base_gr = measure_model.create_gr()
        return measure_model.create('килограмм', base_gr, 1000)

    @staticmethod
    def create_gr():
        return measure_model.create('грамм')
    
    @staticmethod
    def create_pcs():
        return measure_model.create('штука')
    
    @staticmethod
    def create_l():
        return measure_model.create('литр')
    
    @staticmethod
    def create_ml():
        base_l = measure_model.create_l()
        return measure_model.create('миллилитр', base_l, 0.001)

    @staticmethod
    def create(name: str, base = None, coef: float | int = 1):
        if name in measure_model._instances.keys():
            return measure_model._instances[name]
        inner_base = None
        item = measure_model(name)
        if base is not None:
            validator.validate(base, measure_model)
            inner_base = base
            item.base_measure = inner_base
        item.coef = coef
        measure_model._instances[name] = item
        return item
        
