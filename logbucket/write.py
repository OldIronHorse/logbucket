from pymongo import MongoClient

from pprint import pprint

import config

client = MongoClient(config.DATABASE['connection_string'])
db=client.logbucket
events=db.events
event = {
  'topic': 'location/sublocation/dimension',
  'payload': {
    'name': 'nom',
    'value': 1234,
  },
}
event_id = events.insert_one(event).inserted_id
print('Inserted', event, 'as event', event_id)
