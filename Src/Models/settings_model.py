from Src.Models.company_model import company_model
from Src.Core.validator import validator
from Src.Core.response_format import response_formats

class settings_model:
    """
    Контейнер настроек приложения.
    
    Поля:
        company (company_model): Настройки организации.
    """
    __company: company_model = company_model()
    __response_format: str = ""

    """
    company (company_model): Настройки организации.
    """
    @property
    def company(self):
        return self.__company

    @company.setter
    def company(self, value: company_model):
        validator.validate(value, company_model)
        self.__company = value

    @property
    def response_format(self):
        return self.__response_format

    @response_format.setter
    def response_format(self, value: str):
        validator.validate(value, str)
        self.__response_format = value

    def __init__(self, is_default=True):
        if(is_default):
            self.default()
        
    def default(self):
        self.__company.__name = ""
        self.__company.__INN = 129741029323
        self.__company.__account = 12309184023
        self.__company.__correspondent_acc = 93029318293
        self.__company.__BIK = 129031223
        self.__company.__type_of_property = "33333"
        self.__response_format = response_formats.md()

    @staticmethod
    def company_attrs():
        return [attr for attr in dir(company_model) if not attr.startswith('_') and attr != 'unique_code']
            

