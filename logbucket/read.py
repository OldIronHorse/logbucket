from pymongo import MongoClient

from pprint import pprint

import config

client = MongoClient(config.DATABASE['connection_string'])
db=client.logbucket
for collection in ['iot-test', 'app-log']:
  print('#### Collection:', collection, '####')
  for event in db[collection].find():
    pprint(event)
