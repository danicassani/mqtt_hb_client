import paho.mqtt.client as mqtt
import time

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

while True:
    infot = mqttc.publish("heartbeat", "boom-boom", qos=2)
    infot.wait_for_publish()
    time.sleep(5)
