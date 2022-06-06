import random
import json, csv
import multiprocessing as mp

from datetime import datetime

from flask import Blueprint, request, session, g

from api.bigtable import get_bigtable
from google.cloud.bigtable import row_filters

from constant import *


def read_data(f):
    rows = csv.reader(f, delimiter='\t')
    data = [r for r in rows]
    return data
    

#-----API Construction-----#
uploadApi = Blueprint('uploadApi', __name__)
# ------------------- new code block -------------------- #
table_anno = get_bigtable('annotation')
def upload_a_sentence(input_tuple):
    uploader, tag, sentence, timestamp = input_tuple[0], input_tuple[1], input_tuple[2], input_tuple[3]
    try:
        row_key = f'{uploader}#{tag}#not_annotate#{hash(sentence)}'
        row = table_anno.direct_row(row_key)
        row.set_cell('text', 'text', sentence, timestamp)
        row.set_cell('annotation', 'already_annotated', str(0), timestamp)

        row.commit()
        return 1
    except UnicodeEncodeError:
        print('UNICODE ERROR:', sentence)
        return 0

# ------------------- new code block enc -------------------- #

#-----Routing Definition-----#
@uploadApi.route('upload', methods=['POST'])
def updatedbforreview():    
    """
    連接DB, 上傳這一個upload file
    """
    table = get_bigtable('annotation')
    data = request.files['file']
    
    # TODO: check if we have this 2 columns; update: add tag
    uploader = request.args['user']
    tag = request.args['category']
    timestamp = datetime.utcnow()
    

    # -------------------------------- new code block ---------------------- #
    num_cpu = mp.cpu_count()
    upload_volume = []
        
    sentences = [(uploader, tag, s.decode('utf-8'), timestamp) for s in data]
    pool = mp.Pool(num_cpu)
    upload_volume = pool.map(upload_a_sentence, sentences)
    upload_volume = sum(upload_volume)

    # update information of auth table
    metadata_table = get_bigtable('metadata')
    row_read = metadata_table.read_row(uploader)
    row_write = metadata_table.direct_row(uploader)
    # print_row(row_read)
    # print(row_read.cells['information'])
    try:
        previous_num = int(row_read.cells['information'][b'upload_amount'][0].value.decode())
        new_num = previous_num + upload_volume
    except KeyError:
        new_num = upload_volume
    
    row_write.set_cell('information', 'upload_amount', str(new_num), timestamp)
    row_write.commit()
    
    # -------------------------------- new code block ends ---------------------- #
    return "Nothing"
