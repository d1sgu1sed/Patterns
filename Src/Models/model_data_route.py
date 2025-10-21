from flask import jsonify
from Src.reposity import reposity


class model_data_route:
    """
    Класс для обработки маршрутов работы с моделями данных
    """
    
    @staticmethod
    def get_raw_model_data(model_type, data):
        """
        Получение сырых данных модели (без сериализации в JSON)
        """
        try:
            model_mapping = {
                'nomenclature': reposity.nomenclature_key(),
                'nomenclature_group': reposity.groups_key(),
                'ingredient': reposity.ingredients_key(),
                'measure': reposity.measure_key(),
                'recipe': reposity.recipes_key(),
                'recipe_step': reposity.recipies_steps_key()
            }
            
            if model_type not in model_mapping:
                available_types = list(model_mapping.keys())
                return jsonify({
                    'error': f'Unknown model type: {model_type}',
                    'available_types': available_types
                }), 404
            
            data_key = model_mapping[model_type]
            model_data = data.get(data_key, [])
            
            return model_data
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @staticmethod
    def __serialize_object(obj):
        """
        Сериализация объекта в словарь
        """
        try:
            if hasattr(obj, 'to_dict') and callable(getattr(obj, 'to_dict')):
                return obj.to_dict()
            elif hasattr(obj, 'dict') and callable(getattr(obj, 'dict')):
                return obj.dict()
            elif hasattr(obj, '__dict__'):
                result = {}
                for key, value in obj.__dict__.items():
                    if key.startswith('_'):
                        continue
                    result[key] = model_data_route.__process_value(value)
                return result
            else:
                return dict(obj)
        except (TypeError, ValueError, AttributeError):
            return str(obj)
    
    @staticmethod
    def __process_value(value):
        """
        Рекурсивная обработка значений для сериализации
        """
        if value is None:
            return None
        elif isinstance(value, (str, int, float, bool)):
            return value
        elif isinstance(value, list):
            return [model_data_route.__process_value(item) for item in value]
        elif isinstance(value, dict):
            return {str(k): model_data_route.__process_value(v) for k, v in value.items()}
        elif hasattr(value, '__dict__'):
            return model_data_route.__serialize_object(value)
        else:
            return str(value)