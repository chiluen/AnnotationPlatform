from flask import Blueprint, request, session
import json, csv
from datetime import datetime

from api.bigtable import get_bigtable
from google.cloud.bigtable import row_filters


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
    # TODO: check if we have this 2 columns
    task_name = request.form['task_name']
    # description = request.form['description']
    uploader = session.get("user")
    timestamp = datetime.utcnow()

    corpus = data.readlines()
    for i, sentence in enumerate(corpus):
        row_key = f'{uploader}#{task_name}#{i}'
        row = table.direct_row(row_key)
        row.set_cell('text', 'text', sentence, timestamp)
        row.set_cell('annotation', 'already_annotated', 0, timestamp)

        row.commit()
    
    return "Nothing"
