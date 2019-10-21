import base
import pandas as pd

# project
import read_raw as rr

def read_places() -> pd.DataFrame:
    df = pd.read_csv(base.get_prep_places_path(), index_col=0)
    return df


def read_occupations() -> pd.DataFrame:
    # using the command below throws a numpy future warning at the first function call
    # df = pd.read_csv(base.get_prep_occupations_path(), index_col=0)
    df = pd.read_csv(base.get_prep_occupations_path())
    df.set_index(rr.INDEX_COLUMN)
    return df


def read_fishnet(grid: int) -> pd.DataFrame:
    df = pd.read_csv(base.get_prep_fishnet_path(grid), index_col=0)
    return df
