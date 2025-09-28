from Src.Core.validator import validator
from Src.Core.abstract import abstract

class company_model(abstract):
    __INN: int
    __account: int
    __correspondent_acc: int
    __BIK: int
    __type_of_property: str

    @property
    def INN(self):
        return self.__INN
    
    @property
    def account(self):
        return self.__account
    
    @property
    def correspondent_acc(self):
        return self.__correspondent_acc
    
    @property
    def BIK(self):
        return self.__BIK
    
    @property
    def type_of_property(self):
        return self.__type_of_property

    @INN.setter
    def INN(self, value: int):
        validator.validate(value, int, 12)
        self.__INN = value

    @account.setter
    def account(self, value: int):
        validator.validate(value, int, 11)        
        self.__account = value
    
    @correspondent_acc.setter
    def correspondent_acc(self, value: int):
        validator.validate(value, int, 11)        
        self.__correspondent_acc = value

    @BIK.setter
    def BIK(self, value: int):
        validator.validate(value, int, 9)
        self.__BIK = value

    @type_of_property.setter
    def type_of_property(self, value: str):
        validator.validate(value, str, 5)
        self.__type_of_property = value