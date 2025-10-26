from Src.Core.abstract_dto import abstract_dto
from Src.Core.validator import validator

class recipe_step_dto(abstract_dto):
    """
    Модель шага рецепта (dto)
    Пример
        "steps": [
            [
            "Как испечь вафли хрустящие в вафельнице? Подготовьте необходимые продукты. Из данного количества у меня получилось {n} штук диаметром около {diam} см.",
            {
                "n": 8,
                "diam": 10
            }
            ],
            "Масло положите в сотейник с толстым дном. Растопите его на маленьком огне на плите, на водяной бане либо в микроволновке.",
        ]
    """
    __step: list = []


    @property
    def step(self) -> list:
        return self.__step

    @step.setter
    def step(self, value:list):
        if isinstance(value, list):
            for item in value:
                validator.validate(item, str|dict)
        else:
            validator.validate(value, str)
        self.__step = value