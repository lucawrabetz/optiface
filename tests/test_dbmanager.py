from pathlib import Path

_TEST_PSPACE_NAME: str = "testproblem"

_SPACE = "space"
_EXPERIMENTS_DB = "experiments.db"
_TEST_PSPACEDB_PATH: Path = Path(_SPACE) / _TEST_PSPACE_NAME / _EXPERIMENTS_DB


class TestDBM:
    """
    Behaviors:
    - maintain results table in experiments.db with problemspace features as columns
        - create table if it does not exist
        - check correctness of columns against pspace
        - check it is the only table
    - insert row of data
        - when row is complete -> row is there when queried
        - when row has missing values -> correct defaults are used
        - when row has incorrect columns -> error
    - add new column to database
        - new insert with full row (including new column) is successful
        - query of pre-migration row has correct default for column
    """

    pass
