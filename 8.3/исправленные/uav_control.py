from pymavlink import mavutil
import time
import math
from typing import Optional, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UAVControl:
    """
    Класс для управления БПЛА через MAVLink.
    """

    def __init__(self, connection_string: str):
        """
        Инициализация подключения к БПЛА.
        """
        try:
            self.master = mavutil.mavlink_connection(connection_string)
            self.master.wait_heartbeat()
            logger.info("Соединение установлено")
        except Exception as e:
            logger.error(f"Ошибка подключения: {e}")
            raise

    def arm(self) -> None:
        """
        Взведение (Arm) БПЛА для начала работы двигателей.
        """
        try:
            self.master.arducopter_arm()
            self.master.motors_armed_wait()
            logger.info("БПЛА взведён")
        except Exception as e:
            logger.error(f"Ошибка взведения БПЛА: {e}")
            raise

    def disarm(self) -> None:
        """
        Разоружение (Disarm) БПЛА для остановки двигателей.
        """
        try:
            self.master.arducopter_disarm()
            self.master.motors_disarmed_wait()
            logger.info("БПЛА разоружён")
        except Exception as e:
            logger.error(f"Ошибка разоружения БПЛА: {e}")
            raise

    def set_mode(self, mode: str) -> None:
        """
        Установка режима полёта БПЛА.
        """
        mode_mapping = self.master.mode_mapping()
        mode_id = mode_mapping.get(mode)
        if mode_id is None:
            logger.error(f"Неизвестный режим: {mode}")
            raise ValueError(f"Режим {mode} не найден")

        try:
            self.master.set_mode(mode_id)
            logger.info(f"Режим установлен: {mode}")
        except Exception as e:
            logger.error(f"Ошибка установки режима {mode}: {e}")
            raise

    def takeoff(self, altitude: float) -> None:
        """
        Команда на взлёт до заданной высоты.
        """
        if altitude <= 0:
            raise ValueError("Высота должна быть положительной")

        try:
            self.set_mode('GUIDED')
            self.master.mav.command_long_send(
                self.master.target_system,
                self.master.target_component,
                mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
                0, 0, 0, 0, 0, 0, altitude
            )
            logger.info(f"Взлёт на высоту {altitude} метров")
        except Exception as e:
            logger.error(f"Ошибка взлёта: {e}")
            raise

    def get_telemetry(self) -> Optional[Dict[str, float]]:
        """
        Получение телеметрических данных от БПЛА.
        """
        try:
            msg = self.master.recv_match(type='GLOBAL_POSITION_INT', blocking=True, timeout=5)
            if msg:
                telemetry = {
                    'lat': msg.lat / 1e7,
                    'lon': msg.lon / 1e7,
                    'alt': msg.alt / 1000
                }
                return telemetry
            else:
                logger.warning("Телеметрия недоступна")
                return None
        except Exception as e:
            logger.error(f"Ошибка получения телеметрии: {e}")
            return None
