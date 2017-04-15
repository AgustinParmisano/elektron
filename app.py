# -*- coding: utf-8 -*-

import os
import requests
import operator
import re
import json, ast
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import time
from datetime import datetime
from rq import Queue
from rq.job import Job
from worker import conn
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from highcharts import Highchart
from bson import ObjectId

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])

client = MongoClient('localhost', 27017)
db = client['test_db']

q = Queue(connection=conn)

data_list = {}
data = "Nada"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("esp8266status")

def on_message(client, userdata, msg):
    #print(msg.topic+" "+str(msg.payload))
    data = json.loads(str(msg.payload))
    data["time"] = str(datetime.now().isoformat())
    print(data)
    result = db.measures.insert_one(data)

def on_subscribe(client, userdata,mid, granted_qos):
    print "userdata : " +str(userdata)

def on_publish(mosq, obj, mid):
    print("mid: " + str(mid))

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/pwd', methods=['GET', 'POST'])
def pwd():
    dato = os.popen('pwd').read()
    print dato
    return dato

@app.route("/data")
def get_all_measures(chartID = 'chart_ID', chart_type = 'spline', chart_height = 350):
    chart = {"renderTo": chartID, "type": chart_type, "height": chart_height,}
    title = {"text": 'My Title'}
    xAxis = {"categories": ['xAxis Data1', 'xAxis Data2', 'xAxis Data3']}
    yAxis = {"title": {"text": 'yAxis Label'}}

    print("Sending 2...")
    publish.single("ledStatus", "2", hostname="localhost")
    measure_list = []

    data_last_10 = db.measures.find().limit(10).sort("time",-1)
    for d in data_last_10:
        measure_list.append(ast.literal_eval(json.dumps(str(d.get("data")))))

    single_data = list(db.measures.find().limit(1).sort("time",-1))

    series = [{"name": 'Label1', "data": [map(float, measure_list)]}]

    return render_template('index.html', data=measure_list, chartID=chartID, chart=chart, series=series, title=title, xAxis=xAxis, yAxis=yAxis)

@app.route("/off")
def relay_off():
   print("Sending 1...")
   publish.single("ledStatus", "1", hostname="localhost")
   return "Relay Off!"

@app.route("/on")
def relay_on():
    print("Sending 0...")
    publish.single("ledStatus", "0", hostname="localhost")
    return "Relay On!"

@app.route('/ajax_data', methods=['GET', 'POST'])
def ajax_data():
    single_data = list(db.measures.find().limit(1).sort("time",-1))

    yAxis = ast.literal_eval(json.dumps(float(single_data[0].get("data"))))

    return jsonify({'measure':yAxis})

if __name__ == '__main__':
    app.run()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("localhost", 1883, 60)
client.loop_start()
