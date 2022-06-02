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
    # print(request.data) #可以拿到前端POST
    column_family_id = "validation".encode()
    row_key = "0#1#0"
    annotator = "user0".encode()
    score = 3
    timestamp = datetime.datetime.utcnow()
    row = table.row(row_key)
    row.set_cell(column_family_id, annotator, score, timestamp)
    row.commit()
    print("Successfully wrote row {}.".format(row_key))
    return "Nothing"


@reviewApi.route('getreview', methods=['GET'])
def getreview():
    
    #這邊應該還要再傳入一個user id, 不要拿到自己上傳的資料
    """
    連接DB, 得到新的一筆data
    """
    #用新的會出事,可惡時間出錯了嗚嗚
    # reviwer should not be annotator or uploader
    reviewer = 'cai' # request.args['user']
    table = get_bigtable('annotation')

    condition_not_uploader = row_filters.RowFilterChain(
        filters=[
            row_filters.RowKeyRegexFilter(f'^(?:$|[^{reviewer}]).*$'.encode()),
            row_filters.ColumnQualifierRegexFilter('already_annotated'),
            row_filters.CellsColumnLimitFilter(1),
            row_filters.ValueRegexFilter('^1$'.encode()),
        ]    
    )
    condition_not_annotator = row_filters.RowFilterChain(
        filters=[
            row_filters.ColumnQualifier('annotator'),
            row_filters.CellsColumnLimitFilter(1),
            row_filters.ValueRegexFilter(),
        ]
    )

    
    return {"result": sentence,"key":key,"decision":label,"annotator":anno_list[len(anno_list)-1]}
