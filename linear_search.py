# Список команд БПЛА с параметрами: команда, время, координаты и приоритет.
commands = [
    {"команда": "Взлет", "время": "2024-10-10 14:45", "координаты": (55.7558, 37.6173), "приоритет": 3},
    {"команда": "Наведение на цель", "время": "2024-10-10 14:30", "координаты": (55.7558, 37.6173), "приоритет": 1},
    {"команда": "Посадка", "время": "2024-10-10 14:50", "координаты": (55.7558, 37.6173), "приоритет": 2},
    {"команда": "Обход препятствия", "время": "2024-10-10 14:40", "координаты": (55.7558, 37.6173), "приоритет": 1}
]

# Функция для линейного поиска команды по типу, времени, координатам и приоритету
def linear_search(commands, search_params):
    for command in commands:
        # Проверяем, совпадают ли все параметры команды с искомыми
        if (command['команда'] == search_params['команда'] and
            command['время'] == search_params['время'] and
            command['координаты'] == search_params['координаты'] and
            command['приоритет'] == search_params['приоритет']):
            return command  # Возвращаем найденную команду
    return None  # Если команда не найдена, возвращаем None

# Параметры команды, которую мы ищем
search_command = {
    "команда": "Посадка",
    "время": "2024-10-10 14:50",
    "координаты": (55.7558, 37.6173),
    "приоритет": 2
}

# Поиск команды
found_command = linear_search(commands, search_command)

# Вывод результата поиска
if found_command:
    print("Команда найдена:")
    print(f"Команда: {found_command['команда']}, Время: {found_command['время']}, Координаты: {found_command['координаты']}, Приоритет: {found_command['приоритет']}")
else:
    print("Команда не найдена.")
