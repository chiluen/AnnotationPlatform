from datetime import datetime
from api.bigtable import get_bigtable

PROJECT_ID = 'final-annotation-352116'
BIGTABLE_INSTANCE_ID = 'final-annotation'
TABLE_ID_AUTH = 'auth'
TABLE_ID_ANNOTATION = 'annotation'
TAGS = ["Finance", "Science", "Other", "Technology", "Sports"]
PROHIBIT_NAMES = ["already_annotate", "already_review", "not_annotate"] + TAGS

def print_row(row):
    print("Reading data for {}:".format(row.row_key.decode("utf-8")))
    for cf, cols in sorted(row.cells.items()):
        print("Column Family {}".format(cf))
        for col, cells in sorted(cols.items()):
            for cell in cells:
                labels = (
                    " [{}]".format(",".join(cell.labels)) if len(cell.labels) else ""
                )
                print(
                    "\t{}: {} @{}{}".format(
                        col.decode("utf-8"),
                        cell.value.decode(),
                        cell.timestamp,
                        labels,
                    )
                )
    print("")


