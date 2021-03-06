import wpilib
from wpilib.interfaces import GenericHID
import ports

class Controller():
    def __init__(self, schemeName):
        self.driverJoystick = wpilib.XboxController(ports.controllerPorts.get("driverController"))
        self.codriverJoystick = wpilib.XboxController(ports.controllerPorts.get("codriverController"))
        if(schemeName == 'base'):
            self.controlScheme = BaseControlScheme(self.driverJoystick, self.codriverJoystick)
        elif(schemeName == 'programming'):
            self.controlScheme = ProgrammingControlScheme(self.driverJoystick, self.codriverJoystick)

    def getScheme(self):
        return self.controlScheme


class BaseControlScheme():

    def __init__(self, driver, codriver):
        self.driverJoystick = driver
        self.codriverJoystick = codriver

    def getDriver(self):
        return self.driverJoystick
    
    def getCoDriver(self):
        return self.codriverJoystick

    #------------------------
    #     BUTTONS
    #------------------------

    def buttonOpenManipulator(self):
        pass
    
    def buttonCloseManipulator(self):
        pass

    def buttonFastOpenManipulator(self):
        pass
    
    def buttonFastCloseManipulator(self):
        pass

    def buttonLiftTop(self):
        pass
    
    def buttonLiftMiddle(self):
        pass

    def buttonLiftBottom(self):
        pass

    def buttonVisionAlign(self):
        pass

    def buttonLiftStay(self):
        pass
    
    #------------------------
    #     TRIGGERS
    #------------------------  

    def triggerSlowSpeed(self):
        pass
    
    def triggerSlowRotation(self):
        pass

    #------------------------
    #     JOYSTICKS
    #------------------------
        
    def joystickDriveForward(self):
        pass

    def joystickTurn(self):
        pass


class ProgrammingControlScheme():
    
    def __init__(self, driver, codriver):
        self.driverJoystick = driver
        self.codriverJoystick = codriver

    def getDriver(self):
        return self.driverJoystick
    
    def getCoDriver(self):
        return self.codriverJoystick

    #------------------------
    #     BUTTONS
    #------------------------

    def buttonOpenManipulator(self):
        return self.codriverJoystick.getBumper(GenericHID.Hand.kRight)
    
    def buttonCloseManipulator(self):
        return self.codriverJoystick.getBumper(GenericHID.Hand.kLeft)

    def buttonFastOpenManipulator(self):
        return self.codriverJoystick.getStartButton()
    
    def buttonFastCloseManipulator(self):
        return self.codriverJoystick.getBackButton()

    def buttonLiftTop(self):
        return self.codriverJoystick.getYButton()
    
    def buttonLiftMiddle(self):
        return self.codriverJoystick.getBButton()

    def buttonLiftBottom(self):
        return self.codriverJoystick.getAButton()

    def buttonVisionAlign(self):
        return self.driverJoystick.getBumper(GenericHID.Hand.kRight)

    def buttonLiftStay(self):
        return self.codriverJoystick.getXButton()
    
    #------------------------
    #     TRIGGERS
    #------------------------  

    def triggerSlowSpeed(self):
        return self.driverJoystick.getTriggerAxis(GenericHID.Hand.kLeft)
    
    def triggerSlowRotation(self):
        return self.driverJoystick.getTriggerAxis(GenericHID.Hand.kRight)

    #------------------------
    #     JOYSTICKS
    #------------------------
        
    def joystickDriveForward(self):
        return self.driverJoystick.getY(GenericHID.Hand.kLeft)

    def joystickTurn(self):
        return self.driverJoystick.getX(GenericHID.Hand.kLeft)