from Src.Core.validator import validator


class reposity:
    """
    Хранилище данных
    """
    __data: dict = {}

    @property
    def data(self):
        return self.__data
    
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

    """
    Инициализация
    """
    def initalize(self):
        keys = [key for key in self.__dir__() if key.endswith('_key')]
        for key in keys:
            key_method = getattr(self, key)
            self.__data[key_method()] = []
