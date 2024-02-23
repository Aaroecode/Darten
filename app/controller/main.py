from flask import Flask, request, render_template, Response
import os, hashlib, qrcode, random
from datetime import datetime
from app.config.appConfig import Config

app = Flask(__name__)




@app.route("/qr/add", methods=["POST"])
async def index():
    content = request.json
    headers = request.headers
    status = Config.authorizer.check(headers["Authorization"])
    if status is True :
        date = datetime.now().strftime("%H:%M:%S - %d/%m/%Y")
        transactionId = str(content["razorpay_payment_id"])
        event = str(content["membersData"]["event"])
        TeamName = str(content["membersData"]["team"])
        TeamId = str(content["id"])   



        try:
            for datafix in content["membersData"]["membersData"][0]['nestedMembers']:
                print(datafix)
                content["membersData"]["membersData"].append(datafix)
            del content["membersData"]["membersData"][0]['nestedMembers']
        except:
            pass
        




        for member in content["membersData"]["membersData"]:
            id = str(member["id"])[12:].replace("-", "")
            if str(member["id"]).startswith("Member"):
                id = str(member["id"])[8:].replace("-", "")
                id = int(id) + Config.idList
                Config.idList += 1
                id = str(id)
            
            
            print(id)
            name = str(member["name"])
            course = str(member["course"])
            contact = str(member["contact"])
            email = str(member["email"])

            
            Config.sql.cursor.execute(f'Select * from `tickets` where events = "{event}" and email = "{member["email"]}"')
            result = Config.sql.cursor.fetchall()
           
            if len(result)>0:
                return Response(f"User Already Registered: {result}", status=208)
            tid = str(id)
            data = hashlib.sha1(tid.encode())
            make_qrcode(str(data.hexdigest()))
            hashId = str(data.hexdigest())
            mailcontent = {r"<qr_code>": os.path.join(os.getcwd(), "app", "assets", "qrcodes", hashId +".png")}
            
            template = Config.events[event.strip().lower()]["mailtemplate"] 
            eventDate = Config.events[event.strip().lower()]["eventdate"]
            eventTime = Config.events[event.strip().lower()]["eventtime"]
            eventLocation = Config.events[event.strip().lower()]["eventlocation"]
            rules = Config.events[event.strip().lower()]["rule"]



            Config.logger.log(20, f"User Registered with Transaction id: {transactionId}, Event Name: {event}, Team Name: {TeamName}, Team ID: {TeamId}, Member ID: {id}, Name: {name}, Course: {course}, Contact: {contact}, email: {email}")
            Config.sql.add("tickets", [{"hashid": hashId,"Transaction_ID": transactionId, "Events": event, "Team_Name": TeamName, "Team_id": TeamId,
                                        "id": id, "name": name, "course": course, "contact": contact, "email": email}], createTable=True)
            await Config.mail.send("Ticket Confirmation", "tickets@techrise.club",email, "Ticket Confirmation", template=os.path.join(os.getcwd(), "app", "assets", template),
                             contents=mailcontent,
                             placeholder={"{Name of Attendee}":name, "{date}":eventDate, "{time}": eventTime, "{locations}": eventLocation, "{event}": event, "{ruleLink}": rules})
            Config.sheet.append([date, TeamId, TeamName, event, id, name, course, contact, email])


    else:
        return Response("Invalid Token", status=401)
    return Response("Added successfully", status=200)


def make_qrcode(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=15,
        border=5,)
    qr.add_data(data)
    path = os.path.join(os.getcwd(), "app", "assets", "qrcodes", data+".png")
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    img.save(path)





    


