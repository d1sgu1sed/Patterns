from Src.Models.company_model import company_model
from Src.Core.validator import validator

class settings_model:
    """
    Контейнер настроек приложения.
    
    Поля:
        company (company_model): Настройки организации.
    """
    __company: company_model = company_model()

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

    def company_attrs(self):
        return ['name', 'INN', 'account', 
                'correspondent_acc', 'BIK', 'type_of_property']
            

