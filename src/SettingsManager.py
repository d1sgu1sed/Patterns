import json
import os
from src.models.CompanyModel import CompanyModel
from src.models.Settings import Settings

class SettingsManager:
    __instance = False
    __filename: str = ''
    __model: CompanyModel = None
    __config_dict: dict
    __attrs = Settings().attrs()
    
    def __init__(self, filename: str):
        self.__filename = filename
        self.default()

    def __new__(cls, filename):
        if not cls.__instance:
            cls.__instance = True
            cls.__model = super(SettingsManager, cls).__new__(cls)
        return cls.__model

    @property
    def model(self) -> CompanyModel:
        return self.__model

    @property
    def filename(self):
        return self.__filename

    @filename.setter
    def filename(self, value: str):
        if value.strip() == '':
            return
        
        if os.path.exists(value):
            self.__filename = value.strip()

    def load(self):
        if self.__filename.strip() == '':
            raise FileNotFoundError('Не найден файл настроек')
        
        try:
            file = open(self.__filename)
            self.__config_dict = json.load(file)['company']

            if len(self.__config_dict.keys()) == len(self.__attrs):
                for key in self.__config_dict.keys():
                    if key not in self.__attrs:
                        return False
                settings = self.convert_to_settings()
                self.__model.settings = settings
                return True
            return False
        except:
            return False

    def default(self):
        self.__model = CompanyModel()
        settings = Settings()
        settings.name = "Рога и копыта"
        self.__model.settings = settings 
    
    def convert_to_settings(self):
        settings = Settings()
        for item in self.__config_dict.keys():
            if item in self.__attrs:
                setattr(settings, item, self.__config_dict[item])
        return settings
        

        
