from Src.Core.abstract_response import abstract_response
from Src.Logics.response_json import response_json
from Src.Logics.response_md import response_md
from Src.Logics.response_csv import response_csv
from Src.Logics.response_xlsx import response_xlsx
from Src.Core.validator import operation_exception

class factory_entities:
    __match = {
        "csv": response_csv,
        "md": response_md,
        "json": response_json,
        "xlsx": response_xlsx
    }

    # Получить нужный тип
    def create(self, format:str) -> abstract_response:
        if format not in self.__match.keys():
            raise operation_exception("Формат неверный")
        
        return self.__match[format]