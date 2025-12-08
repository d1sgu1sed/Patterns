import os
import time
import unittest
from datetime import datetime, timedelta

from Src.start_service import start_service
from Src.reposity import reposity
from Src.Models.osv_model import osv_model
from Src.Models.transaction_model import transaction_model

# Путь к settings.json – поменяй на свой, если нужно
SETTINGS_PATH = '/home/ivan/Desktop/Patterns/settings.json'


def prepare_service_with_settings() -> start_service:
    """
    Инициализирует start_service и загружает данные из settings.json.
    """
    service = start_service()
    service.filename = SETTINGS_PATH
    load_result = service.load()
    assert load_result, "Не удалось загрузить данные из settings.json"
    return service


class Test_osv_blocking_date(unittest.TestCase):
    """
    Модульный тест:
    - считаем ОСВ по реальным данным из settings.json
    - меняем дату блокировки
    - проверяем, что итоговые суммы (start/add/sub/finish) не меняются
      и соответствуют ожидаемым значениям.
    """

    def test_osv_is_stable_when_blocking_date_changes(self):
        # подготовка
        service = prepare_service_with_settings()
        repo = service.reposity

        # Берём единственный склад из settings.json
        storages = repo.data[reposity.storage_key()]
        assert len(storages) > 0
        storage = storages[0]

        # Все номенклатуры
        nomenclatures = repo.data[reposity.nomenclature_key()]
        assert len(nomenclatures) > 0

        # Период ОСВ: начинаем после всех транзакций из settings.json
        # В settings.json все транзакции 20-10-2025 до 14:00
        start_date = datetime(2025, 10, 20, 15, 0, 0)
        finish_date = datetime(2025, 10, 21, 0, 0, 0)

        # Две разные даты блокировки, обе раньше start_date
        blocking1 = datetime(2025, 10, 20, 11, 0, 0)
        blocking2 = datetime(2025, 10, 20, 13, 30, 0)

        # Собираем все транзакции
        transactions = repo.data[reposity.transaction_key()]
        assert len(transactions) > 0

        # Первая ОСВ
        service.blocking_date = blocking1
        osv1 = osv_model.create(start_date, finish_date, storage)
        # Если ты уже передаёшь blocking_date и balance_history внутри create_osv,
        # можно заменить на service.create_osv(...)
        osv1.generate_units(
            transactions,
            nomenclatures,
            blocking_date=service.blocking_date,
            balance_history=getattr(service, "balance_history", [])
        )

        # Вторая ОСВ
        service.blocking_date = blocking2
        osv2 = osv_model.create(start_date, finish_date, storage)
        osv2.generate_units(
            transactions,
            nomenclatures,
            blocking_date=service.blocking_date,
            balance_history=getattr(service, "balance_history", [])
        )

        # проверка: количество единиц ОСВ одинаковое
        assert len(osv1.units) == len(osv2.units)

        # Хелпер для поиска единицы ОСВ по имени номенклатуры
        def find_unit(osv, name: str):
            for u in osv.units:
                # в осва-юнитах обычно есть либо name, либо ссылка на nomenclature
                if getattr(u, "name", None) == name:
                    return u
                if getattr(u, "nomenclature", None) and u.nomenclature.name == name:
                    return u
            return None

        unit_egg_1 = find_unit(osv1, "Яйцо")
        unit_egg_2 = find_unit(osv2, "Яйцо")
        unit_flour_1 = find_unit(osv1, "Пшеничная мука")
        unit_flour_2 = find_unit(osv2, "Пшеничная мука")

        assert unit_egg_1 is not None and unit_egg_2 is not None
        assert unit_flour_1 is not None and unit_flour_2 is not None

        # 1) При смене даты блокировки значения не меняются
        for u1, u2 in [(unit_egg_1, unit_egg_2), (unit_flour_1, unit_flour_2)]:
            assert abs(u1.start_amount - u2.start_amount) < 1e-9
            assert abs(u1.add - u2.add) < 1e-9
            assert abs(u1.sub - u2.sub) < 1e-9
            assert abs(u1.finish_amount - u2.finish_amount) < 1e-9

        # 2) Проверяем корректность расчётов с точки зрения данных settings.json.
        # Период начинается после последней транзакции, значит весь оборот
        # должен попасть в начальный и конечный остаток (add = sub = 0).
        #
        # По settings.json:
        # Яйцо: +3 (10:00) -2 (12:00) = 1 штука
        # Пшеничная мука: +1 кг (13:00) -150 г (14:00) = 850 г (в базовой единице "Грамм")

        # Яйцо
        assert abs(unit_egg_1.start_amount - 1.0) < 1e-9
        assert abs(unit_egg_1.finish_amount - 1.0) < 1e-9
        assert abs(unit_egg_1.add - 0.0) < 1e-9
        assert abs(unit_egg_1.sub - 0.0) < 1e-9

        # Пшеничная мука
        assert abs(unit_flour_1.start_amount - 850.0) < 1e-9
        assert abs(unit_flour_1.finish_amount - 850.0) < 1e-9
        assert abs(unit_flour_1.add - 0.0) < 1e-9
        assert abs(unit_flour_1.sub - 0.0) < 1e-9


class Test_osv_performance(unittest.TestCase):
    """
    Нагрузочный тест:
    - загружаем данные из settings.json
    - добавляем 1000+ транзакций
    - при разных датах блокировки считаем ОСВ, замеряем время
    - пишем результат в Markdown-файл.
    """

    def test_osv_performance_with_many_transactions(self):
        # подготовка
        service = prepare_service_with_settings()
        repo = service.reposity

        storages = repo.data[reposity.storage_key()]
        assert len(storages) > 0
        storage = storages[0]

        nomenclatures = repo.data[reposity.nomenclature_key()]
        assert len(nomenclatures) > 0

        # Возьмём первую номенклатуру для генерации дополнительных транзакций
        product = nomenclatures[0]
        measure = product.measure

        # Базовые транзакции уже загружены из settings.json
        transactions = repo.data[reposity.transaction_key()]
        base_count = len(transactions)
        assert base_count > 0

        # Добавляем 1000 дополнительных транзакций
        base_date = datetime(2025, 10, 1, 0, 0, 0)
        extra_count = 1000

        for i in range(extra_count):
            # чередуем приход/расход
            amount = 1.0 if i % 2 == 0 else -1.0
            tr_date = base_date + timedelta(minutes=i)

            tr = transaction_model.create(tr_date, product, storage, amount, measure)
            transactions.append(tr)

        # Итоговое количество транзакций
        total_transactions = len(transactions)
        assert total_transactions >= base_count + extra_count

        # Период ОСВ – пусть это будет диапазон, перекрывающий все транзакции
        start_date = datetime(2025, 10, 1, 0, 0, 0)
        finish_date = datetime(2025, 10, 31, 23, 59, 59)

        # разные варианты даты блокировки
        blocking_dates = [
            datetime(2025, 9, 30, 23, 59, 59),  # до всех транзакций
            datetime(2025, 10, 10, 0, 0, 0),
            datetime(2025, 10, 20, 0, 0, 0),
            datetime(2025, 11, 1, 0, 0, 0),    # после всех транзакций
        ]

        results = []

        for blocking in blocking_dates:
            t_start = time.perf_counter()

            # установка даты блокировки (должна вызвать пересчёт остатков)
            service.blocking_date = blocking

            # расчёт ОСВ
            osv = osv_model.create(start_date, finish_date, storage)
            osv.generate_units(
                transactions,
                nomenclatures,
                blocking_date=service.blocking_date,
                balance_history=getattr(service, "balance_history", [])
            )

            elapsed = time.perf_counter() - t_start
            results.append((blocking, elapsed))

            # простая sanity-проверка
            assert len(osv.units) > 0

        # формируем Markdown-отчёт
        report_lines = [
            "# Результаты нагрузочного теста ОСВ\n",
            f"- Количество транзакций: {total_transactions}\n",
            "",
            "| Дата блокировки       | Время расчёта, сек |",
            "|-----------------------|-------------------:|",
        ]

        for blocking, elapsed in results:
            report_lines.append(
                f"| {blocking.strftime('%Y-%m-%d %H:%M:%S')} | {elapsed:.6f} |"
            )

        # путь для сохранения отчёта
        report_dir = os.path.join("Tests")
        os.makedirs(report_dir, exist_ok=True)
        report_path = os.path.join(report_dir, "osv_performance.md")

        with open(report_path, "w", encoding="utf-8") as f:
            f.write("\n".join(report_lines))

        # проверка: файл отчёта создан и в нём есть строки с результатами
        assert os.path.exists(report_path)
        assert len(results) == len(blocking_dates)


if __name__ == "__main__":
    unittest.main()
