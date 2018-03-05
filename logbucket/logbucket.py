from pymongo import MongoClient
import paho.mqtt.client as mqtt
import json
from datetime import datetime, timezone
import logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

all_payload_handlers = {
  'json': (lambda p: json.loads(p.decode('utf-8'))),
  'integer': (lambda p: int(p.decode('utf-8'))),
  'string': (lambda p: p.decode('utf-8')),
}

domain_payload_handlers = {}

def on_message(client, userdata, message):
  log.info('on_message: topic %s, payload: %s', message.topic, message.payload)
  topic = message.topic.split('/')
  domain = topic[1]
  event = {
    'timestamp': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f %z'),
    'topic': topic,
    'payload': domain_payload_handlers[domain](message.payload),
  }
  userdata['db'][domain].insert_one(event)
  log.info('on_message: [%s] inserted %s', domain, event)

def main(cfg):
  db_client = MongoClient(cfg['database']['connection_string'])
  db = db_client.logbucket
  log.info('main: Connecting to MQTT broker %s as %s', 
           cfg['mqtt']['host'], 
           cfg['mqtt']['client_id'])
  client = mqtt.Client(cfg['mqtt']['client_id'], 
                       userdata={'db': db})
  client.connect(cfg['mqtt']['host'])
  client.on_message = on_message
  for domain in cfg['logbucket']['domains']:
    topic = 'logbucket/' + domain +'/#'
    domain_payload_handlers[domain] = \
        all_payload_handlers[cfg['logbucket']['domains'][domain]['payload_type']]
    log.info('main: domain: %s, topic: %s', domain, topic)
    client.subscribe(topic)
  client.loop_forever()


