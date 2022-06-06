import json
import random
from datetime import datetime

from flask import Blueprint, request, jsonify
#from test_data import annotation_example
from google.cloud import bigtable
from google.cloud.bigtable import row_filters
from google.cloud.bigtable import column_family

from constant import *
from api.bigtable import get_bigtable, update_metadata

#-----API Construction-----#
annotationApi = Blueprint('annotationApi', __name__)


#-----Routing Definition-----#
@annotationApi.route('postannotation', methods=['POST'])
def updatedbforannotation():
    
    """
    連接DB, 更新目前的status
    """
    table = get_bigtable('annotation')
    column_family_id = "annotation".encode()

    # capture request
    request_data = json.loads(request.data.decode())
    annotator = request.args['user']
    row_key = request_data['key']

    # TODO: pass by requests
    label = request_data['decision']
    timestamp = datetime.utcnow()
    
    uploader, tag, status, sentence_hash = row_key.split("#")
    # prepare input
    row_key_write = f'{uploader}#{tag}#already_annotate#{annotator}#{label}#{sentence_hash}'
    row = table.row(row_key_write)
    row.set_cell(column_family_id, 'label', label, timestamp)
    row.set_cell(column_family_id, "already_annotated", str(1), timestamp)
    row.commit()
    # ------------------------------- new code ------------------ #
    update_metadata(uploader, 'already_annotated_by', 1)
    # ---------------------- new code ned ----------------------- #


    return "Nothing"


@annotationApi.route('getannotation', methods=['GET'])
def getannotation():
    
    #這邊應該還要再傳入一個user id, 不要拿到自己上傳的資料
    """
    連接DB, 得到新的一筆data
    """
    #annotator = 'yus' # random.choice(['yus', 'leo'])
    # each time user get in gets a bunch of sentences, which is slow

    annotator = request.args['user']
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
    # TODO: will O(N) influence
    # query in multiple time is slow

    sentences = [(r.row_key.decode(), r.cells["text"]["text".encode()][0].value.decode()) for r in rows_data]
    sentences_not_select = set([r.row_key.decode().split('#')[-1] for r in rows_data_not_selected])
    sentences = [s for s in sentences if s[0].split('#')[-1] not in sentences_not_select]
    try:
        selected = random.choice(sentences)
        key, sentence = selected[0], selected[1]
        output = {"data": sentence, "remain": len(sentences), "key": key}
    except IndexError:
        output = {
            "data": "Well Done! That's enough for today!",
            "remain": 0,
            "key": None
        }

    return output
