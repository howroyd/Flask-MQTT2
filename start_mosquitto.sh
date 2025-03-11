#!/bin/bash
# Description: Start mosquitto container

docker run -it -p 1883:1883 -v "./mosquitto/config:/mosquitto/config" -v /mosquitto/data -v /mosquitto/log  eclipse-mosquitto