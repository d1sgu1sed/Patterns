import unittest
from Src.start_service import start_service
from Src.reposity import reposity
from Src.Models.measure_model import measure_model

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
        assert data[reposity.groups_key]['Животного происхождения'] is not None

    """
    Проверка равенства созданных базовых единиц
    """
    def test_equal_instances(self):
        # подготовка
        data = self.__start_service.reposity.data
        
        # действие

        # проверка
        assert data[reposity.measure_key]['гр'] is data[reposity.measure_key]['кг'].base_measure
        assert data[reposity.measure_key]['л'] is data[reposity.measure_key]['мл'].base_measure
        assert data[reposity.measure_key]['шт'] is measure_model.create_pcs() 
        assert data[reposity.measure_key]['л'] is measure_model.create_l() 
        assert data[reposity.measure_key]['гр'] is measure_model.create_gr() 
        
        assert measure_model.create_l() is measure_model.create_l()
        assert measure_model.create_gr() is measure_model.create_gr()



if __name__ == 'name':
    unittest.main()