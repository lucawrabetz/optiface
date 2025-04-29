import sqlite3
import argparse
import pandas as pd

from pathlib import Path

from optiface.core.optispace import ProblemSpace, read_pspace_from_yaml

from optiface.dbmanager.dbm import DBM


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
    dbm.insert_rows(df)


if __name__ == "__main__":
    main()
