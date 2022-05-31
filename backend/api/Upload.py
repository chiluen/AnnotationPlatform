import random
import random
import json, csv
from flask import Blueprint, request, session, g
from datetime import datetime

from api.bigtable import get_bigtable
from google.cloud.bigtable import row_filters

from constant import *


def read_data(f):
    rows = csv.reader(f, delimiter='\t')
    data = [r for r in rows]
    return data
    

#-----API Construction-----#
uploadApi = Blueprint('uploadApi', __name__)

#-----Routing Definition-----#
@uploadApi.route('upload', methods=['POST'])
def updatedbforreview():    
    """
    連接DB, 上傳這一個upload file
    """
    table = get_bigtable('annotation')
    data = request.files['file']
    # TODO: check if we have this 2 columns; update: add tag
    # task_name = request.form['task_name']
    # description = request.form['description']
    # uploader = request.args['user']
    uploader = random.choice(['leo', 'yus'])
    timestamp = datetime.utcnow()
    
    upload_volume = 0
    for i, sentence in enumerate(data):
        sentence = sentence.decode()
        row_key = f'{uploader}#{hash(sentence)}'
        row = table.direct_row(row_key)
        row.set_cell('text', 'text', sentence, timestamp)
        row.set_cell('annotation', 'already_annotated', str(0), timestamp)

        row.commit()
        upload_volume += 1

    # update information of auth table
    auth_table = get_bigtable('auth')
    row_read = auth_table.read_row(uploader)
    row_write = auth_table.direct_row(uploader)
    # print_row(row_read)
    # print(row_read.cells['information'])
    try:
        previous_num = int(row_read.cells['information'][b'upload_amount'][0].value.decode())
        # print(previous_num)
        new_num = previous_num + upload_volume
    except KeyError:
        new_num = upload_volume
    
    # print(new_num)
    row_write.set_cell('information', 'upload_amount', str(new_num), timestamp)
    row_write.commit()
    
    return "Nothing"
