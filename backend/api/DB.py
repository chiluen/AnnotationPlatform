from flask import Blueprint, request
import json
from test_data import tableinfo_data


#-----API Construction-----#
dbApi = Blueprint('dbApi', __name__)


#-----Routing Definition-----#
@dbApi.route('tableinfo', methods=['GET'])
def returntableinfo():
    
    """
    連接DB, 拿到table information (全部)
    """
    return json.dumps(tableinfo_data)


@dbApi.route('selecttableinfo', methods=['GET'])
def returnselecttableinfo():
    scope = request.args['scope']
    minstar = request.args['minstar']
    status = request.args['status']
    print(request.args)

    """
    連接DB, 並依據這三個條件對data做篩選
    """
    return json.dumps(tableinfo_data[:5])




