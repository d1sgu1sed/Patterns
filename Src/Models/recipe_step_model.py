from Src.Core.validator import validator
from Src.Core.abstract import abstract

class recipe_step_model(abstract):
    """
    Модель описания шага рецепта

    Поля:
        description(str): Шаг рецепта, до 1024 символов. Можно указывать параметры внутри строки при
                          помощи фигурных скобок (Например: {0} или {name}).
        params(list|dict): Значения, подставляющиеся в плейсхолдер строки description.
    """
    __description: str
    __params: list = None

    def __init__(self, description:str = "", params: list|dict = None, name = ""):
        super().__init__(name)
        self.__description = description
        if params is not None:
            validator.validate(params, list|dict)
            self.__params = params

    """
    Параметры
    """
    @property
    def params(self):
        return self.__params
    
    """
    Описание рецепты
    """
    @property
    def description(self):
        return self.__description
    
    @params.setter
    def params(self, value: list|dict):
        validator.validate(value, list|dict)
        self.__params = value
    
    @description.setter
    def description(self, value: str):
        validator.validate(value, str, 1024)
        self.__description = value

    """
    Фабричный метод создания шага рецепта
    """
    @staticmethod
    def create(description: str, params: list|dict = None):
        # validator.validate(description, str, 1024)
        
        item = recipe_step_model()
        item.description = description

        if params is not None:
            validator.validate(params, list|dict)
            item.params = params

        return item