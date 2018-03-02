from setuptools import setup

setup(name='logbucket',
      version='0.1',
      description='Event logging with MQTT and MongoDB',
      url='http://github.com/oldironhorse/logbucket',
      license='GPL 3.0',
      packages=['logbucket'],
      install_requires=[
        'flask',
        'pymongo',
        'dnspython',
        'paho-mqtt',
        'PyYAML',
      ],
      test_suite='nose.collector',
      tests_require=['nose'],
      zip_safe=False)
