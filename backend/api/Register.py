from flask import Blueprint, request
import json
from datetime import datetime

from api.bigtable import get_bigtable
from google.cloud.bigtable import row_filters
from test_data import user_list


#-----API Construction-----#
registerApi = Blueprint('registerApi', __name__)

#-----Routing Definition-----#
@registerApi.route('register', methods=['POST'])
def register():   
    """  
    連接DB, 更新目前的status
    """
    table = get_bigtable('auth')
    row_filter = row_filters.CellsColumnLimitFilter(1)
    rows = table.read_rows(filter_=row_filter)
    user_list = [{'user': r.row_key, 'password': r.cells['information']['password'][0]} for r in rows]

    data = json.loads(request.data.decode('utf-8'))
    print(data)
    print(type(data))
    for d in user_list:
        if d["user"] == data["user"]:
            return {"result": "repeat"}
    if data["user"] == "already_annotated":
        return {"result": "prohibited username"}
    
    timestamp = datetime.utcnow()
    row_key = data["user"]
    row = table.direct_row(row_key)
    row.set_cell('information', 'password', data['password'], timestamp)
    row.commit()

    return {"result": "Ok"}
