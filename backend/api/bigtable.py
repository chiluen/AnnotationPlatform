import datetime

from google.cloud import bigtable
from google.cloud.bigtable import column_family
from google.cloud.bigtable import row_filters

# TODO: the IDs are fixed
def get_bigtable(table_id, project_id='final-annotation-351318', instance_id='final-annotation'):
    client = bigtable.Client(project=project_id, admin=True)
    instance = client.instance(instance_id)
    table = instance.table(table_id)
    return table
