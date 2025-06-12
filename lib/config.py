import json

JSON_FILE = 'config.json'

class Config:
    def __init__(self):
        f = open(JSON_FILE)
        self.data = json.load(f)
        f.close()

    def hex2rgb(hex):
        return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))

    def update(self, data):
        json_string = self.json_pretty_print(json.loads(data),indent=4)
        #print(data)
        #print(json_string)
        #json_string = data
        with open(JSON_FILE, 'w') as f:
            f.write(json_string)

    def getValue(self, path):
        keys = path.split('.')
        val = self.data
        for key in keys:
            if key in val:
                val = val[key]
            else: return None
        return val
    
    def setValue(self, path, value):
        print(1)

    def json_pretty_print(self, json_data, indent=4):

        def iter_json(obj, level=1):
            if isinstance(obj, dict):
                indent_str = ' ' * (level * indent)
                pairs = []
                for key, value in obj.items():
                    pairs.append(f'"{key}": {iter_json(value, level+1)}')
                return '{{\n{}\n{}}}'.format(',\n'.join(pairs), indent_str)
            elif isinstance(obj, list):
                indent_str = ' ' * (level * indent)
                items = []
                for value in obj:
                    items.append(iter_json(value, level+1))
                return '[\n{}\n{}]'.format(',\n'.join(items), indent_str)
            else:
                return json.dumps(obj)
        
        return iter_json(json_data, level=1)
