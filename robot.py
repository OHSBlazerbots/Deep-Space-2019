#!/usr/bin/env python3
import ctre

import wpilib

import ports
import RobotMethods
import ControllerMethods
from NetworkData import SendData

class MyRobot(wpilib.TimedRobot):

    def robotInit(self):
        '''Robot initialization function'''
        self.driveMethods = RobotMethods.Driver()
        self.armMethods = RobotMethods.ArmMotorDriver()
        self.liftMethods = RobotMethods.LiftDriver()

        self.controllerClass = ControllerMethods.Controller('programming')
        self.controlScheme = self.controllerClass.getScheme()
        
        self.driverController = wpilib.XboxController(ports.controllerPorts.get("driverController"))
        self.coDriverController = wpilib.XboxController(ports.controllerPorts.get("codriverController"))

        self.driveMethods.driveTrainInit(self, self.controlScheme)
        self.armMethods.armMotorDriverInit(self, self.controlScheme)
        self.liftMethods.liftDriverInit(self, self.controlScheme)

        wpilib.CameraServer.launch()

        #self.sendData = SendData()
        #self.sendData.init()

    def autonomousPeriodic(self):
        self.teleopPeriodic()

    def teleopPeriodic(self):
        #self.sendData.sendPDPData()
        self.driveMethods.driveRobotWithJoystick()
        self.armMethods.driveArmMotorWithJoystick()
        self.liftMethods.driveLiftWithJoystick()


if __name__ == "__main__":
    wpilib.run(MyRobot)
