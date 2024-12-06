from unittest import TestCase
from unittest.mock import Mock, patch, call

from mock import GPIO
from mock.ibs import IBS
from src.cleaning_robot import CleaningRobot, CleaningRobotError


class TestCleaningRobot(TestCase):

    def test_initialize_robot(self):
        system=CleaningRobot()
        system.initialize_robot()
        self.assertEqual(system.robot_status(),"(0,0,N)")

    @patch.object(IBS, "get_charge_left")
    @patch.object(GPIO, "output")
    def test_manage_cleaning_system_up_10(self, mock_ledclean: Mock, mock_ibs: Mock):
        system=CleaningRobot()
        mock_ibs.return_value= 15
        system.manage_cleaning_system()
        mock_ledclean.assert_has_calls([call(system.RECHARGE_LED_PIN, GPIO.LOW), call(system.CLEANING_SYSTEM_PIN, GPIO.HIGH)])

    @patch.object(IBS, "get_charge_left")
    @patch.object(GPIO, "output")
    def test_manage_cleaning_system_minus_10(self, mock_ledclean: Mock, mock_ibs: Mock):
        system = CleaningRobot()
        mock_ibs.return_value= 5
        system.manage_cleaning_system()
        mock_ledclean.assert_has_calls([call(system.RECHARGE_LED_PIN, GPIO.HIGH), call(system.CLEANING_SYSTEM_PIN, GPIO.LOW)])

    def test_execute_command_forward(self):
        system = CleaningRobot()
        system.initialize_robot()
        system.execute_command(system.FORWARD)
        self.assertEqual(system.robot_status(), "(0,1,N)")

    def test_execute_command_rotation_r(self):
        system = CleaningRobot()
        system.initialize_robot()
        system.execute_command(system.RIGHT)
        self.assertEqual(system.robot_status(), "(0,0,E)")

    def test_execute_command_rotation_l(self):
        system = CleaningRobot()
        system.initialize_robot()
        system.execute_command(system.LEFT)
        self.assertEqual(system.robot_status(), "(0,0,W)")

    def test_execute_command_error(self):
        system = CleaningRobot()
        system.initialize_robot()
        self.assertRaises(CleaningRobotError, system.execute_command, "b")



