from datetime import datetime
from Src.Core.abstract_dto import abstract_dto
from Src.Core.validator import validator
from Src.Models.osv_unit_model import osv_unit_model


class osv_dto(abstract_dto):
    """
    Модель ОСВ (dto)
    """

    __storage_id: str
    __start_date: datetime
    __finish_date: datetime
    __units: list = []

    @property
    def storage_id(self):
        return self.__storage_id

    @property
    def start_date(self):
        return self.__start_date

    @property
    def finish_date(self):
        return self.__finish_date

    @property
    def units(self) -> list:
        return self.__units
    
    @storage_id.setter
    def storage_id(self, value: str):
        self.__storage_id = value

    @start_date.setter
    def start_date(self, value: str):
        validator.validate(value, str|datetime)
        if isinstance(value, str):
            self.__start_date = datetime.strptime(value, "%d-%m-%Y %H:%M:%S")
        if isinstance(value, datetime):
            self.__start_date = value

    @finish_date.setter
    def finish_date(self, value: str):
        validator.validate(value, str|datetime)
        if isinstance(value, str):
            self.__finish_date = datetime.strptime(value, "%d-%m-%Y %H:%M:%S")
        if isinstance(value, datetime):
            self.__finish_date = value

    @units.setter
    def units(self, value: list):
        validator.validate(value, list)
        for unit in value:
            validator.validate(unit, osv_unit_model)
        self.__units = value