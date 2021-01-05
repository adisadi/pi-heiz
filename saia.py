import requests

def get_value(query):
    return requests.get("http://192.168.1.104/cgi-bin/readVal.exe?"+query).text




