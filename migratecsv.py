import argparse
import pandas as pd

from pathlib import Path

from optiface.core.optispace import ProblemSpace, read_pspace_from_yaml

from optiface.dbmanager.dbm import AlchemyAPI, init_alchemy_api


def main():
    parser = argparse.ArgumentParser(
        prog="OptiFace csv migrator",
    )
    parser.add_argument("problem", type=str)
    parser.add_argument("csv", type=str)
    args = parser.parse_args()
    pname = args.problem
    csv_path = args.csv

    pspace = read_pspace_from_yaml(pname)
    db_api = init_alchemy_api(pspace)

    if not db_api:
        # TODO: this is stupid rn, need to figure out union[error | AlchemyAPI] return values
        # this path will never actually be reached because if the function returned None it would have raised an error first
        # in summary: currently, functions are signed -> None | AlchemyAPI, but raise hacky errors in the function
        # need to refactor to be able to return these errors and handle them when I want in the call stack
        print("error in pspace - db reconcile")
    else:
        df = pd.read_csv(csv_path)
        db_api.insert_rows(df)


if __name__ == "__main__":
    main()
