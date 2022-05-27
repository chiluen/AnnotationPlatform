from flask import Blueprint, request
import json

#from test_data import user_list, finish_data, dbstat_data, pieinfo_data, tableinfo_data #test data
from google.cloud import bigtable
from google.cloud.bigtable import row_filters
from google.cloud.bigtable import column_family
from google.cloud.bigtable.row_set import RowSet

#-----API Construction-----#
mainpageApi = Blueprint('mainpageApi', __name__)

#-----GCP account info-----#
project_id = "annotation-project-351010"
instance_id = "finalproject"
table_id = "uploadtb"

#-----connect to bigtable-----#
client = bigtable.Client(project=project_id, admin=True)
instance = client.instance(instance_id)
table = instance.table(table_id)

#-----Routing Definition-----#
@mainpageApi.route('userprofile', methods=['GET'])
def returnUserprofile():
    user = request.args['user']
    
    """
    連接DB, 拿到user information
    """

    # for d in user_list:
    #     if d["user"] == user:
    #         print(d)
    #         return d


@mainpageApi.route('finishinfo', methods=['GET'])
def returnFinishinfo():

    """
    連接DB, 拿到Finish info
    """
    row_filter = row_filters.CellsColumnLimitFilter(1)
    row_set = RowSet()
    #不知道怎麼抓完成的有那些(沒有該column卻呼叫的話會出現keyerror,而不是null/false之類的), 也不知道怎麼數最快QQ, 如果沒有分TASK可能會比較好算
    #user = request.user
    #row_set.add_row_range_with_prefix(user+"#")
    row_set.add_row_range_with_prefix("0#")
    rows = table.read_rows(row_set=row_set)
    finish = 0
    unfinish = 0
    # task_set = RowSet()
    for row in rows:
        if (~(row.cells["annotation"][(bytes.decode(list(row.cells["annotation"])[0])).encode()][0])):
            unfinish +=1
        else:
            finish += 1
    #     task_name = row.row_key.decode("utf-8").split('#')[1] 
    #     if (task_name not in task_set):
    #         task_set.add(row)
    # for task in task_set:
        # print(bytes.decode(row.row_key.decode("utf-8")))
        # print(type(row.row_key))
        
    return {"finish": finish,"unfinish": unfinish}
    # return finish_data

@mainpageApi.route('dbstat', methods=['GET'])
def returnDBstatistic():

    """
    連接DB, 拿到DB的統計資料
    """

    # return dbstat_data


@mainpageApi.route('pieinfo', methods=['GET'])
def returnpieinfo():

    """
    連接DB, 拿到pie graph 所需資料
    """

    #return pieinfo_data


@mainpageApi.route('tableinfo', methods=['GET'])
def returntableinfo():

    """
    連接DB, 拿到pie graph 所需資料
    """

    #return json.dumps(tableinfo_data)