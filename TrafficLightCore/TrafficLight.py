
import socket
import requests

import paho.mqtt.publish as publish

class TrafficLight:

    def __init__(self, id, location, driverHostname, port, settings, mqttClient, startState="OFF", redTime=7, greenTime=5, transTime=2):
        # Init the state and behaviour of the light
        self.local_id = id
        self.location = location
        self.startState = startState
        self.state = startState
        self.prevState = self.state

        self.redTime = redTime
        self.greenTime = greenTime
        self.transitionTime = transTime

        # Connection details
        self.hostname = driverHostname
        self.port = port

        # Create socket
        self.socket = 0

        self.timer = 0
        self.running = False

        self.mqttClient = mqttClient
        self.settings = settings
        # Initiate with the backend
        r = requests.get("http://{}:{}/tlight/initiate/{}/{}".format(settings.get("backend_ip"),settings.get("backend_port"),location,self.state))
        print(r.content)
        self.id = int(r.content)
        self.updateState()

    def step(self):
        if not self.running:
            return

        if self.timer % self.redTime == 0 and self.state == "RED":
            self.prevState = self.state
            self.state = "TRANSITION"
        elif self.timer % self.greenTime == 0 and self.state == "GREEN":
            self.prevState = self.state
            self.state = "TRANSITION"
        elif self.timer % self.transitionTime == 0 and self.state == "TRANSITION":
            if self.prevState == "RED":
                self.state = "GREEN"
            else:
                self.state = "RED"

        self.updateState()
        self.timer += 1

    def updateState(self):
        if self.state == "RED":
            self.switchRed()
        elif self.state == "GREEN":
            self.switchGreen()
        else:
            self.switchRed()
        #Send update message to backend
        self.mqttClient.publish("LIGHT/{}".format(self.id), self.state)

    def getState(self):
        return self.state

    def setState(self, state):
        self.state = state

    def start(self):
        self.running = True

    def stop(self):
        self.running = False
        self.timer = 0

    def reset(self):
        self.timer = 0
        self.state = self.startState
        self.updateState()

    def switchGreen(self):
        # Switch the light to green
        self.send("LIGHT {} GREEN".format(self.local_id))
        return

    def switchRed(self):
        # Switch the light to red
        self.send("LIGHT {} RED".format(self.local_id))

        return

    def switchOff(self):
        self.send("LIGHT {} OFF".format(self.local_id))
        self.state = "OFF"
        return

    def send(self, message):
        # Open socket for communication
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.hostname, self.port))
            self.socket.send(str.encode(message))
        except:
            print("Error trying to connect to traffic light driver")
        finally:
            self.socket.close()

    def __del__(self):
        r = requests.get(
            "http://{}:{}/tlight/delete/{}/".format(self.settings.get("backend_ip"), self.settings.get("backend_port"),
                                                    self.id))
