import os
import json
import uuid
import unittest
from datetime import datetime

# Для тестирования Flask приложения
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Src.start_service import start_service
from Src.reposity import reposity
from Src.Core.reference_checker import reference_checker
from Src.Core.settings_processor import settings_processor
from Src.Logics.reference_service import reference_service

# Тестовый settings.json (минимум необходимого)
TEST_SETTINGS = {
    "company": {
        "name": "Рога и копыта",
        "INN": 129741029322,
        "account": 12309184024,
        "correspondent_acc": 93029318292,
        "BIK": 129031229,
        "type_of_property": "33333"
    },
    "response_format": "markdown",
    "first_start": True,
    "blocking_date": "20-10-2025 14:00:00",
    "default_receipt": {
        "name": "Вафли хрустящие в вафельнице",
        "nomenclature_groups": [
            {
                "name": "Ингредиенты",
                "id": "7f4ecdab-0f01-4216-8b72-4c91d22b8918"
            }
        ],
        "measures": [
            {
                "name": "Грамм",
                "id": "adb7510f-687d-428f-a697-26e53d3f65b7",
                "base_id": None,
                "value": 1
            },
            {
                "name": "Штуки",
                "id": "f8346e8b-7260-4db8-a673-c8c826ab08b7",
                "base_id": None,
                "value": 1
            }
        ],
        "nomenclatures": [
            {
                "name": "Пшеничная мука",
                "measure_id": "adb7510f-687d-428f-a697-26e53d3f65b7",
                "group_id": "7f4ecdab-0f01-4216-8b72-4c91d22b8918",
                "id": "0c101a7e-5934-4155-83a6-d2c388fcc11a"
            }
        ],
        "ingredients": [
            {
                "nomenclature_id": "0c101a7e-5934-4155-83a6-d2c388fcc11a",
                "measure_id": "adb7510f-687d-428f-a697-26e53d3f65b7",
                "value": 100
            }
        ],
        "remark": "Тест",
        "steps": ["Шаг 1"]
    },
    "storages": [
        {
            "name": "Продуктовый склад",
            "id": "ndet5a2x-6f2a-nv5z-f561-md7vb421"
        }
    ],
    "transactions": [
        {
            "nomenclature_id": "0c101a7e-5934-4155-83a6-d2c388fcc11a",
            "measure_id": "adb7510f-687d-428f-a697-26e53d3f65b7",
            "amount": 3.0,
            "storage_id": "ndet5a2x-6f2a-nv5z-f561-md7vb421",
            "date": "20-10-2025 10:00:00",
            "id": "ji96c2b4-sda7-gh54-4hj3-jkhv3jc3"
        }
    ]
}


def write_temp_settings(path: str):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(TEST_SETTINGS, f, ensure_ascii=False, indent=4)


def prepare_service_from_temp_settings(tmp_path: str):
    service = start_service()
    full = os.path.abspath(tmp_path)
    service.filename = full
    ok = service.load()
    if not ok:
        raise AssertionError("service.load() returned False")
    repo = service.reposity
    return service, repo


class TestAPIReferenceBlocking(unittest.TestCase):
    """
    Тестируем блокировку удаления через reference_service (который используется в API)
    """

    @classmethod
    def setUpClass(cls):
        cls.test_dir = os.path.join("Tests")
        os.makedirs(cls.test_dir, exist_ok=True)
        cls.settings_path = os.path.join(cls.test_dir, "settings_api_test.json")
        cls.dump_path = os.path.join("new_settings.json")
        if os.path.exists(cls.dump_path):
            os.remove(cls.dump_path)
        write_temp_settings(cls.settings_path)

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.settings_path):
            os.remove(cls.settings_path)
        if os.path.exists(cls.dump_path):
            os.remove(cls.dump_path)

    def test_api_delete_blocks_when_reference_used(self):
        """
        Тест проверяет, что при попытке удалить номенклатуру через API
        (используя reference_service), удаление будет заблокировано,
        если номенклатура используется в транзакциях
        """
        service, repo = prepare_service_from_temp_settings(self.settings_path)

        # Инициализируем наблюдателей (как в main.py)
        try:
            _ = reference_checker()
        except Exception:
            pass

        try:
            _ = settings_processor()
        except Exception:
            pass

        ref_srv = reference_service()

        # Попытка удалить номенклатуру "Пшеничная мука", которая используется в транзакции
        nomenclature_id = "0c101a7e-5934-4155-83a6-d2c388fcc11a"

        # Должно вызвать Exception, так как номенклатура используется
        with self.assertRaises(Exception) as context:
            ref_srv.delete_reference(reposity.nomenclature_key(), nomenclature_id)

        # Проверяем сообщение об ошибке
        self.assertIn("используется в других объектах", str(context.exception))

        # Убеждаемся, что номенклатура НЕ была удалена
        noms = repo.data[reposity.nomenclature_key()]
        found = [n for n in noms if n.unique_code == nomenclature_id]
        self.assertEqual(len(found), 1, "Номенклатура не должна быть удалена")

    def test_api_delete_allows_when_no_references(self):
        """
        Тест проверяет, что удаление разрешено, если объект не используется
        """
        service, repo = prepare_service_from_temp_settings(self.settings_path)

        # Инициализируем наблюдателей
        try:
            _ = reference_checker()
        except Exception:
            pass

        try:
            _ = settings_processor()
        except Exception:
            pass

        ref_srv = reference_service()

        # Создадим новую группу, которая не используется
        new_group_id = "g-test-" + str(uuid.uuid4())
        group_data = {"name": "Тестовая группа", "id": new_group_id}
        added = ref_srv.add_reference(reposity.groups_key(), group_data)
        self.assertTrue(added)

        # Удаление должно пройти успешно
        result = ref_srv.delete_reference(reposity.groups_key(), new_group_id)
        self.assertTrue(result)

        # Убеждаемся, что группа была удалена
        groups = repo.data[reposity.groups_key()]
        found = [g for g in groups if g.unique_code == new_group_id]
        self.assertEqual(len(found), 0, "Группа должна быть удалена")


if __name__ == "__main__":
    unittest.main()
