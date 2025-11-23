from datetime import datetime
import json
import connexion
from flask import abort, jsonify
import flask

from Dtos.filter_dto import filter_dto
from Dtos.filter_sort_dto import filter_sort_dto
from Src.Core.prototype import prototype
from Src.Logics.factory_entities import factory_entities
from Src.Logics.prototype_osv import prototype_osv
from Src.Logics.response_json import response_json
from Src.Logics.response_md import response_md
from Src.Logics.response_xml import response_xml
from Src.reposity import reposity
from Src.start_service import start_service

flask_app = connexion.FlaskApp(__name__)
app = flask_app.app
strt_service = start_service() 
data = None
responses_factory = factory_entities()


"""
Проверить доступность REST API
"""
@app.route("/api/accessibility", methods=['GET'])
def formats():
    return "SUCCESS"


"""
Получение рецепта нужного формата
"""
@app.route("/response/<string:type>", methods=['GET'])
def get_response(type):
    if type not in responses_factory.formats:
        abort(404)
    response = responses_factory.create(type)
    text = response().generate([data[reposity.recipes_key()][0]])
    return text


"""
Получение данных в указанном формате для указанного типа модели
"""
@app.route("/response/<string:format_type>/<string:model_type>", methods=['GET'])
def get_response_with_model(format_type, model_type):
    if format_type not in responses_factory.formats:
        abort(404)
    if model_type not in data.keys():
        abort(404)

    result_format = factory_entities().create(format_type)()
    result = result_format.generate(list(data[model_type]))
    return result


"""
Получить список рецептов
"""
@app.route("/response/recipes", methods=['GET'])
def get_recipes():
    result_format = factory_entities().create("json")()
    result = result_format.generate(data[reposity.recipes_key()])
    return result


"""
Получить рецепт по идентификатору
"""
@app.route("/response/recipe/<string:id>", methods=['GET'])
def get_recipe(id):
    result_format = factory_entities().create("json")()
    for recipe in data[reposity.recipes_key()]:
        if recipe.unique_code == id:
            result = result_format.generate([recipe])
            return result
    abort(404)

"""
Получить отчет по оборотной ведомости для указанного склада и периода
"""
@app.route("/report/<string:code>/<string:start>/<string:end>", methods=['GET'])
def get_report(code, start, end):
    result_format = factory_entities().create("csv")()
    res = data[reposity.storage_key()]
    storage = None
    
    try:
        start_date = datetime.strptime(start,"%d-%m-%Y %H:%M:%S")
        finish_date = datetime.strptime(end,"%d-%m-%Y %H:%M:%S")
    except:
        return "Неправильный формат дат!"
    
    for item in res:
        if item.unique_code == code:
            storage = item
            break
            
    if storage is None:
        return "Неправильный код склада!"
    
    osv = strt_service.create_osv(start_date, finish_date, storage.unique_code)
    
    # Задаем желаемый порядок полей для CSV
    field_order = ["name", "measure_id", "nomenclature_id", "start_amount", "finish_amount", "add", "sub"]
    
    # Передаем порядок полей в генератор CSV
    result = result_format.generate(osv.units, field_order)
    return flask.Response(response=result, status=200, 
               content_type="text/plain;charset=utf-8")

"""
Фильтровать элементы указанной доменной модели по DTO фильтра
"""
@app.route("/api/filter/<string:model_type>", methods=['POST'])
def filter_domain(model_type):
    if data is None or model_type not in data.keys():
        abort(404)

    payload = flask.request.get_json()
    if payload is None:
        return jsonify({
            "status": "error",
            "message": "Тело запроса должно содержать JSON с параметрами фильтра."
        }), 400


    filter_sort_data = filter_sort_dto.create(payload)
    proto = prototype_osv(data[model_type])
    for filter in filter_sort_data.filters:
        proto = prototype.filter(proto, filter)

    # Отдаём отфильтрованный результат в JSON
    result_format = factory_entities().create("json")()
    result = result_format.generate(proto.data)
    return result

"""
Получить отчет по оборотной ведомости для указанного склада и периода с учетом DTO фильтрации (POST)
"""
@app.route("/report/<string:code>/<string:start>/<string:end>", methods=['POST'])
def get_report_osv_filtered(code, start, end):
    result_format = factory_entities().create("csv")()
    res = data[reposity.storage_key()]
    storage = None

    try:
        start_date = datetime.strptime(start, "%d-%m-%Y %H:%M:%S")
        finish_date = datetime.strptime(end, "%d-%m-%Y %H:%M:%S")
    except Exception:
        return "Неправильный формат дат!"

    for item in res:
        if item.unique_code == code:
            storage = item
            break

    if storage is None:
        return "Неправильный код склада!"

    osv = strt_service.create_osv(start_date, finish_date, storage.unique_code)

    payload = flask.request.get_json()
    if payload is not None:
        filter_sort_data = filter_sort_dto().create(payload)

        proto = prototype_osv(osv.units)
        for filter in filter_sort_data.filters:
            proto = prototype_osv.filter(proto, filter)

        filtered_units = proto.data

        # Формируем модель ОСВ с отфильтрованными строками
        osv.units = filtered_units

    field_order = ["name", "measure_id", "nomenclature_id",
                   "start_amount", "finish_amount", "add", "sub"]
    result = result_format.generate(osv.units, field_order)
    return flask.Response(response=result,
                          status=200,
                          content_type="text/plain;charset=utf-8")

"""
Выполнить дамп данных в файл
"""
@app.route("/dump", methods=['POST'])
def dump():
    res = strt_service.dump("settings2.json")
    
    if res:
        result = json.dumps({"status": "success", "message": "Info saved to file!"})
        return result
    else:
        result = json.dumps({"status": "error", "message": "Error with saving info!"})
        return result, 400
    
"""
Изменить дату блокировки в настройках (Settings_model / settings.json)
Формат даты: "дд-мм-ГГГГ чч:мм:cc"
Пример тела запроса:
{
   "blocking_date": "20-10-2025 14:00:00"
}
"""
@app.route("/api/blocking_date", methods=['POST'])
def set_blocking_date():
    payload = flask.request.get_json()
    if payload is None or "blocking_date" not in payload:
        return jsonify({
            "status": "error",
            "message": "Тело запроса должно содержать JSON с полем 'blocking_date'."
        }), 400

    date_str = payload["blocking_date"]

    try:
        new_date = datetime.strptime(date_str, "%d-%m-%Y %H:%M:%S")
    except ValueError:
        return jsonify({
            "status": "error",
            "message": "Неправильный формат даты. Используйте 'дд-мм-ГГГГ чч:мм:cc'."
        }), 400

    # 1. Меняем дату блокировки в сервисе (это вызовет пересчёт остатков)
    strt_service.blocking_date = new_date

    return jsonify({
        "status": "success",
        "blocking_date": date_str
    }), 200

"""
Получить текущую дату блокировки
"""
@app.route("/api/blocking_date", methods=['GET'])
def get_blocking_date():
    # Сначала смотрим, не установлена ли дата блокировки в сервисе
    if strt_service.blocking_date is not None:
        date_str = strt_service.blocking_date.strftime("%d-%m-%Y %H:%M:%S")
        return jsonify({"blocking_date": date_str}), 200

    return jsonify({"blocking_date": date_str}), 200

"""
Получить остатки на указанную дату.
Формат даты в URL: "дд-мм-ГГГГ чч:мм:cc"
Пример: /api/balance/20-10-2025%2014:00:00
"""
@app.route("/api/balance/<string:date_str>", methods=['GET'])
def get_balance_on_date(date_str: str):
    try:
        target_date = datetime.strptime(date_str, "%d-%m-%Y %H:%M:%S")
    except ValueError:
        return jsonify({
            "status": "error",
            "message": "Неправильный формат даты. Используйте 'дд-мм-ГГГГ чч:мм:cc'."
        }), 400

    strt_service.blocking_date = target_date
    balances = getattr(strt_service, "balance_history", [])

    result = []
    for bal in balances:
        result.append({
            "storage_id": bal.storage.unique_code,
            "storage_name": bal.storage.name,
            "nomenclature_id": bal.nomenclature.unique_code,
            "nomenclature_name": bal.nomenclature.name,
            "measure_id": bal.measure.unique_code,
            "measure_name": bal.measure.name,
            "amount": bal.amount
        })

    return jsonify(result), 200


@app.errorhandler(404)
def page_not_found(error):
    return f'Маршрут не найден.', 404


@app.errorhandler(500)
def internal_server_error(error):
    return f'Внутренняя ошибка сервера: {str(error)}', 500


@app.errorhandler(405)
def method_not_allowed(error):
    return f'Метод не разрешен для данного маршрута. Разрешенные методы: {error.valid_methods}', 405


if __name__ == '__main__':
    strt_service.start()
    data = strt_service.reposity.data
    app.run(host="0.0.0.0", port=8080)