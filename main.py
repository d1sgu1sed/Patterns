import connexion
from flask import abort, jsonify

from Src.Logics.factory_entities import factory_entities
from Src.Logics.response_json import response_json
from Src.Logics.response_md import response_md
from Src.Logics.response_xml import response_xml
from Src.reposity import reposity
from Src.start_service import start_service
from Src.Models.model_data_route import model_data_route

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
    # Если format_type - это формат вывода (json, xml, md, csv)
    if format_type in responses_factory.formats:
        return __get_formatted_response(format_type, model_type, data)
    else:
        abort(404)


"""
Получение данных в указанном формате
"""
def __get_formatted_response(format_type, model_type, data):
    try:
        # Получаем данные модели
        model_data = model_data_route.get_raw_model_data(model_type, data)
        if isinstance(model_data, tuple):  # Если вернулась ошибка
            return model_data
        
        # Создаем форматтер
        response = responses_factory.create(format_type)
        formatter = response()
        
        # Генерируем данные в нужном формате
        text = formatter.generate(model_data)
        return text
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

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