class Connector:
    def __init__(self):
        connector_info = open("connector_properties", "r")
        self.ip = connector_info.readline().strip().split("=")[1]
        self.port = connector_info.readline().strip().split("=")[1]
        connector_info.close()

    def set_ip(self, ip):
        self.ip = ip

    def get_ip(self):
        return self.ip

    def set_port(self, port):
        self.port = port

    def get_port(self):
        return self.port

    def update_info(self):
        connector_info = open("connector_properties", "r")
        self.ip = connector_info.readline().strip().split("=")[1]
        self.port = connector_info.readline().strip().split("=")[1]
        connector_info.close()



