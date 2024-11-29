import pandas as pd
import numpy as np


def tabularise_data_by_season_and_area(
    seasons: pd.DataFrame,
    data: pd.DataFrame,
    dependent_variables: np.array,
    season_max_lookback: int,
    include_seasons_day: bool,
    skip_missing_days: bool,
) -> pd.DataFrame:
    data["Date"] = pd.to_datetime(data["Date"])

    col_seasons_day = "day_of_season"
    # other_variables = sorted(
    #     list(set(data.columns.tolist()) - set(dependent_variables))
    # )

    other_variables = [col for col in data.columns if col not in dependent_variables]

    dependent_columns = [
        f"{var.lower().replace(" ", "_")}_{i}"
        for var in dependent_variables
        for i in range(season_max_lookback)
    ]

    all_columns = other_variables.copy()
    if include_seasons_day:
        all_columns.append(col_seasons_day)
    all_columns += dependent_columns
    index = "index"

    cols = [index]
    cols.extend(all_columns)
    output = pd.DataFrame(columns=cols)

    indices = [i * season_max_lookback for i in range(len(dependent_variables))]

    for _, season in seasons.iterrows():
        start = pd.to_datetime(season["season_start"]).date()
        end = pd.to_datetime(season["season_end"]).date()
        season_data = data[
            (data["Date"].dt.date >= start) & (data["Date"].dt.date <= end)
        ]

        for _, area_data in season_data.groupby("Area", as_index=False):
            area_data = area_data.sort_values(by="Date", ascending=True)
            dependent_row_bit = np.zeros(len(dependent_columns))
            day_of_season_prev = 0

            for idx, row_input in area_data.iterrows():
                day_of_season = (row_input["Date"].date() - start).days + 1
                shift = 1 if skip_missing_days else day_of_season - day_of_season_prev

                dependent_row_bit = np.roll(dependent_row_bit, shift)
                dependent_row_bit[0:shift] = 0

                row_output = [idx]
                row_output.extend(row_input[other_variables])
                if include_seasons_day:
                    row_output.append(day_of_season)

                dependent_row_bit[indices] = row_input[dependent_variables]
                row_output.extend(dependent_row_bit)

                output.loc[len(output)] = row_output

                day_of_season_prev = day_of_season

    return output.set_index(index)
