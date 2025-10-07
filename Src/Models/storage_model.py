from Src.Core.abstract import abstract

class storage_model(abstract):
    """
    Модель склад.
    Представляет место хранения продуктов по номенклатуре.
    """
    
    """
    Наследование функции инициализации
    """
    def __init__(self, name = ""):
        super().__init__(name)