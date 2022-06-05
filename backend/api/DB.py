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
    
    table = get_bigtable('annotation')
    rows = table.read_rows(filter_=row_filters.PassAllFilter(True))


    # TODO: implement O(N) is kinda waste of time
    tableinfo_data, example = {}, {'status': 'Not Graded', 'rank': 0}
    for r in rows:
        row_name = r.row_key.decode()
        row_name_elements = row_name.split('#')
        uploader = row_name_elements[0]
        tag = row_name_elements[1]
        status = row_name_elements[2]
        sentence_hash = row_name_elements[-1]

        row_dict_key = '#'.join([uploader, tag, sentence_hash])
        row_dict = tableinfo_data.get(row_dict_key, example.copy())

        if status == 'not_annotate':
            sentence =  r.cells['text'][b'text'][0].value.decode()
            row_dict['data'] = sentence
        elif status == 'already_annotate':
            row_dict['status'] = r.cells['annotation'][b'label'][0].value.decode()
        elif status == 'already_review':
            rank = r.cells['review'][b'score'][0].value.decode()
            try:
                score = int(rank)
            except ValueError:
                score = 0
            row_dict['rank'] = score

        tableinfo_data[row_dict_key] = row_dict

    tableinfo_data = [i for i in tableinfo_data.values()]

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
