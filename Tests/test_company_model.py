from Src.Models.company_model import company_model
import unittest

class Test_company_model(unittest.TestCase):
    """
    Проверка создания основной модели
    Данные после создания должны быть пустыми
    """
    def test_create(self):
        # подготовка
        model = company_model()
        
        # действие

        # проверка
        assert model.name == ""


    """
    Проверка создания основной модели
    Данные после создания должны быть не пустыми
    """
    def test_not_empty(self):
        # подготовка
        model = company_model()
        
        # действие
        model.name = 'test'
        
        # проверка
        assert model.name != ""
    

if __name__ == 'name':
    unittest.main()