from geopy.distance import distance
from datetime import datetime
from typing import Callable, Tuple, List

import numpy as np
import plotly.express as px
import pandas as pd


def find_necessity_condition(base_coord: float, epicenter_coord: float) -> Callable:
    if base_coord > epicenter_coord:
        condition = float.__gt__
    elif base_coord < epicenter_coord:
        condition = float.__lt__
    else:
        condition = None
    return condition


def reduce_candidates_by_base(epicenter: Tuple[float],
                              base: Tuple[float],
                              candidates: List[Tuple[float]]) -> List[Tuple[float]]:
    lat_condition = find_necessity_condition(base[0], epicenter[0])
    lng_condition = find_necessity_condition(base[1], epicenter[1])
    new_candidates = []

    for candidate in candidates:
        if lat_condition is not None:
            lat_result = lat_condition(base[0], candidate[0])
        else:
            lat_result = None
        if lng_condition is not None:
            lng_result = lng_condition(base[1], candidate[1])
        else:
            lng_result = None
        #         print(lat_result, lng_result)
        if lat_result or lng_result:
            new_candidates.append(candidate)
    return new_candidates


def find_nearby_fishnet(epicenter: Tuple[float], fishnet_points: List[Tuple[float]]) -> List[Tuple[float]]:
    candidates = fishnet_points.copy()
    processed_bases = []
    while True:
        candidates_permutation = np.random.permutation(len(candidates))
        for idx in candidates_permutation:
            if candidates[idx] in processed_bases:
                pass
            else:
                base = candidates.pop(idx)
                processed_bases.append(base)
                candidates = reduce_candidates_by_base(epicenter, base, candidates)
                candidates.append(base)
                break
        else:
            return candidates


def get_closest_fishnet_id(row: pd.Series, df_fishnet: pd.DataFrame) -> int:
    epicenter = row['point']
    fishnet_points = df_fishnet['point'].to_list()
    nearby_fishnet = find_nearby_fishnet(epicenter=epicenter, fishnet_points=fishnet_points)
    nearby_fishnet_dict = {
        k: distance(epicenter, k).m for k in nearby_fishnet
    }
    closes_fishnet, _ = min(nearby_fishnet_dict.items(), key=lambda x: x[1])
    closes_fishnet_ids = df_fishnet.query("point == @closes_fishnet").index
    assert len(closes_fishnet_ids) == 1, "Fishnet index ambiguous {}".format(closes_fishnet_ids)

    return closes_fishnet_ids[0]


def get_exact_fishnet_location_for_places(df_places: pd.DataFrame,
                                          df_fishnet: pd.DataFrame, header=10) -> pd.Series:
    df_places_grid = df_places.loc[:, ['lat', 'lng']]
    df_places_grid['point'] = list(zip(df_places_grid['lat'], df_places_grid['lng']))
    df_fishnet['point'] = list(zip(df_fishnet['lat'], df_fishnet['lng']))
    places_header = df_places_grid.head(header)
    start = datetime.now()
    result = places_header.apply(lambda x: get_closest_fishnet_id(x, df_fishnet), axis=1)
    print(str(datetime.now() - start))
    return result


def plot_candidates_reduction(epicenter: Tuple[float],
                              reference_point: Tuple[float],
                              old_candidates: List[Tuple[float]],
                              new_candidates: List[Tuple[float]],
                              data_size=6,
                              result_size=12):
    data = (
            [
                {
                    'name': 'epicenter',
                    'tag': 'data',
                    'x': epicenter[0],
                    'y': epicenter[1],
                    'size': data_size,
                }
            ]
            +
            [
                {
                    'name': 'reference',
                    'tag': 'data',
                    'x': reference_point[0],
                    'y': reference_point[1],
                    'size': data_size,
                }
            ]
            +
            [
                {
                    'name': 'candidate',
                    'tag': 'data',
                    'x': candidate[0],
                    'y': candidate[1],
                    'size': data_size,
                } for candidate in old_candidates
            ]
            +
            [
                {
                    'name': 'new_candidate',
                    'tag': 'results',
                    'x': candidate[0],
                    'y': candidate[1],
                    'size': result_size,
                } for candidate in new_candidates
            ]
    )
    data_to_plot = pd.DataFrame(data)
    fig = px.scatter(data_to_plot,
                     x='x',
                     y='y',
                     color='name',
                     symbol='tag',
                     symbol_sequence=['circle', 'circle-open'],
                     size='size')
    fig.show()
