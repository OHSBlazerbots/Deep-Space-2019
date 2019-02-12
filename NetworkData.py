from networktables import NetworkTables
from wpilib import PowerDistributionPanel

class SendData():
    def init(self):
        self.dashboard = NetworkTables.getTable("SmartDashboard")
        self.pdp = PowerDistributionPanel(10)

    def sendDriveData(self, speed, rotation):
        self.dashboard.putNumber("RobotSpeed", speed)
        self.dashboard.putNumber("RobotRotation", rotation)
        
    def sendPDPData(self):
        self.dashboard.putNumber("PDPCurrent", self.pdp.getTotalCurrent())
        self.dashboard.putNumber("PDPTemperature", self.pdp.getTemperature())
        self.dashboard.putNumber("PDPVoltage", self.pdp.getVoltage())