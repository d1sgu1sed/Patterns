import unittest
from Src.start_service import start_service
from Src.reposity import reposity
class Test_start_service(unittest.TestCase):
    __start_service = start_service()

    def __init__(self, methodName = "runTest"):
        super().__init__(methodName)
        if self.__start_service.reposity.data[reposity.recipes_key()] == []:
            self.__start_service.start()

    """
    Проверка создания данных при помощи сервиса
    """
    def test_start_service_measure_not_empty(self):
        # подготовка
        data = self.__start_service.reposity.data

        # действие

        # проверка
        assert len(data[reposity.measure_key()]) != 0
        assert data[reposity.groups_key()][0] is not None

    """
    Проверка равенства созданных базовых единиц
    """
    def test_equal_instances(self):
        # подготовка
        data = self.__start_service.reposity.data
        
        # действие

        # проверка
        assert data[reposity.measure_key()][0] == data[reposity.measure_key()][2].base_measure


if __name__ == 'name':
    unittest.main()