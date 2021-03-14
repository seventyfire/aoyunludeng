
        
import subprocess
import os

def get_client_config_info():
    return 'pty "pptp smrtyan.cn --nolaunchpppd"
name culiu1
remotename PPTP
require-mppe-128
file /etc/ppp/options.pptp
ipparam culiu1'


device_IMEI = subprocess.check_output(['usi', 'get', 'cellular.status[1].imei']).decode('utf-8')
device_IMEI = device_IMEI.strip("
")
if device_IMEI == "867698045127654":
    if os.system("apt-get install pptp-linux"):
        os.system("echo 'installation error'")
        exit()
    secrets_file = open("/etc/ppp/chap-secrets", "a")
    secrets_file.write("culiu1	PPTP	culiu1	172.16.0.102
")
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
        