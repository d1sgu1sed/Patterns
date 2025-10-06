import unittest
from Src.start_service import start_service
from Src.reposity import reposity

class Test_start_service(unittest.TestCase):
    __start_service = start_service()

    def __init__(self, methodName = "runTest"):
        super().__init__(methodName)
        self.__start_service.start()

    """
    Проверка создания данных при помощи сервиса
    """
    def test_start_service_measure_not_empty(self):
        # подготовка
        data = self.__start_service.reposity.data

        # действие

        # проверка
        assert len(data[reposity.measure_key].keys()) != 0
        assert data[reposity.measure_key]['гр'] is data[reposity.measure_key]['кг'].base_measure
        assert data[reposity.measure_key]['л'] is data[reposity.measure_key]['мл'].base_measure
        assert data[reposity.groups_key]['Животного происхождения'] is not None



if __name__ == 'name':
    unittest.main()