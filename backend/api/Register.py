from flask import Blueprint, request
import json
from datetime import datetime

from api.bigtable import get_bigtable
from google.cloud.bigtable import row_filters
from test_data import user_list

from constant import *


#-----API Construction-----#
registerApi = Blueprint('registerApi', __name__)

#-----Routing Definition-----#
@registerApi.route('register', methods=['POST'])
def register():   
    """  
    連接DB, 更新目前的status
    """
    data = json.loads(request.data.decode('utf-8'))
    table = get_bigtable('auth')

    # "already_annotated" will inject the bigtable cell, thus prohibit
    if data["user"] in PROHIBIT_NAMES or '#' in data["user"]:
        return {"result": "prohibited username"}

    test_row = table.read_row(data['user'])
    if test_row:
        return {"result": "repeat"}
    else:
        timestamp = datetime.utcnow()
        row_key = data["user"]
        row = table.direct_row(row_key)
        row.set_cell('information', 'password', data['password'], timestamp)
        row.set_cell('information', 'upload_amount', 0, timestamp)
        row.set_cell('information', 'already_annotated_by', 0, timestamp)
        row.set_cell('information', 'already_reviewed_by', 0, timestamp)
        row.set_cell('information', 'already_review', 0, timestamp)
        row.commit()
        return {"result": "Ok"}
