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
