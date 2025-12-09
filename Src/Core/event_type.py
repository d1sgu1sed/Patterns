"""
Типы событий
"""
class event_type:

    """
    Событие - смена даты блокировки
    """
    @staticmethod
    def change_block_period() -> str:
        return "change_block_period"

    """
    Событие - сформирован Json
    """
    @staticmethod
    def convert_to_json() -> str:
        return "convert_to_json"

    """
    Событие - добавление объекта
    """
    @staticmethod
    def add_new_reference() -> str:
        return "add_new_reference"

    """
    Событие - удаление объекта
    """
    @staticmethod
    def deleting_reference() -> str:
        return "deleting_reference"

    """
    Событие - объект удален
    """
    @staticmethod
    def deleted_reference() -> str:
        return "deleted_reference"

    """
    Событие - изменение объекта
    """
    @staticmethod
    def change_reference() -> str:
        return "change_reference"

    """
    Событие - возникла ошибка
    """
    @staticmethod
    def error() -> str:
        return "ERROR"

    """
    Событие - предупреждение
    """
    @staticmethod
    def debug() -> str:
        return "DEBUG"

    """
    Событие - информация
    """
    @staticmethod
    def info() -> str:
        return "INFO"

    """
    Событие - тип вывода логов
    """
    @staticmethod
    def set_logs_output() -> str:
        return "Setted logs output to"

    """
    Событие - тип вывода логов
    """
    @staticmethod
    def set_log_level() -> str:
        return "Setted log level to"

    """
    Получить список всех событий
    """
    @staticmethod
    def events() -> list:
        result = []
        methods = [method for method in dir(event_type) if
                    callable(getattr(event_type, method)) and not method.startswith('__') and method != "events"]
        for method in methods:
            key = getattr(event_type, method)()
            result.append(key)

        return result