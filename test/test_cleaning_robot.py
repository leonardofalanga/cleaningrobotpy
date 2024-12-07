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

    @patch.object(IBS, "get_charge_left")
    def test_execute_command_forward(self, mock_ibs: Mock):
        system = CleaningRobot()
        system.initialize_robot()
        mock_ibs.return_value = 15
        system.execute_command(system.FORWARD)
        self.assertEqual(system.robot_status(), "(0,1,N)")

    @patch.object(IBS, "get_charge_left")
    def test_execute_command_rotation_r(self, mock_ibs: Mock):
        system = CleaningRobot()
        system.initialize_robot()
        mock_ibs.return_value = 15
        system.execute_command(system.RIGHT)
        self.assertEqual(system.robot_status(), "(0,0,E)")

    @patch.object(IBS, "get_charge_left")
    def test_execute_command_rotation_l(self, mock_ibs: Mock):
        system = CleaningRobot()
        system.initialize_robot()
        mock_ibs.return_value = 15
        system.execute_command(system.LEFT)
        self.assertEqual(system.robot_status(), "(0,0,W)")

    @patch.object(IBS, "get_charge_left")
    def test_execute_command_error(self, mock_ibs: Mock):
        system = CleaningRobot()
        system.initialize_robot()
        mock_ibs.return_value = 15
        self.assertRaises(CleaningRobotError, system.execute_command, "b")

    @patch.object(IBS, "get_charge_left")
    @patch.object(GPIO, "input")
    def  test_obstacle_found(self, mock_input: Mock, mock_ibs: Mock):
        system = CleaningRobot()
        system.initialize_robot()
        mock_ibs.return_value = 15
        mock_input.return_value = 1
        self.assertEqual(system.execute_command(system.FORWARD), "(0,0,N)(0,1)")

    @patch.object(IBS, "get_charge_left")
    def test_execute_command_with_charge_left_less_10 (self, mock_ibs: Mock):
        system = CleaningRobot()
        system.initialize_robot()
        mock_ibs.return_value = 9
        system.pos_x = 1
        system.pos_y = 1
        system.heading = "N"
        system.manage_cleaning_system()
        self.assertEqual(system.execute_command(system.FORWARD), "!(1,1,N)")

    @patch.object(IBS, "get_charge_left")
    @patch.object(GPIO, "output")
    def test_vibration_motor_obstacles(self, mock_output: Mock, mock_ibs: Mock):
        system = CleaningRobot()
        system.initialize_robot()
        mock_ibs.return_value = 15
        system.execute_command(system.FORWARD)
        mock_output.assert_called_once_with(system.VIBRATION, GPIO.HIGH)


