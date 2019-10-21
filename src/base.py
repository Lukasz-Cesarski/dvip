import os

# DIRECTORIES NAMES
DATA_DIR_DNAME               = "data"
DATA_DIR_RAW_DNAME           = "raw"
DATA_DIR_PREPROCESSING_DNAME = "preprocessing"
DATA_DIR_MISC_DNAME          = "misc"

# EXTENSIONS
EXT_DATA = ".csv"
EXT_TEXT = ".txt"
EXT_DICT = ".json"

# ENCODING
ENC_BASIC = 'utf-8'
ENC_FISHN = 'utf-8'  # 'iso-8859-1'

# FILE NAMES
PLACES_FNAME                 = "places"
OCCUPATION_FNAME             = "popular_times"
FISHNET_FNAME                = "warsaw_wgs84_every"
DISTRICT_NAMES_CORRECT_FNAME = "correct_districts"
DISTRICT_NAMES_RENAME_FNAME  = "district_rename_map"
DISTRICT_IDS_MAPPING_FNAME   = "district_id_map"

# FILE NAMES SUFFIXES
OCCUPATION_SUFFIXES   = [1, 2]
FISHNET_GRID_SPECIAL  = 500
FISHNET_GRIDS_REGULAR = [100, 1000, 2000]

# DIRECTORY TREE
DATA_DIR               = os.path.join(DATA_DIR_DNAME)
DATA_DIR_RAW           = os.path.join(DATA_DIR, DATA_DIR_RAW_DNAME)
DATA_DIR_PREPROCESSING = os.path.join(DATA_DIR, DATA_DIR_PREPROCESSING_DNAME)
DATA_DIR_MISC          = os.path.join(DATA_DIR, DATA_DIR_MISC_DNAME)


# RAW PATHS
def get_raw_places_path() -> str:
    return os.path.join(DATA_DIR_RAW,
                        PLACES_FNAME + EXT_DATA)


def get_raw_occupations_path(suffix: int) -> str:
    return os.path.join(DATA_DIR_RAW,
                        OCCUPATION_FNAME + "_" + str(suffix) + EXT_DATA)


def get_raw_fishnet_path(grid: int) -> str:
    return os.path.join(DATA_DIR_RAW,
                        FISHNET_FNAME + "_" + str(grid) + "m" + EXT_TEXT)


# PREPROCESSED PATHS
def get_prep_places_path() -> str:
    return os.path.join(DATA_DIR_PREPROCESSING,
                        PLACES_FNAME + EXT_DATA)


def get_prep_occupations_path() -> str:
    return os.path.join(DATA_DIR_PREPROCESSING,
                        OCCUPATION_FNAME + EXT_DATA)


def get_prep_fishnet_path(grid: int) -> str:
    return os.path.join(DATA_DIR_PREPROCESSING,
                        FISHNET_FNAME + "_" + str(grid) + "m" + EXT_TEXT)


def get_district_id_map_path():
    return os.path.join(DATA_DIR_PREPROCESSING, DISTRICT_IDS_MAPPING_FNAME + EXT_DICT)


# MISC PATHS
def get_district_correct_path():
    return os.path.join(DATA_DIR_MISC, DISTRICT_NAMES_CORRECT_FNAME + EXT_DICT)


def get_district_rename_path():
    return os.path.join(DATA_DIR_MISC, DISTRICT_NAMES_RENAME_FNAME + EXT_DICT)

