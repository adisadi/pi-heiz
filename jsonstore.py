import json
from pathlib import Path

JSONROOT='PdcValues'
MAXITEMS=24*4*2

def write_json(data, filename='data.json'): 
    with open(filename,'w') as f: 
        json.dump(data, f, indent=4)

def load_json(filename='data.json'):
    try:
        Path(filename).resolve(strict=True)
    except FileNotFoundError:
        # doesn't exist
        return {}
    else:
        # exists
        with open(filename) as json_file: 
            data = json.load(json_file) 
        return data

def append_json(data,filename='data.json'):
    store=load_json(filename)

    if JSONROOT not in store:
        store[JSONROOT]=[]

    if (len(store[JSONROOT])>=(MAXITEMS-1)):
        store[JSONROOT]=store[JSONROOT][1:]

    store[JSONROOT].append(data)
    write_json(store,filename)
    