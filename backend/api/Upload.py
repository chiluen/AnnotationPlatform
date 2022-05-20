from flask import Blueprint, request
import json


#-----API Construction-----#
uploadApi = Blueprint('uploadApi', __name__)

#-----Routing Definition-----#
@uploadApi.route('upload', methods=['POST'])
def updatedbforreview():
    
    """
    連接DB, 上傳這一個upload file
    """
    data = request.files['file']
    ccc = data.read()
    print(ccc)
    
    return "Nothing"