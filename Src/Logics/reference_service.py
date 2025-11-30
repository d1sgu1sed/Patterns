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
from Src.Core.reference_checker import reference_checker

"""
Сервис создания, удаления и изменения объектов
"""
class reference_service:
    def __init__(self):
        self.__service = start_service()

    """
    Добавление объекта
    """
    def add_reference(self, reference_type: str, reference):
        validator.validate(reference_type, str)
        
        if not reference_type in self.__service.reposity.keys:
            raise argument_exception(f"Неизвестный модификатор типа: \"{reference_type}\"")
        
        result = self.__service.add_reference(reference_type, reference)
        
        observe_service.create_event(event_type.add_new_reference(), 
                                     {"reference_type":reference_type, 
                                      "reference":reference}
                                     )
        
        return result
    
    """
    Изменение объекта
    """
    def change_reference(self, reference_type: str, reference):
        validator.validate(reference_type, str)
        
        if not reference_type in self.__service.reposity.keys:
            raise argument_exception(f"Неизвестный модификатор типа: \"{reference_type}\"")
        
        result = self.__service.change_reference(reference_type, reference)
        
        observe_service.create_event(event_type.change_reference(), 
                                     {"reference_type":reference_type, 
                                      "reference":reference}
                                     )
        
        return result

    """
    Удаление объекта
    """
    def delete_reference(self, reference_type: str, reference_id: str):
        validator.validate(reference_type, str)
        validator.validate(reference_id, str)
        
        if reference_type not in self.__service.reposity.data.keys():
            raise argument_exception(f"Неизвестный модификатор типа: \"{reference_type}\"")
        
        dto = filter_dto()
        dto.field_name = "unique_code"
        dto.value = reference_id
        dto.condition = "EQUALS"
        
        references_proto = prototype_osv(self.__service.reposity.data[reference_type])
        references = references_proto.filter(references_proto, dto).data
        if len(references) == 0:
            raise argument_exception(f"Объект типа {reference_type} не был обнаружен по id {reference_id}!")
        
        observe_service.create_event(event_type.deleting_reference(),
                                     {"reference_type": reference_type, 
                                      "reference": references[0]}
                                     )
        
        self.__service.reposity.data[reference_type].remove(references[0])
        
        observe_service.create_event(event_type.deleted_reference(), 
                                     {"reference_type": reference_type, 
                                      "reference_id": reference_id}
                                     )
        
        return True
        