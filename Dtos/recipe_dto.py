from Src.Core.abstract_dto import abstract_dto
from Src.Models.ingredient_model import ingredient_model
from Src.Models.recipe_step_model import recipe_step_model
from Src.Core.validator import validator

class recipe_dto(abstract_dto):
    """
    Модель рецепта (dto)
    Пример
        "name": "Вафли",
        "ingredients":[...],
        "remark":"10 порций. Время приготовления - 20 мин.",
        "steps": [...]
    """
    __name: str = ""
    __steps: list[recipe_step_model] = []
    __ingredients: list[ingredient_model] = []
    __remark:str = ""

    @property
    def name(self) -> str:
        return self.__name
    
    @name.setter
    def name(self, value: str):
        self.__name = value

    @property
    def steps(self) -> list:
        return self.__steps

    @steps.setter
    def steps(self, value:list):
        for step in value:
            validator.validate(step, recipe_step_model)
        self.__steps = value
    
    @property
    def ingredients(self) -> list:
        return self.__ingredients

    @ingredients.setter
    def ingredients(self, value:list):
        for step in value:
            validator.validate(step, ingredient_model)
        self.__ingredients = value
    
    @property
    def remark(self) -> str:
        return self.__remark

    @remark.setter
    def remark(self, value:str):
        self.__remark = value