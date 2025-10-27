from Src.Core.abstract_converter import abstract_converter
from Src.Core.validator import validator
from Src.Core.abstract import abstract

class reference_converter(abstract_converter):
    """
    Конвертер для моделей
    """

    @staticmethod
    def convert(data):
        validator.validate(data, abstract)

        return data.to_dto()