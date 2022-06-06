import datetime

from google.cloud import bigtable
from google.cloud.bigtable import column_family
from google.cloud.bigtable import row_filters
from constant import *

# TODO: the IDs are fixed
def get_bigtable(
        table_id, 
        project_id=PROJECT_ID, 
        instance_id=BIGTABLE_INSTANCE_ID
    ):
    client = bigtable.Client(project=project_id, admin=True)
    instance = client.instance(instance_id)
    table = instance.table(table_id)
    return table

def update_metadata(user, update_target, amount):
    auth_table = get_bigtable('auth')
    row_read = auth_table.read_row(user)
    row_write = auth_table.direct_row(user)
    try:
        previous_num = int(row_read.cells['information'][update_target.encode()][0].value.decode())
        new_num = previous_num + amount
    except KeyError:
        new_num = amount
    row_write.set_cell('information', update_target, str(new_num), datetime.utcnow())
    row_write.commit()
