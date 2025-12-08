from Core.abstract_logic import abstract_logic
from Core.observe_service import observe_service
from Core.event_type import event_type
from Src.start_service import start_service

"""
Обработчик для перерасчёта остатков
"""
class stock_postprocessor(abstract_logic):

    def __init__(self):
        super().__init__()
        self.__service = start_service()
        observe_service.add(self)

    """
    Обработка событий
    """
    def handle(self, event:str, params):
        super().handle(event, params)  
        if event in [event_type.change_block_period(),
                     event_type.deleted_reference(),
                     event_type.add_new_reference(),
                     event_type.change_reference()]:
            self.__service.create_stocks()