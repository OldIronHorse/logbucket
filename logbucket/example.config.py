DATABASE = {
  'connection_string': <<YOUR MONGODB CONNECTION STRING>>,
}

MQTT = {
  'host': <<YOUR MQTT BROKER HOSTNAME>>,
  'client_id': 'logbucket-dbwriter',
}

LOGBUCKET = {
  'domains': [{
      'name': 'iot-test',
      'payload_type': 'integer',
    },{
      'name': 'app-log',
      'payload_type': 'json'
    }
  ]
}
