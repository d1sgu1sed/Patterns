from Src.Models.nomenclature_group_model import nomenclature_group_model
import unittest


class Test_nomenclature_group_model(unittest.TestCase):
    """
    Проверка создания группы номенклатуры
    """
    def test_create_model(self):
        # подготовка
        nomenclature_group = nomenclature_group_model()
        # действие

        # проверка
        assert nomenclature_group.name == ""


if __name__ == 'name':
    unittest.main()