from typing import Union
import os, json


class permission():
    def __init__(self, permission_file_path: Union[str, None] = os.path.join(os.getcwd(), "app", "database")):
        self.permission_file_path = permission_file_path
        if not os.path.exists(permission_file_path):
            os.makedirs(permission_file_path, exist_ok=True)
    

    def check(self, json_file: Union[str, json.load] = None, id: Union[str, None] = None):
        try:
            target = json_file["target"]
        except KeyError:
            return "Invalid data format"
        
        with open(self.permission_file_path, "r") as f:
            permission_file = json.load(f)
        
        try:
            for content in json_file["content"]:
                if permission_file[id][content] == "False":
                    return f"Permission denied for {content}"
        except KeyError:
            return "Invalid data format"
        
        return True