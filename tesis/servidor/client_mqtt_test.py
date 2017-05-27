import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import random

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("esp8266status")

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    data_list.append(msg.payload)
    """
    list = json.loads(msg.payload)

    for key,value in list.iteritems():
        print ("")
        print key, value
    
    list = make_data_json(list)
    return list
    """
    return data_list

def on_subscribe(client, userdata,mid, granted_qos):
    print "userdata : " +str(userdata)

def on_publish(mosq, obj, mid):
    print("mid: " + str(mid))


def make_data_json(list):
  ip = list['ip']
  time = list['time']
  name = list['name']
  data = list['data']
  measure = {'ip': ip, 'time': time, 'name': name, 'data': data}
  output = {'name' : new_measure['name'], 'data' : new_measure['data']}
  data_json = jsonify({'result' : output})
  return data_json

def relay_off():
   print("Sending 1...")
   publish.single("ledStatus", "1", hostname="localhost")
   return "Relay Off!"

def relay_on():
    print("Sending 0...")
    publish.single("ledStatus", "0", hostname="localhost")
    return "Relay On!"

if __name__ == "__main__":
    print("Starting MQTT Client")
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("localhost", 1883, 60)
    client.loop_start()
    
    text = publish.single("ledStatus", "0", hostname="localhost")
    measure = {'ip': 1, 'time': 1, 'name': 1, 'data': 1}
    while True:
        publish.single("esp8266status", random.randint(0,100), hostname="localhost")
        
