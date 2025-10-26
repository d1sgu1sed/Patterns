import abc
from Src.Core.common import common
from Src.Core.validator import validator, operation_exception


class abstract_dto:
    """
    Абстрактный класс для наследования только dto структур
    Поля:
        name (str): Название dto.
        id (str): id dto.
    """
    __name:str = ""
    __id:str = ""

    @property
    def name(self) ->str:
        return self.__name
    
    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def id(self) -> str:
        return self.__id

    @id.setter
    def id(self, value):
        self.__id = value   

    # Универсальный фабричный метод для загрузки dto из словаря
    def create(self, data) -> "abstract_dto":
        validator.validate(data, dict)
        fields = common.get_fields(self)
        matching_keys = list(filter(lambda key: key in fields, data.keys()))

        try:
            for key in matching_keys:
                setattr(self, key, data[key])
        except:
            raise operation_exception("Невозможно загрузить данные!")    

        return self