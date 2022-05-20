from flask import Blueprint, request
import json

from test_data import user_list


#-----API Construction-----#
registerApi = Blueprint('registerApi', __name__)

#-----Routing Definition-----#
@registerApi.route('register', methods=['POST'])
def register():
    
    """
    連接DB, 更新目前的status
    """
    data = json.loads(request.data.decode('utf-8'))
    print(data)
    print(type(data))
    for d in user_list:
        if d["user"] == data["user"]:
            return {"result": "repeat"}
    return {"result": "Ok"}