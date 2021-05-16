# Start with a basic flask app webpage.
from flask_socketio import SocketIO, emit
from flask import Flask, render_template, url_for, copy_current_request_context
from random import random
from time import sleep
from threading import Thread, Event
import commands
import json
import logging

__author__ = 'affinity'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True

#turn the flask app into a socketio app
socketio = SocketIO(app, async_mode=None, logger=False, engineio_logger=False)
thread = Thread()
thread_stop_event = Event()

#changing variables (declared to be changed)
latTemp = 0
lngTemp = 0
updated = False

def randomNumberGenerator():
    """
    Generate a random number every 1 second and emit to a socketio instance (broadcast)
    Ideally to be run in a separate thread?
    """
    #infinite loop of magical random numbers
    print("Sending information")
    master = commands.connect("COM3")

    while not thread_stop_event.isSet():
        data = commands.display_data(master)

        if ('.' in data["altitude"]):
            i = 0
            decimals = ''
            altList = data["altitude"].split('.')
            altDecimals = list(altList[1])
            for x in altDecimals:
                decimals += altDecimals[i]
                i += 1
                if i >= 3: break
            altitude = altList[0] + '.' + decimals
        else:
            altitude = data["altitude"]
        
        if ('.' in data["groundspeed"]):
            i = 0
            decimals = ''
            altList = data["groundspeed"].split('.')
            altDecimals = list(altList[1])
            for x in altDecimals:
                decimals += altDecimals[i]
                i += 1
                if i >= 3: break
            groundspeed = altList[0] + '.' + decimals
        else:
            groundspeed = data["groundspeed"]
        
        if ('.' in data["latitude"]):
            i = 0
            decimals = ''
            altList = data["latitude"].split('.')
            altDecimals = list(altList[1])
            for x in altDecimals:
                decimals += altDecimals[i]
                i += 1
                if i >= 3: break
            latitude = altList[0] + '.' + decimals
        else:
            latitude = data["latitude"]

        if ('.' in data["longitude"]):
            i = 0
            decimals = ''
            altList = data["longitude"].split('.')
            altDecimals = list(altList[1])
            for x in altDecimals:
                decimals += altDecimals[i]
                i += 1
                if i >= 3: break
            longitude = altList[0] + '.' + decimals
        else:
            longitude = data["longitude"]

        socketio.emit('alt', {'number': altitude}, namespace='/data')
        socketio.emit('aspd', {'number': data["airspeed"]}, namespace='/data')
        socketio.emit('gspd', {'number': groundspeed}, namespace='/data')
        socketio.emit('hdg', {'number': data["heading"]}, namespace='/data')
        socketio.emit('latlng', {'lat': latitude, 'long': longitude}, namespace='/data')
        socketio.emit('vlt', {'number': data["voltage"]}, namespace='/data')
        socketio.emit('fltmd', {'number': data["flightMode"]}, namespace='/data')
        socketio.sleep(0.1)

        if updated is True:
            print('Updated.')
            print(latTemp)
            print(lngTemp)
        else:
            print('No new data.')

@app.route('/')
def index():
    #only by sending this page first will the client be connected to the socketio instance
    return render_template('index.html')

@socketio.on('connect', namespace='/data')
def test_connect():
    # need visibility of the global thread object
    print('Client connected')
    global thread
    #Start the random number generator thread only if the thread has not been started before.
    if not thread.is_alive():
        print("Starting Thread")
        thread = socketio.start_background_task(randomNumberGenerator)

@socketio.on('disconnect', namespace='/data')
def test_disconnect():
        print('Client disconnected')

@socketio.on('waypoint', namespace='/dir')
def waypointSubmit(jsontext, methods=['GET', 'POST']):
        data = json.loads(jsontext)
        print('RECEIVED WAYPOINT DATA: ' + str(data["lat"]) + ', ' + str(data["lng"]))
        global latTemp
        global lngTemp
        global updated
        latTemp = data["lat"]
        lngTemp = data["lng"]
        updated = True
        

if __name__ == "__main__":
    socketio.run(app)  # creates instance of GUI class
