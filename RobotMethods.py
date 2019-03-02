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
        speed = self.controlScheme.joystickDriveForward() * (1-(0.75*self.controlScheme.triggerSlowSpeed()))
        #speed = joystick.getY(GenericHID.Hand.kLeft)*(1-(0.75*joystick.getTriggerAxis(GenericHID.Hand.kRight)))

        rotation = self.alignWithVisionTargets(self.controlScheme.joystickTurn(), self.controlScheme.buttonVisionAlign())*(1-(0.75*self.controlScheme.triggerSlowRotation()))
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
                self.motor.set(-0.2)
        elif(self.controlScheme.buttonFastOpenManipulator()): # Quickly (and unsafely) open the arms
            self.motor.set(0.4)
        elif(self.controlScheme.buttonFastOpenManipulator()): # Quickly (and unsafely) close the arms
            self.motor.set(-0.4)
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
        self.liftMotorSpeed = 0.2

        # Create the Hall Effect Sensor objects
        self.bottomHallEffect = wpilib.AnalogInput(ports.miscPorts.get("LiftHallEffectBottom"))
        self.middleHallEffect = wpilib.AnalogInput(ports.miscPorts.get("LiftHallEffectMiddle"))
        self.topHallEffect = wpilib.AnalogInput(ports.miscPorts.get("LiftHallEffectTop"))

        # Configure Hall Effect code
        self.sensorThreshold = 1.5

        # Movement Code
        self.movingUp = False
        self.movingDown = False
        self.position = 0
        self.nextPosition = 0

    def driveLiftWithJoystick(self, joystick):
        self.bHEVal = self.hallEffectToBool(self.bottomHallEffect)
        self.mHEVal = self.hallEffectToBool(self.middleHallEffect)
        self.tHEVal = self.hallEffectToBool(self.topHallEffect)

        # Flow: Get Up button, check where we are at, if not at top, move up one level.
        # Flow: Get Down Button, check where we are at, if not at bottom, move down one level.
        # Flow: Get Stop Button, Immediately Stop Motor
        if(self.controlScheme.buttonStopLift()):
            self.liftMotor.stopMotor()
            self.movingDown = False
            self.movingUp = False
            
        self.position = self.getPosition()
        if(self.movingUp):
            if(self.position == self.nextPosition):
                self.movingUp = False
                self.liftMotor.stopMotor()
        elif(self.movingDown):
            if(self.position == self.nextPosition):
                self.movingDown = False
                self.liftMotor.stopMotor()

        if(self.controlScheme.buttonLiftUp()):
            if(self.canMoveUp()):
                self.nextPosition = self.position + 1
                self.movingUp = True
                self.movingDown = False
            else:
                self.nextPosition = self.position
                self.movingUp = False
                self.movingDown = False
        
        if(self.controlScheme.buttonLiftDown()):
            if(self.canMoveDown()):
                self.nextPosition = self.position - 1
                self.movingUp = False
                self.movingDown = True
            else:
                self.nextPosition = self.position
                self.movingUp = False
                self.movingDown = False

        if(self.movingUp):
            self.liftMotor.set(self.liftMotorSpeed)
        elif(self.movingDown):
            self.liftMotor.set(-self.liftMotorSpeed)
        else:
            self.liftMotor.stopMotor()


        # Publish Hall Effect Data to Network Tables
        self.sData.sendSensorData("hallEffectBottom", self.bHEVal)
        self.sData.sendSensorData("hallEffectMiddle", self.mHEVal)
        self.sData.sendSensorData("hallEffectTop", self.tHEVal)

    def hallEffectToBool(self, sensor):
        value = sensor.getValue()
        if(value > self.sensorThreshold):
            return False
        else:
            return True
    
    def getPosition(self):
        if(self.bHEVal):
            return 0
        elif(self.mHEVal):
            return 1
        elif(self.tHEVal):
            return 2
        else:
            return 1 # We return 1 here because if we pressed the stop button, we should be between levels, and a value of one lets us move up AND down

    def canMoveUp(self):
        if(self.getPosition() == 2):
            return False
        else:
            return True
    
    def canMoveDown(self):
        if(self.getPosition() == 0):
            return False
        else:
            return True
        