from src.models.CompanyModel import CompanyModel
class Settings:
    __model: CompanyModel = CompanyModel()

    @property
    def model(self):
        return self.__model

    @model.setter
    def model(self, value: CompanyModel):
        self.__model = value

    def __init__(self):
        self.__model.__name = ""
        self.__model.__INN = 129741029323
        self.__model.__account = 12309184023
        self.__model.__correspondent_acc = 93029318293
        self.__model.__BIK = 129031223
        self.__model.__type_of_property = "33333"

    def company_attrs(self):
        return ['name', 'INN', 'account', 
                'correspondent_acc', 'BIK', 'type_of_property']
            

