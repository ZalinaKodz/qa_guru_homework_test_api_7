class Server:
    def __init__(self, env):
        self.reqres = {
            "dev": "http://localhost:8002/",
            "beta": "",
            "rc": "",
        }[env]