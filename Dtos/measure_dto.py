from Src.Core.abstract_dto import abstract_dto

# Модель единицы измерения (dto)
# Пример
#                "name":"Грамм",
#                "id":"adb7510f-687d-428f-a697-26e53d3f65b7",
#                "base_id":null,
#                "value":1
class measure_dto(abstract_dto):
    __base_id:str = None
    __value:float = 1.0

    @property
    def base_id(self) -> str:
        return self.__base_id    
    
    @base_id.setter
    def base_id(self, value: str):
        self.__base_id = value

    @property
    def value(self) -> int:
        return self.__value    
    
    @value.setter
    def value(self, value: float|int):
        self.__value = float(value)