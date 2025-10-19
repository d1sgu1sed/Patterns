from Src.Core.abstract_dto import abstract_dto

# Модель единицы измерения (dto)
# Пример
#       "nomenclature_id":"0c101a7e-5934-4155-83a6-d2c388fcc11a",
#       "range_id":"adb7510f-687d-428f-a697-26e53d3f65b7",
#       "value":100
class ingredient_dto(abstract_dto):
    __nomenclature_id: str = None
    __measure_id: str = None
    __value: float = 1.0

    @property
    def nomenclature_id(self) -> str:
        return self.__nomenclature_id    
    
    @nomenclature_id.setter
    def nomenclature_id(self, value: str):
        self.__nomenclature_id = value

    @property
    def measure_id(self) -> str:
        return self.__measure_id
    
    @measure_id.setter
    def measure_id(self, value: str):
        self.__measure_id = value

    @property
    def value(self) -> int:
        return self.__value    
    
    @value.setter
    def value(self, value: int|float):
        self.__value = float(value)