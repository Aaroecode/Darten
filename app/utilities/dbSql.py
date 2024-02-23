import sqlite3, os
from typing import Any
from app.utilities.clogging import get_logger
from typing import Union
class sqldb():
    def __init__(self, path: str = os.path.join(os.getcwd(), 'app', 'database', 'main.db')):
        """Initializes Databse Class

        Args:
            path (str, optional): path to folder which contains all .db files. Defaults to os.path.join(os.getcwd(), 'app', 'database').

        Raises:
            ConnectionError: When connection can not be established
        """
        self.connection = sqlite3.connect(path, check_same_thread=False)
        self.connection.text_factory = str
        self.cursor = self.connection.cursor()
        if self.cursor:
            print("Connected to SQL Database")
        else:
            raise ConnectionError(path)
        self.logger = get_logger('SQL')

        print("SQL Logger initiated successfully")
    
    def all_tables(self):
        """ Lists all the tables present in database


        Returns:
            _type_: iterable of object tables
        """

        sql_cmd = "SELECT name FROM sqlite_master WHERE type='table';"
        self.cursor.execute(sql_cmd)
        tables = self.cursor.fetchall()
        return [tables[0] for tables in tables]

    
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
            raise TableNotFoundException(table)
        elif table not in tables:
            keys = data[0].keys()
            query = "CREATE TABLE `{TABLE}` ({column})"
            keys = ", ".join(k+" TEXT" for k in keys)
            query = query.format(TABLE=table, column=keys)

            self.cursor.execute(query)

        if isinstance(data[0], dict):
            for element in data:
                keys = element.keys()
                values = tuple(element.values())
                query = 'INSERT INTO `{TABLE}` ({KEYS}) VALUES ({VALUES})'
                keys = ", ".join(k for k in keys)
                param = ",".join("?" for v in values)
                query = query.format(TABLE=table, KEYS=keys, VALUES = param)
                self.cursor.execute(query, values)
        elif isinstance(data[0], list) or isinstance(data[0], tuple):
            for element in data:
                query = 'INSERT INTO `{TABLE}` VALUES ({VALUES})'
                param = ",".join("?" for e in element)
                query = query.format(TABLE=table, VALUES=param)
                self.cursor.execute(query, values)
        elif isinstance(data[0], str):
            query = 'INSERT INTO `{TABLE}` VALUES ({VALUES})'
            param = ",".join("?" for e in data)
            query = query.format(TABLE=table, VALUES = param )
            self.cursor.execute(query, values)
        self.connection.commit()

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
            raise TableNotFoundException(table)
        query = f"DELETE FROM `{table}` WHERE {fieldName}='{data}'"
        self.cursor.execute(query)
        self.connection.commit()
    
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
        query = "SELECT {fetches} FROM `{table}` WHERE {fieldName} = {data}"
        fetched_data = []
        if isinstance(data, list) or isinstance(data, tuple):
            for element in data:
                try:
                    self.cursor.execute(query.format(fetches = fetches, table = table, fieldName = fieldName,data=element))
                    result = self.cursor.fetchall()
                    fetched_data.append(d for d in result)
                except:
                    pass
        elif isinstance(data, str):
            try:
                self.cursor.execute(query.format(fetches = fetches, table = table, fieldName = fieldName,data=data))
                result = self.cursor.fetchall()
                fetched_data.append(d for d in result)
            except:
                pass
        if fieldName == None and data == None:
            try:
                query = f"SELECT {fetches} From {table}"
                self.cursor.execute(query)
                result = self.cursor.fetchall()
                fetched_data.append(d for d in result)
            except:
                pass

        return data


                
        
    def __reper__(self) -> str | tuple[Any, ...]:
        return ("sqlbd(Path to the file containing the Database)")
    
class TableNotFoundException(Exception):
    def __init__(self, table, message="SQL Table {Table} not found"):
        self.message = message
        self.message = self.message.format(Table=table)
        super().__init__(message)

class InvalidHeader(Exception):
    def __init__(self, header, message="Invalid header {header}"):
        self.header = header
        self.message = message.format(self.header)
        super().__init__(message)

class ConnectionError(Exception):
    def __init__(self, database, message = "Could not connect to database {database}") -> None:
        self.database = database
        self.message = message.format(database=self.database)
        super().__init__(message)