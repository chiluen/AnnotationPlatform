import csv
import functools
from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
)

from upload_app.db import get_db


def read_data(f):
    rows = csv.reader(f, delimiter='\t')
    data = [r for r in rows]
    return data

# TODO: the upload routing should under <user_id>?
# TODO: implement required login decorator
bp = Blueprint('upload', __name__, url_prefix='/upload')

@bp.route('/new', methods=('GET', 'POST'))
def new():
    if request.method == 'POST':
        task_name = request.form['task_name']
        description = request.form['description']
        # TODO: auto generate task ID?
        # TODO: regulate only .csv? .tsv?
        # TODO: regulate annotation task type?

        error = None
        if not task_name:
            error = 'task name is required'
        elif not description:
            error = 'task description is required'
        elif 'file' not in request.files:
            error = 'No file uploaded'

        if error is None:
            # write task name and description into database
            # tear down the file and assign sent_id as row name
            file = request.files['file']
            data = read_data(file)
            # TODO: connenct and write into bigtable
            # TODO: get userID from flask, generate sentenceID
            # TODO: row schema, column_family_id check
            column_family_id = 'text'
            column = 'text'.encode()
            for i, sent in enumerate(data):
                row_key = f'{user_id}#{task_name}#{i}'.encode()
                row = table.direct_row(row_key)
                row.set_cell(
                    column_family_id, 
                    column, 
                    sent, 
                    timestamp=datetime.utcnow()
                )
                rows.append(row)
            table.mutate_rows(rows)
            
            return 'successfully upload page'

        flash(error)

    return 'upload new file page'


