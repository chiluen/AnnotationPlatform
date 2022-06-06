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

def update_metadata(user, update_target, amount)
    auth_table = get_bigtable('auth')
    row_read = auth_table.read_row(user)
    row_write = auth_table.direct_row(user)
    try:
        previous_num = int(row_read.cells['information'][update_target.encode()][0].value.decode())
        new_num = previous_num + amount
    except KeyError:
        new_num = amount
