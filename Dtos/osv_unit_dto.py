from datetime import datetime
from Src.Core.abstract_dto import abstract_dto


class osv_unit_dto(abstract_dto):
    """
    Модель элемента ОСВ (dto) 
    """

    __nomenclature_id: str = ""
    __measure_id: str = ""
    __start_amount: float = 0
    __finish_amount: float = 0
    __add: float = 0
    __sub: float = 0

    @property
    def nomenclature_id(self):
        return self.__nomenclature_id

    @property
    def measure_id(self):
        return self.__measure_id

    @property
    def start_amount(self):
        return self.__start_amount

    @property
    def finish_amount(self):
        return self.__finish_amount

    @property
    def add(self):
        return self.__add

    @property
    def sub(self):
        return self.__sub
    
    @nomenclature_id.setter
    def nomenclature_id(self, value: str):
        self.__nomenclature_id = value

    @measure_id.setter
    def measure_id(self, value: str):
        self.__measure_id = value

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