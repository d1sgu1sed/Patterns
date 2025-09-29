import json
import os
from Src.Models.company_model import company_model
from Src.Models.settings_model import settings_model

class settings_manager:
    """
    Загрузчик и контейнер конфигурации приложения.

    Поля:
        filename (str): Название файла для загрузки конфига.
        settings (settings_model): загруженные настройки из файла
    Предназначение:
        - Загружает JSON и парсит его в settings.
        - Предоставляет доступ к текущим настройкам.
    """
    __instance = False
    __filename: str = ''
    __settings: settings_model = None
    __config_dict: dict
    __attrs = settings_model().company_attrs()
    
    def __init__(self, filename: str):
        self.__filename = filename
        self.default()

    """
    Реализация Singleton
    """
    def __new__(cls, filename):
        if not cls.__instance:
            cls.__instance = True
            cls.__company = super(settings_manager, cls).__new__(cls)
        return cls.__company

    """
    settings (settings_model): загруженные настройки из файла
    """
    @property
    def settings(self) -> settings_model:
        return self.__settings

    """
    filename (str): Название файла для загрузки конфига.
    """
    @property
    def filename(self):
        return self.__filename

    @filename.setter
    def filename(self, value: str):
        if value.strip() == '':
            return
        
        if os.path.exists(value):
            self.__filename = value.strip()

    """
    Функция загрузки данных из указанного JSON файла
    """
    def load(self):
        if self.__filename.strip() == '':
            raise FileNotFoundError('Не найден файл настроек')
        
        try:
            file = open(self.__filename)
            global_config: dict = json.load(file)
            if 'company' not in global_config:
                return False
            self.__config_dict = global_config['company']
            if len(self.__config_dict.keys()) == len(self.__attrs):
                for key in self.__config_dict.keys():
                    if key not in self.__attrs:
                        return False
                settings = self.convert_to_settings()
                self.__settings = settings
                return True
            return False
        except:
            print(11)
            return False

    """
    Функция установки дефолтных значений
    """
    def default(self):
        self.__settings = settings_model()
        self.__settings.company = company_model()
        self.__settings.company.name = "Рога и копыта" 
    
    """
    Функция конвертации из dict в settings_model
    """
    def convert_to_settings(self):
        self.__settings = settings_model()
        for item in self.__config_dict.keys():
            if item in self.__attrs:
                setattr(self.__settings.company, item, self.__config_dict[item])
        return self.__settings
        

        
