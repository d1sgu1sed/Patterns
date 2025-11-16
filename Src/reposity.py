from Src.Core.validator import validator


class reposity:
    """
    Хранилище данных
    """
    __data: dict = {}
    __keys: list = []

    def __init__(self):
        keys = [key for key in self.__dir__() if key.endswith('_key')]
        for key in keys: 
            key_method = getattr(self, key)
            self.__keys.append(key_method())

    @property
    def data(self):
        return self.__data
    
    @property
    def keys(self):
        return self.__keys

    """
    Ключ для единий измерений
    """
    @staticmethod
    def measure_key():
        return 'measure'
    
    @staticmethod
    def groups_key():
        return 'groups'
    
    @staticmethod
    def nomenclature_key():
        return 'nomenclature'
    
    @staticmethod
    def ingredients_key():
        return 'ingredients'
    
    @staticmethod
    def recipies_steps_key():
        return 'recipe_steps'
    
    @staticmethod
    def recipes_key():
        return 'recipe'

    @staticmethod
    def storage_key():
        return "storage"

    @staticmethod
    def transaction_key():
        return "transaction"

    """
    Инициализация
    """
    def initalize(self):
        for key in self.__keys:
            self.__data[key] = []
