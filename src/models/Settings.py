class Settings:
    __name: str
    __INN: str
    __account: str
    __correspondent_acc: str
    __BIK: str
    __type_of_property: str

    def __init__(self):
        self.__name = ""
        self.__INN = "129741029323"
        self.__account = "12309184023"
        self.__correspondent_acc = "93029318293"
        self.__BIK = "129031223"
        self.__type_of_property = "33333"

    def attrs(self):
        return ['name', 'INN', 'account', 
                'correspondent_acc', 'BIK', 'type_of_property']

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
    def INN(self, value: str):
        if len(value) != 12:
            return
        
        self.__INN = value

    @name.setter
    def name(self, value: str):
        if value.strip() == '':
            return
        
        self.__name = value

    @account.setter
    def account(self, value: str):
        if len(value) != 11:
            return
        
        self.__account = value
    
    @correspondent_acc.setter
    def correspondent_acc(self, value: str):
        if len(value) != 11:
            return
        
        self.__correspondent_acc = value

    @BIK.setter
    def BIK(self, value: str):
        if len(value) != 9:
            return
        
        self.__BIK = value

    @type_of_property.setter
    def type_of_property(self, value: str):
        if len(value) != 5:
            return
        
        self.__type_of_property = value

    # def is_filled(self):
    #     for i in self.__dict__:
            

