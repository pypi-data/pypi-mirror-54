'''
Created on 02.01.2019

@author: ed
'''

from PyTrinamic.ic.ic_interface import ic_interface
from PyTrinamic.ic.TMC4671.TMC4671_register import TMC4671_register
from PyTrinamic.ic.TMC4671.TMC4671_register_variant import TMC4671_register_variant
from PyTrinamic.ic.TMC4671.TMC4671_fields import TMC4671_fields
from PyTrinamic.helpers import TMC_helpers

class TMC4671(ic_interface):

    def __init__(self, parent):
        self.parent = parent
        self.tmc4671_reg = TMC4671_register()
        self.tmc4671_var = TMC4671_register_variant()
        self.tmc4671_ms = TMC4671_fields()

    def register(self):
        return self.tmc4671_reg

    def variants(self):
        return self.tmc4671_var

    def maskShift(self):
        return self.tmc4671_ms;

    def showChipInfo(self):
        print("TMC4671 chip info:")

        self.writeRegister(self.tmc4671_reg.CHIPINFO_ADDR, self.tmc4671_var.CHIPINFO_ADDR_SI_TYPE)
        print("SI_TYPE:    " + hex(self.readRegister(self.tmc4671_reg.CHIPINFO_DATA)))

        self.writeRegister(self.tmc4671_reg.CHIPINFO_ADDR, self.tmc4671_var.CHIPINFO_ADDR_SI_VERSION)
        print("SI_VERSION: " + hex(self.readRegister(self.tmc4671_reg.CHIPINFO_DATA)))

        self.writeRegister(self.tmc4671_reg.CHIPINFO_ADDR, self.tmc4671_var.CHIPINFO_ADDR_SI_DATA)
        print("SI_DATA:    " + hex(self.readRegister(self.tmc4671_reg.CHIPINFO_DATA)))

        self.writeRegister(self.tmc4671_reg.CHIPINFO_ADDR, self.tmc4671_var.CHIPINFO_ADDR_SI_TIME)
        print("SI_TIME:    " + hex(self.readRegister(self.tmc4671_reg.CHIPINFO_DATA)))

        self.writeRegister(self.tmc4671_reg.CHIPINFO_ADDR, self.tmc4671_var.CHIPINFO_ADDR_SI_VARIANT)
        print("SI_VARIANT: " + hex(self.readRegister(self.tmc4671_reg.CHIPINFO_DATA)))

        self.writeRegister(self.tmc4671_reg.CHIPINFO_ADDR, self.tmc4671_var.CHIPINFO_ADDR_SI_BUILD)
        print("SI_BUILD:   " + hex(self.readRegister(self.tmc4671_reg.CHIPINFO_DATA)))

    " use parent readRegister/writeRegister from evaluation board or interface"
    def writeRegister(self, registerAddress, value):
        self.parent.writeRegister(registerAddress, value);

    def readRegister(self, registerAddress):
        return self.parent.readRegister(registerAddress)

    def writeRegisterField(self, registerAddress, value, mask, shift):
        return self.writeRegister(registerAddress, TMC_helpers.field_set(self.readRegister(registerAddress), mask, shift, value))

    def readRegisterField(self, registerAddress, mask, shift):
        return TMC_helpers.field_get(self.readRegister(registerAddress), mask, shift)

    " ic specific functions "

    def actualVelocity(self):
        return TMC_helpers.toSigned32(self.readRegister(self.tmc4671_reg.PID_VELOCITY_ACTUAL))

    def pwm_maxcnt(self):
        maxcnt = self.readRegister(self.tmc4671_reg.PWM_MAXCNT);
        print("get() : pwm_maxcnt:=" + str(hex(maxcnt)) + "(=" + str(maxcnt) + ")")
        return maxcnt
