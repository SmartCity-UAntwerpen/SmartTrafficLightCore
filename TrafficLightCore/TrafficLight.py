
import socket
import requests

class TrafficLight:

    def __init__(self, id, location, settings, mqttClient, startState="OFF", redTime=7, greenTime=5, transTime=5):
        # Init the state and behaviour of the light
        self.local_id = id
        self.location = location
        self.startState = startState
        self.state = startState
        self.prevState = self.state

        # Timings
        self.redTime = redTime
        self.greenTime = greenTime
        self.transitionTime = transTime

        # Create socket
        self.socket = 0

        self.timer = 0
        self.running = False

        self.mqttClient = mqttClient
        self.settings = settings
        # Initiate with the backend
        r = requests.get("http://{}:{}/tlight/initiate/{}/{}".format(settings.get("backend_ip"),settings.get("backend_port"),location,self.state))
        print("Trafficlight database id: {}".format(r.content))
        self.id = int(r.content)
        self.updateState()

    def step(self):
        """
        Progress the tf, timer increase and check the states, determines the next state
        State chart: RED -> TRANSITION -> GREEN -> TRANSITION -> RED -> ...
        """
        if not self.running:
            return

        if self.timer % self.redTime == 0 and self.state == "RED":
            self.prevState = self.state
            self.state = "TRANSITION"
            self.timer = 0
            self.updateState()
        elif self.timer % self.greenTime == 0 and self.state == "GREEN":
            self.prevState = self.state
            self.state = "TRANSITION"
            self.timer = 0
            self.updateState()
        elif self.timer % self.transitionTime == 0 and self.state == "TRANSITION":
            self.timer = 0
            if self.prevState == "RED":
                self.state = "GREEN"
            else:
                self.state = "RED"
            self.updateState()

        self.timer += 1

    def updateState(self):
        """
        Physically update the state and send MQTT state message
        :return:
        """
        if self.state == "RED":
            self.switchRed()
        elif self.state == "GREEN":
            self.switchGreen()
        else:
            self.switchRed()

        # Send update message to backend
        self.mqttClient.publish("LIGHT/{}".format(self.id), self.state)

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
        # Switch the light off
        self.send("LIGHT {} OFF".format(self.local_id))
        self.state = "OFF"
        return

    def send(self, message):
        """
        Send a message via tcp socket to tf driver
        :param message: the status messages to update the light
        """
        # Open socket for communication
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.settings.get("driver_host"), self.settings.get("driver_port")))
            self.socket.send(str.encode(message))
        except:
            print("Error trying to connect to traffic light driver")
        finally:
            self.socket.close()

    def getState(self):
        return self.state

    def setState(self, state):
        self.state = state

    def __del__(self):
        """
        Send delete request to robotBacked when tf is deleted
        :return:
        """
        r = requests.get(
            "http://{}:{}/tlight/delete/{}/".format(self.settings.get("backend_ip"), self.settings.get("backend_port"),
                                                    self.id))
