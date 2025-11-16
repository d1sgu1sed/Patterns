from datetime import datetime
from Dtos.filter_dto import filter_dto
from Src.Core.prototype import prototype
from Src.Core.validator import validator
from Src.Models.measure_model import measure_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.storage_model import storage_model


class prototype_osv(prototype):
    """
    Класс прототипа для ОСВ (оборотно-сальдовой ведомости).
    Наследует от prototype и добавляет специфичные методы фильтрации для транзакций.
    """
    
    def __init__(self, data:list):
        super().__init__(data)

    def clone(self, data: list = None):
        inner_data = data
        if inner_data is None:
            inner_data = self.__data
        instance = prototype_osv(inner_data)
        return instance
    
    """
    Сделать фильтр по номенклатуре.
    """
    @staticmethod
    def filter_by_nomenclature(source: prototype, 
                               nomenclature: nomenclature_model) -> 'prototype_osv':
        validator.validate(source, prototype)
        validator.validate(nomenclature, nomenclature_model)
        
        result = []
        for item in source.data:
            if item.product == nomenclature:
                result.append(item)
        
        # Возвращаем прототип с данными по номенклатуре
        return source.clone(result)
    
    """
    Сделать фильтр по измерениям.
    """
    @staticmethod
    def filter_by_measure(source: prototype, 
                               measure: measure_model) -> 'prototype_osv':
        validator.validate(source, prototype)
        validator.validate(measure, measure_model)
        
        result = []
        for item in source.data:
            if item.measure == measure:
                result.append(item)
        
        # Возвращаем прототип с данными по единице измерения
        return source.clone(result)
    
    """
    Сделать фильтр по дате в диапазоне.
    """
    @staticmethod
    def filter_by_date_in_range(source: prototype, 
                               first_date: datetime,
                               second_date: datetime) -> 'prototype_osv':
        validator.validate(source, prototype)
        validator.validate(first_date, datetime)
        validator.validate(second_date, datetime)
        
        result = []
        for item in source.data:
            if first_date < item.date < second_date:
                result.append(item)
        
        # Возвращаем прототип с данными по дате
        return source.clone(result)
    
    """
    Сделать фильтр по дате (больше указанной даты).
    """
    @staticmethod
    def filter_by_date_upper(source: prototype, 
                               first_date: datetime) -> 'prototype_osv':
        validator.validate(source, prototype)
        validator.validate(first_date, datetime)
        
        result = []
        for item in source.data:
            if first_date < item.date:
                result.append(item)
        
        # Возвращаем прототип с данными по дате
        return source.clone(result)
    
    """
    Сделать фильтр по дате (меньше указанной даты).
    """
    @staticmethod
    def filter_by_date_lower(source: prototype, 
                               first_date: datetime) -> 'prototype_osv':
        validator.validate(source, prototype)
        validator.validate(first_date, datetime)
        
        result = []
        for item in source.data:
            if first_date > item.date:
                result.append(item)
        
        # Возвращаем прототип с данными по дате
        return source.clone(result)
    
    """
    Сделать фильтр по складу.
    """
    @staticmethod
    def filter_by_storage(source: prototype, 
                               storage: storage_model) -> 'prototype_osv':
        validator.validate(source, prototype)
        
        result = []
        for item in source.data:
            if item.storage == storage:
                result.append(item)
        
        # Возвращаем прототип с данными по складу
        return source.clone(result)
    
    """
    Универсальный фильтр с использованием filter_dto.
    """
    @staticmethod
    def filter(proto: 'prototype', filter: filter_dto) -> 'prototype':
        validator.validate(proto, prototype)
        # Вызывается родительский метод filter
        result = prototype.filter(proto, filter)
        return proto.clone(result.data)