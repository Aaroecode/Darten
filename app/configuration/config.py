from app.utility import logging
from app.utility import data_manager
import configparser, os


configFilePath = os.path.join(os.getcwd(), "config.ini")
conf = configparser.ConfigParser()
def config_init():
    conf["PATHS"] = {}
    conf["PATHS"]["json_data"] = os.path.join(os.getcwd(),"app","database")
    conf["PATHS"]["excel_data"] = os.path.join(os.getcwd(),"app","database")
    conf["PATHS"]["permissions"] = os.path.join(os.getcwd(), "app","database")
    conf["Credentials"] = {}
    conf["Credentials"]["sql_user"] = "None"
    conf["Credentials"]["sql_passwords"] = "None"
    conf["Credentials"]["sql_host"] = "None"
    conf["Credentials"]["sql_port"] = "None"
    conf["Credentials"]["sql_database"] = "None"
    conf["deplyoment"] = {}
    conf["deplyoment"]["host"] = "None"
    conf["deplyoment"]["port"] = "None"
    conf["deplyoment"]["debug"] = "False"
    with open(configFilePath, "w") as f:
        conf.write(f)


class Config():
    logger = logging.get_logger("GLOBAL")
    try:
        conf.read(configFilePath)
    except OSError as e:
        logger.error(f"Unable to read configuration file\n {e}")
        logger.warn("Creating new config file")
        config_init()
        conf.read(configFilePath)
    
    try:
        data_cursor = data_manager.data(data_driver="sql,json,excel", credentials=conf["Credentials"], path = conf["PATHS"])
    except KeyError as e:
        logger.error(f"Unable to read configuration file\n {e}")
        logger.warn("Creating new config file")
        config_init()
        conf.read(configFilePath)
    config = conf



    