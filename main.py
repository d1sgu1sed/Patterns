import connexion
from flask import abort

from Src.Logics.factory_entities import factory_entities
from Src.Logics.response_json import response_json
from Src.Logics.response_md import response_md
from Src.Logics.response_xlsx import response_xlsx
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

@app.route("/response/<string:type>", methods=['GET'])
def get_response(type):
    if type not in responses_factory.formats:
        abort(404)
    response = responses_factory.create(type)
    text = response(f"Docs/waffles.{type}", data[reposity.recipes_key()][0]).generate()
    return text

@app.errorhandler(404)
def page_not_found(error):
    return f'Такого формата не найдено.', 404

@app.errorhandler(500)
def internal_server_error(error):
    return f'Внутренняя ошибка сервера: {str(error)}', 500

if __name__ == '__main__':
    data_service.start()
    data = data_service.reposity.data
    app.run(host="0.0.0.0", port=8080)