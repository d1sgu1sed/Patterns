from Src.Core.abstract_converter import abstract_converter
from Src.Core.validator import validator

class basic_converter(abstract_converter):
    """
    Конвертер для строк и чисел
    """

    @staticmethod
    def convert(data):
        
        return data