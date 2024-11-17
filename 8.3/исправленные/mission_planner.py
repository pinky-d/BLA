from uav_control import UAVControl
import time
from typing import List, Tuple
import logging

logger = logging.getLogger(__name__)

class MissionPlanner:
    """
    Класс для планирования и выполнения миссий БПЛА.
    """

    def __init__(self, connection_string: str):
        """
        Инициализация планировщика миссий.
        """
        self.uav = UAVControl(connection_string)

    def execute_mission(self, waypoints: List[Tuple[float, float, float]]) -> None:
        """
        Выполнение миссии по заданным точкам.
        """
        try:
            self.uav.arm()
            self.uav.set_mode('GUIDED')
            self.uav.takeoff(waypoints[0][2])

            for waypoint in waypoints:
                logger.info(f"Летим к точке {waypoint}")
                self.uav.goto(*waypoint)
                time.sleep(5)

            self.uav.set_mode('RTL')
            logger.info("Возвращение домой")
            self.uav.disarm()
        except Exception as e:
            logger.error(f"Ошибка выполнения миссии: {e}")
            self.uav.disarm()
            raise
