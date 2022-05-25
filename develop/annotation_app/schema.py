import datetime

from google.cloud import bigtable
from google.cloud.bigtable import column_family
from google.cloud.bigtable import row_filters

def initialize_bigtable(project_id, instance_id, table_id):
    client = bigtable.Client(project=project_id, admin=True)
    instance = client.instance(instance_id)
    
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
