from flask import Blueprint, request, jsonify
import json
import datetime

#from test_data import annotation_example
from google.cloud import bigtable
from google.cloud.bigtable import row_filters
from google.cloud.bigtable import column_family


#-----API Construction-----#
annotationApi = Blueprint('annotationApi', __name__)

#-----GCP account info-----#
project_id = "annotation-project-351010"
instance_id = "finalproject"
table_id = "uploadtb"

#-----connect to bigtable-----#
client = bigtable.Client(project=project_id, admin=True)
instance = client.instance(instance_id)
table = instance.table(table_id)

#-----Routing Definition-----#
@annotationApi.route('postannotation', methods=['POST'])
def updatedbforannotation():
    
    """
    連接DB, 更新目前的status
    """
    # print(request.data) #可以拿到前端POST
    column_family_id = "annotation".encode()
    # row_key = request.key
    # annotator = request.userID
    # label = request.decision
    row_key = "0#1#0"
    annotator = "user1".encode()
    label = "Positive"
    timestamp = datetime.datetime.utcnow()
    row = table.row(row_key)
    row.set_cell(column_family_id, annotator, label, timestamp)
    row.set_cell(column_family_id, "already_annotated", 1, timestamp)
    row.commit()
    print("Successfully wrote row {}.".format(row_key))
    return "Nothing"


@annotationApi.route('getannotation', methods=['GET'])
def getannotation():
    
    #這邊應該還要再傳入一個user id, 不要拿到自己上傳的資料
    """
    連接DB, 得到新的一筆data
    """
    import random
    row_filter = row_filters.CellsColumnLimitFilter(1)
    #這裡應該要隨機產生某個使用者的某個DATASET,但是是要去USER表隨機撈嗎?,有被加上標籤的是不是不能出現在這?
    key = "0#1#1"
    # partial_rows = table.read_rows(filter_=row_filter)
    # for row in partial_rows:
    row = table.read_row(key, row_filter)
    print(row.row_key.decode("utf-8"))        
    cell = row.cells["text"]["text".encode()][0]
    print(cell.value.decode("utf-8"))
    sentence=cell.value.decode("utf-8")
    return {"data": sentence,"key":key}
    # import random
    # data = annotation_example[random.randint(0, 2)]
    # return data