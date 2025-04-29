import sqlite3
import pandas as pd

from typing import Any

from pathlib import Path

from optiface.core.optispace import (
    ProblemSpace,
)

# TODO: refactor to SQL query file
# TODO: (CREATE TABLE) to init new table based on pspace config (i.e. columns)
# TODO: (INSERT INTO) inserting columns using pspace config
_SPACE = "space"
_EXPERIMENTS_DB = "experiments.db"

_SQL_GETSCHEMA = "SELECT name FROM sqlite_master"

_SQL_CREATE_RESULTS_DEFAULT = "CREATE TABLE results (run_id INTEGER PRIMARY KEY ASC,timestamp_added TEXT,added_from TEXT,set_name TEXT,nodes INTEGER,rep INTEGER,solver TEXT,objective REAL,time_ms REAL)"
_SQL_CREATE_RESULTS_ASPI = "CREATE TABLE results (run_id INTEGER PRIMARY KEY ASC, timestamp_added TEXT, added_from TEXT, set_name TEXT, nodes INTEGER, arcs INTEGER, k_zero INTEGER, density REAL, scenarios INTEGER, budget INTEGER, policies INTEGER, rep INTEGER, solver TEXT, subsolver TEXT, objective REAL, time_ms REAL, unbounded INTEGER, optimal INTEGER, gap REAL, cuts_rounds INTEGER, cuts_added INTEGER, avg_cbtime_ms REAL, avg_sptime_ms REAL, partition TEXT, m_sym INTEGER, g_sym INTEGER)"
_SQL_CREATE_RESULTS_PSPACE = "CREATE TABLE results (?)"

_SQL_GETALL_RESULTS = "SELECT * FROM results"

_SQL_INSERT_SINGLE_RESULTS_ROW = "INSERT INTO RESULTS (timestamp_added, added_from, set_name, n, rep, solver, objective, time_ms) VALUES(datetime('now'), ?, ?, ?, ?, ?, ?, ?)"
_SQL_INSERT_SINGLE_ASPIRESULTS_ROW = "INSERT INTO RESULTS (timestamp_added, added_from, set_name, nodes, arcs, k_zero, density, scenarios, budget, policies, rep, solver, subsolver, objective, time_ms, unbounded, optimal, gap, cuts_rounds, cuts_added, avg_cbtime_ms, avg_sptime_ms, partition, m_sym, g_sym) VALUES(datetime('now'), ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"


_DEFAULT_ROW = ("MANUAL", "faketest", 1, 0, "MYSOLVER", 100.0, 1000.0)
_ASPI_TEST_ROW = (
    "MANUAL",
    "faketest",
    10,
    100,
    5,
    0.1,
    10,
    5,
    3,
    0,
    "MIP",
    "NA",
    100.0,
    1000.0,
    0,
    1,
    0.0,
    -1,
    -1,
    -1.0,
    -1.0,
    "0-0-0-0-0-0-0-1-2-2",
    -1,
    -1,
)

_ADDED_FROM_CSV: str = "CSV"


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

    def insert_single_row(self, row):
        # TODO: start to work on some "interactive" error handling here
        # user can handle migration errors as rows are added one by one
        # TODO: should (can) we deduplicate here, or when using data?
        sql: str = ""
        final_row: tuple[Any] = row
        if self.pspace.name == "aspi":
            sql = _SQL_INSERT_SINGLE_ASPIRESULTS_ROW
            if final_row is None:
                final_row = _ASPI_TEST_ROW
        else:
            sql = _SQL_INSERT_SINGLE_RESULTS_ROW
            if final_row is None:
                final_row = _DEFAULT_ROW

        # row_id, timestamp (now) are in the sql
        self.cur.execute(sql, final_row)
        self.con.commit()
        print(f"added one row to results table in problem {self.pspace.name}")

    def insert_rows(self, df):
        for _, csv_row in df.iterrows():
            csv_row = list(csv_row)
            valid = self.pspace.validate_row(csv_row)
            row = [_ADDED_FROM_CSV]
            row.extend(csv_row)
            # validate
            if not valid:
                print(f"skipping non-valid row: {row}")
            else:
                self.insert_single_row(tuple(row))

    def results_table_head(self):
        res = self.cur.execute(_SQL_GETALL_RESULTS)
        row = res.fetchone()
        print(row)
