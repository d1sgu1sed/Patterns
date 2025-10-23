from Src.Core.response_format import response_formats
from Src.Core.abstract_response import abstract_response
from Src.Logics.response_json import response_json
from Src.Logics.response_md import response_md
from Src.Logics.response_csv import response_csv
from Src.Logics.response_xml import response_xml
from Src.Core.validator import operation_exception
from Src.Models.settings_model import settings_model

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

    """
    Создает объект ответа по умолчанию на основе настроек
    """
    def create_default(self, settings: settings_model):
        if settings is None:
            raise operation_exception("Настройки не представлены в FactoryEntities!")
        fmt = settings.response_format
        return self.create(fmt)