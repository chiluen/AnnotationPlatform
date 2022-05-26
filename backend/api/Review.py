from flask import Blueprint, request
import json
import datetime

# from test_data import review_example
from google.cloud import bigtable
from google.cloud.bigtable import row_filters
from google.cloud.bigtable import column_family

#-----API Construction-----#
reviewApi = Blueprint('reviewApi', __name__)

#-----GCP account info-----#
project_id = "annotation-project-351010"
instance_id = "finalproject"
table_id = "uploadtb"

#-----connect to bigtable-----#
client = bigtable.Client(project=project_id, admin=True)
instance = client.instance(instance_id)
table = instance.table(table_id)

#-----Routing Definition-----#
@reviewApi.route('postreview', methods=['POST'])
def updatedbforreview():
    
    """
    連接DB, 更新目前的status
    """
    # print(request.data) #可以拿到前端POST
    column_family_id = "validation".encode()
    # row_key = request.key
    # annotator = request.userID
    # score = request.rank
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
    import random
    row_filter = row_filters.CellsColumnLimitFilter(1)
    key = "0#1#0"
    # partial_rows = table.read_rows(filter_=row_filter)
    # for row in partial_rows:
    row = table.read_row(key, row_filter)
    print(row.row_key.decode("utf-8"))        
    cell1 = row.cells["text"]["text".encode()][0]
    anno_list = list()
    for i in range(0, len(list(row.cells["annotation"]))):
        anno_name = bytes.decode(list(row.cells["annotation"])[i])
        if anno_name != "already_annotated":
            anno_list.append(anno_name)
            print(anno_name)    
    cell2 = row.cells["annotation"][anno_list[len(anno_list)-1].encode()][0]
    # print(type(list(row.cells["annotation"])[0]))
    # print(list(row.cells["annotation"])[0])
    # print(type(bytes.decode(list(row.cells["annotation"])[0])))
    # print(bytes.decode(list(row.cells["annotation"])[0]))
    
    # cell2 = row.cells["annotation"][(list(row.cells["annotation"])[0])][0]
    print(cell1.value.decode("utf-8"))
    print(cell2.value.decode("utf-8"))
    sentence=cell1.value.decode("utf-8")
    label=cell2.value.decode("utf-8")
    return {"result": sentence,"key":key,"decision":label,"annotator":anno_list[len(anno_list)-1]}
    # import random
    # data = review_example[random.randint(0, 2)]
    # return data