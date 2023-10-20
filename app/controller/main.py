from flask import Flask, request, Response
from app.utility.api_auth import auth
from app.configuration.config import Config
from app.utility.permission import permission
import requests,json,os,base64

html_folder = os.path.join(os.getcwd(), 'app', 'html')
app = Flask(__name__)

logger = Config.logger
data_cursor = Config.data_cursor

@app.route('/<version>/<id>/database', methods=['POST'])
def index(version, id):
    response_json = {}
    auth_token = request.headers.get('Bearer')
    is_authenticated = auth.authorize(auth_token)
    id, token = auth_token.split(".")
    id_bytes = base64.encode(id)
    id_decoded = base64.b64decode(id_bytes)
    id_string  = base64.decode(id_decoded)


    if is_authenticated is not True:
        Response.headers.add('WWW-Authenticate',is_authenticated)
        logger.info
        return Response(status=401)
    

    if is_authenticated is True:
        if request.mimetype != 'application/json':
            response_json['error']  = 'Invalid mimetype, expected "application/json"'
            return  Response(data = response_json, status=415)
        
        recieved_json = request.json
        request_product = recieved_json['request-product']
        if request_product == "read" or request_product == "write":
            has_permission = permission.check_permission(recieved_json)
        if has_permission is not True:
            response_json["Permission Error"] = f"{has_permission}"
            return Response(data = response_json, status=403)
        if request_product == "read":
            data = data_cursor.read(recieved_json['content'])
        if request_product == "write":
            data = data_cursor.write(recieved_json['content'])
        response_json['content'] = data
        return Response(data = response_json, status=200)
        


        
        
    
        
        
    