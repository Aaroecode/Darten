
import mysql.connector as sqlator
from typing import Union
from app.utility import logging as logging
import configparser, os, json

logger  = logging.get_logger(name = 'Data Driver')

class data():
    def __init__(self, data_driver: Union[str, None] = "json", credentials: Union[dict, None] = None, path: Union[str,configparser.SectionProxy ,None] = None):
        if data_driver == "sql":
            self.mysql = credentials["use mySQL"]
            self.mysqluser = credentials["user"]
            self.mysqlpass = credentials["password"]
            self.mysqlhost = credentials["host"]
            self.mysqlport = credentials["port"]
            self.database = credentials["database"]
            try:
                self.sqlconnection = sqlator.connect(host=self.mysqlhost, port=self.mysqlport, user = self.mysqluser, passwd = self.mysqlpass, database = self.database)
                if not self.sqlconnection.is_connected():
                    logger.warn("Could not connect to database '%s'", self.database)
                    return f"Could not connect to database {self.database}"
                self.cursor = self.sqlconnection.cursor()
                return f"Connected to database {self.database}"
            except Exception as e:
                logger.error(e)
        self.path = path
        self.data_driver = data_driver
        if "json" in data_driver:
            if not os.path.exists(f"{path['json_data']}"):
                os.makedirs(f"{path['json_data']}", exist_ok=True)
    def read(self, key: str, *to_read: Union[int, float, str] ):
        record = {}
        if self.sqlconnection.is_connected():
            self.cursor.execute("show tables")
            tables = self.sqlconnection.fetchall()
            for table in tables:
                self.cursor.execute(f"desc {table}")
                fields = self.sqlconnection.fetchall()
                for field in fields:
                    if field[0] in to_read:
                        self.cursor.execute(f"select {field} from {table} where id = {key}")
                        data = self.sqlconnection.fetchall()
                        record[field] = data
        if "json" in self.data_driver:
            for files in os.listdir(self.path):
                if files.endswith(".json") and not files.startswith("permission"):
                    with open(self.path, "r") as f:
                        file = json.load(f)
                    try:
                        for items in file[key]:
                            if items in to_read:
                                record[f"{key}"] = file[key]
                    except KeyError:
                        pass
    def write():
        return "Under Development"