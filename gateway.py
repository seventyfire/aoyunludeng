class Gateway:
    def __init__(self, IMEI, vpn_ip, vpn_port, server_ip, server_port, culiu):
        self.IMEI = IMEI
        self.vpn_ip = vpn_ip
        self.vpn_port = vpn_port
        self.server_ip = server_ip
        self.server_port = server_port
        self.culiu = culiu

    def get_reverse_proxy_config_info(self):
        return "server{listen " + str(
            self.server_port) + ";server_name _;location / {proxy_pass http://" + self.vpn_ip + ":" + str(
            self.vpn_port) + ";}}"

    def get_script_template(self):
        return '''
        
import subprocess
import os

def get_client_config_info():
    return 'pty "pptp smrtyan.cn --nolaunchpppd"\nname ''' + self.culiu + '''\nremotename PPTP\nrequire-mppe-128\nfile /etc/ppp/options.pptp\nipparam ''' + self.culiu + ''''


device_IMEI = subprocess.check_output(['usi', 'get', 'cellular.status[1].imei']).decode('utf-8')
device_IMEI = device_IMEI.strip("\n")
if device_IMEI == "''' + self.IMEI + '''":
    if os.system("apt-get install pptp-linux"):
        os.system("echo 'installation error'")
        exit()
    secrets_file = open("/etc/ppp/chap-secrets", "a")
    secrets_file.write("''' + self.culiu + '''	PPTP	''' + self.culiu + '''	''' + self.vpn_ip + '''\n")
    secrets_file.close()
    client_config_file = open("/etc/ppp/peers/culiu", "w")
    client_config_file.write(get_client_config_info())
    client_config_file.close()
    os.system("poff culiu")
    if os.system("pon culiu"):
        os.system("echo 'pptp service start error'")
        exit()
    os.system("echo 'pptp service started'")
else:
    os.system("echo 'device imei number is not matched'")
        '''

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

        chap_secrets_file = open("/etc/ppp/chap-secrets", "a")
        chap_secrets_file.write(self.culiu + "   " + "pptpd  " + self.culiu + "   " + self.vpn_ip + "\n")
        chap_secrets_file.close()

        if os.system("nginx -s reload"):
            return "error"
        if os.system("echo 'reloaded nginx'"):
            return "error"
        # step3. create a new bash script file and send it back to caller
        # script file: use to install vpn app on gateway that have the right IMEI
        # and to config some needed information.
        script_file = open("./script/client_config.py", "w")
        script_file.write(self.get_script_template())
        script_file.close()





# apt-get install pptp-linux  -> installation

# # /etc/ppp/peers/culiu   -> config file
# pty "pptp smrtyan.cn --nolaunchpppd"
# name culiu
# remotename PPTP
# require-mppe-128
# file /etc/ppp/options.pptp
# ipparam culiu

# pon culiu -> command



if __name__ == "__main__":
    gateway = Gateway("867698045127654", "172.16.0.102", 5002, "smrtyan.cn", 5002, "culiu1")

    gateway.add()
