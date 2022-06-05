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
    user = request.args['user']
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
    user = request.args['user'] #TODO: no such TOKEN
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
    user = request.args['user']
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
    avg_lens = sum([len(s) for s in sentences]) / len(sentences)
    pos_amount = sum([1 for i in positive_rows])

    dbstat_data = dict()
    dbstat_data['total_data'] = len(sentences) 
    dbstat_data['positive_rate'] = pos_amount / len(sentences)
    dbstat_data['avg_wors'] = avg_lens

    return dbstat_data


@mainpageApi.route('pieinfo', methods=['GET'])
def returnpieinfo():

    """
    連接DB, 拿到pie graph 所需資料
    """
    user = request.args['user']
    result = []
    for i in range(6):
        positive_regtext = f'^{user}#.+?#already_review#.+?#.+?#.+?#{i}#.*$'.encode()
        positive_rows = table.read_rows(filter_=RowKeyRegexFilter(positive_regtext))
        result.append(sum([1 for a in positive_rows]))

    keys = ['zero_star', 'one_star', 'two_star', 'three_star','four_star','five_star']

    pieinfo_data = dict()
    for k, v in zip(keys, result):
        pieinfo_data[k] = v

    return pieinfo_data


@mainpageApi.route('tableinfo', methods=['GET'])
def returntableinfo():

    """
    連接DB, 拿到pie graph 所需資料
    """
    # copy function from DB.py

    return json.dumps(tableinfo_data)
