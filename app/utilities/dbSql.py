import sqlite3, os
from typing import Any
from app.utilities import logging
from typing import Union
import logging
class sqldb():
    def __init__(self, path: str = os.path.join(os.getcwd(), 'app', 'database')):
        """Initializes Databse Class

        Args:
            path (str, optional): path to folder which contains all .db files. Defaults to os.path.join(os.getcwd(), 'app', 'database').

        Raises:
            ConnectionError: When connection can not be established
        """
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
        """ Lists all the tables present in database

        Raises:
            ConnectionError: When no Connection if Found

        Returns:
            _type_: iterable of object tables
        """
        if self.connect!="":
            raise ConnectionError
        else:
            sql_cmd = "SELECT name FROM sqlite_master WHERE type='table';"
            return [tables[0] for tables in self.cursor(sql_cmd)]

    
    def add(self, table: str, data: Union[str, list, tuple, dict], createTable: bool = False) -> Union[str, bool]:
        """Adding content to table

        Args:
            table (str): Name of Table
            data (Union[str, list, tuple, dict]): List of elements that needs to be added
            createTable (bool, optional): Wether to create table is it is not created already. Defaults to False.

        Raises:
            TableNotFoundException: When table is not found

        Returns:
            Union[str, bool]: _description_
        """
        tables = self.all_tables()
        if table not in tables and createTable is False:
            raise TableNotFoundException
        elif table not in tables:
            keys = data[0].keys()
            query = "CREATE TABLE {TABLE} ({column})"
            keys = ", ".join("str "+k for k in keys)
            query = query.format(TABLE=table, column=keys)
            self.cursor.execute(query)

        if isinstance(data[0], dict):
            for element in data:
                keys = element.keys()
                values = element.values()
                query = 'INSERT INTO {TABLE} ({KEYS}) VALUES ({VALUES})'
                keys = ", ".join(k for k in keys)
                values = ",".join("?" for v in values)
                self.cursor.execute(query.format(TABLE=table, KEYS=keys), values)
        elif isinstance(data[0], list) or isinstance(data[0], tuple):
            for element in data:
                query = 'INSERT INTO {TABLE} VALUES ({VALUES})'
                values = ",".join("?" for e in element)
                self.cursor.execute(query.format(table), values)
        elif isinstance(data[0], str):
            query = 'INSERT INTO {TABLE} VALUES ({VALUES})'
            values = ",".join("?" for e in data)
            self.cursor.execute(query, values)

    def remove(self, table: str, fieldName: str, data: str):
        """Removes Data from table

        Args:
            table (str): Name of Table
            fieldName (str): Column Name
            data (str): data to find

        Raises:
            TableNotFoundException: _description_
        """
        tables = self.all_tables()
        if table not in tables:
            raise TableNotFoundException
        query = f"DELETE FROM {table} WHERE {fieldName} = '{data}'"
        self.cursor.execute(query)
    
    def find(self, table: str,  fieldName: Union[str, None], data: Union[str, list, tuple, None], fetches: str = "*") -> list:
        """Finds Data in Tables

        Args:
            table (str): Name of Table
            fieldName (Union[str, None]): Column Name 
            data (Union[str, list, tuple, None]): Key to find data
            fetches (str, optional): What data to fetch. Defaults to "*".

        Returns:
            list: List of fetched data
        """
        query = "SELECT {fetches} FROM {table} WHERE {fieldName} = {data}"
        query = query.format(fetches = fetches, table = table, fieldName = fieldName)
        fetched_data = []
        if isinstance(data, list) or isinstance(data, tuple):
            for element in data:
                self.cursor.execute(query.format(data=element))
                result = self.cursor.fetchall()
                fetched_data.append(d for d in result)
        elif isinstance(data, str):
            self.cursor.execute(query.format(data=data))
            result = self.cursor.fetchall()
            fetched_data.append(d for d in result)
        return data


                
        
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