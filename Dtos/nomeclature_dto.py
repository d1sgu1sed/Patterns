from Src.Core.abstract_dto import abstract_dto
from Src.Core.validator import validator

# Модель номенклатуры (dto)
# Пример
#                "name":"Пшеничная мука",
#                "range_id":"a33dd457-36a8-4de6-b5f1-40afa6193346",
#                "category_id":"7f4ecdab-0f01-4216-8b72-4c91d22b8918",
#                "id":"0c101a7e-5934-4155-83a6-d2c388fcc11a"

class nomenclature_dto(abstract_dto):
    __measure_id:str = ""
    __nomenclature_model_id:str = ""


    @property
    def measure_id(self) -> str:
        return self.__measure_id

    @measure_id.setter
    def measure_id(self, value: str):
        validator.validate(value, str)
        self.__measure_id = value

    @property
    def nomenclature_model_id(self) -> str:
        return self.__nomenclature_model_id

    @nomenclature_model_id.setter
    def nomenclature_model_id(self, value: str):
        validator.validate(value, str)
        self.__nomenclature_model_id = value
