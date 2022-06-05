import random
from flask import Blueprint, request
import json
import datetime

# from test_data import review_example
from google.cloud import bigtable
from google.cloud.bigtable import row_filters
from google.cloud.bigtable import column_family

from api.bigtable import get_bigtable

#-----API Construction-----#
reviewApi = Blueprint('reviewApi', __name__)

#-----Routing Definition-----#
@reviewApi.route('postreview', methods=['POST'])
def updatedbforreview():
    
    """
    連接DB, 更新目前的status
    """

    request_data = json.loads(request.data.decode())
    print("ddddd")
    print(request.data) #可以拿到前端POST
    table = get_bigtable('annotation') 
    reviewer = request.args['user']
    
    score = request_data['decision']
    row_key = request_data['key']

    uploader, tag, status, annotator, label, hash_sent = row_key.split('#')
    row_key_write = f'{uploader}#{tag}#already_review#{annotator}#{label}#{reviewer}#{score}#{hash_sent}'
    timestamp = datetime.datetime.utcnow()
    row = table.row(row_key_write)
    row.set_cell('review', 'score', str(score), timestamp)
    row.set_cell('review', 'already_review', str(1), timestamp)
    row.commit()
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
   
    # get those annotated
    # the re2 regex did not support negate lookaround, I'm not sure what is here
    # but small data testing looks fine (won't retrieve uploader and annotator's data)
    regex_text_candidate = f'^(?:$|[^{reviewer}]).+?#.+?#already_annotate#(?:$|[^{reviewer}]).+?#.*$'
    condition_candidate = row_filters.RowKeyRegexFilter(regex_text_candidate.encode())
    rows_data = table.read_rows(filter_=condition_candidate)
    
    # get those have been reviewed
    regex_text_not_candidate = f'^(?:$|[^{reviewer}]).+?#.+?#already_review#(?:|[^{reviewer}]).+?#.*$'
    condition_not_candidate = row_filters.RowKeyRegexFilter(regex_text_not_candidate.encode())
    rows_data_not_candidate = table.read_rows(filter_=condition_not_candidate)
    not_candidates = set([r.row_key.decode().split('#')[-1] for r in rows_data_not_candidate])

    sentences = [r.row_key.decode() for r in rows_data]
    sentences = [s for s in sentences if s.split('#')[-1] not in not_candidates]

    texts = [table.read_row(get_text_row_key(s)).cells["text"][b"text"][0].value.decode() for s in sentences]

    pairs = [(i, s) for i, s in zip(sentences, texts)]

    selected = random.choice(pairs)
    row_key, sentence = selected[0], selected[1]
    number_of_remain = len(pairs)
    label = table.read_row(row_key).cells['annotation'][b'label'][0].value.decode()
    

    output = {
        "remain": number_of_remain , 
        "data": sentence, 
        "classification": label,
        "key": row_key
    } 
    
    return output

# return {"result": sentence,"key":key,"decision":label,"annotator":anno_list[len(anno_list)-1]}
