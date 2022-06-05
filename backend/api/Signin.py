from flask import Blueprint, request, session, g
import json

from test_data import user_list
from api.bigtable import get_bigtable
from constant import *

#-----API Construction-----#
signinApi = Blueprint('signinApi', __name__)

#-----Routing Definition-----#
@signinApi.route('signinresult', methods=['GET'])
def varifysignin():
    
    """
    連接DB, 確認這個人是否有在DB之中
    """
    row_key = request.args["user"]
    table = get_bigtable("auth")
    row = table.read_row(row_key)
    # print(row.cells['information'])
    # print(type(row.cells['information'][b'password'][0].value)) # this will be bytes in BT
    if not row:
        return {"result": False}
    elif request.args["password"] == row.cells['information'][b'password'][0].value.decode():
        # session.clear()
        print(request.args['user'])
        session["user"] = request.args["user"]
        return {"result": True}
    return {"result": False}

# this is failed since we are not using the flask env totally
@signinApi.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    g.user = user_id

