import pandas as pd
from os import makedirs
import re
import matplotlib.pyplot as plt


class LatexHelpers:

    def __init__(self):
        pass

    @staticmethod
    def save_as_latex_table(
        df: pd.DataFrame,
        name: str,
        path: str,
        caption: str = None,
        index: bool = True,
        float_format: str = "{:0.1f}"
    ) -> None:
        makedirs(path, exist_ok=True)

        # replace '_' in column names with a space as this would mess with latex
        if isinstance(df, pd.DataFrame):
            df.columns = df.columns.str.replace("_", " ")

        # remove file extension if present
        name = re.sub(r"\..*", "", name)
        with open(f"{path}/{name}.tex", "w") as f:
            f.write(
                df.to_latex(
                    index=index,
                    caption=caption,
                    label=f"tbl:{name}",
                    position="H",
                    float_format=float_format.format,
                )
            )

    @staticmethod
    def save_text_snippet(text: str, name: str, path: str) -> None:
        makedirs(path, exist_ok=True)

        name = re.sub(r"\..*", "", name)
        with open(f"{path}/{name}.txt", "w") as f:
            f.write(text)

    @staticmethod
    def save_value_count_plot(
        df: pd.DataFrame,
        column: str,
        name: str,
        title_prefix: str,
        path: str,
    ) -> None:
        makedirs(path, exist_ok=True)
        name = re.sub(r"\..*", "", name)

        value_counts = df[column].value_counts()
        plt.vlines(x=value_counts.index, ymin=0, ymax=value_counts.values, color="blue")
        plt.xlabel(column)
        plt.ylabel("count")
        plt.title(f"{title_prefix} ({df[column].min()} - {df[column].max()})")
        plt.savefig(f"{path}/{name}.png")

    @staticmethod
    def breakdown_per_other_column(
        df: pd.DataFrame, main_column: str, breakdown_column: str
    ) -> pd.DataFrame:
        labels = sorted(df[main_column].unique())
        breakdown = pd.DataFrame()
        for i in range(len(labels)):
            breakdown[f"{labels[i]}"] = (
                df[df[main_column] == labels[i]].groupby(breakdown_column).size()
            )

        return breakdown

    @staticmethod
    def fillna_and_log_value(
        df: pd.DataFrame, column: str, value: float, log: pd.DataFrame
    ) -> None:
        na_count = df[column].isna().sum()
        df[column] = df[column].fillna(value)
        action = f'{na_count} NAs filled with "{value}"'
        log.loc[len(log)] = [column, action]

    @staticmethod
    def describe(df: pd.DataFrame) -> pd.DataFrame:
        summary = df.describe(include="all").transpose()
        summary["dtype"] = df.dtypes
        summary["non-null"] = df.count().astype(int)
        summary["unique"] = df.nunique()

        return summary[["non-null", "unique", "dtype", "mean", "min", "max"]]
