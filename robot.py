#!/usr/bin/env python3
'''
    This sample program shows how to control a motor using a joystick. In the
    operator control part of the program, the joystick is read and the value
    is written to the motor.

    Joystick analog values range from -1 to 1 and speed controller inputs also
    range from -1 to 1 making it easy to work together. The program also delays
    a short time in the loop to allow other threads to run. This is generally
    a good idea, especially since the joystick values are only transmitted
    from the Driver Station once every 20ms.
'''

import wpilib
import ctre
from wpilib.drive import DifferentialDrive
from wpilib.interfaces import GenericHID

class MyRobot(wpilib.TimedRobot):
    
    def robotInit(self):
        '''Robot initialization function'''
        print("ROBORINIT")
        self.leftMotor = ctre.WPI_TalonSRX(8)        # initialize the motor as a Talon on channel 0
        self.rightMotor = ctre.WPI_TalonSRX(4)
        self.extraMotor = ctre.WPI_TalonSRX(2)
        self.stick = wpilib.XboxController(0)     # initialize the joystick on port 0
        self.right = wpilib.SpeedControllerGroup(self.rightMotor)
        self.left = wpilib.SpeedControllerGroup(self.leftMotor)
        wpilib.CameraServer.launch()

        self.drive = DifferentialDrive(self.left, self.right)

    def teleopPeriodic(self):
        #self.drive.arcadeDrive(self.stick, True)
        print(self.stick.getX(GenericHID.Hand.kLeft))
        self.drive.arcadeDrive(self.stick.getY(GenericHID.Hand.kLeft), self.stick.getX(GenericHID.Hand.kLeft), squareInputs=True)
        print(self.stick.getX(GenericHID.Hand.kLeft))
        if self.stick.getAButton():
            self.extraMotor.set(50)
        else:
            self.extraMotor.stopMotor()

if __name__ == "__main__":
    wpilib.run(MyRobot)
