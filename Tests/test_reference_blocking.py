import os
import json
import unittest
import uuid
from datetime import datetime, timedelta

from Src.start_service import start_service
from Src.reposity import reposity
from Src.Core.reference_checker import reference_checker
from Src.Core.settings_processor import settings_processor
from Src.Core.observe_service import observe_service
from Src.Logics.reference_service import reference_service
from Src.Models.osv_model import osv_model
from Src.Models.balance_model import balance_model

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
            },
            {
                "name": "Киллограмм",
                "id": "a33dd457-36a8-4de6-b5f1-40afa6193346",
                "base_id": "adb7510f-687d-428f-a697-26e53d3f65b7",
                "value": 1000
            }
        ],
        "nomenclatures": [
            {
                "name": "Пшеничная мука",
                "measure_id": "a33dd457-36a8-4de6-b5f1-40afa6193346",
                "group_id": "7f4ecdab-0f01-4216-8b72-4c91d22b8918",
                "id": "0c101a7e-5934-4155-83a6-d2c388fcc11a"
            },
            {
                "name": "Сахар",
                "measure_id": "adb7510f-687d-428f-a697-26e53d3f65b7",
                "group_id": "7f4ecdab-0f01-4216-8b72-4c91d22b8918",
                "id": "39d9349d-28fa-4c7b-ad92-5c5fc7cf93da"
            },
            {
                "name": "Сливочное масло",
                "measure_id": "adb7510f-687d-428f-a697-26e53d3f65b7",
                "group_id": "7f4ecdab-0f01-4216-8b72-4c91d22b8918",
                "id": "de92caf7-731c-44cf-a9f4-31237e6fe707"
            },
            {
                "name": "Яйцо",
                "measure_id": "f8346e8b-7260-4db8-a673-c8c826ab08b7",
                "group_id": "7f4ecdab-0f01-4216-8b72-4c91d22b8918",
                "id": "3ce75449-05e8-4921-9310-9bcd0be7095b"
            },
            {
                "name": "Ванилин",
                "measure_id": "adb7510f-687d-428f-a697-26e53d3f65b7",
                "group_id": "7f4ecdab-0f01-4216-8b72-4c91d22b8918",
                "id": "fc389d90-2c41-4495-8d04-56d75acff008"
            }
        ],
        "ingredients": [
            {
                "nomenclature_id": "0c101a7e-5934-4155-83a6-d2c388fcc11a",
                "measure_id": "a33dd457-36a8-4de6-b5f1-40afa6193346",
                "value": 100
            },
            {
                "nomenclature_id": "39d9349d-28fa-4c7b-ad92-5c5fc7cf93da",
                "measure_id": "adb7510f-687d-428f-a697-26e53d3f65b7",
                "value": 80
            },
            {
                "nomenclature_id": "de92caf7-731c-44cf-a9f4-31237e6fe707",
                "measure_id": "adb7510f-687d-428f-a697-26e53d3f65b7",
                "value": 70
            },
            {
                "nomenclature_id": "3ce75449-05e8-4921-9310-9bcd0be7095b",
                "measure_id": "f8346e8b-7260-4db8-a673-c8c826ab08b7",
                "value": 1
            },
            {
                "nomenclature_id": "fc389d90-2c41-4495-8d04-56d75acff008",
                "measure_id": "adb7510f-687d-428f-a697-26e53d3f65b7",
                "value": 5
            }
        ],
        "remark": "10 порций. Время приготовления - 20 мин.",
        "steps": [
            [
                "Как испечь вафли хрустящие в вафельнице? Подготовьте необходимые продукты. Из данного количества у меня получилось {n} штук диаметром около {diam} см.",
                {"n": 8, "diam": 10}
            ],
            "Масло положите в сотейник с толстым дном. Растопите его на маленьком огне на плите, на водяной бане либо в микроволновке.",
            "Добавьте в теплое масло сахар. Перемешайте венчиком до полного растворения сахара. От тепла сахар довольно быстро растает.",
            "Добавьте в масло яйцо. Предварительно все-таки проверьте масло, не горячее ли оно, иначе яйцо может свариться. Перемешайте яйцо с маслом до однородности.",
            "Всыпьте муку, добавьте ванилин.",
            "Перемешайте массу венчиком до состояния гладкого однородного теста.",
            "Разогрейте вафельницу по инструкции к ней. У меня очень старая, еще советских времен электровафельница. Она может и не очень красивая, но печет замечательно! Я не смазываю вафельницу маслом, в тесте достаточно жира, да и к ней уже давно ничего не прилипает. Но вы смотрите по своей модели. Выкладывайте тесто по столовой ложке. Можно класть немного меньше теста, тогда вафли будут меньше и их получится больше.",
            "Пеките вафли несколько минут до золотистого цвета. Осторожно откройте вафельницу, она очень горячая! Снимите вафлю лопаткой. Горячая она очень мягкая, как блинчик."
        ]
    },
    "storages": [
        {
            "name": "Продуктовый склад",
            "id": "ndet5a2x-6f2a-nv5z-f561-md7vb421"
        }
    ],
    "transactions": [
        {
            "nomenclature_id": "3ce75449-05e8-4921-9310-9bcd0be7095b",
            "measure_id": "f8346e8b-7260-4db8-a673-c8c826ab08b7",
            "amount": 3.0,
            "storage_id": "ndet5a2x-6f2a-nv5z-f561-md7vb421",
            "date": "20-10-2025 10:00:00",
            "id": "ji96c2b4-sda7-gh54-4hj3-jkhv3jc3"
        },
        {
            "nomenclature_id": "3ce75449-05e8-4921-9310-9bcd0be7095b",
            "measure_id": "f8346e8b-7260-4db8-a673-c8c826ab08b7",
            "amount": -2.0,
            "storage_id": "ndet5a2x-6f2a-nv5z-f561-md7vb421",
            "date": "20-10-2025 12:00:00",
            "id": "8w7vc2b4-sda7-gh54-4hj3-jkhv3jc3"
        },
        {
            "nomenclature_id": "0c101a7e-5934-4155-83a6-d2c388fcc11a",
            "measure_id": "a33dd457-36a8-4de6-b5f1-40afa6193346",
            "amount": 1.0,
            "storage_id": "ndet5a2x-6f2a-nv5z-f561-md7vb421",
            "date": "20-10-2025 13:00:00",
            "id": "ifd9s4r4-sda7-gh54-8uj3-jkhv3jc3"
        },
        {
            "nomenclature_id": "0c101a7e-5934-4155-83a6-d2c388fcc11a",
            "measure_id": "adb7510f-687d-428f-a697-26e53d3f65b7",
            "amount": -150.0,
            "storage_id": "ndet5a2x-6f2a-nv5z-f561-md7vb421",
            "date": "20-10-2025 14:00:00",
            "id": "bdv3aoo4-sda7-gp154-8uj3-jk9jsc4"
        }
    ]
}


def write_temp_settings(path: str):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(TEST_SETTINGS, f, ensure_ascii=False, indent=4)


def prepare_service_from_temp_settings(tmp_path: str):
    """
    Helper: создаёт start_service, указывает filename на tmp_path и загружает данные.
    Если загрузка падает — выводит содержимое файла и пытается поймать и показать ошибку.
    Возвращает (service, repo).
    """
    service = start_service()

    # filename setter проверяет существование файла, поэтому используем абсолютный путь
    full = os.path.abspath(tmp_path)
    service.filename = full

    # Попробуем загрузить и, если не удалось — выплюнем подробности
    try:
        ok = service.load()
    except Exception as ex:
        # Если load бросил исключение — показываем содержимое файла и пробрасываем дальше
        with open(full, 'r', encoding='utf-8') as f:
            content = f.read()
        raise AssertionError(
            "service.load() raised exception: {}\n\nsettings file ({}):\n{}\n".format(
                repr(ex), full, content
            )
        ) from ex

    if not ok:
        # load вернул False — соберём как можно больше данных для диагностики
        with open(full, 'r', encoding='utf-8') as f:
            content = f.read()

        # Попробуем проверить вручную, какие ключи найдены
        try:
            settings = json.loads(content)
        except Exception as ex_json:
            raise AssertionError(
                "service.load() returned False and settings.json is invalid JSON: {}\n\nFile: {}\n{}".format(
                    repr(ex_json), full, content
                )
            )

        # Сформируем диагностическое сообщение
        msg = [
            "service.load() returned False",
            f"settings path: {full}",
            "top-level keys found: " + ", ".join(list(settings.keys())),
            "",
            "default_receipt keys (if present): " + (", ".join(list(settings.get("default_receipt", {}).keys())) if "default_receipt" in settings else "<missing>"),
            "",
            "Full file contents:",
            content
        ]
        raise AssertionError("\n".join(msg))

    repo = service.reposity
    return service, repo



class TestReferenceService(unittest.TestCase):
    """
    Тестируем reference_service (add/change/delete), поведение наблюдателя и пересчёт остатков.
    """

    @classmethod
    def setUpClass(cls):
        # папка Tests/tmp для временных файлов
        cls.test_dir = os.path.join("Tests")
        os.makedirs(cls.test_dir, exist_ok=True)
        cls.settings_path = os.path.join(cls.test_dir, "settings_test.json")
        # удаляем старый new_settings.json, если есть
        cls.dump_path = os.path.join("new_settings.json")
        if os.path.exists(cls.dump_path):
            os.remove(cls.dump_path)
        write_temp_settings(cls.settings_path)

    @classmethod
    def tearDownClass(cls):
        # cleanup
        if os.path.exists(cls.settings_path):
            os.remove(cls.settings_path)
        if os.path.exists(cls.dump_path):
            os.remove(cls.dump_path)
        # do not remove tmp folder to not disturb other tests

    def test_add_change_delete_reference_and_blocking(self):
        service, repo = prepare_service_from_temp_settings(self.settings_path)
        try:
            _ = reference_checker()
        except Exception:
            pass

        try:
            _ = settings_processor()
        except Exception:
            pass
        ref_srv = reference_service()

        # 1) Добавим новую единицу измерения (measure)
        new_measure_id = "m-test-" + str(uuid.uuid4())
        measure_data = {
            "name": "Тестовая мера",
            "id": new_measure_id,
            "base_id": None,
            "value": 1
        }
        added = ref_srv.add_reference(reposity.measure_key(), measure_data)
        assert added is True

        # проверим, что мера в репозитории
        measures = repo.data[reposity.measure_key()]
        found_m = [m for m in measures if getattr(m, "unique_code", None) == new_measure_id or getattr(m, "name", None) == "Тестовая мера"]
        assert len(found_m) == 1

        # 2) Добавим склад
        new_storage_id = "st-test-" + str(uuid.uuid4())
        storage_data = {"name": "ТестСклад", "id": new_storage_id}
        added = ref_srv.add_reference(reposity.storage_key(), storage_data)
        assert added is True
        storages = repo.data[reposity.storage_key()]
        found_s = [s for s in storages if getattr(s, "unique_code", None) == new_storage_id]
        assert len(found_s) == 1

        # 3) Добавим группу и номенклатуру, которая ссылается на созданную меру/группу
        new_group_id = "g-test-" + str(uuid.uuid4())
        group_data = {"name": "GTest", "id": new_group_id}
        added = ref_srv.add_reference(reposity.groups_key(), group_data)
        assert added is True

        new_nomenclature_id = "nom-test-" + str(uuid.uuid4())
        nom_data = {
            "name": "Продукт-Тест",
            "measure_id": new_measure_id,
            "group_id": new_group_id,
            "id": new_nomenclature_id
        }
        added = ref_srv.add_reference(reposity.nomenclature_key(), nom_data)
        assert added is True

        # убедимся, что номенклатура добавлена
        noms = repo.data[reposity.nomenclature_key()]
        found_nom = [n for n in noms if getattr(n, "unique_code", None) == new_nomenclature_id]
        assert len(found_nom) == 1

        # 4) Добавим транзакцию, которая ссылается на номенклатуру и склад — чтобы блокировать удаление
        trans_id = "t-test-" + str(uuid.uuid4())
        transaction_data = {
            "nomenclature_id": new_nomenclature_id,
            "measure_id": new_measure_id,
            "amount": 5.0,
            "storage_id": new_storage_id,
            "date": "01-01-2025 10:00:00",
            "id": trans_id
        }
        added = ref_srv.add_reference(reposity.transaction_key(), transaction_data)
        assert added is True

        # 5) Попытка удалить номенклатуру должна быть заблокирована reference_checker
        with self.assertRaises(Exception):
            ref_srv.delete_reference(reposity.nomenclature_key(), new_nomenclature_id)

        # 6) Изменим номенклатуру через change_reference - поменяем имя
        new_name = "Продукт-Тест-NEW"
        nom_change_data = {
            "name": new_name,
            "measure_id": new_measure_id,
            "group_id": new_group_id,
            "id": new_nomenclature_id
        }
        changed = ref_srv.change_reference(reposity.nomenclature_key(), nom_change_data)
        assert changed is True

        # проверим, что имя изменилось в репозитории
        noms = repo.data[reposity.nomenclature_key()]
        found = [n for n in noms if getattr(n, "unique_code", None) == new_nomenclature_id and getattr(n, "name", None) == new_name]
        assert len(found) == 1

        # 7) settings_processor должен был записать дамп (new_settings.json) на событие добавления/изменения.
        # убедимся, что файл появился
        assert os.path.exists("new_settings.json")

    def test_balance_recalc_and_osv_stability(self):
        service, repo = prepare_service_from_temp_settings(self.settings_path)
        try:
            _ = reference_checker()
        except Exception:
            pass

        try:
            _ = settings_processor()
        except Exception:
            pass

        # Убедимся, что в репозитории есть склад и номенклатуры из тестовых данных
        storages = repo.data[reposity.storage_key()]
        storage = storages[0]
        nomenclatures = repo.data[reposity.nomenclature_key()]
        transactions = repo.data[reposity.transaction_key()]

        # Пара дат блокировки — одна раньше 12:00, вторая позже 12:00 но до start_date
        blocking_early = datetime(2025, 10, 20, 11, 0, 0)
        blocking_late = datetime(2025, 10, 20, 14, 30, 0)

        # Период ОСВ — начинается позже всех транзакций
        start_date = datetime(2025, 10, 20, 15, 0, 0)
        finish_date = datetime(2025, 10, 21, 0, 0, 0)

        # 1) Установим раннюю дату, пересчитаем остатки и запомним balances
        service.blocking_date = blocking_early
        
        balances_early = { (b.nomenclature.unique_code, b.storage.unique_code): b.amount for b in service.balance_history }

        # 2) Установим более позднюю дату и пересчитаем
        service.blocking_date = blocking_late
        
        balances_late = { (b.nomenclature.unique_code, b.storage.unique_code): b.amount for b in service.balance_history }
                # Определяем реальные unique_code номенклатур по имени (чтобы тест был независим от id)
        def find_nomenclature_code_by_name(name: str):
            for n in nomenclatures:
                if getattr(n, "name", None) == name:
                    return getattr(n, "unique_code", None)
            return None

        egg_nom_code = find_nomenclature_code_by_name("Яйцо")
        flour_nom_code = find_nomenclature_code_by_name("Пшеничная мука")

        assert egg_nom_code is not None, "Номенклатура 'Яйцо' не найдена в репозитории теста"
        assert flour_nom_code is not None, "Номенклатура 'Пшеничная мука' не найдена в репозитории теста"

        egg_key = (egg_nom_code, storage.unique_code)
        flour_key = (flour_nom_code, storage.unique_code)

        # Для диагностики — распечатаем доступные ключи в случае ошибки
        if egg_key not in balances_early:
            print("Доступные ключи в balances_early:", list(balances_early.keys()))
        if egg_key not in balances_late:
            print("Доступные ключи в balances_late:", list(balances_late.keys()))

        assert egg_key in balances_early
        assert egg_key in balances_late
        assert balances_early[egg_key] == 3.0
        assert balances_late[egg_key] == 1.0

        assert flour_key in balances_late
        assert abs(balances_late[flour_key] - 850.0) < 1e-9


        # 3) Создадим ОСВ на основе balance_history и транзакций — и убедимся, что finish_amount совпадает
        service.blocking_date = blocking_early
        osv1 = osv_model.create(start_date, finish_date, storage)
        osv1.generate_units(transactions, nomenclatures, blocking_date=service.blocking_date, balance_history=service.balance_history)

        service.blocking_date = blocking_late
        osv2 = osv_model.create(start_date, finish_date, storage)
        osv2.generate_units(transactions, nomenclatures, blocking_date=service.blocking_date, balance_history=service.balance_history)

        # Найдём юниты для Яйца и сравним finish_amount — они должны совпадать (итоговый остаток не зависит от точки блокировки)
        def find_unit(osv, name):
            for u in osv.units:
                if getattr(u, "nomenclature", None) and u.nomenclature.name == name:
                    return u
                if getattr(u, "name", None) == name:
                    return u
            return None

        egg_u1 = find_unit(osv1, "Яйцо")
        egg_u2 = find_unit(osv2, "Яйцо")
        assert egg_u1 is not None and egg_u2 is not None
        assert abs(egg_u1.finish_amount - egg_u2.finish_amount) < 1e-9

        # Для муки тоже
        flour_u1 = find_unit(osv1, "Пшеничная мука")
        flour_u2 = find_unit(osv2, "Пшеничная мука")
        assert flour_u1 is not None and flour_u2 is not None
        assert abs(flour_u1.finish_amount - flour_u2.finish_amount) < 1e-9


if __name__ == "__main__":
    unittest.main()
