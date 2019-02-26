import ports
from NetworkData import SensorData

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
        speed = joystick.getY(GenericHID.Hand.kLeft)*(1-(0.75*joystick.getTriggerAxis(GenericHID.Hand.kRight)))

        rotation = self.alignWithVisionTargets(joystick)*(1-(0.75*joystick.getTriggerAxis(GenericHID.Hand.kLeft)))

        self.drive.arcadeDrive(-speed, rotation, squareInputs=True)
    
    def alignWithVisionTargets(self, joystick):
        rotation = joystick.getX(GenericHID.Hand.kLeft)
        
        visionTable = NetworkTables.getTable('PiData')
        
        if(joystick.getBumper(GenericHID.Hand.kRight)):
            visionAlignment = visionTable.getNumber('yawToTarget', 0)
            if(visionAlignment < 0):
                rotation = -0.4
            elif(visionAlignment > 0):
                rotation = 0.4
            else:
                rotation = rotation

        return rotation



class ArmMotorDriver():
    def armMotorDriverInit(self, robot):
        self.motor = ctre.WPI_TalonSRX(ports.talonPorts.get("testArmMotor"))
        self.sensorCollection = ctre.sensorcollection.SensorCollection(self.motor)
        self.motorRunning = False
        self.NTSensor = SensorData()
        self.NTSensor.init("Manipulator")
        self.position = 0

    def driveArmMotorWithJoystick(self, joystick):
        self.NTSensor.sendSensorData("QuadPosition", self.sensorCollection.getQuadraturePosition())
        self.NTSensor.sendSensorData("QuadVelocity", self.sensorCollection.getQuadratureVelocity())

        self.position = self.sensorCollection.getQuadraturePosition()

        if(joystick.getAButton()): # Open the arms
            if(self.position <= -3000):
                self.motor.stopMotor()
            elif(self.position <= -150):
                self.motor.stopMotor()
            else:
                self.motor.set(0.2)
        elif(joystick.getBButton()): # Close the arms
            if(self.position >= 135):
                self.motor.stopMotor()
            else:
                self.motor.set(-0.2)
        elif(joystick.getXButton()):
            self.motor.set(0.4)
        elif(joystick.getYButton()):
            self.motor.set(-0.4)
        else:
            self.motor.stopMotor()

class LiftDriver():
    def liftDriverInit(self, robot):
        self.liftMotor = ctre.WPI_TalonSRX(ports.talonPorts.get("liftMotor"))
    def driveLiftWithJoystick(self, joystick):
        liftMotorSpeed = joystick.getX(GenericHID.Hand.kRight)
        self.liftMotor.set(liftMotorSpeed)