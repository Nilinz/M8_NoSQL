# config.py
import configparser

def get_mongo_uri():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['mongodb']['uri']

