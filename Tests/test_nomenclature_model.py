from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.nomenclature_group_model import nomenclature_group_model
from Src.Models.measure_model import measure_model
import unittest


class Test_nomenclature_model(unittest.TestCase):
    """
    Проверка создания группы номенклатуры
    """
    def test_create_model(self):
        # подготовка
        nomenclature_group = nomenclature_group_model()
        measure_gr = measure_model('гр.', 1)
        nomenclature = nomenclature_model('товары', 
                                          nomenclature_group,
                                          measure_gr)
        # действие

        # проверка
        assert nomenclature.name == "товары"
        assert nomenclature.measure.name == 'гр.'
        assert nomenclature.group.name == ''


if __name__ == 'name':
    unittest.main()