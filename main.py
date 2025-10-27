import connexion
from flask import abort, jsonify

from Src.Logics.factory_entities import factory_entities
from Src.Logics.response_json import response_json
from Src.Logics.response_md import response_md
from Src.Logics.response_xml import response_xml
from Src.reposity import reposity
from Src.start_service import start_service

flask_app = connexion.FlaskApp(__name__)
app = flask_app.app
data_service = start_service() 
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
    text = response().generate(data[reposity.recipes_key()][0])
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
Получить список рецептов
"""
@app.route("/response/recipe/<string:id>", methods=['GET'])
def get_recipe(id):
    result_format = factory_entities().create("json")()
    for recipe in data[reposity.recipes_key()]:
        if recipe.unique_code == id:
            result = result_format.generate([recipe])
            return result

@app.errorhandler(404)
def page_not_found(error):
    return f'Маршрут не найден.', 404

@app.errorhandler(500)
def internal_server_error(error):
    return f'Внутренняя ошибка сервера: {str(error)}', 500

if __name__ == '__main__':
    data_service.start()
    data = data_service.reposity.data
    app.run(host="0.0.0.0", port=8080)