import hashlib


class Authenticator():
    def __init__(self) -> None:
        pass

    def check(self, token: str):
        t = "Hitesh"
        t = t.encode()
        t = hashlib.sha256(t)
        t = "Bearer " + str(t.hexdigest())
        if token == t:
            return True
        else:
            return False
        
