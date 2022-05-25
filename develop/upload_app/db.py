import os
import click
from datetime import datetime

from flask import current_app, g
from flask.cli import with_appcontext

from google.cloud import bigtable
from google.cloud.bigtable import (
    column_family,
    row_filters
)

def get_db():
    if 'db' not in g:
        # TODO: figure out how to pass data
        # the project_id, instance_id, table_id should be retrieve from some data
        client = bigtable.Client(project=project_id, admin=True)
        instance = client.instance(instance_id)
        table = instance.table(table_id)

        # TODO
        g.db.row_factory = 'sqlite.row'

    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        # figure out how to close bigtable
        'db.close()'

def init_db():
    db = get_db()
    # TODO: write big table version to execute python
    with current_app.open_resource('schema.py') as f:
        db.executescript(f.read().decode('utf8'))

@click.commnad('init-db')
@with_appcontext  # TODO: not so sure if need this decorator
def init_db_command():
    '''reinitialize and clear previous db'''
    init_db()
    click.echo('intializaed the BigTable')


def init_app(app):
    # call the function when cleaning up after returning the response
    # TODO: not so sure if needed here
    app.teardown_appcontext(close_db)
    # add so that can use "flask init-db'
    app.cli.add_command(init_db_command)



