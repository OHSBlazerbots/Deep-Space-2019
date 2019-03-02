import wpilib

class DriverChooser(object):
    def  __init__ (self):
        self.chooser1 = wpilib.SendableChooser()
        self.chooser2 = wpilib.SendableChooser()
        self.counter = 1 

    def addScheme(self, scheme()):
        chooser.addObject('option1', self.counter)
        self.counter += 1

    def getSelectedScheme(self) 





