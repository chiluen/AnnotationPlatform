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
    if row_key is None:
        return 'Nothing'
    row_old = table.row(row_key)
    row_old.set_cell("annotation", "already_annotated", str(1), timestamp)
    row_old.commit()

    # TODO: pass by requests
    label = request_data['decision']
    timestamp = datetime.utcnow()
    
    uploader, tag, status, sentence_hash = row_key.split("#")
    # prepare input
    row_key_write = f'{uploader}#{tag}#already_annotate#{annotator}#{label}#{sentence_hash}'
    row = table.row(row_key_write)
    row.set_cell(column_family_id, 'label', label, timestamp)
    row.commit()
    # ------------------------------- new code ------------------ #
    update_metadata(uploader, 'already_annotated_by', 1)
    update_metadata('overall', f'num_of_{label}', 1)
    update_metadata('overall', 'num_of_annotated', 1)
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
    condition_annotate = row_filters.RowFilterChain(
        filters=[
            row_filters.RowKeyRegexFilter(f'^(?:$|[^{annotator}]).*$'.encode()),
            row_filters.RowKeyRegexFilter(f'^.+#not_annotate#.+$'.encode()),
            row_filters.ColumnQualifierRegexFilter(f'already_annotated'.encode()),
            row_filters.ValueRegexFilter('0'.encode()),
            row_filters.RowSampleFilter(0.5),
        ]
    )
    
    candidates = table.read_rows(filter_=condition_annotate)
    candidate_row_keys = [r.row_key.decode() for r in candidates]
    print('look here')
    print(candidate_row_keys)
    sentences = [table.read_row(k).cells["text"][b"text"][0].value.decode() for k in candidate_row_keys]
    pairs = [(k, v) for k, v in zip(candidate_row_keys, sentences)]

    try:
        selected = random.choice(pairs)
        key, sentence = selected[0], selected[1]
        output = {"data": sentence, "remain": len(sentences), "key": key}
    except IndexError:
        output = {
            "data": "Well Done! That's enough for today!",
            "remain": 0,
            "key": None
        }

    return output
