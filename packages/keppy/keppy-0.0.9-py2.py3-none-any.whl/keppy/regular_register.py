"""Normal register module"""
from keppy.register import Register

class RegularRegister(Register):
    """Represents a normal register
    Between K0000 - K9999.
    Each address is a byte on an 8-bit device and a word on a 16-bit
    device.
    To get a bit, you specify KXXXX.Y on an 8-bit device
    and KXXXX.YY on a 16-bit device.
    Can be data type Word, Short, BCD,
    DWord, Long, LBCD, Float, LLong, QWord,
    Double, Date, Boolean"""

    def __init__(self, is_16bit, initial_address="K0000"):
        Register.__init__(self, is_16bit, initial_address)
