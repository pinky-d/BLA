# Массив скоростей полета БЛА (в км/ч)
flight_speeds = [50, 60, 55, 70, 45, 65, 80]

# Функция для линейного поиска значения скорости в массиве
def linear_search_speed(speeds, target_speed):
    for i in range(len(speeds)):
        if speeds[i] == target_speed:
            return i  # Возвращаем индекс, если скорость найдена
    return -1  # Возвращаем -1, если значение не найдено

# Тестирование алгоритма линейного поиска
def test_linear_search_speed():
    # Массив скоростей для тестирования
    speeds_to_test = [55, 100, 80, 45, 90]

    # Проходим по каждому тестовому значению
    for speed in speeds_to_test:
        result = linear_search_speed(flight_speeds, speed)
        if result != -1:
            print(f"Скорость {speed} км/ч найдена на индексе {result}.")
        else:
            print(f"Скорость {speed} км/ч не найдена в массиве.")

# Запускаем тестирование
test_linear_search_speed()
