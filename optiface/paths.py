import os

_DAT_DIR = "instances"
_RESULTS_DIR = "out"
_LOGS_DIR = "logs"
_IMPLEMENTER_DIR = os.path.join("optiface", "implementer")
_FINAL_FILE = "final.csv"
_SERVICE_HORIZON_FILE = "service.csv"
_ITERATION_TIME_FILE = "time.csv"
_FACILITIES_FILE = "facilities.csv"
_FINALDB = os.path.join(_RESULTS_DIR, _FINAL_FILE)
_SERVICEDB = os.path.join(_RESULTS_DIR, _SERVICE_HORIZON_FILE)
_TIMEDB = os.path.join(_RESULTS_DIR, _ITERATION_TIME_FILE)
_FACILITIESDB = os.path.join(_RESULTS_DIR, _FACILITIES_FILE)
FEATURE_SET_YML_PATH = os.path.join(_IMPLEMENTER_DIR, "featureset.yml")
SOLVER_TYPE_YML_PATH = os.path.join(_IMPLEMENTER_DIR, "solvers.yml")
