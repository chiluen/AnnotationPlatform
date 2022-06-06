from flask import Blueprint, request, session
import json
from api.bigtable import get_bigtable
from google.cloud.bigtable import row_filters 
from google.cloud.bigtable.row_filters import RowKeyRegexFilter

from test_data import user_list, finish_data, dbstat_data, pieinfo_data, tableinfo_data #test data
from constant import *


#-----API Construction-----#
mainpageApi = Blueprint('mainpageApi', __name__)

def get_user_data_rows(user):
    table = get_bigtable('annotation')
    upload_regtext = f'^{user}#.+?#not_annotate#.*$'.encode()
    upload_data_rows = table.read_rows(filter_=RowKeyRegexFilter(upload_regtext))

    annotate_regtext = f'^.+?#.+?#already_annotate#{user}#.+?#.+$'.encode()
    annotate_data_rows = table.read_rows(filter_=RowKeyRegexFilter(annotate_regtext))

    annotated_by_regtext = f'{user}?#.+?#already_annotate#.+?#.+?#.+$'.encode()
    annotated_by_data_rows = table.read_rows(filter_=RowKeyRegexFilter(annotate_regtext))

    review_regtext = f'^.+?#.+?#already_review#.+?#.+?#{user}#.+?#.+$'.encode()
    review_data_rows = table.read_rows(filter_=RowKeyRegexFilter(review_regtext))

    reviewed_by_regtext = f'^.+?#.+?#already_review#{user}#.+?#.+?#.+?#.+$'.encode()
    reviewed_by_data_rows = table.read_rows(filter_=RowKeyRegexFilter(reviewed_by_regtext))

    auth_table = get_bigtable('auth')
    password = auth_table.read_row(user).cells["information"][b"password"][0].value.decode()
    return upload_data_rows, annotate_data_rows, annotated_by_data_rows, review_data_rows, reviewed_by_data_rows, password


#-----Routing Definition-----#
@mainpageApi.route('userprofile', methods=['GET'])
def returnUserprofile():
    
    """
    連接DB, 拿到user information
    """
    # user = request.args['user']
    user = 'yus'
    upload_data_rows, annotate_data_rows, annotated_by_data_rows, review_data_rows, reviewed_by_data_rows, password = get_user_data_rows(user)

    d = {}
    d["user"] = user
    d["password"] = password
    d["numberOfUpload"] = sum([1 for i in upload_data_rows])
    d["numberOfReview"] = sum([1 for i in review_data_rows])
    d["reviewRank"] = sum([1 for i in reviewed_by_data_rows])

    print(d)
    return d

@mainpageApi.route('finishinfo', methods=['GET'])
def returnFinishinfo():

    """
    連接DB, 拿到Fin
    """
    # user = request.args['user'] #TODO: no such TOKEN
    user = 'yus'
    upload_data_rows, annotate_data_rows, annotated_by_data_rows, review_data_rows, reviewed_by_data_rows, password = get_user_data_rows(user)

    d = {}
    d['finish'] = sum([1 for i in annotated_by_data_rows])
    d['unfinish'] = sum([1 for i in upload_data_rows]) - d['finish']
    
    print(d)
    return d

@mainpageApi.route('dbstat', methods=['GET'])
def returnDBstatistic():

    """
    連接DB, 拿到DB的統計資料
    """
    # user = request.args['user']
    user = 'yus'
    table = get_bigtable('annotation')

    text_regtext = f'^.+?#^.+?#not_annotate#.+$'.encode()
    text_filter = row_filters.RowFilterChain(
        filters=[
            RowKeyRegexFilter(text_regtext),
            row_filters.CellsColumnLimitFilter(1),
            row_filters.FamilyNameRegexFilter(b"text"),
        ]
    )
    text_rows = table.read_rows(filter_=text_filter)

    positive_regtext = f'^.+?#.+?#already_annotate#.+?#Positive#.*$'.encode()
    positive_rows = table.read_rows(filter_=RowKeyRegexFilter(positive_regtext))


    # TODO: get all sentenece from db
    sentences = [r.cells[b'text'][0].values.decode().split() for r in text_rows]
    print(sentences)
    avg_lens = sum([len(s) for s in sentences]) / len(sentences) if len(sentences) > 0 else 0
    pos_amount = sum([1 for i in positive_rows])

    dbstat_data = dict()
    dbstat_data['total_data'] = len(sentences)
    dbstat_data['positive_rate'] = pos_amount / len(sentences) if len(sentences) > 0 else 0
    dbstat_data['avg_wors'] = avg_lens

    return dbstat_data


@mainpageApi.route('pieinfo', methods=['GET'])
def returnpieinfo():

    """
    連接DB, 拿到pie graph 所需資料
    """
    # user = request.args['user']
    user = 'yus'
    table = get_bigtable('annotation')
    result = []
    for i in range(6):
        positive_regtext = f'^{user}#.+?#already_review#.+?#.+?#.+?#{i}#.*$'.encode()
        positive_rows = table.read_rows(filter_=RowKeyRegexFilter(positive_regtext))
        result.append(sum([1 for a in positive_rows]))

    keys = ['zero_star', 'one_star', 'two_star', 'three_star','four_star','five_star']

    pieinfo_data = dict()
    for k, v in zip(keys, result):
        pieinfo_data[k] = v
    print(pieinfo_data)
    return pieinfo_data


@mainpageApi.route('tableinfo', methods=['GET'])
def returntableinfo():

    """
    連接DB, 拿到pie graph 所需資料
    """
    # copy function from DB.py
    user = 'yus'
    table = get_bigtable('annotation')
    rows = table.read_rows(filter_=RowKeyRegexFilter('^{user}#.*$'))

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
    print(tableinfo_data)
    return json.dumps(tableinfo_data)
