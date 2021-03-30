from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin
from gateway import Gateway
from flask import send_file

app = Flask(__name__)
CORS(app)


@app.route('/add_gateway', methods=['GET', 'POST'])
def add_gateway_by_IMEI():
    IMEI = request.args.get('IMEI')
    latest_info_file = open("./latest_info", "r")
    # 101,5001,1
    info = latest_info_file.readline().strip().split(",")
    latest_info_file.close()
    ip = str(int(info[0]) + 1)
    vpn_ip = "172.16.0." + ip
    vpn_port = str(int(info[1]) + 1)
    server_ip = "smrtyan.cn"
    server_port = vpn_port
    num = str(int(info[2]) + 1)
    culiu = "culiu" + num

    gateway = Gateway(IMEI, vpn_ip, vpn_port, server_ip, server_port, culiu)
    # "867698045127654", "172.16.0.102", 5002, "smrtyan.cn", 5002, "culiu2"
    gateway.add()

    latest_info_file = open("./latest_info", "w")
    latest_info_file.write(ip + "," + vpn_port + "," + num)
    latest_info_file.close()
    # return the ./script/client_config.py file
    try:
        return send_file('./script/client_config.py', attachment_filename='client_config.py')
    except Exception as e:
        return str(e)


if __name__ == "__main__":
    app.run(host='0.0.0.0')