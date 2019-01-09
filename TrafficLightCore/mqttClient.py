import paho.mqtt.client as mqtt

class MqttClient:

    def __init__(self, settings):
        user = {
            'username': settings.get("mqtt_username"),
            'password': settings.get("mqtt_password")
        }
        self.client = mqtt.Client()
        self.client.username_pw_set(settings.get("mqtt_username"), settings.get("mqtt_password"))
        print("MQTT connecting...")
        self.client.on_publish = self.on_publish
        self.client.connect(settings.get("mqtt_ip"), settings.get("mqtt_port"))
        self.client.loop_start()

    def publish(self, topic, message):
        x = self.client.publish(topic, message, qos=2)

    def on_publish(self):
        print("Message published!")


