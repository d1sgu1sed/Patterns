from Src.Core.abstract_logic import abstract_logic
from Src.Core.observe_service import observe_service
from Src.Core.event_type import event_type
from Src.start_service import start_service
from Src.Core.validator import validator,argument_exception
from Src.Logics.prototype_osv import prototype_osv
from Dtos.filter_dto import filter_dto
from Src.reposity import reposity
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.storage_model import storage_model
from Src.Models.measure_model import measure_model
from Src.Models.nomenclature_group_model import nomenclature_group_model

"""
Объект для предотвращения объекта при его использовании в других объектах
"""
class reference_checker(abstract_logic):

    def __init__(self):
        super().__init__()
        self.__service = start_service()
        observe_service.add(self)
        
    """
    Проверка наличия номенклатуры в других объектах
    """
    def __check_nomenclatures(self, nomenclature: nomenclature_model) -> bool:
        validator.validate(nomenclature, nomenclature_model)

        dto = filter_dto()
        dto.field_name = "product.id"
        dto.value = nomenclature.id
        dto.condition = "EQUALS"

        # Проверка в рецептах
        for recipe in self.__service.reposity.data[reposity.recipes_key()]:
            ingredients_proto = prototype_osv(recipe.ingredients)
            ingredients_nom = ingredients_proto.filter(ingredients_proto, dto).data

            if len(ingredients_nom) > 0:
                return True

        # Проверка в транзакциях
        transactions_proto = prototype_osv(self.__service.reposity.data[reposity.transaction_key()])
        transactions_nom = transactions_proto.filter(transactions_proto, dto).data

        if len(transactions_nom) > 0:
            return True

        return False
    
    """
    Проверка наличия склада в других объектах
    """
    def __check_storages(self, storage: storage_model) -> bool:
        validator.validate(storage, storage_model)

        dto = filter_dto()
        dto.field_name = "storage.id"
        dto.value = storage.id
        dto.condition = "EQUALS"

        transactions = prototype_osv(self.__service.reposity.data[reposity.transaction_key()])
        transactions_with_storage = transactions.filter(transactions, dto).data

        if len(transactions_with_storage) > 0:
            return True

        stocks = prototype_osv(self.__service.reposity.data[reposity.balance_key()])
        stocks_with_storage = stocks.filter(stocks, dto).data

        if len(stocks_with_storage) > 0:
            return True

        return False
    
    """
    Проверка наличия единицы измерения в других объектах
    """
    def __check_measures(self, measure: measure_model) -> bool:
        validator.validate(measure, measure_model)

        dto = filter_dto()
        dto.field_name = "measure.id"
        dto.value = measure.id
        dto.condition = "EQUALS"

        nomenclatures_proto = prototype_osv(self.__service.reposity.data[reposity.nomenclature_key()])
        nomenclatures_measure = nomenclatures_proto.filter(nomenclatures_proto, dto).data

        if len(nomenclatures_measure) > 0:
            return True

        dto.field_name = "base_measure.id"
        dto.value = measure.id

        measure_proto = prototype_osv(self.__service.reposity.data[reposity.measure_key()])
        base_measures = measure_proto.filter(measure_proto, dto).data
        if len(base_measures) > 0:
            return True

        return False

    """
    Проверка наличия группы в других объектах
    """
    def __check_groups(self,group):
        validator.validate(group, nomenclature_group_model)
        
        dto = filter_dto()
        dto.field_name = "group.id"
        dto.value = group.id
        dto.condition = "EQUALS"

        nomenclature_proto = prototype_osv(self.__service.reposity.data[reposity.nomenclature_key()])
        nomenclature_groups = nomenclature_proto.filter(nomenclature_proto, dto).data
        
        if len(nomenclature_groups) > 0:
            return True
        
        return False

    """
    Обработка событий
    """
    def handle(self, event:str, params):
        super().handle(event, params)

        if event == event_type.deleting_reference():
            reference_type = params["reference_type"]
            reference = params["reference"]

            if reference_type == reposity.nomenclature_key():
                if self.__check_nomenclatures(reference):
                    raise Exception("Номенклатура используется в других объектах")

            elif reference_type == reposity.measure_key():
                if self.__check_measures(reference):
                    raise Exception("Единица измерения используется в других объектах")

            elif reference_type == reposity.storage_key():
                if self.__check_storages(reference):
                    raise Exception("Склад используется в других объектах")

            elif reference_type == reposity.groups_key():
                if self.__check_groups(reference):
                    raise Exception("Группа номенклатуры используется в других объектах")