import sqlite3

from pathlib import Path

from optiface.core.optispace import (
    ProblemSpace,
)

_SPACE = "space"
_EXPERIMENTS_DB = "experiments.db"
_SQL_GETSCHEMA = "SELECT name FROM sqlite_master"
_SQL_CREATE_RESULTS_DEFAULT = "CREATE TABLE results (run_id INTEGER PRIMARY KEY ASC,timestamp_added TEXT,added_from TEXT,set_name TEXT,nodes INTEGER,rep INTEGER,solver TEXT,objective REAL,time_ms REAL)"
_SQL_CREATE_RESULTS_ASPI = "CREATE TABLE results (run_id INTEGER PRIMARY KEY ASC, timestamp_added TEXT, added_from TEXT, set_name TEXT, nodes INTEGER, arcs INTEGER, k_zero INTEGER, density REAL, scenarios INTEGER, budget INTEGER, policies INTEGER, rep INTEGER, solver TEXT, subsolver TEXT, objective REAL, time_ms REAL, unbounded INTEGER, optimal INTEGER, gap REAL, cuts_rounds INTEGER, cuts_added INTEGER, avg_cbtime_ms REAL, avg_sptime_ms REAL, partition TEXT, m_sym INTEGER, g_sym INTEGER)"
_SQL_CREATE_RESULTS_PSPACE = "CREATE TABLE results (?)"

_SQL_GETALL_RESULTS = "SELECT * FROM results"


class DBM:
    def __init__(self, pspace):
        self.pspace: ProblemSpace = pspace
        self.pspace_dbpath: Path = Path(_SPACE) / pspace.name / _EXPERIMENTS_DB
        self.con = sqlite3.connect(self.pspace_dbpath)
        self.cur = self.con.cursor()
        self.check_results_table()

    def create_results_table(self):
        if self.pspace.name == "defaultproblem":
            self.cur.execute(_SQL_CREATE_RESULTS_DEFAULT)
        elif self.pspace.name == "aspi":
            self.cur.execute(_SQL_CREATE_RESULTS_ASPI)

    def check_results_table(self):
        res = self.cur.execute(_SQL_GETSCHEMA)

        if res.fetchone() is None:
            # switch for based on pspace
            self.create_results_table()
            print("created results table")
        else:
            print("results table exists already")

        self.results_table_head()

    def results_table_head(self):
        res = self.cur.execute(_SQL_GETALL_RESULTS)
        rows = res.fetchmany(size=min(10, res.arraysize))
        for i in rows:
            print(i)
