import datetime

from google.cloud import bigtable
from google.cloud.bigtable import column_family
from google.cloud.bigtable import row_filters

from constant import *

def initialize_bigtable(project_id, instance_id):
    client = bigtable.Client(project=project_id, admin=True)
    instance = client.instance(instance_id)
    
    table_id = 'annotation'
    print(f"create {table_id} table...")
    table = instance.table(table_id)
    # define the garbage collection strategy
    max_version_rule = column_family.MaxVersionsGCRule(2)
    # define column family --> column
    # row: uploader/task_id_or_name/sentence_id
    # TODO: design column family full picture
    column_family_id_text = 'text'
    column_family_id_annotation = 'annotation'
    column_family_id_validation = 'validation'
    column_families = {
        column_family_id_text: max_version_rule,
        column_family_id_annotation: max_version_rule,
        column_family_id_validation: max_version_rule
    }
    if not table.exists():
        table.create(column_families=column_families)
    else:
        print(f"table {table_id} already exists")

    # -------- create auth table ------- #
    print(f"create auth table...")
    table_auth = instance.table('auth')
    max_version_rule_auth = column_family.MaxVersionsGCRule(1)
    column_families_auth = {
        'information': max_version_rule_auth 
    }
    if not table.exists():
        table.create(column_families=column_families_auth)
    else:
        print(f"table auth already exists")

if __name__ == '__main__':
    initialize_bigtable(PROJECT_ID, BIGTABLE_INSTANCE_ID)
