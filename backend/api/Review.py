import random
from flask import Blueprint, request
import json
from datetime import datetime

# from test_data import review_example
from google.cloud import bigtable
from google.cloud.bigtable import row_filters
from google.cloud.bigtable import column_family

from api.bigtable import get_bigtable, update_metadata

#-----API Construction-----#
reviewApi = Blueprint('reviewApi', __name__)

#-----Routing Definition-----#
@reviewApi.route('postreview', methods=['POST'])
def updatedbforreview():
    
    """
    連接DB, 更新目前的status
    """

    timestamp = datetime.utcnow()
    request_data = json.loads(request.data.decode())
    print("data get at postreview")
    print(request_data) #可以拿到前端POST
    table = get_bigtable('annotation') 
    reviewer = request.args['user']
    
    score = request_data['decision']
    row_key = request_data['key']
    if row_key is None:
        return "Nothing"
    
    uploader, tag, status, annotator, label, hash_sent = row_key.split('#')
    
    row_key_text = f'{uploader}#{tag}#not_annotate#{hash_sent}'
    row_old = table.direct_row(row_key_text)
    row_old.set_cell("review", "already_reviewed", str(1), timestamp)
    row_old.commit()
    
    # write score to DB
    row_key_write = f'{uploader}#{tag}#already_review#{annotator}#{label}#{reviewer}#{score}#{hash_sent}'
    row = table.direct_row(row_key_write)
    row.set_cell('review', 'score', str(score), timestamp)
    # row.set_cell('review', 'already_reviewed', str(1), timestamp)
    row.commit()

    update_metadata(uploader, 'already_reviewed_by', 1)
    update_metadata(reviewer, 'already_review', 1)
    update_metadata('overall', 'num_of_reviewed', 1)

    print("Successfully wrote row {}.".format(row_key_write))
    return "Nothing"


def get_text_row_key(annotation_row_key):
    uploader, tag, status, annotator, label, hash_sent = annotation_row_key.split('#')
    text_row_key = f'{uploader}#{tag}#not_annotate#{hash_sent}'
    return text_row_key

@reviewApi.route('getreview', methods=['GET'])
def getreview():
    
    #這邊應該還要再傳入一個user id, 不要拿到自己上傳的資料
    """
    連接DB, 得到新的一筆data
    """
    #用新的會出事,可惡時間出錯了嗚嗚
    # reviwer should not be annotator or uploader
    reviewer = request.args['user']
    table = get_bigtable('annotation')
    condition_review = row_filters.RowFilterChain(
        filters=[
            row_filters.RowKeyRegexFilter(f'^(?:$|[^{reviewer}]).*$'.encode()),
            row_filters.RowKeyRegexFilter(f'^.+?#not_annotate#.+$'.encode()),
            row_filters.ColumnQualifierRegexFilter(f'already_reviewed'.encode()),
            row_filters.CellsColumnLimitFilter(1),
            row_filters.ValueRegexFilter('0'.encode()),
            row_filters.RowSampleFilter(0.99),
        ]
    )
    
    candidates = table.read_rows(filter_=condition_review)
    candidate_row_keys = [r.row_key.decode() for r in candidates]
    print('look here')
    print(candidate_row_keys)
    sentences = [table.read_row(k).cells["text"][b"text"][0].value.decode() for k in candidate_row_keys]
    pairs = [(k, v) for k, v in zip(candidate_row_keys, sentences)]
    
    auth_table = get_bigtable('auth')
    row_meta = auth_table.read_row('overall')
    row_anno = auth_table.read_row(reviewer)
    
    total_annotate = int.from_bytes(row_meta.cells['information'][b'num_of_annotated'][0].value, 'big')
    total_review = int.from_bytes(row_meta.cells['information'][b'num_of_reviewed'][0].value, 'big')
    num_of_reviewer_upload = int.from_bytes(row_anno.cells['information'][b'upload_amount'][0].value, 'big')
    num_of_reviewer_annotate = int.from_bytes(row_anno.cells['information'][b'already_annotate'][0].value, 'big')
    num_of_reviewer_review = int.from_bytes(row_anno.cells['information'][b'already_review'][0].value, 'big')

    remain = total_annotate - num_of_reviewer_upload - num_of_reviewer_annotate - num_of_reviewer_review
    if remain <= 0:
        return {
            "remain": 0,
            "data": 'Well Done! There is no more data to review.',
            "classification": "Positive",
            "key": None
        }
 
    try:
        selected = random.choice(pairs)
        row_key, sentence = selected[0], selected[1]


        label = table.read_row(row_key).cells['annotation'][b'label'][0].value.decode()

        uploader, tag, status, hash_sent = row_key.split('#')
        get_annotator_filter = row_filters.RowKeyRegexFilter(f'{uploader}#{tag}#already_annotate#.+?#.+?#{hash_sent}'.encode())
        row_annotate = table.read_rows(filter_=get_annotator_filter)
        row_annotate_key = [r.row_key.decode() for r in row_annotate]
        assert len(row_annotate_key) == 1
    
        output = {
            "remain": remain , 
            "data": sentence, 
            "classification": label,
            "key": row_annotate_key[0]
        }
    except IndexError:
        output = {
            "remain": 0,
            "data": 'Well Done! There is no more data to review.',
            "classification": "Positive",
            "key": None
        }
    print('data return at getannotation')
    print(output)
    return output
