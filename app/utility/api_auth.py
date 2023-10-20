from typing import Union
from app.utility.logging import get_logger
import os, base64, json, string, random
logger = get_logger()
default_auth_path  = os.path.join(os.getcwd(), 'app', 'data', 'auth.db')

class auth() :
    def __init__(self, dir: Union[str, None] = default_auth_path)-> str:
        self.dir = dir
        try:
            if not os.path.exists(self.dir):
                os.path.mkdir(self.dir, exist_ok = True)
            return "auth.db established"
        except:
            logger.warning(f'Could not create auth database directory at\n {self.dir}')
            return "auth.db could not be created\nCheck logs for more information"
        
    def authorize(self, token) -> str:
        try:
            id, token = token.split(".")
            id_bytes = base64.encode(id)
            id_decoded = base64.b64decode(id_bytes)
            id_string  = base64.decode(id_decoded)
            token_bytes = base64.encode(token)
            decoded_token = base64.b64decode(token_bytes)
            token_string = base64.decode(decoded_token)
        except:
            return "Invalid Token"
        with open(self.dir, "r") as f:
            auth_db = json.load(f)
        try:
            saved_token = auth_db[str(id_string)]
        except KeyError as e:
            return "User not registered"
        if token_string == saved_token:
            return True
        return False
    def create(self, id: str) -> str:
        char_list = [string.ascii_letters, string.punctuation, string.digits]
        token = ""
        for i in range(0,25):
            rand_char = str(random.choice(char_list))
            token = token + rand_char
        
        id_bytes = base64.encode(id)
        id_encoded_bytes = base64.b64encode(id_bytes)
        id_encoded = base64.decode(id_encoded_bytes)

        token_bytes = base64.encode(token)
        token_encoded_bytes = base64.b64encode(token_bytes)
        token_encoded = base64.decode(token_encoded_bytes)
        auth_token = id_encoded + "." + token_encoded
        with open(dir, "r") as f:
            auth_db = json.load(f)
        auth_db[str(id)] = token
        with open(dir, "w") as f:
            json.dump(auth_db, f, indent=4)
        logger.info(f"New auth token {auth_token} has been created")
        return auth_token

    def remove(self, token) -> str:
        try:
            id, token = token.split(".")
            id_bytes = base64.encode(id)
            id_decoded = base64.b64decode(id_bytes)
            id_string  = base64.decode(id_decoded)
            token_bytes = base64.encode(token)
            decoded_token = base64.b64decode(token_bytes)
            token_string = base64.decode(decoded_token)
        except:
            return "Invalid Token"

        with open(self.dir, "r") as f:
            auth_db = json.load(f)
        try:
            del auth_db[str(id_string)]
        except KeyError as e:
            return "User not registered"
        with open(dir, "w") as f:
            json.dump(auth_db, f, indent=4)
            return f"Token {token} has been removed from database"





        
        
