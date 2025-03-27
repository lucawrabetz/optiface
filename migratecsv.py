import sqlite3
import argparse

from pathlib import Path

from optiface.core.optispace import ProblemSpace, read_pspace_from_yaml

from optiface.dbmanager.dbm import DBM


def main():
    parser = argparse.ArgumentParser(
        prog="OptiFace csv migrator",
    )
    parser.add_argument("problem")
    args = parser.parse_args()
    pname = args.problem

    pspace = read_pspace_from_yaml(pname)
    dbm = DBM(pspace)


if __name__ == "__main__":
    main()
