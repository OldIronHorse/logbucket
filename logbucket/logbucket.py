from pymongo import MongoClient
import paho.mqtt.client as mqtt
import json

import config

def on_message(client, userdata, message):
  print('on_message...')
  event = {
   'topic': message.topic,
   'payload': json.loads(message.payload.decode('utf-8')),
  }
  userdata['db_collection'].insert_one(event)
  print('\t inserted:', event)

if __name__ == '__main__':
  client = MongoClient(config.DATABASE['connection_string'])
  db=client.logbucket
  events=db.events
  print('Connecting to', config.MQTT['host'], 'as', config.MQTT['client_id'])
  client = mqtt.Client(config.MQTT['client_id'], 
                       userdata={'db_collection':events})
  client.connect(config.MQTT['host'])
  client.on_message=on_message
  topic = 'logbucket/' + config.LOGBUCKET['domain'] +'/#'
  print('Subscribing to', topic)
  client.subscribe(topic)
  client.loop_forever()

