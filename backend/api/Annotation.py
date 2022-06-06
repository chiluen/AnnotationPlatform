import json
import random
import datetime

from flask import Blueprint, request, jsonify
#from test_data import annotation_example
from google.cloud import bigtable
from google.cloud.bigtable import row_filters
from google.cloud.bigtable import column_family

from constant import *
from api.bigtable import get_bigtable

#-----API Construction-----#
annotationApi = Blueprint('annotationApi', __name__)


#-----Routing Definition-----#
@annotationApi.route('postannotation', methods=['POST'])
def updatedbforannotation():
    
    """
    連接DB, 更新目前的status
    """
    # print(request.data) #可以拿到�
    table = get_bigtable('annotation')
    column_family_id = "annotation".encode()

    # capture request
    # annotator = request.args['user']
    request_data = json.loads(request.data.decode())
    annotator = "leo" # request.args['user']
    row_key = b'yus#finance#not_annotate#-1407824835996527616'.decode()
    # TODO: pass by requests
    label = request_data['decision']
    timestamp = datetime.datetime.utcnow()
    
    uploader, tag, status, sentence_hash = row_key.split("#")

    # prepare input
    row_key_write = f'{uploader}#{tag}#already_annotate#{annotator}#{label}#{sentence_hash}'
    row = table.row(row_key_write)
    row.set_cell(column_family_id, 'label', label, timestamp)
    row.set_cell(column_family_id, "already_annotated", str(1), timestamp)
    row.commit()

    return "Nothing"


@annotationApi.route('getannotation', methods=['GET'])
def getannotation():
    
    #這邊應該還要再傳入一個user id, 不要拿到自己上傳的資料
    """
    連接DB, 得到新的一筆data
    """
    annotator = 'leo' # random.choice(['yus', 'leo'])
    # annotator = request.args['user']
    table = get_bigtable('annotation')

    # dont get annotator's query
    # TODO: it is not efficient to query all ~user data at each time
    # bigtable has random row filter, using that will be faster 
    condition_not_annotate = row_filters.RowFilterChain(
        filters=[
            row_filters.RowKeyRegexFilter(f'^(?:$|[^{annotator}]).*$'.encode()),
            row_filters.RowKeyRegexFilter(f'^.+#not_annotate#.+$'.encode()),
        ]
    )

    rows_data = table.read_rows(filter_=condition_not_annotate)
    
    condition_annotate = row_filters.RowFilterChain(
        filters=[
            row_filters.RowKeyRegexFilter(f'^(?:$|[^{annotator}]).*$'.encode()),
            row_filters.RowKeyRegexFilter(f'^.+#already_annotate#.+$'.encode()),
        ]
    )

    rows_data_not_selected = table.read_rows(filter_=condition_annotate)
    '''
    # old version # select by value is not suitable for BT
    condition = row_filters.RowFilterChain(
        filters=[
            row_filters.RowKeyRegexFilter(f'^(?:$|[^{annotator}]).*$'.encode()),
            row_filters.ColumnQualifierRegexFilter('already_annotated'),
            row_filters.CellsColumnLimitFilter(1), # only get the most recent cell
            row_filters.ValueRegexFilter('^0$'.encode()),
        ]
    )

    rows_data = table.read_rows(
        filter_=row_filters.ConditionalRowFilter(
            base_filter=condition,
            true_filter=row_filters.PassAllFilter(True),
            false_filter=row_filters.BlockAllFilter(True),
        )
    ) # RowData not Row
    '''
    # len(rows_data.rows) returns 0
    # TODO: will O(N) influence

    sentences = [(r.row_key.decode(), r.cells["text"]["text".encode()][0].value.decode()) for r in rows_data]
    sentences_not_select = set([r.row_key.decode().split('#')[-1] for r in rows_data_not_selected])
    print(sentences_not_select)
    sentences = [s for s in sentences if s[0].split('#')[-1] not in sentences_not_select]
    print('remain', len(sentences)) 
    print(sentences)
    selected = random.choice(sentences)
    key, sentence = selected[0], selected[1]
    # TODO: return one more key for recording
    print(key)
    return {"data": sentence, "remain": len(sentences), "key": key}
