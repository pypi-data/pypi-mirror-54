import requests

name = "easydb-io"

class DB:
    def __init__(self, config):
        if not config:
            raise Exception("Config is required")

        db = config.get("database")
        token = config.get("token")
        if not db:
            raise Exception("Database must be provided")

        if not token:
            raise Exception("Token must be provided")
        self.database = db
        self.token = token

    def Get(self, key):
        r = requests.get('https://app.easydb.io/{}/{}'.format(self.database, key))
        return r.json()

    def Put(self, key, value):
        data = {
            "token": self.token,
            "value": value
        }
        r = requests.post('https://app.easydb.io/{}/{}'.format(self.database, key), json=data)
    
    def Delete(self, key):
        data = {
            "token": self.token,
        }
        r = requests.delete('https://app.easydb.io/{}/{}'.format(self.database, key), json=data)
        
    def List(self):
        r = requests.get('https://app.easydb.io/{}'.format(self.database))
        return r.json()