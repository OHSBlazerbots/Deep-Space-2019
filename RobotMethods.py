import ports
from NetworkData import SensorData

import ctre
import wpilib
from wpilib.drive import DifferentialDrive
from wpilib.interfaces import GenericHID
from networktables import NetworkTables
import ControllerMethods

class Driver():
    def driveTrainInit(self, robot, controlScheme):
        self.controlScheme = controlScheme

        self.leftMotorGroup = wpilib.SpeedControllerGroup(ctre.WPI_TalonSRX(ports.talonPorts.get("leftChassisMotor")))
        self.rightMotorGroup = wpilib.SpeedControllerGroup(ctre.WPI_TalonSRX(ports.talonPorts.get("rightChassisMotor")))
        self.drive = DifferentialDrive(self.leftMotorGroup, self.rightMotorGroup)
        self.drive.setRightSideInverted(True)

    def driveRobotWithJoystick(self):
        speed = self.controlScheme.joystickDriveForward() * (1-(0.95*self.controlScheme.triggerSlowSpeed()))
       #speed = joystick.getY(GenericHID.Hand.kLeft)*(1-(0.75*joystick.getTriggerAxis(GenericHID.Hand.kRight)))

        rotation = self.alignWithVisionTargets(self.controlScheme.joystickTurn(), self.controlScheme.buttonVisionAlign())*(1-(0.95*self.controlScheme.triggerSlowRotation()))
        #rotation = self.alignWithVisionTargets(joystick)*(1-(0.75*joystick.getTriggerAxis(GenericHID.Hand.kLeft)))

        self.drive.arcadeDrive(-speed, rotation, squareInputs=True)
    
    def alignWithVisionTargets(self, rotation, buttonVisionAlign):
        visionTable = NetworkTables.getTable('PiData')
        
        if(buttonVisionAlign):
            visionAlignment = visionTable.getNumber('yawToTarget', 0)
            if(visionAlignment < 0):
                rotation = -0.4
            elif(visionAlignment > 0):
                rotation = 0.4
            else:
                rotation = rotation

        return rotation



class ArmMotorDriver():
    def armMotorDriverInit(self, robot, controlScheme):
        self.controlScheme = controlScheme

        self.motor = ctre.WPI_TalonSRX(ports.talonPorts.get("testArmMotor"))
        self.sensorCollection = ctre.sensorcollection.SensorCollection(self.motor)
        self.motorRunning = False
        self.NTSensor = SensorData("Manipulator")
        self.position = 0

    def driveArmMotorWithJoystick(self):
        self.NTSensor.sendSensorData("QuadPosition", self.sensorCollection.getQuadraturePosition())
        self.NTSensor.sendSensorData("QuadVelocity", self.sensorCollection.getQuadratureVelocity())

        self.position = self.sensorCollection.getQuadraturePosition()

        if(self.controlScheme.buttonOpenManipulator()): # Open the arms
            if(self.position <= -3000):
                self.motor.stopMotor()
            elif(self.position <= -150):
                self.motor.stopMotor()
            else:
                self.motor.set(0.2)
        elif(self.controlScheme.buttonCloseManipulator()): # Close the arms
            if(self.position >= 135):
                self.motor.stopMotor()
            else:
                self.motor.set(-0.4)
        elif(self.controlScheme.buttonFastOpenManipulator()): # Quickly (and unsafely) open the arms
            self.motor.set(0.4)
        else:
            self.motor.stopMotor()

class LiftDriver():
    def liftDriverInit(self, robot, controlScheme):
        # Setup control stuff
        self.controlScheme = controlScheme
        
        # Network Tables for Data Comms
        self.sData = SensorData("liftTable")

        # Set the motor to use
        self.liftMotor = ctre.WPI_TalonSRX(ports.talonPorts.get("liftMotor"))
        
        # Configure the Lift Motor
        self.liftMotorSpeed = 0.75

        # Configure Down Motor Speed
        self.liftMotorSpeedDown = -.25

        # Create the Hall Effect Sensor objects
        self.bottomHallEffect = wpilib.AnalogInput(ports.miscPorts.get("LiftHallEffectBottom"))
        self.middleHallEffect = wpilib.AnalogInput(ports.miscPorts.get("LiftHallEffectMiddle"))
        self.topHallEffect = wpilib.AnalogInput(ports.miscPorts.get("LiftHallEffectTop"))

        # Test AnalogTrigger
        #self.testTrigger = wpilib.AnalogTrigger(ports.miscPorts.get("LiftHallEffectBottom"))
        #self.testTrigger.setLimitsVoltage(0.0, 1.0)

        # Configure Hall Effect code
        self.sensorThreshold = 2.5

        self.aboveMid = False
        self.notMoving = False
        self.movingDown = False
        self.movingUp = False
        self.hSensor = SensorData("LIFT")

    def boolFromVal(self, value):
        if(value < 500):
            return True
        else:
            return False

    def driveLiftWithJoystick(self):
        self.hSensor.sendSensorData("Value", self.bottomHallEffect.getValue())
        self.hSensor.sendSensorData("Voltage", self.bottomHallEffect.getVoltage())
        #self.hSensor.sendSensorData("AnalogTriggered", self.testTrigger.getTriggerState())
        #self.hSensor.sendSensorData("AnalogInWindow", self.testTrigger.getInWindow())
        # Trigger Bounds: 0v - 0.1v

        self.hSensor.sendSensorData("bottom", self.boolFromVal(self.bottomHallEffect.getValue()))
        self.hSensor.sendSensorData("middle", self.boolFromVal(self.middleHallEffect.getValue()))
        self.hSensor.sendSensorData("top", self.boolFromVal(self.topHallEffect.getValue()))

        self.notMoving = self.boolFromVal(self.bottomHallEffect.getValue()) or self.boolFromVal(self.middleHallEffect.getValue()) or self.boolFromVal(self.topHallEffect.getValue())

        if(self.controlScheme.buttonLiftStay()):
            self.notMoving = True
            self.movingDown = False
            self.movingUp = False
    
        if(self.controlScheme.buttonLiftTop()):
                self.movingUp = not self.boolFromVal(self.topHallEffect.getValue())
                self.notMoving = False
                self.movingDown = False

        if(self.controlScheme.buttonLiftBottom()):
                self.movingUp = False
                self.movingDown = not self.boolFromVal(self.bottomHallEffect.getValue())
                self.notMoving = False


        if(self.notMoving):
            self.liftMotor.set(.125)
        elif(self.movingUp):
            self.liftMotor.set(self.liftMotorSpeed)
        elif(self.movingDown):
            self.liftMotor.set(self.liftMotorSpeedDown)
        else:
            self.liftMotor.stopMotor()

        
        