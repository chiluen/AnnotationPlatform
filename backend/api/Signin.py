from flask import Blueprint, request
import json

from test_data import user_list
from api.bigtable import get_bigtable

#-----API Construction-----#
signinApi = Blueprint('signinApi', __name__)

#-----Routing Definition-----#
@signinApi.route('signinresult', methods=['GET'])
def varifysignin():
    
    """
    連接DB, 確認這個人是否有在DB之中
    """
    table = get_bigtable('auth')
    row_filter = row_filters.CellsColumnLimitFilter(1)
    rows = table.read_rows(filter_=row_filter)
    user_list = [{'user': r.row_key, 'password': r.cells['information']['password'][0]} for r in rows]
    
    for d in user_list:
        if d["user"] == request.args["user"] and d["password"] == request.args["password"]:
            return {"result": True}
    return {"result": False}
    







