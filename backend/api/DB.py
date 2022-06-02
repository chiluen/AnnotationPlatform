from flask import Blueprint, request, session
import json
from test_data import tableinfo_data
from datetime import datetime

from api.bigtable import get_bigtable
from google.cloud.bigtable import row_filters
from google.cloud.bigtable.row_set import RowSet



#-----API Construction-----#
dbApi = Blueprint('dbApi', __name__)


#-----Routing Definition-----#
@dbApi.route('tableinfo', methods=['GET'])
def returntableinfo():
    """
    連接DB, 拿到table information (全部)
    [{data, status, rank}]
    """
    table = get_bigtable("annotation")
    prefix = 'leo' + '#'
    # prefix = request.args['user'] + '#'
    end_key = prefix[:-1] + chr(ord(prefix[-1]) + 1)
    
    row_set = RowSet()
    row_set.add_row_range_from_keys(prefix.encode("utf-8"), end_key.encode("utf-8"))

    rows = table.read_rows(row_set=row_set)
    tableinfo_data = []
    for r in rows:
        sentence = r.cells['text'][b'text']
        status = r.cells['annotation'][b'label'] if bool(r.cells['annotation'][b'already_annotated']) else 'Not Graded'
        rank = r.cells['validation'][1] if r.cells['annotation']['already_annotated'] else 0
        
        tableinfo_data.append({'data': sentence, 'status': status, 'rank': rank})

    return json.dumps(tableinfo_data)


# TODO: no post?
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
