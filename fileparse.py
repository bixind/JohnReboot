import json

def jsonRead(name):
    with open(name, 'r') as f:
        return json.loads(f.readline())

def jsonSave(name, data):
    with open(name, 'w') as f:
        print(json.dumps(data), file = f)
