# Список команд БПЛА. Каждая команда — это словарь с приоритетом и временем получения.
commands = [
    {"команда": "Взлет", "приоритет": 3, "время": "2024-10-10 14:45"},
    {"команда": "Наведение на цель", "приоритет": 1, "время": "2024-10-10 14:30"},
    {"команда": "Посадка", "приоритет": 2, "время": "2024-10-10 14:50"},
    {"команда": "Обход препятствия", "приоритет": 1, "время": "2024-10-10 14:40"}
]

# Функция для реализации пузырьковой сортировки по приоритету, а затем по времени
def bubble_sort(commands):
    n = len(commands)  # Длина списка команд
    for i in range(n):
        for j in range(0, n - i - 1):
            # Сравниваем приоритет команд. Если приоритет первой команды больше, меняем их местами.
            if commands[j]['приоритет'] > commands[j + 1]['приоритет']:
                commands[j], commands[j + 1] = commands[j + 1], commands[j]
            # Если приоритеты одинаковые, сортируем по времени получения.
            elif commands[j]['приоритет'] == commands[j + 1]['приоритет']:
                if commands[j]['время'] > commands[j + 1]['время']:
                    commands[j], commands[j + 1] = commands[j + 1], commands[j]

# Сортируем команды с помощью пузырьковой сортировки
bubble_sort(commands)

# Выводим отсортированные команды
print("Отсортированные команды (по приоритету и времени):")
for command in commands:
    print(f"Команда: {command['команда']}, Приоритет: {command['приоритет']}, Время получения: {command['время']}")
