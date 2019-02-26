from networktables import NetworkTables
from wpilib import PowerDistributionPanel
import ports

class SendData():
    def init(self):
        self.dashboard = NetworkTables.getTable("SmartDashboard")
        self.pdp = PowerDistributionPanel(ports.miscPorts.get("pdp"))

    def sendDriveData(self, speed, rotation):
        self.dashboard.putNumber("RobotSpeed", speed)
        self.dashboard.putNumber("RobotRotation", rotation)
        
    def sendPDPData(self):
        self.dashboard.putNumber("PDPCurrent", self.pdp.getTotalCurrent())
        self.dashboard.putNumber("PDPTemperature", self.pdp.getTemperature())
        self.dashboard.putNumber("PDPVoltage", self.pdp.getVoltage())

class SensorData():
    def init(self, table):
        self.dashboard = NetworkTables.getTable(table)

    def sendSensorData(self, tag, data):
        self.dashboard.putNumber(tag, data)