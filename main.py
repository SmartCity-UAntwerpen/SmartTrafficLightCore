import signal
from threading import Thread
from TrafficLightCore import RestAPI as REST
from TrafficLightCore.Terminal import Terminal
from TrafficLightCore.Crossing import Crossing
from TrafficLightCore.TrafficLight import TrafficLight
from TrafficLightCore.mqttClient import MqttClient

models = None

settings = {
    # MQTT settings
    'mqtt_ip': "localhost",  # "broker.mqttdashboard.com"
    #'mqtt_ip': "smartcity.ddns.net",  # "broker.mqttdashboard.com"
    'mqtt_port': 1883,
    'mqtt_username': "smartcity",
    #'mqtt_username': "root",
    'mqtt_password': "smartcity",

    # Robot backend settings
    'backend_ip': "localhost",
    #'backend_ip': "smartcity.ddns.net",
    'backend_port': "1994",
    #'backend_port': "8083",

    # Trafficlight driver
    'driver_host' : "172.16.0.200",
    'driver_port' : 1315
}


def service_shutdown(signum, frame):
    print("Shutdown received")
    raise ServiceExit


class ServiceExit(Exception):
    """
    Custom exception which is used to trigger the clean exit
    of all running threads and the main program.
    """
    pass


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

    # Register the signal handlers
    signal.signal(signal.SIGTERM, service_shutdown)
    signal.signal(signal.SIGINT, service_shutdown)

    mqttClient = MqttClient(settings)
    # Initialize traffic light models (hardcoded for now)
    t1 = TrafficLight(1, 76, settings, mqttClient, startState="RED", redTime=15, greenTime=10)
    t2 = TrafficLight(2, 69, settings, mqttClient, startState="GREEN", redTime=15, greenTime=10)

    models = Crossing({1: t1, 2: t2})
    terminal = Terminal(models)
    try:
        terminal.start()
        REST.RestApi(models)

    except ServiceExit:
        # Terminate the running threads.
        # Set the shutdown flag on each thread to trigger a clean shutdown of each thread.
        terminal.shutdown_flag.set()
        #terminal.join()
        terminal.stop()
        exit(1)
