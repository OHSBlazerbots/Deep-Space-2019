import wpilib

class DriverChooser(object):
    def  __init__ (self, dashboard):
        self.chooser1 = wpilib.SendableChooser()
        self.chooser2 = wpilib.SendableChooser()
        self.schemes = []
        self.counter = 0 
        self.dashboard = dashboard

    def addScheme(self, scheme):
        self.schemes.append(scheme)
        if self.counter == 0:
            self.chooser1.addDefault(scheme.name(), self.counter)
            self.chooser2.addDefault(scheme.name(), self.counter)
        else:
            self.chooser1.addObject(scheme.name(), self.counter)
            self.chooser2.addObject(scheme.name(), self.counter)
        self.counter += 1

    def getDriverOption(self):
        index = self.chooser1.getSelected()
        if index >= 0:
            return self.schemes[index]
        else:
            return None

    def getCodriverOption(self):
        index = self.chooser2.getSelected()
        if index >= 0:
            return self.schemes[index]
        else:
            return None

    def sendToDashboard(self):
        self.dashboard.putData('Driver 1 Control Schemes', self.chooser1)
        self.dashboard.putData('Driver 2 Control Schemes', self.chooser2)
        
        

    







