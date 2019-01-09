from threading import Timer


class Crossing:

    def __init__(self, trafficLights):
        self.trafficLights = trafficLights
        self.globalTimer = None

    def start(self):
        for tlight in self.trafficLights:
            self.trafficLights[tlight].start()
        self.globalTimer = Timer(1, self.step)
        self.globalTimer.start()

    def reset(self):
        for tlight in self.trafficLights:
            self.trafficLights[tlight].reset()

    def stop(self, _id):
        self.trafficLights.get(int(_id)).stop()

    def kill(self):
        for tlight in self.trafficLights:
            self.trafficLights[tlight].stop()

    def get(self, _id):
        return self.trafficLights.get(int(_id)).getState()

    def status(self):
        res = ""
        for tlight in self.trafficLights:
            res += "Traffic light {} status: {}\n".format(self.trafficLights[tlight].id,self.trafficLights[tlight].getState())
        return res

    def step(self):
        for tlight in self.trafficLights:
            self.trafficLights[tlight].step()
        # Restart the timer
        self.globalTimer = Timer(1, self.step)
        self.globalTimer.start()

    def manualState(self, tfid, state):
        self.trafficLights.get(int(tfid)).setState(state)
        self.trafficLights.get(int(tfid)).updateState()

    def deleteAll(self):
        for tlight in self.trafficLights:
            del tlight
        del self.trafficLights
