import ports

import ctre
import wpilib
from wpilib.drive import DifferentialDrive
from wpilib.interfaces import GenericHID
from networktables import NetworkTables

class Driver():
    def driveTrainInit(self, robot):
        self.leftMotorGroup = wpilib.SpeedControllerGroup(ctre.WPI_TalonSRX(ports.talonPorts.get("leftChassisMotor")))
        self.rightMotorGroup = wpilib.SpeedControllerGroup(ctre.WPI_TalonSRX(ports.talonPorts.get("rightChassisMotor")))
        self.drive = DifferentialDrive(self.leftMotorGroup, self.rightMotorGroup)
        self.drive.setRightSideInverted(True)

    def driveRobotWithJoystick(self, joystick):
        speed = joystick.getX(GenericHID.Hand.kLeft)

        rotation = self.alignWithVisionTargets(joystick)

        self.drive.arcadeDrive(rotation, speed, squareInputs=True)
    
    def alignWithVisionTargets(self, joystick):
        rotation = joystick.getY(GenericHID.Hand.kLeft)
        
        visionTable = NetworkTables.getTable('PiData')
        
        if(joystick.getBumper(GenericHID.Hand.kRight)):
            visionAlignment = visionTable.getNumber('yawToTarget', 0)
            if(visionAlignment < 0):
                rotation = -0.5
            elif(visionAlignment > 0):
                rotation = 0.5
            else:
                rotation = rotation

        return rotation



class ArmMotorDriver():
    def armMotorDriverInit(self, robot):
        self.motor = ctre.WPI_TalonSRX(ports.talonPorts.get("testArmMotor"))

    def driveArmMotorWithJoystick(self, joystick):
        if(joystick.getAButton() and not self.motor.isFwdLimitSwitchClosed()):
            self.motor.set(1)
        elif(joystick.getBButton() and not self.motor.isRevLimitSwitchClosed()):
            self.motor.set(-1)
        else:
            self.motor.stopMotor()