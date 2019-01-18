#!/usr/bin/env python3
import ctre

import wpilib

import ports
import RobotMethods

class MyRobot(wpilib.TimedRobot):

    def robotInit(self):
        '''Robot initialization function'''
        self.driveMethods = RobotMethods.Driver()
        self.armMethods = RobotMethods.ArmMotorDriver()
        
        self.controller = wpilib.XboxController(ports.controllerPorts.get("driverController"))

        self.driveMethods.driveTrainInit(self)
        self.armMethods.armMotorDriverInit(self)

    def teleopPeriodic(self):
        self.driveMethods.driveRobotWithJoystick(self.controller)
        self.armMethods.driveArmMotorWithJoystick(self.controller)

if __name__ == "__main__":
    wpilib.run(MyRobot)
