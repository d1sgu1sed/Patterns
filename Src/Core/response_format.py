from Src.Logics.response_csv import response_csv
from Src.Logics.response_json import response_json
from Src.Logics.response_md import response_md
from Src.Logics.response_xml import response_xml


class response_formats:
    """
    Класс, который возвращает 
    """

    @staticmethod
    def csv() -> str:
        return "csv"
    
    @staticmethod
    def xml() -> str:
        return "xml"
    
    @staticmethod
    def md() -> str:
        return "md"
    
    @staticmethod
    def json() -> str:
        return "json"
    
    @staticmethod
    def get_formats() -> dict:
        result = {}
        for func in dir(response_formats):
            if not func.startswith('_') and func.find('get') == -1:
                format = getattr(response_formats, func)()
                result[format] = globals()[f'response_{format}']
        return result