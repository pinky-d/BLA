import pytest
from unittest.mock import MagicMock, patch
from uav_module import UAVControl  # Замените на ваш модуль

@pytest.fixture
def mock_uav_control():
    """Фикстура для создания мока UAVControl."""
    with patch('uav_module.mavutil.mavlink_connection') as mock_connection:
        mock_connection.return_value = MagicMock()
        uav_control = UAVControl(connection_string="udp:127.0.0.1:14550")
        return uav_control

def test_land_success(mock_uav_control):
    """Тест успешной посадки."""
    mock_uav_control.master.recv_match = MagicMock(side_effect=[
        MagicMock(command=mavutil.mavlink.MAV_CMD_DO_LAND_START, result=mavutil.mavlink.MAV_RESULT_ACCEPTED)
    ])
    mock_uav_control.wait_command_ack = MagicMock(return_value=True)

    mock_uav_control.land()

    mock_uav_control.set_mode.assert_called_with('LAND')
    mock_uav_control.wait_command_ack.assert_called_with(mavutil.mavlink.MAV_CMD_DO_LAND_START)

def test_land_fail(mock_uav_control):
    """Тест неудачной посадки (нет подтверждения)."""
    mock_uav_control.wait_command_ack = MagicMock(return_value=False)

    with pytest.raises(RuntimeError, match="Команда на посадку не подтверждена"):
        mock_uav_control.land()

def test_land_exception(mock_uav_control):
    """Тест исключения в процессе посадки."""
    mock_uav_control.set_mode = MagicMock(side_effect=RuntimeError("Ошибка режима"))

    with pytest.raises(RuntimeError, match="Failed to land UAV: Ошибка режима"):
        mock_uav_control.land()
