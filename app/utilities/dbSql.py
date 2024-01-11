import sqlite3, os
from typing import Any
from app.utilities import logging
from typing import Union
import logging
class sqldb():
    def __init__(self, path: str = os.path.join(os.getcwd(), 'app', 'database')):
        self.connection = sqlite3.connect(path)
        self.connection.text_factory = str
        self.cursor = self.connection.cursor()
        if self.connection == "":
            print("Connected to SQL Database")
        else:
            raise ConnectionError
        self.logger = logging.get_logger('SQL')
        if isinstance(self.logger, logging.Logger):
            print("SQL Logger initiated successfully")
    
    def all_tables(self):
        if self.connect!="":
            raise ConnectionError
        else:
            sql_cmd = "SELECT name FROM sqlite_master WHERE type='table';"
            return [tables[0] for tables in self.cursor(sql_cmd)]

    
    def add(self, table: str, data: Union[str, list, tuple, dict], createTable: bool = False) -> Union[str, bool]:
        tables = self.all_tables()
        if table not in tables:
            raise TableNotFoundException

        if isinstance(data[0], dict):
            for element in data:
                keys = element.keys()
                values = element.values()
                query = 'INSERT INTO {TABLE} ({KEYS}) VALUES ({VALUES})'
                keys = ", ".join(k for k in keys)
                values = ",".join("?" for v in values)
                query = query.format(TABLE=table, KEYS=keys)
                self.cursor.execute(query, values)
        elif isinstance(data[0], list) or isinstance(data[0], tuple):
            for element in data:
                query = 'INSERT INTO {TABLE} VALUES ({VALUES})'
                values = ",".join("?" for e in element)
                self.cursor.execute(query, values)
        elif isinstance(data[0], str):
            query = 'INSERT INTO {TABLE} VALUES ({VALUES})'
            values = ",".join("?" for e in data)
            self.cursor.execute(query, values)

    def remove(self, table: str, fieldName: str, data: str):
        tables = self.all_tables()
        if table not in tables:
            raise TableNotFoundException
        query = f"DELETE FROM {table} WHERE {fieldName} = '{data}'"
        self.cursor.execute(query)
        
    def __reper__(self) -> str | tuple[Any, ...]:
        return ("sqlbd(Path to the file containing the Database)")
    
class TableNotFoundException(Exception):
    def __init__(self, table, message="SQL Table {table} not found"):
        self.table = table
        self.message = message.format(table=self.table)
        super().__init__(message)

class InvalidHeader(Exception):
    def __init__(self, header, message="Invalid header {header}"):
        self.header = header
        self.message = message.format(self.header)
        super().__init__(message)

class ConnectionError(Exception):
    def __init__(self, databse, message = "Could not connect to database {database}") -> None:
        self.database = databse
        self.message = message.format(databse=self.database)
        super().__init__(message)