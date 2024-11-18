"""
Модуль для управления БПЛА с использованием MAVLink.
"""

import time
import math
import logging
from typing import Optional, Dict, Union

from pymavlink import mavutil

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class UAVControl:
    """
    Класс для управления БПЛА через MAVLink.

    Args:
        connection_string (str): Строка подключения MAVLink.

    Attributes:
        master (mavutil.mavlink_connection): Экземпляр MAVLink соединения.
        seq (int): Последовательный номер для отправки пунктов миссии.
    """

    def __init__(self, connection_string: str):
        """
        Инициализация подключения к БПЛА.

        Args:
            connection_string (str): Строка подключения MAVLink.

        Raises:
            ConnectionError: Если соединение не удалось установить.
        """
        try:
            self.master = mavutil.mavlink_connection(connection_string)
            self.master.wait_heartbeat()
            logger.info("Соединение установлено")
            self.seq = 0  # Инициализация последовательного номера миссии
        except Exception as e:
            logger.error("Ошибка подключения: %s", e)
            raise ConnectionError(f"Failed to connect to UAV: {e}") from e

    def arm(self) -> None:
        """
        Армирование БПЛА для начала работы двигателей.

        Raises:
            RuntimeError: Если армирование не удалось.
        """
        try:
            self.master.arducopter_arm()
            self.master.motors_armed_wait()
            logger.info("БПЛА армирован")
        except Exception as e:
            logger.error("Ошибка армирования БПЛА: %s", e)
            raise RuntimeError(f"Failed to arm UAV: {e}") from e

    def disarm(self) -> None:
        """
        Остановка работы двигателей (Disarm).

        Raises:
            RuntimeError: Если остановка двигателей не удалась.
        """
        try:
            self.master.arducopter_disarm()
            self.master.motors_disarmed_wait()
            logger.info("БПЛА disarmed")
        except Exception as e:
            logger.error("Ошибка disarm БПЛА: %s", e)
            raise RuntimeError(f"Failed to disarm UAV: {e}") from e

    def set_mode(self, mode: str) -> None:
        """
        Установка режима полета БПЛА.

        Args:
            mode (str): Название режима (например, 'GUIDED', 'LAND').

        Raises:
            ValueError: Если режим не найден.
            RuntimeError: Если не удалось установить режим.
        """
        mode_mapping = self.master.mode_mapping()
        if not isinstance(mode_mapping, dict):
            logger.error("Ошибка: mode_mapping() не вернул словарь")
            raise RuntimeError("Не удалось получить список режимов полета")

        mode_id = mode_mapping.get(mode)
        if mode_id is None:
            raise ValueError(f"Неизвестный режим: {mode}")

        try:
            self.master.set_mode(mode_id)
            logger.info("Режим установлен: %s", mode)
        except Exception as e:
            logger.error("Ошибка установки режима %s: %s", mode, e)
            raise RuntimeError(f"Failed to set mode {mode}: {e}") from e

    def takeoff(self, altitude: float) -> None:
        """
        Команда на взлет до заданной высоты.

        Args:
            altitude (float): Целевая высота взлета в метрах.

        Raises:
            ValueError: Если высота отрицательная или равна нулю.
            RuntimeError: Если команда взлета не подтверждена.
        """
        if altitude <= 0:
            raise ValueError("Высота должна быть положительной")

        try:
            self.set_mode('GUIDED')
            self.arm()

            msg = self.master.recv_match(type='GLOBAL_POSITION_INT', blocking=True, timeout=5)
            if msg:
                current_lat = msg.lat / 1e7
                current_lon = msg.lon / 1e7
            else:
                raise RuntimeError("Не удалось получить текущие координаты для взлета")

            self.master.mav.command_long_send(
                self.master.target_system,
                self.master.target_component,
                mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
                0,
                0, 0, 0, 0,
                current_lat,
                current_lon,
                altitude
            )

            if not self.wait_command_ack(mavutil.mavlink.MAV_CMD_NAV_TAKEOFF):
                raise RuntimeError("Команда взлета не подтверждена")
            logger.info("Взлет на высоту %s метров", altitude)
        except Exception as e:
            logger.error("Ошибка взлета: %s", e)
            raise RuntimeError(f"Failed to take off: {e}") from e

    def land(self) -> None:
        """
        Команда на посадку.

        Raises:
            RuntimeError: Если команда посадки не подтверждена.
        """
        try:
            self.set_mode('LAND')
            if not self.wait_command_ack(mavutil.mavlink.MAV_CMD_NAV_LAND):
                raise RuntimeError("Команда посадки не подтверждена")
            logger.info("Посадка начата")
        except Exception as e:
            logger.error("Ошибка посадки: %s", e)
            raise RuntimeError(f"Failed to land: {e}") from e

    def wait_command_ack(self, command: int, timeout: int = 10) -> bool:
        """
        Ожидание подтверждения выполнения команды.

        Args:
            command (int): Код команды MAVLink.
            timeout (int): Время ожидания в секундах.

        Returns:
            bool: True, если команда подтверждена, False в противном случае.
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            ack_msg = self.master.recv_match(type='COMMAND_ACK', blocking=True, timeout=1)
            if ack_msg and ack_msg.command == command:
                if ack_msg.result == mavutil.mavlink.MAV_RESULT_ACCEPTED:
                    logger.info("Команда %s подтверждена", command)
                    return True
                logger.error("Команда %s отклонена с кодом %s", command, ack_msg.result)
                return False
        logger.error("Не получено подтверждение для команды %s", command)
        return False

    def get_telemetry(self) -> Optional[Dict[str, Union[float, int]]]:
        """
        Получение телеметрических данных от БПЛА.

        Returns:
            Optional[Dict[str, Union[float, int]]]: Словарь с телеметрией (координаты, высота, скорость, батарея)
            или None в случае ошибки.
        """
        try:
            telemetry = {}

            msg = self.master.recv_match(type=['GLOBAL_POSITION_INT', 'VFR_HUD', 'SYS_STATUS'], blocking=True, timeout=5)
            if msg:
                if msg.get_type() == 'GLOBAL_POSITION_INT':
                    telemetry['lat'] = msg.lat / 1e7
                    telemetry['lon'] = msg.lon / 1e7
                    telemetry['alt'] = msg.alt / 1000
                elif msg.get_type() == 'VFR_HUD':
                    telemetry['ground_speed'] = msg.groundspeed
                    telemetry['airspeed'] = msg.airspeed
                elif msg.get_type() == 'SYS_STATUS':
                    telemetry['battery'] = msg.battery_remaining
            return telemetry
        except Exception as e:
            logger.error("Ошибка получения телеметрии: %s", e)
            return None
