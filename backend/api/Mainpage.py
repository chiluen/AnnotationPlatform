from flask import Blueprint, request, session
import json
from api.bigtable import get_bigtable, update_metadata
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

    # yus#Technology#not_annotate#-5526783738657794297
    annotated_by_regtext = f'^{user}#.+?#already_annotate#.+$'.encode()
    annotated_by_data_rows = table.read_rows(filter_=RowKeyRegexFilter(annotated_by_regtext))   

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

    d = {}
    d["user"] = user
    auth_table = get_bigtable('auth')
    password = auth_table.read_row(user).cells["information"][b"password"][0].value.decode() 
    d["password"] = password
    
    auth_table = get_bigtable('auth')
    try:
        upload_amount = auth_table.read_row(user).cells["information"][b"upload_amount"][0].value 
        d["numberOfUpload"] = int.from_bytes(upload_amount, 'big')
    except KeyError:
        d["numberOfUpload"] = 0
    
    try:
        reviewed_by_amount = auth_table.read_row(user).cells["information"][b"already_reviewed_by"][0].value.decode() 
        d["numberOfReview"] = reviewed_by_amount
    except KeyError:
        d["numberOfReview"] = 0
   
    reviewed_by_regtext = f'^.+?#.+?#already_review#{user}#.+?#.+?#.+?#.+$'.encode()
    reviewed_by_data_rows = auth_table.read_rows(filter_=RowKeyRegexFilter(reviewed_by_regtext))
    d["reviewRank"] = sum([1 for i in reviewed_by_data_rows])

    print(d)
    return d

@mainpageApi.route('finishinfo', methods=['GET'])
def returnFinishinfo():

    """
    連接DB, 拿到Fin
    """
    user = request.args['user'] #TODO: no such TOKEN
    upload_rows, annotate_rows, annotated_by_rows, review_rows, reviewed_by_rows, password = get_user_data_rows(user)
    
    d = {}
    d['finish'] = sum([1 for i in annotated_by_rows])
    d['unfinish'] = sum([1 for i in upload_rows]) - d['finish']
    
    print(d)
    return d

@mainpageApi.route('dbstat', methods=['GET'])
def returnDBstatistic():

    """
    連接DB, 拿到DB的統計資料
    """
    user = request.args['user']
    table = get_bigtable('annotation')
    auth_table = get_bigtable('auth')

    row_overall = auth_table.read_row('overall')
    total_amount = row_overall.cells['information'][b'total_sentences'][0].value
    total_amount = int.from_bytes(total_amount, 'big')
    pos_amount = row_overall.cells['information'][b'num_of_Positive'][0].value
    pos_amount = int.from_bytes(pos_amount, 'big')
    total_token = int.from_bytes(row_overall.cells['information'][b'num_of_tokens'][0].value, 'big')
    avg_lens = total_token / total_amount if total_amount > 0 else 0
    positive_ratio = pos_amount / total_amount if total_amount > 0 else 0


    dbstat_data = dict()
    dbstat_data['total_data'] = total_amount
    dbstat_data['positive_rate'] = positive_ratio
    dbstat_data['avg_words'] = avg_lens

    return dbstat_data


@mainpageApi.route('pieinfo', methods=['GET'])
def returnpieinfo():

    """
    連接DB, 拿到pie graph 所需資料
    """
    user = request.args['user']
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
    user = request.args['user']
    table = get_bigtable('annotation')
    rows = table.read_rows(filter_=RowKeyRegexFilter(f'^{user}#.+$'))

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
        row_dict['tag'] = tag
        row_dict['uploader'] = uploader

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
