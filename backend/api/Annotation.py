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

    timestamp = datetime.utcnow()
    # capture request
    request_data = json.loads(request.data.decode())
    annotator = request.args['user']
    print('data received in postannotation')
    print(request_data)
    row_key = request_data['key']
    print('old', row_key)
    if row_key is None:
        return 'Nothing'
    else:
        print(row_key)
        row_old = table.direct_row(row_key)
        # prevent to be retrieved at next getannotation
        row_old.set_cell("annotation", "already_annotated", str(1), timestamp)
        row_old.set_cell('annotation', 'already_reviewed', str(0), timestamp)
        row_old.commit()

        uploader, tag, status, sentence_hash = row_key.split("#")
        
        label = request_data['decision'] 
        # prepare input
        row_key_write = f'{uploader}#{tag}#already_annotate#{annotator}#{label}#{sentence_hash}'
        row = table.direct_row(row_key_write)
        row.set_cell('annotation', 'label', label, timestamp)
        row.commit()

        row_old.set_cell("annotation", "label", label, timestamp)
        row_old.commit()

        # ------------------------------- new code ------------------ #
        # update metadata, the value use integer
        update_metadata(uploader, 'already_annotated_by', 1)
        update_metadata(annotator, 'already_annotate', 1)
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
    '''
    condition_annotate = row_filters.RowFilterChain(
        filters=[
            row_filters.RowKeyRegexFilter(f'^(?:$|[^{annotator}]).*$'.encode()),
            row_filters.RowKeyRegexFilter(f'^.+?#not_annotate#.+$'.encode()),
            row_filters.FamilyNameRegexFilter('annotation'),
            row_filters.ColumnQualifierRegexFilter(f'already_annotated'.encode()),
            row_filters.CellsColumnLimitFilter(1),
            row_filters.ValueRegexFilter('0'.encode()),
            row_filters.RowSampleFilter(0.05),
            # TODO: to make it scalable: set a lower probability
        ]
    )
    '''
    # think: save a tmp file locally?
    condition_annotate = row_filters.RowKeyRegexFilter(f'^test#.+?#not_annotate#.+$')
    candidates = table.read_rows(filter_=condition_annotate)
    candidate_row_keys = [r.row_key.decode() for r in candidates]
    print('look here')
    
    sentences = [table.read_row(k).cells["text"][b"text"][0].value.decode() for k in candidate_row_keys]
    pairs = [(k, v) for k, v in zip(candidate_row_keys, sentences)]
    print(pairs)
    
    auth_table = get_bigtable('auth')
    row_meta = auth_table.read_row('overall')
    row_anno = auth_table.read_row(annotator)


    # get reamin number
    # total number = annotated + not_annotated
    #              = (upload by anno + upload by other) + (upload by anno + by other)
    # remain = total - annotate - upload by anno + upload by anno ^ annotate
    total_sentence = int.from_bytes(row_meta.cells['information'][b'total_sentences'][0].value, 'big')
    total_annotate = int.from_bytes(row_meta.cells['information'][b'num_of_annotated'][0].value, 'big')
    num_of_annotator_upload = int.from_bytes(row_anno.cells['information'][b'upload_amount'][0].value, 'big')
    num_of_annotator_upload_annotate = int.from_bytes(row_anno.cells['information'][b'already_annotated_by'][0].value, 'big')

    remain = total_sentence - total_annotate - num_of_annotator_upload + num_of_annotator_upload_annotate 
    
    example_output = {
            "data": "well done! that's enough for today!",
            "remain": 0,
            "key": None
        }
    '''
    if remain <= 0:
        return example_output
    '''

    try:
        selected = random.choice(pairs)
        key, sentence = selected[0], selected[1]
        output = {"data": sentence, "remain": remain, "key": key}
        print('data received in getannotation')
        print(output)
    except IndexError:
        output = {
            "data": "well done! that's enough for today!",
            "remain": 0,
            "key": None
        }

    return output
