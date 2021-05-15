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

class FlaskApp:
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret!'
    app.config['DEBUG'] = True

    #turn the flask app into a socketio app
    socketio = SocketIO(app, async_mode=None, logger=False, engineio_logger=False)

    def __init__(self, masterParam):
        self.master = masterParam

        self.thread = Thread()
        self.thread_stop_event = Event()
    

    def randomNumberGenerator(self):
        """
        Generate a random number every 1 second and emit to a socketio instance (broadcast)
        Ideally to be run in a separate thread?
        """
        #infinite loop of magical random numbers
        print("Sending information")

        while not self.thread_stop_event.isSet():
            
            data = commands.display_data(self.master)
            self.socketio.emit('alt', {'number': data["altitude"]}, namespace='/data')
            self.socketio.emit('aspd', {'number': data["airspeed"]}, namespace='/data')
            self.socketio.emit('gspd', {'number': data["groundspeed"]}, namespace='/data')
            self.socketio.emit('hdg', {'number': data["heading"]}, namespace='/data')
            self.socketio.emit('latlng', {'lat': data["latitude"], 'long': data["longitude"]}, namespace='/data')
            self.socketio.emit('vlt', {'number': data["voltage"]}, namespace='/data')
            self.socketio.emit('fltmd', {'number': data["flightMode"]}, namespace='/data')
            self.socketio.sleep(0.1)

    @app.route('/')
    def index(self):
        #only by sending this page first will the client be connected to the socketio instance
        return render_template('index.html')

    @socketio.on('connect', namespace='/data')
    def test_connect(self):
        # need visibility of the global thread object
        print('Client connected')

        #Start the random number generator thread only if the thread has not been started before.
        if not self.thread.is_alive():
            print("Starting Thread")
            thread = self.socketio.start_background_task(randomNumberGenerator)

    @socketio.on('disconnect', namespace='/data')
    def test_disconnect(self):
        print('Client disconnected')

    @socketio.on('waypoint', namespace='/dir')
    def waypointSubmit(self, jsontext, methods=['GET', 'POST']):
        data = json.loads(jsontext)
        print('RECEIVED WAYPOINT DATA: ' + str(data["lat"]) + ', ' + str(data["lng"]))
        commands.upload_mission(self.master, (data["lat"]), data["lng"], 5)

    def run(self):
        self.socketio.run(self.app)

if __name__ == "__main__":
    master = commands.connect("COM3")
    app = FlaskApp(master)  # creates instance of GUI class
    try:
        app.run()  # starts the application
    except KeyboardInterrupt:
        app.quitting()  # safely quits the application when crtl+C is pressed