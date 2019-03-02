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

    def buttonLiftUp(self):
        pass
    
    def buttonLiftDown(self):
        pass

    def buttonLiftStop(self):
        pass

    def buttonVisionAlign(self):
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


class ProgrammingControlScheme(BaseControlScheme):
    
    def __init__(self, driver, codriver):
        self.driverJoystick = driver
        self.codriverJoystick = codriver
        super.__init__(driver, codriver)

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

    def buttonLiftUp(self):
        return self.codriverJoystick.getYButton()
    
    def buttonLiftDown(self):
        return self.codriverJoystick.getAButton()

    def buttonLiftStop(self):
        return self.codriverJoystick.getBButton()

    def buttonVisionAlign(self):
        return self.driverJoystick.getBumper(GenericHID.Hand.kRight)
    
    #------------------------
    #     TRIGGERS
    #------------------------  

    def triggerSlowSpeed(self):
        return self.driverJoystick.getTrigger(GenericHID.Hand.kLeft)
    
    def triggerSlowRotation(self):
        return self.driverJoystick.getTrigger(GenericHID.Hand.kRight)

    #------------------------
    #     JOYSTICKS
    #------------------------
        
    def joystickDriveForward(self):
        return self.driverJoystick.getYAxis(GenericHID.Hand.kLeft)

    def joystickTurn(self):
        return self.driverJoystick.getXAxis(GenericHID.Hand.kLeft)