from Src.Core.validator import validator
from Src.Core.abstract import abstract
import re

"""
Исключение при форматировании пустой строки
"""  
class empty_description_exception(Exception):
    pass

"""
Исключение при неравном количестве 
плейсхолдеров и параметров шага
"""  
class non_equal_params(Exception):
    pass

"""
Исключение при форматировании
"""  
class formatting_error(Exception):
    pass

class recipe_step_model(abstract):
    __description: str
    __params: list = None

    def __init__(self, description:str = "", params: list|dict = None, name = ""):
        super().__init__(name)
        self.__description = description
        if params is not None:
            validator.validate(params, list|dict)
            self.__params = params

    @property
    def params(self):
        return self.__params
    
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

    @staticmethod
    def create_waffles_step_list():
        steps = []
        
        steps.append(recipe_step_model.create(
            'Как испечь вафли хрустящие в вафельнице? Подготовьте необходимые продукты. Из данного количества у меня получилось {n} штук диаметром около {diam} см.',
            {'n': 8, 'diam': 10}
        ))

        steps.append(recipe_step_model.create(
            'Масло положите в сотейник с толстым дном. Растопите его на маленьком огне на плите, на водяной бане либо в микроволновке.'
        ))

        steps.append(recipe_step_model.create(
            'Добавьте в теплое масло сахар. Перемешайте венчиком до полного растворения сахара. От тепла сахар довольно быстро растает.'
        ))

        steps.append(recipe_step_model.create(
            'Добавьте в масло яйцо. Предварительно все-таки проверьте масло, не горячее ли оно, иначе яйцо может свариться. Перемешайте яйцо с маслом до однородности.'
        ))

        steps.append(recipe_step_model.create(
            'Всыпьте муку, добавьте ванилин.'
        ))

        steps.append(recipe_step_model.create(
            'Перемешайте массу венчиком до состояния гладкого однородного теста.'
        ))

        steps.append(recipe_step_model.create(
            """Разогрейте вафельницу по инструкции к ней. У меня очень старая, еще советских времен электровафельница. Она может и не очень красивая, но печет замечательно!
Я не смазываю вафельницу маслом, в тесте достаточно жира, да и к ней уже давно ничего не прилипает. Но вы смотрите по своей модели. Выкладывайте тесто по столовой ложке.
Можно класть немного меньше теста, тогда вафли будут меньше и их получится больше."""
        ))

        steps.append(recipe_step_model.create(
            'Пеките вафли несколько минут до золотистого цвета. Осторожно откройте вафельницу, она очень горячая! Снимите вафлю лопаткой. Горячая она очень мягкая, как блинчик.'
        ))

        return steps

    @staticmethod
    def create(description: str, params: list|dict = None):
        # validator.validate(description, str, 1024)
        
        item = recipe_step_model()
        item.description = description

        if params is not None:
            validator.validate(params, list|dict)
            item.params = params

        return item

    def formatting(self) -> str:
        """
        Форматирует строку __description, подставляя параметры из __params
        в плейсхолдеры в фигурных скобках.
        
        Проверяет соответствие количества плейсхолдеров и длины списка параметров.
        В дальнейшем можно добавить функционал для преобразования в различные форматы
        """
        if not self.__description:
            raise empty_description_exception("Пустое описание")
        
        if self.__params is None:
            self.__params = []
        
        placeholders = re.findall(r'\{([^}]+)\}', self.__description)
        
        if len(placeholders) != len(self.__params):
            raise non_equal_params(
                f"Количество плейсхолдеров {len(placeholders)} не соответствует количеству параметров {len(self.__params)}"
            )
        
        try:
            if isinstance(self.__params, dict):
                # Для dict-параметров
                formatted_description = self.__description.format(**self.__params)
            else:
                # Для list-параметров
                formatted_description = self.__description.format(*self.__params)
            return formatted_description
        except:
            raise formatting_error(
                f"Ошибка при форматировании строки. Плейсхолдеры: {placeholders}, Параметры: {self.__params}"
            )