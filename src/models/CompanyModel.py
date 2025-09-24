class CompanyModel:
    __name: str = ""
    __INN: int
    __account: int
    __correspondent_acc: int
    __BIK: int
    __type_of_property: str

    @property
    def INN(self):
        return self.__INN
    
    @property
    def name(self):
        return self.__name
    
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
        if len(str(value)) != 12:
            return
        
        self.__INN = value

    @name.setter
    def name(self, value: str):
        if value.strip() == '':
            return
        
        self.__name = value

    @account.setter
    def account(self, value: int):
        if len(str(value)) != 11:
            return
        
        self.__account = value
    
    @correspondent_acc.setter
    def correspondent_acc(self, value: int):
        if len(str(value)) != 11:
            return
        
        self.__correspondent_acc = value

    @BIK.setter
    def BIK(self, value: int):
        if len(str(value)) != 9:
            return
        
        self.__BIK = value

    @type_of_property.setter
    def type_of_property(self, value: str):
        if len(value) != 5:
            return
        
        self.__type_of_property = value