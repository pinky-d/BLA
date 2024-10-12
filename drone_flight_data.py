# Пример программы на Python для работы с данными о полетах БЛА

# Список данных о полетах. Каждый полет представлен в виде словаря.
# Ключи: 'время', 'координаты', 'высота', 'скорость'
flights_data = [
    {"время": "2024-10-10 14:30", "координаты": (55.7558, 37.6173), "высота": 300, "скорость": 50},
    {"время": "2024-10-10 14:45", "координаты": (55.7558, 37.6173), "высота": 350, "скорость": 60},
    {"время": "2024-10-10 15:00", "координаты": (55.7558, 37.6173), "высота": 280, "скорость": 55},
    {"время": "2024-10-10 15:15", "координаты": (55.7558, 37.6173), "высота": 330, "скорость": 70}
]

# Функция для сортировки данных по времени полета от старых к новым
def sort_by_time(flights):
    # Используем функцию sorted и сортируем по ключу 'время'
    sorted_flights = sorted(flights, key=lambda x: x['время'])
    return sorted_flights

# Функция для поиска полетов, где высота превышает 320 метров
def find_flight_by_altitude(flights, min_altitude):
    # Проходим по каждому полету и проверяем, превышает ли высота заданный порог
    for flight in flights:
        if flight['высота'] > min_altitude:
            return flight  # Возвращаем первый найденный полет, подходящий по условию
    return None  # Если нет таких полетов, возвращаем None

# Сортируем данные по времени полета
sorted_flights = sort_by_time(flights_data)

# Ищем полет с высотой больше 320 метров
flight_with_high_altitude = find_flight_by_altitude(sorted_flights, 320)

# Вывод данных
print("Сортировка полетов по времени (от старых к новым):")
for flight in sorted_flights:
    print(f"Время: {flight['время']}, Координаты: {flight['координаты']}, Высота: {flight['высота']} м, Скорость: {flight['скорость']} км/ч")

if flight_with_high_altitude:
    print("\nПолет с высотой больше 320 метров:")
    print(f"Время: {flight_with_high_altitude['время']}, Координаты: {flight_with_high_altitude['координаты']}, Высота: {flight_with_high_altitude['высота']} м, Скорость: {flight_with_high_altitude['скорость']} км/ч")
else:
    print("\nНет полетов с высотой больше 320 метров.")