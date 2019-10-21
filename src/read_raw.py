import json
import pandas as pd

# project
import base

DISTRICT_NAME_COLUMN = 'district_name'
DISTRICT_ID_COLUMN = "district_id"
INDEX_COLUMN = "id"

PLACES_READ_OPTIONS = dict()
OCCUPATIONS_READ_OPTIONS = dict()
FISHNET_READ_OPTIONS_REGULAR = dict(
    encoding=base.ENC_FISHN,
    sep='\t',
    header=None,
    names=['lng', 'lat', DISTRICT_NAME_COLUMN],
)

FISHNET_READ_OPTIONS_SPECIAL = dict(
    encoding=base.ENC_FISHN,
    sep='\t',
    header=None,
    names=['lng', 'lat', DISTRICT_ID_COLUMN, DISTRICT_NAME_COLUMN],
)


def read_district_rename_dict() -> dict:
    with open(base.get_district_correct_path()) as fr:
        correct = json.load(fr)
    with open(base.get_district_rename_path()) as fr:
        rename = json.load(fr)

    return {
        **{k: k for k in correct},
        **rename
    }


def read_district_id_dict() -> dict:
    with open(base.get_district_id_map_path()) as fr:
        district_name_to_id = json.load(fr)
    return district_name_to_id


def normalize_district_name(df: pd.DataFrame):
    df[DISTRICT_NAME_COLUMN] = df[DISTRICT_NAME_COLUMN].str.strip().str.title()
    rename_dict = read_district_rename_dict()
    df[DISTRICT_NAME_COLUMN] = df[DISTRICT_NAME_COLUMN].apply(lambda x: rename_dict[x])


def read_places() -> pd.DataFrame:
    df = pd.read_csv(base.get_raw_places_path(), **PLACES_READ_OPTIONS)
    return df


def read_occupations() -> pd.DataFrame:
    df = pd.concat(
        [
            pd.read_csv(base.get_raw_occupations_path(suffix), **OCCUPATIONS_READ_OPTIONS)
            for suffix in base.OCCUPATION_SUFFIXES
        ]).reset_index(drop=True)
    return df


def read_fishnet_special() -> pd.DataFrame:
    df = pd.read_csv(
        base.get_raw_fishnet_path(base.FISHNET_GRID_SPECIAL),
        **FISHNET_READ_OPTIONS_SPECIAL)
    normalize_district_name(df)
    return df


def read_fishnet_regular(grid: int) -> pd.DataFrame:
    assert grid in base.FISHNET_GRIDS_REGULAR, \
        "Given grid size:'{}' not in {}!".format(grid, base.FISHNET_GRIDS_REGULAR)
    df = pd.read_csv(base.get_raw_fishnet_path(grid), **FISHNET_READ_OPTIONS_REGULAR)
    df.dropna(inplace=True)
    normalize_district_name(df)

    with open(base.get_district_id_map_path()) as fr:
        district_id_mapping = json.load(fr)

    df[DISTRICT_ID_COLUMN] = df[DISTRICT_NAME_COLUMN].apply(lambda x: district_id_mapping[x])
    df.drop(columns=DISTRICT_NAME_COLUMN, inplace=True)
    return df

# DEMO #
def read_sample_places():
    df = pd.read_csv("data/sample/amrit.csv", **PLACES_READ_OPTIONS)
    return df


def read_sample_occupations():
    df = pd.read_csv("data/sample/amrit_popular_times.csv", **OCCUPATIONS_READ_OPTIONS)
    return df
