"""

A small Test application to show how to use Flask-MQTT.

"""
#import eventlet

#eventlet.monkey_patch()

import json
import logging
import time

from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_socketio import SocketIO

from flask_mqtt import Mqtt

app = Flask(__name__)
#app.config["SECRET"] = "my secret key"
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["MQTT_BROKER_URL"] = "localhost"
app.config["MQTT_BROKER_PORT"] = 1883
app.config["MQTT_CLIENT_ID"] = "flask_mqtt"
app.config["MQTT_CLEAN_SESSION"] = True
#app.config["MQTT_USERNAME"] = ""
#app.config["MQTT_PASSWORD"] = ""
app.config["MQTT_KEEPALIVE"] = 5
app.config["MQTT_TLS_ENABLED"] = False
app.config["MQTT_LAST_WILL_TOPIC"] = "home/lastwill"
app.config["MQTT_LAST_WILL_MESSAGE"] = "bye"
app.config["MQTT_LAST_WILL_QOS"] = 2
app.config['MQTT_TLS_ENABLED'] = False  # set TLS to disabled for testing purposes

# Parameters for SSL enabled
# app.config['MQTT_BROKER_PORT'] = 8883
# app.config['MQTT_TLS_ENABLED'] = True
# app.config['MQTT_TLS_INSECURE'] = True
# app.config['MQTT_TLS_CA_CERTS'] = 'ca.crt'


if __name__ == "__main__":
    with app.app_context():
        mqtt = Mqtt(app)
        #socketio = SocketIO(app)
        #bootstrap = Bootstrap(app)
        connected = False

        @app.route("/")
        def index():
            return render_template("index.html")

        #@socketio.on("publish")
        #def handle_publish(json_str):
        #    data = json.loads(json_str)
        #    mqtt.publish(data["topic"], data["message"], data["qos"])

        #@socketio.on("subscribe")
        #def handle_subscribe(json_str):
        #    data = json.loads(json_str)
        #    mqtt.subscribe(data["topic"], data["qos"])

        #@socketio.on("unsubscribe_all")
        #def handle_unsubscribe_all():
        #    mqtt.unsubscribe_all()

        @mqtt.on_connect()
        def handle_connect(client, userdata, flags, rc):
            global connected
            connected = True
            logging.critical("handle_connect %s %s %s %s", client, userdata, flags, rc)
            mqtt.subscribe("test")

        @mqtt.on_message()
        def handle_mqtt_message(client, userdata, message):
            data = dict(
                topic=message.topic,
                payload=message.payload.decode(),
                qos=message.qos,
            )
            logging.critical(f"handle_mqtt_message {data}")
            #socketio.emit("mqtt_message", data=data)

        @mqtt.on_log()
        def handle_logging(client, userdata, level, buf):
            # print(level, buf)
            pass

        while True:
            if connected:
                mqtt.publish("test", "test")
            time.sleep(1)

        #socketio.run(app, host="0.0.0.0", port=1883, use_reloader=False, debug=True)
