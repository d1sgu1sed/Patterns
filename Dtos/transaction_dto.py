from Src.Core.abstract_dto import abstract_dto
from Src.Core.validator import validator
from datetime import datetime
from Src.Models.measure_model import measure_model
from Src.Models.nomenclature_group_model import nomenclature_group_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.storage_model import storage_model

class transaction_dto(abstract_dto):
    """
    Модель транзакции (dto)
    Пример:
        "amount": 3.0,
        "date": "2025-10-20 10:00:00",
        "id": "ji96c2b4-sda7-gh54-4hj3-jkhv3jc3",
        "measure_id": "f8346e8b-7260-4db8-a673-c8c826ab08b7",
        "name": "",
        "nomenclature_id": "3ce75449-05e8-4921-9310-9bcd0be7095b",
        "storage_id": "ndet5a2x-6f2a-nv5z-f561-md7vb421"
    """
    __date: datetime = None
    __nomenclature_id: str = None
    __storage_id: str = None
    __amount: float = 0
    __measure_id: str = None

    @property
    def date(self) -> datetime:
        return self.__date

    @date.setter
    def date(self, value):
        validator.validate(value, str|datetime)
        if isinstance(value, str):
            self.__date = datetime.strptime(value, "%d-%m-%Y %H:%M:%S")
        if isinstance(value, datetime):
            self.__date = value
            
    @property
    def nomenclature_id(self) -> str:
        return self.__nomenclature_id

    @nomenclature_id.setter
    def nomenclature_id(self, value: str):
        validator.validate(value, str)
        self.__nomenclature_id = value

    @property
    def storage_id(self) -> str:
        return self.__storage_id

    @storage_id.setter
    def storage_id(self, value: str):
        validator.validate(value, str)
        self.__storage_id = value

    @property
    def amount(self) -> float:
        return self.__amount

    @amount.setter
    def amount(self, value: float):
        validator.validate(value, float)
        self.__amount = value

    @property
    def measure_id(self) -> str:
        return self.__measure_id

    @measure_id.setter
    def measure_id(self, value: str):
        validator.validate(value, str)
        self.__measure_id = value
