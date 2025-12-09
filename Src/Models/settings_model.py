from datetime import datetime
from Src.Core.event_type import event_type
from Src.Core.observe_service import observe_service
from Src.Models.company_model import company_model
from Src.Core.validator import validator
from Src.Core.response_format import response_formats

class settings_model:
    """
    Контейнер настроек приложения.
    
    Поля:
        company (company_model): Настройки организации.
        response_format(str): Формат ответа.
        blocking_date(datetime): Дата закрытия периода
    """
    __company: company_model = company_model()
    __response_format: str = ""
    __blocking_date: datetime = None 
    __logs_output: str
    __log_level: str

    """
    company (company_model): Настройки организации.
    """
    @property
    def company(self):
        return self.__company

    @company.setter
    def company(self, value: company_model):
        validator.validate(value, company_model)
        self.__company = value

    """
    Формат ответа
    """
    @property
    def response_format(self):
        return self.__response_format

    @response_format.setter
    def response_format(self, value: str):
        validator.validate(value, str)
        self.__response_format = value
        observe_service.create_event(
            event_type.info(),
            f"Формат ответа установлен: {self.__response_format}",
        )
        
    """
    Дата блокировки
    """
    @property
    def blocking_date(self) -> datetime:
        return self.__blocking_date

    @blocking_date.setter
    def blocking_date(self, value):
        if isinstance(value, str):
            self.__blocking_date = datetime.strptime(value, "%d-%m-%Y %H:%M:%S")
        if isinstance(value, datetime):
            self.__blocking_date = value
        observe_service.create_event(
            event_type.debug(),
            f"Дата блокировки настроек обновлена: {self.__blocking_date}",
        )
    
    """
    Уровень логирования
    """
    @property
    def log_level(self) -> str:
        return self.__log_level
    
    @log_level.setter
    def log_level(self,value):
        validator.validate(value,str)
        observe_service.create_event(event_type.set_log_level(),value)
        self.__log_level=value

    """
    Вывод логов
    """
    @property
    def logs_output(self) -> str:
        return self.__logs_output
    
    @logs_output.setter
    def logs_output(self,value):
        validator.validate(value,str)
        observe_service.create_event(event_type.set_logs_output(), value)
        self.__logs_output=value

    def __init__(self, is_default=True):
        if(is_default):
            self.default()
        
    def default(self):
        self.__company.__name = ""
        self.__company.__INN = 129741029323
        self.__company.__account = 12309184023
        self.__company.__correspondent_acc = 93029318293
        self.__company.__BIK = 129031223
        self.__company.__type_of_property = "33333"
        self.__response_format = response_formats.md()
        self.__log_level = "INFO"
        self.__logs_output = "FILE"
        observe_service.create_event(
            event_type.debug(),
            "Созданы настройки по умолчанию",
        )

    @staticmethod
    def company_attrs():
        return [attr for attr in dir(company_model) if not attr.startswith('_') and attr != 'unique_code']
            
