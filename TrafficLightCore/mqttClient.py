import paho.mqtt.client as mqtt

class MqttClient:

    def __init__(self, settings):
        """
        Start MQTT connection with provided settings
        :param settings: mqtt settings
        """
        self.client = mqtt.Client()
        self.client.username_pw_set(settings.get("mqtt_username"), settings.get("mqtt_password"))
        print("MQTT connecting...")
        self.client.on_publish = self.on_publish
        self.client.connect(settings.get("mqtt_ip"), settings.get("mqtt_port"))
        self.client.loop_start()
        self.client.on_message = self.on_message

    def publish(self, topic, message):
        """
        Publish a mqtt message
        :param topic: (string) mqtt topic
        :param message: (string)
        """
        x = self.client.publish(topic, message, qos=2)

    def on_publish(self):
        print("Message published!")

    def on_message(self, topic, message):
        print("Message received!: " +str(message)) # message.payload

    def parse_message(self, message):
        print("Message parsed!")
