FIELDS = {
    'name': {'type': str, 'required': True, 'label': 'Название маршрута', 'max_length': 100},
    'description': {'type': str, 'required': True, 'label': 'Описание', 'max_length': 500},
    'duration': {'type': int, 'required': True, 'label': 'Продолжительность (дни)', 'min_value': 1},
    'price': {'type': float, 'required': True, 'label': 'Цена (USD)', 'min_value': 0.01},
    'difficulty': {'type': str, 'required': True, 'label': 'Сложность', 'choices': ['easy', 'medium', 'hard']},
}