import uuid
from Src.Models.storage_model import storage_model
import unittest


class Test_storage_model(unittest.TestCase):
    """
    Проверка создания моделей склада
    Они должны быть неравными, т.к. у них разные uuid
    """
    def test_not_equals(self):
        # подготовка
        storage1 = storage_model()
        storage2 = storage_model()

        # действие

        # проверка
        assert storage1 != storage2
    
    """
    Проверка создания моделей склада
    Они должны быть равными, т.к. у них заданные uuid
    """
    def test_equals(self):
        # подготовка
        storage1 = storage_model()
        storage2 = storage_model()
        id = uuid.uuid4().hex

        # действие
        storage1.unique_code = id
        storage2.unique_code = id

        # проверка
        assert storage1 == storage2


if __name__ == 'name':
    unittest.main()