from pathlib import Path

_TEST_PSPACE_NAME: str = "testproblem"

_SPACE = "space"
_EXPERIMENTS_DB = "experiments.db"
_TEST_PSPACEDB_PATH: Path = Path(_SPACE) / _TEST_PSPACE_NAME / _EXPERIMENTS_DB


class TestAlchemyFactory:
    """
    Behaviors:
    -  maintain experiments.db with problemspace features as columns (for active pspace)
        - create db if it does not exist
        - create results table if there are no tables
        - raise RuntimeError if incorrect schema (other tables present)
        - check correctness of columns against pspace - raise RuntimeError if columns don't match exactly
    """

    pass


class TestAlchemyAPI:
    """
    - insert row of data
        - when row is complete -> row is there when queried
        - when row has missing values -> correct defaults are used
        - when row has incorrect columns -> error
    """

    pass


class TestMigrations:
    """
    Behaviors:
    - add new column to database
        - new insert with full row (including new column) is successful
        - query of pre-migration row has correct default for column
    """

    pass
