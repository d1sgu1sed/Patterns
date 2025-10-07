from Src.reposity import reposity
from Src.Models.measure_model import measure_model
from Src.Models.nomenclature_group_model import nomenclature_group_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.ingredient_model import ingredient_model
from Src.Models.recipe_model import recipe_model
from Src.Models.recipe_step_model import recipe_step_model

class start_service:
    __reposity: reposity = reposity()
    __instance = None

    def __init__(self):
        self.__reposity.data[reposity.measure_key] = {}
        self.__reposity.data[reposity.groups_key] = {}
        self.__reposity.data[reposity.nomenclature_key] = {}
        self.__reposity.data[reposity.recipies_steps_key] = {}
        self.__reposity.data[reposity.ingredients_key] = {}
        self.__reposity.data[reposity.recipies_key] = {}

    """
    Реализация Singleton
    """
    def __new__(cls):
        if not cls.__instance:
            cls.__instance = super(start_service, cls).__new__(cls)
        return cls.__instance
    
    @property
    def reposity(self):
        return self.__reposity
    
    def default_create_measure(self):
        measures = reposity.measure_key
        self.__reposity.data[measures]['гр'] = measure_model.create_gr()
        self.__reposity.data[measures]['кг'] = measure_model.create_kg()
        self.__reposity.data[measures]['шт'] = measure_model.create_pcs()
        self.__reposity.data[measures]['л'] = measure_model.create_l()
        self.__reposity.data[measures]['мл'] = measure_model.create_ml()

    def default_create_groups(self):
        groups = reposity.groups_key
        
        # Животного происхождения
        self.__reposity.data[groups]['Животного происхождения'] = \
            nomenclature_group_model.create('Животного происхождения')
        # Бакалея
        self.__reposity.data[groups]['Бакалея'] = \
            nomenclature_group_model.create('Бакалея')
        # Пищевые добавки
        self.__reposity.data[groups]['Пищевые добавки'] = \
            nomenclature_group_model.create('Пищевые добавки')
    
    def default_create_nomenclature(self):
        nomenclature = reposity.nomenclature_key
        groups = self.__reposity.data[reposity.groups_key]
        measures = self.__reposity.data[reposity.measure_key]
        
        # Сахар
        self.__reposity.data[nomenclature]['Сахар'] = \
            nomenclature_model.create('Сахар', groups['Бакалея'], measures['гр'])
        # Масло
        self.__reposity.data[nomenclature]['Сливочное масло'] = \
            nomenclature_model.create('Сливочное масло', groups['Животного происхождения'], measures['гр'])
        # Яйца
        self.__reposity.data[nomenclature]['Яйцо куриное'] = \
            nomenclature_model.create('Яйцо куриное', groups['Животного происхождения'], measures['шт'])
        # Мука
        self.__reposity.data[nomenclature]['Мука пшеничная'] = \
            nomenclature_model.create('Мука пшеничная', groups['Бакалея'], measures['гр'])
        # Ванилин
        self.__reposity.data[nomenclature]['Ванилин'] = \
            nomenclature_model.create('Ванилин', groups['Пищевые добавки'], measures['гр'])
        # Молоко
        self.__reposity.data[nomenclature]['Молоко'] = \
            nomenclature_model.create('Молоко', groups['Животного происхождения'], measures['мл'])
        # Соль
        self.__reposity.data[nomenclature]['Соль'] = \
            nomenclature_model.create('Соль', groups['Пищевые добавки'], measures['гр'])
    
    def create_default_ingredients(self):
        ingredients = reposity.ingredients_key
        nomenclature = self.__reposity.data[reposity.nomenclature_key]

        # Сахар
        self.__reposity.data[ingredients]['Сахар'] = \
            ingredient_model.create(nomenclature['Сахар'], 80)
        # Сливочное масло 
        self.__reposity.data[ingredients]['Сливочное масло'] = \
            ingredient_model.create(nomenclature['Сливочное масло'], 70)
        # Пшеничная мука
        self.__reposity.data[ingredients]['Мука пшеничная'] = \
            ingredient_model.create(nomenclature['Мука пшеничная'], 100)
        # Яйцо куриное
        self.__reposity.data[ingredients]['Яйцо куриное'] = \
            ingredient_model.create(nomenclature['Яйцо куриное'], 1)
        # Ванилин
        self.__reposity.data[ingredients]['Ванилин'] = \
            ingredient_model.create(nomenclature['Ванилин'], 5)
        # Молоко
        self.__reposity.data[ingredients]['Молоко'] = \
            ingredient_model.create(nomenclature['Молоко'], 500)
        # Соль
        self.__reposity.data[ingredients]['Соль'] = \
            ingredient_model.create(nomenclature['Соль'], 5)

    def create_default_receipt_steps(self):
        steps_key = reposity.recipies_steps_key
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

        self.__reposity.data[steps_key]['Вафли'] = steps
        
    def create_pancakes_steps(self):
        """Создание шагов для рецепта блинов"""
        steps_key = reposity.recipies_steps_key
        
        # Шаги для блинов
        pancakes_steps = []
        
        pancakes_steps.append(recipe_step_model.create(
            'Подготовьте все ингредиенты для блинов. У вас получится около {count} тонких блинов.',
            {'count': 12}
        ))

        pancakes_steps.append(recipe_step_model.create(
            'В глубокой миске смешайте муку, сахар и соль.'
        ))

        pancakes_steps.append(recipe_step_model.create(
            'В другой миске взбейте яйца с молоком до однородной массы.'
        ))

        pancakes_steps.append(recipe_step_model.create(
            'Постепенно вливайте яично-молочную смесь в мучную, постоянно помешивая венчиком.'
        ))

        pancakes_steps.append(recipe_step_model.create(
            'Добавьте растопленное сливочное масло и ванилин. Тщательно перемешайте тесто.'
        ))

        pancakes_steps.append(recipe_step_model.create(
            'Тесто должно получиться жидким, как жирные сливки. Оставьте его на {minutes} минут.',
            {'minutes': 15}
        ))

        pancakes_steps.append(recipe_step_model.create(
            'Разогрейте сковороду на среднем огне. Слегка смажьте ее маслом.'
        ))

        pancakes_steps.append(recipe_step_model.create(
            'Выливайте тесто половником на горячую сковороду и распределяйте тонким слоем.'
        ))

        pancakes_steps.append(recipe_step_model.create(
            'Жарьте блин около {time} секунд с одной стороны до золотистого цвета, затем переверните.',
            {'time': 40}
        ))

        pancakes_steps.append(recipe_step_model.create(
            'Подавайте блины горячими с вареньем, медом или сметаной.'
        ))

        self.__reposity.data[steps_key]['Блины'] = pancakes_steps
        
    def create_pancakes_receipt(self):
        """Создание рецепта блинов"""
        recipies_key = reposity.recipies_key
        steps_key = reposity.recipies_steps_key
        ingredients_key = reposity.ingredients_key

        # Рецепт блинов
        pancakes_name = 'Тонкие блины на молоке'
        pancakes_steps = self.__reposity.data[steps_key]['Блины']
        pancakes_ingredients = [
            self.__reposity.data[ingredients_key]['Мука пшеничная'],
            self.__reposity.data[ingredients_key]['Молоко'],
            self.__reposity.data[ingredients_key]['Яйцо куриное'],
            self.__reposity.data[ingredients_key]['Сахар'],
            self.__reposity.data[ingredients_key]['Сливочное масло'],
            self.__reposity.data[ingredients_key]['Соль'],
            self.__reposity.data[ingredients_key]['Ванилин']
        ]
        pancakes_remark = '12 порций. Время приготовления - 30 мин. Идеальный завтрак для всей семьи!'
        self.__reposity.data[recipies_key]['Блины'] = recipe_model.create(pancakes_name, pancakes_steps, pancakes_ingredients, pancakes_remark)
        
    def create_default_receipt(self):
        recipies_key = reposity.recipies_key
        steps_key = reposity.recipies_steps_key
        ingredients_key = reposity.ingredients_key

        # Рецепт вафель
        name = 'Вафли хрустящие в вафельнице'
        steps = self.__reposity.data[steps_key]['Вафли']
        ingredients = [
            self.__reposity.data[ingredients_key]['Сливочное масло'],
            self.__reposity.data[ingredients_key]['Сахар'],
            self.__reposity.data[ingredients_key]['Яйцо куриное'],
            self.__reposity.data[ingredients_key]['Мука пшеничная'],
            self.__reposity.data[ingredients_key]['Ванилин']
        ]
        remark = '10 порций. Время приготовления - 20 мин.'
        self.__reposity.data[recipies_key]['Вафли'] = recipe_model.create(name, steps, ingredients, remark)
        
    def start(self):
        self.default_create_measure()
        self.default_create_groups()
        self.default_create_nomenclature()
        self.create_default_ingredients()
        self.create_default_receipt_steps()
        self.create_default_receipt()
        self.create_pancakes_steps()
        self.create_pancakes_receipt()