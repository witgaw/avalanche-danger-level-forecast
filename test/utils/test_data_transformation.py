from src.utils.data_transformation import tabularise_data_by_season_and_area
import pandas as pd
import numpy as np


def test_tabularise_data_by_season_and_area():
    np.random.seed(1)

    seasons = pd.DataFrame(
        {
            "season_start": ["2020-11-01", "2021-11-01"],
            "season_end": ["2021-03-01", "2022-02-01"],
        }
    )

    data = pd.DataFrame(
        {
            "Date": pd.date_range(start="2021-01-01", periods=60, freq="D").tolist()
            + pd.date_range(start="2021-12-01", periods=60, freq="D").tolist(),
            "Area": ["Area1"] * 60 + ["Area2"] * 60,
            "Variable1": np.random.rand(120),
            "Variable2": np.random.rand(120),
        }
    )

    dependent_variables = np.array(["Variable1", "Variable2"])
    season_max_lookback = 3
    include_seasons_day = True
    skip_missing_days = False

    result = tabularise_data_by_season_and_area(
        seasons,
        data,
        dependent_variables,
        season_max_lookback,
        include_seasons_day,
        skip_missing_days,
    )

    assert not result.empty
    assert "day_of_season" in result.columns
    assert all(
        col in result.columns
        for col in [
            "variable1_0",
            "variable1_1",
            "variable1_2",
            "variable2_0",
            "variable2_1",
            "variable2_2",
        ]
    )
    assert (
        len(result.columns)
        == len(data.columns)
        + len(dependent_variables) * (season_max_lookback - 1)
        + include_seasons_day
    )
    assert all(result["Area"] == data["Area"])

    dependent_variables = np.array(["Variable1", "Variable2"])
    season_max_lookback = 2
    include_seasons_day = False
    skip_missing_days = False

    result = tabularise_data_by_season_and_area(
        seasons,
        data,
        dependent_variables,
        season_max_lookback,
        include_seasons_day,
        skip_missing_days,
    )

    assert not result.empty
    assert not "day_of_season" in result.columns
    assert all(
        col in result.columns
        for col in ["variable1_0", "variable1_1", "variable2_0", "variable2_1"]
    )
    assert (
        len(result.columns)
        == len(data.columns)
        + len(dependent_variables) * (season_max_lookback - 1)
        + include_seasons_day
    )

    data = pd.DataFrame(
        {
            "Date": ["2020-11-03", "2020-11-05", "2020-11-06"],
            "Area": ["Area1", "Area1", "Area1"],
            "Variable1": [13, 15, 16],
            "Variable2": [23, 25, 26],
        }
    )

    dependent_variables = np.array(["Variable1", "Variable2"])
    season_max_lookback = 4
    skip_missing_days = True
    include_seasons_day = True

    result = tabularise_data_by_season_and_area(
        seasons,
        data,
        dependent_variables,
        season_max_lookback,
        include_seasons_day,
        skip_missing_days,
    )

    expected_result = pd.DataFrame(
        {
            "Date": ["2020-11-03", "2020-11-05", "2020-11-06"],
            "Area": ["Area1", "Area1", "Area1"],
            "day_of_season": [3, 5, 6],
            "variable1_0": [13, 15, 16],
            "variable1_1": [0, 13, 15],
            "variable1_2": [0, 0, 13],
            "variable1_3": [0, 0, 0],
            "variable2_0": [23, 25, 26],
            "variable2_1": [0, 23, 25],
            "variable2_2": [0, 0, 23],
            "variable2_3": [0, 0, 0],
        }
    )

    assert expected_result.eq(result).all().all()

    dependent_variables = np.array(["Variable1", "Variable2"])
    season_max_lookback = 4
    skip_missing_days = False
    include_seasons_day = False

    result = tabularise_data_by_season_and_area(
        seasons,
        data,
        dependent_variables,
        season_max_lookback,
        include_seasons_day,
        skip_missing_days,
    )

    expected_result = pd.DataFrame(
        {
            "Date": ["2020-11-03", "2020-11-05", "2020-11-06"],
            "Area": ["Area1", "Area1", "Area1"],
            "variable1_0": [13, 15, 16],
            "variable1_1": [0, 0, 15],
            "variable1_2": [0, 13, 0],
            "variable1_3": [0, 0, 13],
            "variable2_0": [23, 25, 26],
            "variable2_1": [0, 0, 25],
            "variable2_2": [0, 23, 0],
            "variable2_3": [0, 0, 23],
        }
    )

    assert expected_result.eq(result).all().all()
