from threading import Timer


class Crossing:

    def __init__(self, trafficLights):
        self.trafficLights = trafficLights
        self.globalTimer = None

    def start(self):
        """
        Starts the timer and activates the traffic lights
        """
        for tlight in self.trafficLights:
            self.trafficLights[tlight].start()
        self.globalTimer = Timer(1, self.step)
        self.globalTimer.start()

    def reset(self):
        """
        Reset all trafficlights to their start state
        :return:
        """
        for tlight in self.trafficLights:
            self.trafficLights[tlight].reset()

    def stop(self, _id):
        """
        Stop a specific traffic light
        :param _id: (int) local id
        """
        self.trafficLights.get(int(_id)).stop()

    def kill(self):
        """
        Stops all traffic lights
        """
        for tlight in self.trafficLights:
            self.trafficLights[tlight].stop()

    def get(self, _id):
        return self.trafficLights.get(int(_id)).getState()

    def status(self):
        """
        Get the status of a all traffic light
        :return: string with all trafficlight statuses
        """
        res = ""
        for tlight in self.trafficLights:
            res += "Traffic light {} status: {}\n".format(self.trafficLights[tlight].id,self.trafficLights[tlight].getState())
        return res

    def step(self):
        """
        Time step, let the trafficlight progress step by step
        This fucntion is periodically called every second
        """
        for tlight in self.trafficLights:
            self.trafficLights[tlight].step()
        # Restart the timer
        self.globalTimer = Timer(1, self.step)
        self.globalTimer.start()

    def manualState(self, tfid, state):
        """
        Manually overide a tf state
        :param tfid: local tf id
        :param state: desired state
        """
        self.trafficLights.get(int(tfid)).setState(state)
        self.trafficLights.get(int(tfid)).updateState()

    def deleteAll(self):
        """
        Remove all traffic lights
        """
        for tlight in self.trafficLights:
            del tlight
        del self.trafficLights
