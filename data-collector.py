import configparser
import datetime
import saia
import jsonstore
import os

basePath = os.environ.get('PIHEIZ')
basePath= basePath if basePath is not None else os.getcwd() 

config = configparser.ConfigParser()
config.read(os.path.join(basePath, 'config.ini'))

data = { "time": datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")}

for key in config['READVALUES']:  
    data[key]= saia.get_value(config['READVALUES'][key])
    
jsonstore.append_json(data,os.path.join(basePath,'data.json'))
