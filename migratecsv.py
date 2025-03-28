import sqlite3
import argparse
import pandas as pd

from pathlib import Path

from optiface.core.optispace import ProblemSpace, read_pspace_from_yaml

from optiface.dbmanager.dbm import DBM


_ADDED_FROM_CSV: str = "CSV"


def main():
    parser = argparse.ArgumentParser(
        prog="OptiFace csv migrator",
    )
    parser.add_argument("problem")
    parser.add_argument("csv")
    args = parser.parse_args()
    pname = args.problem
    csv_path = args.csv

    pspace = read_pspace_from_yaml(pname)

    df = pd.read_csv(csv_path)

    dbm = DBM(pspace)

    base_row = [_ADDED_FROM_CSV]

    for _, csv_row in df.iterrows():
        row = base_row
        row.extend(list(csv_row))
        import pdb

        pdb.set_trace()
        dbm.insert_single_row(tuple(row))


if __name__ == "__main__":
    main()
