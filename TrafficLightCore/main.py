
from threading import Thread
from TrafficLightCore import RestAPI as REST
from TrafficLightCore.Terminal import Terminal
from TrafficLightCore.Crossing import Crossing
from TrafficLightCore.TrafficLight import TrafficLight
from TrafficLightCore.mqttClient import MqttClient

models = None

settings = {
    # MQTT settings
    'mqtt_ip': "smartcity.ddns.net",
    'mqtt_port': 1883,
    'mqtt_username': "root",
    'mqtt_password': "smartcity",

    # Robot backend settings
    'backend_ip' : "172.16.0.109",#"smartcity.ddns.net",
    'backend_port' : "8083"
}


def activate_terminal(backend):
    def run_terminal():
        terminal = Terminal(backend)
        terminal.start()

    thread1 = Thread(target=run_terminal)
    thread1.start()


if __name__ == "__main__":
    print(" _____          __  __ _      _     _       _     _    ____               ")
    print("|_   _|        / _|/ _(_)    | |   (_)     | |   | |  / __ \               ")
    print("  | |_ __ __ _| |_| |_ _  ___| |    _  __ _| |__ | |_| /  \/ ___  _ __ ___ ")
    print("  | | '__/ _\`|  _|  _| |/ __| |   | |/ _ \` |  \| __| |   /  _ \| '  / _ \\")
    print("  | | | | (_| | | | | | | (__| |___| | (_| | | | | |_| \__/\ (_) | | |  __/")
    print("  \_/_|  \__,_|_| |_| |_|\___\_____/_|\__, |_| |_|\__|\____/\___/|_|  \___|")
    print("                                       __/ |                               ")
    print("                                      |___/                                ")
    print("                                                                           ")
    print("Universiteit Antwerpen - [2018-2019]                                       ")
    print("v0.0.1                                                                     ")
    mqttClient = MqttClient(settings)
    # Initialize models (hardcoded for now)
    t1 = TrafficLight(1, 17, "172.16.0.200", 1315, settings, mqttClient, startState="RED", redTime=2, greenTime=1)
    #t2 = TrafficLight(2, 22, "172.16.0.200", 1315, settings, mqttClient, startState="GREEN", redTime=2, greenTime=1)
    models = Crossing({1: t1}) # , 2: t2})
    activate_terminal(models)
    REST.RestApi(models)
