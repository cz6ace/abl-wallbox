from enum import Enum
import logging
import minimalmodbus
import serial

ABL_REG_DEVICE_ID = (0x0001, 2, "R")
ABL_REG_MODBUS_SETTINGS = (0x0003, 1, "R")
ABL_REG_MOD_STATE = (0x0005, 1, "W")
ABL_REG_SYSTEM_FLAGS = (0x0006, 2, "R")
ABL_REG_SET_ICMAX = (0x0014, 1, "W")
ABL_REG_SET_DEVICE_ID = (0x002C, 1, "W")
ABL_REG_READ_CURRENT_FULL = (0x002E, 5, "R")
ABL_REG_READ_CURRENT_AMPS = (0x0033, 3, "R")

class Status(Enum):
	NO_RESPONSE         =   0, "No response from EVCC"
	WAIT_FOR_CONNECTION = 161, "Wait for connection"
	WAIT_FOR_ENABLEMENT = 177, "Wait for enablement"
	CHARGING_ENABLED =    178, "Charging enabled"
	CHARGING =            194, "Charging"

	@staticmethod
	def from_val(val):
		for e in Status:
			if e.value[0] == val:
				return e
		return NO_RESPONSE
# Definition of states
# A1 - Waiting for EV
# B1 - EV is asking for charging
# B2 - EV has the permission to charge
# C2 - EV is charged
# C3 - C2, reduced current (error F16, F17)
# C4 - C2, reduced current (imbalance F15)
# E0 - Outlet disabled
# E1 - Production test
# E2 - EVCC setup mode
# E3 - Bus idle
# F1 - Unintended closed contact (Welding)
# F2 - Internal error
# F3 - DC residual current detected
# F4 - Upstream communication timeout
# F5 - Lock of socket failed
# F6 - CS out of range
# F7 - State D requested by EV
# F8 - CP out of range
# F9 - Overcurrent detected
# F10 - Temperature outside limits
# F11 - Unintended opened contactu


class Abl():
    def __init__(self, ABL):
        self.ABL=ABL
        self.Initialize_Wallbox()

    def Initialize_Wallbox(self):
        self.ABL.serial.baudrate = 38400
        self.ABL.serial.parity = serial.PARITY_EVEN
        self.ABL.serial.bytesize = 8
        self.ABL.serial.stopbits = 1

    def Wake_Up(self):
        try:
            self.ABL.read_registers(15,5)
        except:
            pass

    def Read_Status(self):
        registers = self.ABL.read_registers(ABL_REG_READ_CURRENT_FULL[0], ABL_REG_READ_CURRENT_FULL[1])
        status = registers[0] & 0xFF
        logging.info(registers)
        cycle = (registers[1] & 0b111111111111) / 10
        return (Status.from_val(status), cycle, *(registers[2:]))

    def To_Current(self, cycle):
        return cycle / 1.66667

    def Set_Duty(self,duty):
        """Set duty 8..100%"""
        assert 8 <= duty <= 100, f"Passed {duty}"
        logging.info(f"Set duty to {duty}")
        self.ABL.write_registers(20, [int(duty*10)])

    def Set_Current(self, current):
        """Set current 6..16A"""
        assert 6 <= current <= 16, f"Passed {current}"
        # 10…85 %
        # DC * 0,6 A
        # 8…10 %: max 6 A
        # 1/0.6 == 16.6667
        duty = current * 1.6667
        self.Set_Duty(duty)


