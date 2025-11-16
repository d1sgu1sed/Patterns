from datetime import datetime
from Dtos.filter_dto import filter_dto
from Dtos.osv_dto import osv_dto
from Dtos.storage_dto import storage_dto
from Src.Core.abstract import abstract
from Src.Core.validator import argument_exception, operation_exception, validator
from Src.Logics.prototype_osv import prototype_osv
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.osv_unit_model import osv_unit_model
from Src.Models.storage_model import storage_model
from Src.Models.transaction_model import transaction_model

class osv_model(abstract):
    """
    Модель ОСВ.
    Представляет информацию об обороте продуктов за определённый период.
    """
    __start_date: datetime = None
    __finish_date: datetime = None
    __storage: storage_model = None
    __units: list[osv_unit_model] = []

    """
    Наследование функции инициализации
    """
    def __init__(self, name = ""):
        super().__init__(name)

    """
    Дата начала
    """
    @property
    def start_date(self) -> datetime:
        return self.__start_date
    
    """
    Дата окончания
    """
    @property
    def finish_date(self) -> datetime:
        return self.__finish_date
    
    """
    Склад с продукцией
    """
    @property
    def storage(self) -> storage_model:
        return self.__storage
    
    """
    Элементы ОСВ
    """
    @property
    def units(self) -> list:
        return self.__units

    @start_date.setter
    def start_date(self, value: datetime):
        validator.validate(value, datetime)
        self.__start_date = value

    @finish_date.setter
    def finish_date(self, value: datetime):
        validator.validate(value, datetime)
        self.__finish_date = value
    
    @storage.setter
    def storage(self, value: storage_model):
        validator.validate(value, storage_model)
        self.__storage = value
    
    @units.setter
    def units(self, value: list):
        validator.validate(value, list)
        for unit in value:
            validator.validate(unit, osv_unit_model)
        self.__units = value

    """
    Фабричный метод создания модели ОСВ
    """
    @staticmethod
    def create(start_date: datetime, finish_date: datetime,
               storage: storage_model):
        item = osv_model()
        item.start_date = start_date
        item.finish_date = finish_date
        item.storage = storage
        return item

    """
    Функция перевода объекта в DTO
    """
    def to_dto(self):
        item = osv_dto()
        item.start_date = self.__start_date
        item.finish_date = self.__finish_date
        item.storage_id = self.__storage.unique_code
        item.units = self.__units
        item.id = self.unique_code
        return item
    
    """
    Функция для нахождения элемента ОСВ по номенклатуре
    """
    def find_unit(self, nomenclature):
        for item in self.__units:
            if item.nomenclature == nomenclature:
                return item
        raise operation_exception("Элемент ОСВ не найден!")

    """
    Функция создания элементов ОСВ по транзакциям
    """
    def generate_units(self, transactions: list[transaction_model], 
                   nomenclatures: list[nomenclature_model]):
        # Инициализируем элементы ОСВ
        self.__units = [
            osv_unit_model.create_default(nomenclature.name, nomenclature,\
                                        nomenclature.measure.base_measure or nomenclature.measure)
            for nomenclature in nomenclatures
        ]

        # Фильтр на склад
        filter_storage = filter_dto()
        filter_storage.field_name = "storage.unique_code"
        filter_storage.value = str(self.__storage.unique_code)
        filter_storage.condition = "EQUALS"
        
        # Фильтр на количество продукции
        filter_amount = filter_dto()
        filter_amount.field_name = "date"
        filter_amount.value = self.__start_date
        filter_amount.condition = "LESS"
        
        # Фильтр на приходы и расходы
        filter_add_sub = filter_dto()
        filter_add_sub.field_name = "date"
        filter_add_sub.value = (self.__start_date, self.__finish_date)
        filter_add_sub.condition = "IN RANGE"

        
        proto_osv = prototype_osv(transactions)
        proto_storage = proto_osv.filter(proto_osv, filter_storage)
        proto_amount = proto_storage.filter(proto_storage, filter_amount)
        proto_add_sub = proto_storage.filter(proto_storage, filter_add_sub)
        
        # Обрабатываем все транзакции в одном цикле
        for transaction in proto_storage.data:
            try:
                item = self.find_unit(transaction.product)
                amount = transaction.amount
                
                # Корректируем количество по коэффициенту диапазона
                if transaction.measure.base_measure and transaction.measure.base_measure == item.measure:
                    amount *= transaction.measure.coef
                
                # Определяем тип транзакции по дате
                if transaction in proto_amount.data:
                    # Транзакция до начала периода - влияет только на начальный и конечный остаток
                    item.start_amount += amount
                    item.finish_amount += amount
                    
                elif transaction in proto_add_sub.data:
                    # Транзакция в периоде ОСВ
                    if transaction.amount > 0:
                        item.add += amount
                    else:
                        item.sub += abs(amount)  # Берем модуль для расхода
                    
                    # Обновляем конечный остаток
                    item.finish_amount += amount
                
                # Транзакции после finish_date игнорируются
                
            except operation_exception:
                # Пропускаем транзакции для номенклатур, которых нет в ОСВ
                continue