from Src.Models.measure_model import measure_model
import unittest


class Test_measure_model(unittest.TestCase):
    """
    Проверка создания модели меры измерения 
    """
    def test_create_model(self):
        # подготовка
        measure = measure_model("гр.", 1)
        # действие

        # проверка
        assert measure.name == "гр."
        assert measure.coef == 1
        assert type(measure.coef) == float
    
    """
    Проверка создания вложенной модели меры измерения 
    """
    def test_enclosed_model(self):
        # подготовка
        measure_gr = measure_model("гр.", 1)
        measure_kg = measure_model("кг.", 1000, measure_gr)
        # действие

        # проверка
        assert measure_kg.name == "кг."
        assert measure_kg.coef == 1000
        assert measure_kg.base_measure.name == 'гр.'
        assert measure_kg.base_measure.coef == 1.0
    

if __name__ == 'name':
    unittest.main()