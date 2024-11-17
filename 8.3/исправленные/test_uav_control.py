import unittest
from unittest.mock import MagicMock, patch
from uav_control import UAVControl


class TestUAVControl(unittest.TestCase):

    @patch('uav_control.mavutil.mavlink_connection')
    def setUp(self, mock_connection):
        # Создаём mock для MAVLink
        self.mock_master = MagicMock()
        mock_connection.return_value = self.mock_master
        self.uav = UAVControl("tcp:127.0.0.1:5760")

    def test_arm_success(self):
        self.mock_master.motors_armed_wait.return_value = True
        self.uav.arm()
        self.mock_master.arducopter_arm.assert_called_once()
        self.mock_master.motors_armed_wait.assert_called_once()

    def test_disarm_success(self):
        self.mock_master.motors_disarmed_wait.return_value = True
        self.uav.disarm()
        self.mock_master.arducopter_disarm.assert_called_once()
        self.mock_master.motors_disarmed_wait.assert_called_once()

    def test_set_mode_success(self):
        self.mock_master.mode_mapping.return_value = {'GUIDED': 4}
        self.uav.set_mode('GUIDED')
        self.mock_master.set_mode.assert_called_once_with(4)

    def test_takeoff_invalid_altitude(self):
        with self.assertRaises(ValueError):
            self.uav.takeoff(-10)

    @patch('uav_control.logger')
    def test_get_telemetry_no_message(self, mock_logger):
        self.mock_master.recv_match.return_value = None
        telemetry = self.uav.get_telemetry()
        self.assertIsNone(telemetry)
        mock_logger.warning.assert_called_once_with("Телеметрия недоступна")
