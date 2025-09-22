from src.models.Settings import Settings
class CompanyModel:
    # __name:str = ""
    # __inn:str = ""
    __settings = Settings()

    @property
    def settings(self) -> Settings:
        return self.__settings

    @settings.setter
    def settings(self, value: Settings):
        self.__settings = value