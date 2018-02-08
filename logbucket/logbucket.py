from pymongo import MongoClient
import paho.mqtt.client as mqtt
import json
from datetime import datetime, timezone

import config



all_payload_handlers = {
  'json': (lambda p: json.loads(p.decode('utf-8'))),
  'integer': (lambda p: int(p.decode('utf-8'))),
}

domain_payload_handlers = {}

def on_message(client, userdata, message):
  print('on_message...')
  print('\ttopic:', message.topic)
  print('\tpayload:', message.payload)
  topic = message.topic.split('/')
  domain = topic[1]
  event = {
    'timestamp': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f %z'),
    'topic': topic,
    'payload': domain_payload_handlers[domain](message.payload),
  }
  userdata['db'][domain].insert_one(event)
  print('\tinserted into', domain, ':', event)

if __name__ == '__main__':
  db_client = MongoClient(config.DATABASE['connection_string'])
  db = db_client.logbucket
  print('Connecting to', config.MQTT['host'], 'as', config.MQTT['client_id'])
  client = mqtt.Client(config.MQTT['client_id'], 
                       userdata={'db': db})
  client.connect(config.MQTT['host'])
  client.on_message = on_message
  for domain in config.LOGBUCKET['domains']:
    topic = 'logbucket/' + domain['name'] +'/#'
    domain_payload_handlers[domain['name']] = all_payload_handlers[domain['payload_type']]
    print('Subscribing to', topic)
    client.subscribe(topic)
  client.loop_forever()

