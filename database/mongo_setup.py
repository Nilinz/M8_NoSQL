import configparser
from mongoengine import connect

config = configparser.ConfigParser()
config.read('config.ini')

mongodb_config = config['mongodb']

host = mongodb_config['host']
username = mongodb_config['username']
password = mongodb_config['password']
database = mongodb_config['database']

connect(
    db=database,
    host=host,
    username=username,
    password=password,
    authentication_source='admin',  # аутентифікація на рівні бази даних
    authentication_mechanism='SCRAM-SHA-1',  # механізм аутентифікації
)
