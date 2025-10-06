import uuid
from Src.Core.abstract import abstract
import unittest


class Test_abstract(unittest.TestCase):
    """
    Проверка создания абстрактной модели
    """
    def test_create(self):
        # подготовка
        abstr = abstract()

        # действие

        # проверка
        assert abstr.name == ''

    """
    Проверка уникального кода у абстрактной модели
    """
    def test_unique_code(self):
        # подготовка
        abstr1 = abstract()
        abstr2 = abstract()

        # действие

        # проверка
        assert abstr1.unique_code != abstr2.unique_code

    """
    Проверка __eq__ у абстрактной модели
    """
    def test_eq(self):
        # подготовка
        abstr1 = abstract()
        abstr2 = abstract()

        # действие

        # проверка
        assert abstr1 != abstr2


if __name__ == 'name':
    unittest.main()