
import ssl
import smtplib
from typing import Union
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email import utils
from app.utilities.clogging import get_logger
import time

mailLogger = get_logger("Mail Client")


class Mail():
    def __init__(self, username: str, password: str, host: str = "localhost", port: int = 465):
        context = ssl.create_default_context()
        self.mailer = smtplib.SMTP_SSL(host=host, port=port, context=context)
        self.mailer.login(user=username, password=password)
    
    async def send(self, format_name: str, sender:str, reciever:str, subject:str, template, contents: Union[dict,None], placeholder: dict):
        messge = MIMEMultipart("alternative")
        messge["Subject"] = subject
        messge["From"] = utils.formataddr((format_name , sender))
        messge["To"] = reciever
        messge["message-id"] = utils.make_msgid(domain="techrise.club")

        with open(template, "r") as f:
            htmlemail = f.read()
        
        for item in placeholder:
            htmlemail = htmlemail.replace(str(item), str(placeholder[item]))
        htmlemail = MIMEText(htmlemail, "html")
        messge.attach(htmlemail)
        if contents is not None:
            for key, value in contents.items():
                with open(value, "rb") as f:
                    image = MIMEImage(f.read())
                image.add_header("Content-ID", str(key))
                messge.attach(image)
        time_stamps = [10,60, 600, 3600,7200, 18000, 36000]
        retryTime = 0
        while retryTime<7:
            try:
                self.mailer.sendmail(sender, reciever, messge.as_string())
                mailLogger.log(20, "Mail Sent")
                break
            except:
                time.sleep(time_stamps[retryTime])
                retryTime += 1





