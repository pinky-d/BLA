import unittest
from unittest.mock import MagicMock, patch
from mission_planner import MissionPlanner


class TestMissionPlanner(unittest.TestCase):

    @patch('mission_planner.UAVControl')
    def setUp(self, mock_uav_control):
        self.mock_uav = MagicMock()
        mock_uav_control.return_value = self.mock_uav
        self.mission_planner = MissionPlanner("tcp:127.0.0.1:5760")

    def test_execute_mission_success(self):
        waypoints = [(47.3977, 8.5456, 10), (47.3980, 8.5460, 20)]
        self.mock_uav.get_telemetry.side_effect = [
            {'lat': 47.3977, 'lon': 8.5456, 'alt': 10},
            {'lat': 47.3980, 'lon': 8.5460, 'alt': 20}
        ]

        self.mission_planner.execute_mission(waypoints)

        self.mock_uav.arm.assert_called_once()
        self.mock_uav.set_mode.assert_any_call('GUIDED')
        self.mock_uav.takeoff.assert_called_once_with(10)
        self.mock_uav.goto.assert_any_call(47.3977, 8.5456, 10)
        self.mock_uav.goto.assert_any_call(47.3980, 8.5460, 20)
        self.mock_uav.set_mode.assert_any_call('RTL')
        self.mock_uav.disarm.assert_called_once()

    def test_execute_mission_fail_reach_waypoint(self):
        waypoints = [(47.3977, 8.5456, 10), (47.3980, 8.5460, 20)]
        self.mock_uav.get_telemetry.return_value = {'lat': 47.3977, 'lon': 8.5456, 'alt': 10}

        with self.assertRaises(Exception):
            self.mission_planner.execute_mission(waypoints)

        self.mock_uav.arm.assert_called_once()
        self.mock_uav.set_mode.assert_any_call('GUIDED')
        self.mock_uav.takeoff.assert_called_once_with(10)
        self.mock_uav.goto.assert_any_call(47.3977, 8.5456, 10)
        self.mock_uav.disarm.assert_called_once()
