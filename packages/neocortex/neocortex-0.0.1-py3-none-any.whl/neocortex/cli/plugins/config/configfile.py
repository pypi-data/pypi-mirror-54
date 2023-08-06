import configparser
import logging

def get_config(config_path):
    config = configparser.ConfigParser()
    config.read(config_path)
    return config

def write_config(config_path,server='127.0.0.1',port='5800',user='admin',password='admin'):
    config = configparser.ConfigParser()
    config['NEOSERVER'] = {'server': server,
                        'serverport': port,
                        'username': user,
                        'password': password}
    with open(config_path,'w') as configfile:
        config.write(configfile)
    return config.read(config_path)