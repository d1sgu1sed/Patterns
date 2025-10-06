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
    __remark: str
    _instances = {}

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
    Создание рецепта вафель
    """
    @staticmethod
    def create_waffles():
        name = 'Вафли хрустящие в вафельнице'
        steps = recipe_step_model.create_waffles_step_list()
        ingredients = [
            ingredient_model.create_butter(70),
            ingredient_model.create_sugar(80),
            ingredient_model.create_egg(1),
            ingredient_model.create_flour(100),
            ingredient_model.create_vanilin(5)
        ]
        remark = '10 порций. Время приготовления - 20 мин.'
        return recipe_model.create(name, steps, ingredients, remark)

    """
    Фабричный метод создания рецепта
    """
    @staticmethod
    def create(name: str, steps: list, ingredients: list, remark: str):
        validator.validate(name, str, 50)
        if name in recipe_model._instances.keys():
            return recipe_model._instances[name]
        
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
        recipe_model._instances[name] = item
        return item
    
    """
    Форматирует рецепт в Markdown строку и записывает в файл
    """
    def formatting(self):
        filename = "Docs/receipt.md"
        
        # Формируем заголовок
        md_content = f"# {self.name.upper()}\n\n"
        
        # Таблица ингредиентов
        md_content += self.__format_ingredients_table()
        
        # Добавляем ремарку после таблицы
        if self.__remark:
            md_content += f"{self.__remark}\n\n"
        
        md_content += "## ПОШАГОВОЕ ПРИГОТОВЛЕНИЕ\n\n"
        
        # Шаги приготовления
        md_content += self.__format_steps()
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        return md_content

    def __format_ingredients_table(self) -> str:
        """Форматирует таблицу ингредиентов"""
        if not self.__ingredients:
            return ""
        
        table = "| Ингредиенты | Количество |\n"
        table += "|-------------|------------|\n"
        
        for ingredient in self.__ingredients:
            name = ingredient.product.name
            quantity = f"{ingredient.amount} {ingredient.product.measure.name}"
            table += f"| {name} | {quantity} |\n"
        
        table += "\n"
        return table

    def __format_steps(self) -> str:
        """Форматирует шаги приготовления"""
        if not self.__steps:
            return ""
        
        steps_text = ""
        for i, step in enumerate(self.__steps, 1):
            try:
                formatted_step = step.formatting()
                steps_text += f"{i}. {formatted_step}\n"
            except Exception as e:
                steps_text += f"{i}. [Ошибка форматирования шага: {e}]\n"
        
        return steps_text