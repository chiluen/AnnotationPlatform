from flask import Blueprint, request
import json

from test_data import user_list


#-----API Construction-----#
signinApi = Blueprint('signinApi', __name__)

#-----Routing Definition-----#
@signinApi.route('signinresult', methods=['GET'])
def varifysignin():
    
    """
    連接DB, 確認這個人是否有在DB之中
    """
    
    for d in user_list:
        if d["user"] == request.args["user"] and d["password"] == request.args["password"]:
            return {"result": True}
    return {"result": False}
    







