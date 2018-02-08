import paho.mqtt.client as mqtt
import json
import time
import os
import socket

import config

if __name__ == '__main__':
  pid = os.getpid()
  client = mqtt.Client('app-log-client-01')
  client.connect(config.MQTT['host'])
  for i in range(0, 30):
    print(i)
    topic = 'logbucket/app-log/{}/{}/testapp/info'.format(socket.gethostname(),
                                                          os.getpid())
    client.publish(topic, json.dumps({
                    'level': 'info',
                    'file': __file__,
                    'function': 'main',
                    'description': 'loop counter incremented',
                    'value': i,
                  }))
    time.sleep(1)
