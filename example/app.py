"""

A small Test application to show how to use Flask-MQTT.

"""

import logging
import threading
import time
from typing import Final

from flask import Flask

from flask_mqtt2 import Mqtt
from paho.mqtt.client import error_string




logging.getLogger().setLevel(logging.INFO)


def make_app() -> Flask:
    app = Flask(__name__)
    # app.config["SECRET"] = "my secret key"
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.config["MQTT_BROKER_URL"] = "localhost"
    app.config["MQTT_BROKER_PORT"] = 1883
    app.config["MQTT_CLIENT_ID"] = "flask_mqtt"
    app.config["MQTT_CLEAN_SESSION"] = True
    # app.config["MQTT_USERNAME"] = ""
    # app.config["MQTT_PASSWORD"] = ""
    app.config["MQTT_KEEPALIVE"] = 5
    app.config["MQTT_TLS_ENABLED"] = False
    app.config["MQTT_LAST_WILL_TOPIC"] = "home/lastwill"
    app.config["MQTT_LAST_WILL_MESSAGE"] = "bye"
    app.config["MQTT_LAST_WILL_QOS"] = 2
    app.config["MQTT_TLS_ENABLED"] = False  # set TLS to disabled for testing purposes

    # Parameters for SSL enabled
    # app.config['MQTT_BROKER_PORT'] = 8883
    # app.config['MQTT_TLS_ENABLED'] = True
    # app.config['MQTT_TLS_INSECURE'] = True
    # app.config['MQTT_TLS_CA_CERTS'] = 'ca.crt'

    return app


def make_mqtt(app: Flask) -> Mqtt:
    mqtt: Mqtt = Mqtt(app)
    connected: Final = threading.Event()

    @mqtt.on_connect()
    def handle_connect(client, userdata, flags, rc):
        connected.set()
        logging.info(f"handle_connect ({error_string(rc)})")
        mqtt.subscribe("test")

    @mqtt.on_message()
    def handle_mqtt_message(client, userdata, message):
        data = dict(
            topic=message.topic,
            payload=message.payload.decode(),
            qos=message.qos,
        )
        logging.info(f"handle_mqtt_message {data}")

    @mqtt.on_log()
    def handle_logging(client, userdata, level, buf):
        # print(level, buf)
        pass

    @mqtt.on_disconnect()
    def handle_disconnect(client, userdata, rc):
        logging.critical(f"handle_disconnect ({error_string(rc)})")

    logging.info("Waiting for connection...")
    if not connected.wait(timeout=10):
        raise IOError("Could not connect to broker (timeout)")
    logging.info("Connected!")

    return mqtt


def main():
    app: Final = make_app()

    with app.app_context():
        mqtt: Final = make_mqtt(app)

        while True:
            mqtt.publish("test", "test")
            time.sleep(1)


if __name__ == "__main__":
    main()
