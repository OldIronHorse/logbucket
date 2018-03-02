import argparse
import yaml
from pymongo import MongoClient
import paho.mqtt.client as mqtt
import json
from datetime import datetime, timezone

all_payload_handlers = {
  'json': (lambda p: json.loads(p.decode('utf-8'))),
  'integer': (lambda p: int(p.decode('utf-8'))),
  'string': (lambda p: p.decode('utf-8')),
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

# main
parser = argparse.ArgumentParser(prog='logbucket')
parser.add_argument('-c', '--config', type=str, required=True,
                    help='path to configuration file (YAML)')
args = parser.parse_args()
print(args)
with open(args.config, 'r') as config_file:
  cfg = yaml.load(config_file)

print(cfg)

db_client = MongoClient(cfg['database']['connection_string'])
db = db_client.logbucket
print('Connecting to', cfg['mqtt']['host'], 'as', cfg['mqtt']['client_id'])
client = mqtt.Client(cfg['mqtt']['client_id'], 
                     userdata={'db': db})
client.connect(cfg['mqtt']['host'])
client.on_message = on_message
for domain in cfg['logbucket']['domains']:
  print(domain)
  topic = 'logbucket/' + domain +'/#'
  domain_payload_handlers[domain] = \
      all_payload_handlers[cfg['logbucket']['domains'][domain]['payload_type']]
  print('Subscribing to', topic)
  client.subscribe(topic)
client.loop_forever()


