#!/usr/bin/env python3
from front.app import OptiFaceTUI

import sqlite3

from pathlib import Path

from optiface.core.optispace import ProblemSpace, read_pspace_from_yaml
from optiface.core.optidatetime import OptiDateTimeFactory

from optiface.dbmanager.dbm import DBM

_SPACE = "space"
_PROBLEM_NAME = "defaultproblem"
_EXPERIMENTS_DB = "experiments.db"

_SQL_CREATE_RESULTS_DEFAULT = "CREATE TABLE results (run_id INTEGER PRIMARY KEY ASC,timestamp_added TEXT,added_from TEXT,set_name TEXT,n INTEGER,rep INTEGER,solver TEXT,objective REAL,time_ms REAL)"
_SQL_GETSCHEMA = "SELECT * FROM sqlite_master"
_SQL_GETSCHEMA2 = "SELECT name FROM sqlite_master"


def main():
    pspace: ProblemSpace = read_pspace_from_yaml(_PROBLEM_NAME)
    # pspace.print_features()
    opti_dt = OptiDateTimeFactory()
    print(opti_dt.optinow())
    print(opti_dt.optidefault())

    # pspace_dbpath: Path = Path(_SPACE) / pspace.name / _EXPERIMENTS_DB
    # con = sqlite3.connect(pspace_dbpath)
    # cur = con.cursor()
    # cur.execute(_SQL_CREATE_RESULTS_DEFAULT)
    # res = cur.execute(_SQL_GETSCHEMA2)
    # print(res)
    # print(res.fetchone())
    # print(len(res.fetchone()))


if __name__ == "__main__":
    main()
