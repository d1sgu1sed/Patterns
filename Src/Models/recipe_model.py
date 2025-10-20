from Src.Core.validator import validator
from Src.Core.abstract import abstract
from Src.Models.recipe_step_model import recipe_step_model
from Src.Models.ingredient_model import ingredient_model

class recipe_model(abstract):
    """
    Модель для описания рецептов

    Поля:
        steps (list[recipe_step_model]): Описание шагов рецепта.
        ingredients (list[ingredient_model]): Ингридиенты для рецепта.
        remark (str): Ремарка рецепа, до 1024 символов.
    """
    __steps: list
    __ingredients: list
    __remark: str = None

    def __init__(self, name = ""):
        super().__init__(name)
    
    """
    Ингредиенты
    """
    @property
    def ingredients(self):
        return self.__ingredients

    """
    Шаги рецепта
    """
    @property
    def steps(self):
        return self.__steps
    
    """
    Ремарка
    """
    @property
    def remark(self):
        return self.__remark
    
    @ingredients.setter
    def ingredients(self, values: list):
        validator.validate(values, list)
        for value in values:
            validator.validate(value, ingredient_model)
        self.__ingredients = values

    @steps.setter
    def steps(self, values: list):
        validator.validate(values, list)
        for value in values:
            validator.validate(value, recipe_step_model)
        self.__steps = values

    @remark.setter
    def remark(self, value: str):
        validator.validate(value, str, 1024)
        self.__remark = value

    """
    Фабричный метод создания рецепта
    """
    @staticmethod
    def create(name: str, steps: list, ingredients: list, remark: str):
        validator.validate(name, str, 50)
        validator.validate(remark, str, 1024)
        validator.validate(steps, list)
        
        for step in steps:
            validator.validate(step, recipe_step_model)

        validator.validate(ingredients, list)
        for ingredient in ingredients:
            validator.validate(ingredient, ingredient_model)

        item = recipe_model(name)
        item.remark = remark
        item.steps = steps
        item.ingredients = ingredients

        return item