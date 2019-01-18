import ports

import ctre
import wpilib
from wpilib.drive import DifferentialDrive
from wpilib.interfaces import GenericHID

class Driver():
    def driveTrainInit(self, robot):
        self.leftMotorGroup = wpilib.SpeedControllerGroup(ctre.WPI_TalonSRX(ports.talonPorts.get("leftChassisMotor")))
        self.rightMotorGroup = wpilib.SpeedControllerGroup(ctre.WPI_TalonSRX(ports.talonPorts.get("rightChassisMotor")))
        self.drive = DifferentialDrive(self.leftMotorGroup, self.rightMotorGroup)

    def driveRobotWithJoystick(self, joystick):
        speed = joystick.getY(GenericHID.Hand.kLeft)
        rotation = joystick.getX(GenericHID.Hand.kLeft)

        self.drive.arcadeDrive(speed, rotation, squareInputs=True)



class ArmMotorDriver():
    def armMotorDriverInit(self, robot):
        self.motor = ctre.WPI_TalonSRX(ports.talonPorts.get("testArmMotor"))

    def driveArmMotorWithJoystick(self, joystick):
        if(joystick.getAButton()):
            self.motor.set(50)
        else:
            self.motor.stopMotor()