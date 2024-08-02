import paho.mqtt.client as mqtt
import time
from datetime import datetime
import psutil

def on_connect(mqttc, obj, flags, reason_code, properties):
    print("reason_code: " + str(reason_code))


def on_message(mqttc, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))


def on_publish(mqttc, obj, mid, reason_code, properties):
    print("mid: " + str(mid))


def on_log(mqttc, obj, level, string):
    print(string)

MSG_TEMPLATE = {
    "status": "",
    "datetime": "",
    "cpu_usage": "",
    "ram_usage": "",
    "nas_usage": ""
}

WARNING_CPU=95
WARNING_RAM=70
WARNING_NAS=80

def calc_status(cpu, ram, nas):
    error_list = []
    if cpu > WARNING_CPU:
        error_list.append(f"High CPU usage: {cpu}%")
    if ram > WARNING_RAM:
        error_list.append(f"High RAM usage: {ram}%")
    if nas > 80:
        error_list.append(f"NAS is running out of space. Usage: {nas}%")

    if len(error_list)==0:
        return "OK"
    else:
        return error_list.join(';')

def get_status_msg():
    status_msg = MSG_TEMPLATE
    status_msg["datetime"] = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    status_msg["cpu_usage"] = psutil.cpu_percent()
    status_msg["ram_usage"] = psutil.virtual_memory().percent
    status_msg["nas_usage"] = psutil.disk_usage('/mnt/nas').percent
    status_msg["status"] = calc_status(status_msg["cpu_usage"], status_msg["ram_usage"], status_msg["nas_usage"])

    return status_msg

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="sideClient")
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
# Uncomment to enable debug messages
# mqttc.on_log = on_log

mqttc.connect("localhost", 1883, 60)

mqttc.loop_start()


while True:
    new_message = get_status_msg()
    infot = mqttc.publish("raspberry/monitoring", str(new_message), qos=2)
    infot.wait_for_publish()
    time.sleep(5)
