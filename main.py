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


mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="sideClient")
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
# Uncomment to enable debug messages
# mqttc.on_log = on_log
mqttc.connect("localhost", 1883, 60)

mqttc.loop_start()

msg_template = {
    "status": "",
    "datetime": "",
    "cpu_usage": "",
    "ram_usage": "",
    "nas_usage": ""
}

while True:
    new_message = msg_template
    new_message["datetime"] = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    new_message["cpu_usage"] = psutil.cpu_percent()
    new_message["ram_usage"] = psutil.virtual_memory().percent
    new_message["nas_usage"] = psutil.disk_usage('/mnt/nas').percent
    infot = mqttc.publish("raspberry/monitoring", str(new_message), qos=2)
    infot.wait_for_publish()
    time.sleep(5)
