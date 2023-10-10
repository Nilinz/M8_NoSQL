import configparser
import pika

config = configparser.ConfigParser()
config.read('config.ini')

rabbitmq_config = config['rabbitmq']

host = rabbitmq_config['host']
username = rabbitmq_config['username']
password = rabbitmq_config['password']

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=host, credentials=pika.PlainCredentials(username, password))
)
channel = connection.channel()
