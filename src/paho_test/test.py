import paho.mqtt.client as mqtt
import datetime
import json


# connect and subscribe to esys/Thom&Doug/test
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    client.subscribe("esys/Thom&Doug/test")

# When message received dump as JSON into our 'database'
def on_message(client, userdata, msg):
    with open('../../website/web/db/mqtt.json', 'r') as infile:
        saved_data = json.load(infile)
    # get date and time
    t = datetime.datetime.now().strftime("%y-%m-%d-%H-%M")
    # add time to the payload
    payload = json.loads(msg.payload)
    payload["time"] = t
    # get device id and remove from payload
    dev_id = payload["id"]
    del payload["id"]
    # check if already received data from device
    if str(dev_id) in saved_data:
        print("found")
        data_list = saved_data[str(dev_id)]
        data_list.append(payload)
        saved_data[str(dev_id)] = data_list
    else:
        print("nop")
        saved_data[str(dev_id)] = [payload]

    print(saved_data)
    with open('../../website/web/db/mqtt.json', 'w') as outfile:
        json.dump(saved_data, outfile)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# connect on the right IP and port
client.connect("192.168.0.10", 1883, 60)

client.loop_forever()