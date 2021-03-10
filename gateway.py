class Gateway:
    def __init__(self, IMEI, vpn_ip, vpn_port, server_ip, server_port):
        self.IMEI = IMEI
        self.vpn_ip = vpn_ip
        self.vpn_port = vpn_port
        self.server_ip = server_ip
        self.server_port = server_port


    def get_reverse_proxy_config_info(self):
        return "server{listen " + str(self.server_port) + ";server_name _;location / {proxy_pass http://" + self.vpn_ip + ":" + str(self.vpn_port) + ";}}"


    def add(self):
        import os
        # step1. IMEI link to a server port(write into a config file)
        config_file = open("IMEI_ServerPort.properties", "a")
        config_file.write(self.IMEI + "=" + str(self.server_port) + "\n")
        config_file.close()

        # step2. create a new reverse proxy config file
        # to map the server port to a specific available vpn ip(172.16.0.xxx) and port(default 5000)
        reverse_proxy_config_file = open("/etc/nginx/sites-enabled/" + self.IMEI + ".conf", "w")
        reverse_proxy_config_file.write(self.get_reverse_proxy_config_info())
        reverse_proxy_config_file.close()

        os.system("sudo nginx -s reload")
        os.system("echo 'reloaded nginx'")
        # step3. create a new bash script file and send it back to caller
        # script file: use to install vpn app on gateway that have the right IMEI
        # and to config some needed information.


if __name__ == "__main__":
    gateway = Gateway("0123456789", "172.16.0.102", 5002, "smrtyan.cn", 5002)
    gateway.add()
