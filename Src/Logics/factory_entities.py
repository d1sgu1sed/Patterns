from Src.Core.response_format import response_formats
from Src.Core.abstract_response import abstract_response
from Src.Logics.response_json import response_json
from Src.Logics.response_md import response_md
from Src.Logics.response_csv import response_csv
from Src.Logics.response_xlsx import response_xlsx
from Src.Core.validator import operation_exception

class factory_entities:
    """
    Фабричный класс для создания экземпляра ответа нужного типа
    """
    __formats = response_formats.get_formats()

    @property
    def formats(self):
        return self.__formats
    
    """
    Получить экземпляр класса нужного типа
    """ 
    def create(self, format:str) -> abstract_response:
        if format not in self.__formats.keys():
            raise operation_exception("Формат неверный")
        
        return self.__formats[format]