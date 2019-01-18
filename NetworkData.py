from networktables import NetworkTables

class SendData():
    def init(self):
        self.dashboard = NetworkTables.getTable("SmartDashboard")        

    def sendDriveData(self, speed, rotation):
        self.dashboard.putNumber("RobotSpeed", speed)
        self.dashboard.putNumber("RobotRotation", rotation)