from pymongo import MongoClient

from pprint import pprint

import config

client = MongoClient(config.DATABASE['connection_string'])
db=client.logbucket
events=db.events
for event in events.find():
  pprint(event)
