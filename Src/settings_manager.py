from datetime import datetime
import json
import os
from Src.Core.event_type import event_type
from Src.Core.observe_service import observe_service
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
    __global_attrs: list = ['response_format', 'company', 'blocking_date', 'log_level', 'logs_output']
    __list_attrs: list = ['company']
    
    def __init__(self, filename: str):
        self.__filename = filename
        self.default()
        observe_service.create_event(
            event_type.debug(),
            f"Инициализация settings_manager с файлом {self.__filename}",
        )

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
            observe_service.create_event(
                event_type.debug(),
                "Попытка установить пустой путь к файлу настроек",
            )
            return
        
        if os.path.exists(value):
            self.__filename = value.strip()
            observe_service.create_event(
                event_type.info(),
                f"Установлен файл настроек {self.__filename}",
            )
        else:
            observe_service.create_event(
                event_type.error(),
                f"Файл настроек {value} не найден",
            )

    """
    Функция загрузки данных из указанного JSON файла
    """
    def load(self):
        if self.__filename.strip() == '':
            raise FileNotFoundError('Не найден файл настроек')

        observe_service.create_event(
            event_type.debug(),
            f"Загрузка настроек из {self.__filename}",
        )

        try:
            file = open(self.__filename)
            config: dict = json.load(file)
            for key in self.__global_attrs:
                if key not in config.keys():
                    observe_service.create_event(
                        event_type.error(),
                        f"В файле {self.__filename} отсутствует ключ {key}",
                    )
                    return False
                
            self.__settings = settings_model()
            
            for key in self.__global_attrs:
                if key in self.__list_attrs:
                    self.__convert_to_settings(key, config[key])
                else:
                    setattr(self.__settings, key, config[key])
            observe_service.create_event(
                event_type.info(),
                f"Настройки успешно загружены из {self.__filename}",
            )
            return True
        except Exception as error:
            observe_service.create_event(
                event_type.error(),
                f"Ошибка загрузки настроек из {self.__filename}: {error}",
            )
            return False

    """
    Функция установки дефолтных значений
    """
    def default(self):
        self.__settings = settings_model()
        self.__settings.company = company_model()
        self.__settings.company.name = "Рога и копыта" 
        self.__settings.blocking_date = "01-01-1990 00:00:00"
        observe_service.create_event(
            event_type.info(),
            "Настройки установлены по умолчанию",
        )
    
    """
    Функция конвертации из dict в settings_model
    """
    def __convert_to_settings(self, key: str, data: dict):
        attrs = getattr(settings_model, key + '_attrs')()
        for item in data.keys():
            if item in attrs:
                model = getattr(self.__settings, key)
                setattr(model, item, data[item])
        

        
