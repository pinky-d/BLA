import unittest
from unittest.mock import MagicMock, patch
from uav_control import UAVControl, mavutil


class TestUAVControl(unittest.TestCase):
    """
    Тесты для класса UAVControl.
    """

    def setUp(self):
        """
        Настройка перед каждым тестом.
        Создаётся mock-объект для mavutil.mavlink_connection.
        """
        self.mock_master = MagicMock()
        self.mock_connection = patch("uav_control.mavutil.mavlink_connection", return_value=self.mock_master)
        self.mock_connection.start()

        # Инициализация тестируемого объекта
        self.uav_control = UAVControl("udp:127.0.0.1:14550")

    def tearDown(self):
        """
        Очистка после каждого теста.
        """
        self.mock_connection.stop()

    def test_arm_success(self):
        """
        Тест успешного армирования.
        """
        self.mock_master.motors_armed_wait.return_value = True
        self.uav_control.arm()
        self.mock_master.arducopter_arm.assert_called_once()
        self.mock_master.motors_armed_wait.assert_called_once()

    def test_arm_failure(self):
        """
        Тест ошибки армирования.
        """
        self.mock_master.arducopter_arm.side_effect = RuntimeError("Failed to arm UAV")

        with self.assertRaises(RuntimeError) as context:
            self.uav_control.arm()

        self.assertIn("Failed to arm UAV", str(context.exception))
        self.mock_master.arducopter_arm.assert_called_once()

    def test_get_telemetry(self):
        """
        Тест получения телеметрии.
        """
        # Mock для GLOBAL_POSITION_INT
        telemetry_data = {
            "lat": 52.0,
            "lon": 13.0,
            "alt": 100.0,
            "groundspeed": 10.0,
            "battery_remaining": 90.0,
        }

        self.mock_master.recv_match.side_effect = [
            MagicMock(get_type=lambda: "GLOBAL_POSITION_INT", lat=520000000, lon=130000000, alt=100000),
            MagicMock(get_type=lambda: "VFR_HUD", groundspeed=10.0),
            MagicMock(get_type=lambda: "SYS_STATUS", battery_remaining=90),
        ]

        telemetry = self.uav_control.get_telemetry()

        self.assertIsNotNone(telemetry)
        self.assertEqual(telemetry["lat"], telemetry_data["lat"])
        self.assertEqual(telemetry["lon"], telemetry_data["lon"])
        self.assertEqual(telemetry["alt"], telemetry_data["alt"])
        self.assertEqual(telemetry["groundspeed"], telemetry_data["groundspeed"])
        self.assertEqual(telemetry["battery_remaining"], telemetry_data["battery_remaining"])

    def test_get_telemetry_no_data(self):
        """
        Тест получения телеметрии при отсутствии данных.
        """
        self.mock_master.recv_match.return_value = None
        telemetry = self.uav_control.get_telemetry()
        self.assertIsNone(telemetry)

    def test_land_success(self):
        """
        Тест успешной посадки.
        """
        self.mock_master.set_mode.return_value = None
        self.mock_master.recv_match.side_effect = [
            MagicMock(command=mavutil.mavlink.MAV_CMD_NAV_LAND, result=mavutil.mavlink.MAV_RESULT_ACCEPTED)
        ]

        self.uav_control.land()

        self.mock_master.set_mode.assert_called_once_with(self.mock_master.mode_mapping()["LAND"])
        self.mock_master.recv_match.assert_called()

    def test_land_failure(self):
        """
        Тест ошибки при посадке.
        """
        self.mock_master.recv_match.side_effect = [
            MagicMock(command=mavutil.mavlink.MAV_CMD_NAV_LAND, result=mavutil.mavlink.MAV_RESULT_DENIED)
        ]

        with self.assertRaises(RuntimeError) as context:
            self.uav_control.land()

        self.assertIn("Посадка не подтверждена", str(context.exception))

    def test_takeoff_success(self):
        """
        Тест успешного взлёта.
        """
        self.mock_master.recv_match.side_effect = [
            MagicMock(get_type=lambda: "GLOBAL_POSITION_INT", lat=520000000, lon=130000000),
            MagicMock(command=mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, result=mavutil.mavlink.MAV_RESULT_ACCEPTED),
        ]

        self.uav_control.takeoff(altitude=50.0)

        self.mock_master.mav.command_long_send.assert_called()
        self.mock_master.recv_match.assert_called()

    def test_takeoff_failure(self):
        """
        Тест ошибки при взлёте.
        """
        self.mock_master.recv_match.side_effect = [
            MagicMock(get_type=lambda: "GLOBAL_POSITION_INT", lat=520000000, lon=130000000),
            MagicMock(command=mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, result=mavutil.mavlink.MAV_RESULT_DENIED),
        ]

        with self.assertRaises(RuntimeError) as context:
            self.uav_control.takeoff(altitude=50.0)

        self.assertIn("Команда взлёта не подтверждена", str(context.exception))

    def test_set_mode_success(self):
        """
        Тест успешной установки режима.
        """
        mode_mapping = {"GUIDED": 4}
        self.mock_master.mode_mapping.return_value = mode_mapping
        self.uav_control.set_mode("GUIDED")
        self.mock_master.set_mode.assert_called_once_with(4)

    def test_set_mode_failure(self):
        """
        Тест ошибки установки режима.
        """
        mode_mapping = {"GUIDED": 4}
        self.mock_master.mode_mapping.return_value = mode_mapping

        with self.assertRaises(ValueError) as context:
            self.uav_control.set_mode("UNKNOWN")

        self.assertIn("Неизвестный режим", str(context.exception))
        self.mock_master.set_mode.assert_not_called()


if __name__ == "__main__":
    unittest.main()
