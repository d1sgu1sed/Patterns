from Src.Core.abstract_converter import abstract_converter
from Src.Core.validator import validator
from datetime import datetime

class datetime_converter(abstract_converter):
    """
    Конвертер для даты
    """

    @staticmethod
    def convert(data):
        validator.validate(data, datetime)

        return data.strftime("%Y-%m-%d %H:%M:%S")