from Src.Core.validator import validator
from Dtos.filter_dto import filter_dto

"""
DTO для представления фильтров и сортировок.
Содержит список фильтров и список полей для сортировки.
"""
class filter_sort_dto():
    __filters: list[filter_dto]
    __sorting: list[str]

    def __init__(self):
        self.__filters = []
        self.__sorting = []

    """
    Массив filter_dto
    """
    @property
    def filters(self) -> list[filter_dto]:
        return self.__filters

    @filters.setter
    def filters(self, value: list[filter_dto]):
        validator.validate(value, list)
        self.__filters = value

    """
    Массив полей сортировки
    """
    @property
    def sorting(self) -> list[str]:
        return self.__sorting

    @sorting.setter
    def sorting(self, value: list[str]):
        validator.validate(value, list)
        self.__sorting = value

    """
    Метод создания экземпляра из словаря
    
    Ожидаемый JSON:
    {
      "filters": [
        {
          "filter_name": "name",
          "value": "Пшеничная мука",
          "type": "LIKE"
        },
        {
          "filter_name": "measure.name",   # для вложенных полей
          "value": "кг",
          "type": "EQUALS"
        }
      ],
      "sorting": ["name", "measure.name"]
    }
    """
    @staticmethod
    def create(data: dict) -> "filter_sort_dto":
        validator.validate(data, dict)
        item = filter_sort_dto()
        filters_data = data.get("filters", [])
        item.filters = []
        for filter in filters_data:
            filter_data = filter_dto.create(filter)
            item.filters.append(filter_data)

        item.sorting = data.get("sorting", [])
        return item