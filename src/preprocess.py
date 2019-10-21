import os
import shutil
import json
import pandas as pd

#
import base
import read_raw as rr

DESTINATION_ENCODING = 'utf-8'


def extract_district_ids_from_special_df(df_special: pd.DataFrame):
    df = df_special[[rr.DISTRICT_NAME_COLUMN, rr.DISTRICT_ID_COLUMN]]
    df = df.set_index(rr.DISTRICT_NAME_COLUMN).drop_duplicates()
    df = df.sort_values(by=rr.DISTRICT_ID_COLUMN)
    df_dict = df.squeeze().to_dict()
    with open(base.get_district_id_map_path(), 'w') as fw:
        json.dump(df_dict, fw, indent=4, ensure_ascii=False)


def save_dataframe_to_csv(data_frame: pd.DataFrame, path: str, encoding=DESTINATION_ENCODING):
    data_frame.index.name = rr.INDEX_COLUMN
    data_frame.to_csv(path, encoding=encoding)


def run_preprocessing():
    # REMOVE PREVIOUS PREPROCESSING
    try:
        shutil.rmtree(base.DATA_DIR_PREPROCESSING)
    except FileNotFoundError:
        pass
    os.makedirs(base.DATA_DIR_PREPROCESSING)

    # FISHNETS
    df_special = rr.read_fishnet_special()
    extract_district_ids_from_special_df(df_special)
    save_dataframe_to_csv(
        data_frame=df_special.drop(columns=[rr.DISTRICT_NAME_COLUMN]),
        path=base.get_prep_fishnet_path(base.FISHNET_GRID_SPECIAL)
    )

    for grid in base.FISHNET_GRIDS_REGULAR:
        df = rr.read_fishnet_regular(grid)
        save_dataframe_to_csv(
            data_frame=df,
            path=base.get_prep_fishnet_path(grid)
        )

    # PLACES
    save_dataframe_to_csv(
        data_frame=rr.read_places(),
        path=base.get_prep_places_path()
    )

    # OCCUPATIONS
    save_dataframe_to_csv(
        data_frame=rr.read_occupations(),
        path=base.get_prep_occupations_path()
    )


if __name__ == "__main__":
    run_preprocessing()
