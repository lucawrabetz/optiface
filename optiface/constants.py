from pathlib import Path
import shutil
import os
from platformdirs import user_config_dir, user_data_dir


_DEFAULT = "default"
_KNAPSACK = "knapsack"
_SPACE = Path("space")
_MIGRATIONS = Path("migrations")

_PS_FILE = "problemspace.yaml"
_EXPERIMENTS_DBFILE = "experiments.db"

_APP_NAME = "optiface"
_APP_AUTHOR = "lucawrabetz"
_SQLITE_PREF = "sqlite+pysqlite:///"


def opti_user_data_dir() -> Path:
    return Path(user_data_dir(appname=_APP_NAME, appauthor=_APP_AUTHOR))


# we are not using user_config_dir for now, my understanding from XDG is this is for linux config stuff (for macos and Windows, it gives the same path as user_data_dir)


# pspace configuration should be managed by the application only and not touched manually by the user ideally, so this puts it in contrast, in my opinion, to the stuff that typically goes in a linux-y .config
def opti_user_config_dir() -> Path:
    return Path(user_config_dir(appname=_APP_NAME, appauthor=_APP_AUTHOR))


def check_make_dir(path: str | Path, i) -> Path:
    """
    Recursively check if a directory exists, or create one with the highest number
        - example - if "path" string is "/dat/experiments/test-01_29_22", and there already exist:
            - "/dat/experiments/test-01_29_22-0"
            - "/dat/experiments/test-01_29_22-1"
            - "/dat/experiments/test-01_29_22-2"
        we have to create the dir "/dat/experiments/test-01_29_22-3"
    """
    str_path: str = str(path)

    isdir = os.path.isdir(str_path + "-" + str(i))

    # if the directory exists, call on the next i
    if isdir:
        return check_make_dir(str_path, i + 1)

    # base case - create directory for given i (and return final str_path)
    else:
        os.mkdir(str_path + "-" + str(i))
        return Path(str_path + "-" + str(i))


def copy_dir(src: str | Path, dst: str | Path) -> Path:
    shutil.copytree(src, dst)
    return Path(dst)


def main():
    pass


if __name__ == "__main__":
    main()
