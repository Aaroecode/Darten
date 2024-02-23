import os
from configparser import ConfigParser
from app.utilities.dbSql import sqldb
from app.utilities.emailClient import Mail
from app.utilities.gsheets import Gsheets
from app.utilities.clogging import get_logger
from app.utilities.authenticator import Authenticator
from dotenv import load_dotenv
config_path = os.path.join(os.getcwd(), "config.conf")
envpath = os.path.join(os.getcwd(), ".env")
load_dotenv(envpath)
configObject = ConfigParser()


def createConfig():
    var = configObject
    var["event1"] = {}
    var["event1"]["eventTime"] = "None"
    var["event1"]["eventDate"] = "None"
    var["event1"]["eventLocation"] = "None"
    var["event1"]["mailTemplate"] = "None"
    with open(config_path, "w") as f:
        var.write(f)

mail_user = os.getenv("MAIL_USER")
mail_password = os.getenv("MAIL_PASSWORD")

if os.path.exists(config_path):
    configObject.read(config_path)
else:
    createConfig()

    
class Config():
    sql = sqldb()
    logger = get_logger("app")
    mail = Mail(mail_user, mail_password, "mail.techrise.club")
    sheet = Gsheets("1euuUXN28zBf8ZolLKXkzsriMosTyiXkziknUzjNIFOI")
    authorizer = Authenticator()
    events = configObject




