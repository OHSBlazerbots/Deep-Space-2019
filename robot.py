#!/usr/bin/env python3
import ctre

import wpilib

import ports
import RobotMethods
from NetworkData import SendData

class MyRobot(wpilib.TimedRobot):

    def robotInit(self):
        '''Robot initialization function'''
        self.driveMethods = RobotMethods.Driver()
        self.armMethods = RobotMethods.ArmMotorDriver()
        self.liftMethods = RobotMethods.LiftDriver()
        
        self.driverController = wpilib.XboxController(ports.controllerPorts.get("driverController"))
        self.coDriverController = wpilib.XboxController(ports.controllerPorts.get("codriverController"))

        self.driveMethods.driveTrainInit(self)
        self.armMethods.armMotorDriverInit(self)
        self.liftMethods.liftDriverInit(self)

        wpilib.CameraServer.launch()

        #self.sendData = SendData()
        #self.sendData.init()

    def autonomousPeriodic(self):
        self.teleopPeriodic()

    def teleopPeriodic(self):
        #self.sendData.sendPDPData()
        self.driveMethods.driveRobotWithJoystick(self.driverController)
        self.armMethods.driveArmMotorWithJoystick(self.coDriverController)
        self.liftMethods.driveLiftWithJoystick(self.coDriverController)

if __name__ == "__main__":
    wpilib.run(MyRobot)
