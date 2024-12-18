from typing import List, Tuple
from enum import Enum
import pandas as pd
import numpy as np
from numpy.typing import ArrayLike
from utils.latex import LatexHelpers
from sklearn import metrics
import matplotlib.pyplot as plt


class DatasetCategory(Enum):
    TRAINING = "training"
    DEVELOPMENT = "development"
    TEST = "test"


class MulticlassErrorMetrics:
    def __init__(
        self,
        dataset_name: str,
        classes: ArrayLike,
        y_true_train: ArrayLike,
        y_true_dev: ArrayLike,
        y_true_test: ArrayLike,
        assets_path: str = "../tex/assets/",
        confussion_mat_entry_format=".1%",
    ) -> None:

        self.dataset_name = dataset_name
        self.assets_path = assets_path

        self.y_true = {
            DatasetCategory.TRAINING: y_true_train,
            DatasetCategory.DEVELOPMENT: y_true_dev,
            DatasetCategory.TEST: y_true_test,
        }
        self.classes = classes

        self._metrics = [
            "MSE",
            "average error",
            "accuracy",
            "precision:",
            "1 ",
            "2  ",
            "3   ",
            "4    ",
            "    ",
            "prec. (macro)",
            "recall:",
            "1     ",
            "2      ",
            "3       ",
            "4        ",
            "        ",
            "recall (macro)",
            "$F_1$:",
            "1         ",
            "2          ",
            "3           ",
            "4            ",
            "            ",
            "$F_1$ (macro)",
            "confusion matrix",
        ]
        self.__confusion_matrix_index = -1
        self.confussion_mat_entry_format = confussion_mat_entry_format

        self.tables = {
            DatasetCategory.TRAINING: pd.DataFrame(columns=self._metrics),
            DatasetCategory.DEVELOPMENT: pd.DataFrame(columns=self._metrics),
            DatasetCategory.TEST: pd.DataFrame(columns=self._metrics),
        }

    def metrics(self) -> List[str]:
        return self._metrics

    def _to_loc(self, model_name: str, independent_variables: str) -> str:
        if independent_variables != None and "," in independent_variables:
            raise ValueError(
                f"independent_variables string cannot contain commas, got: {independent_variables}"
            )
        return f"{model_name}, {independent_variables}"

    def _from_loc(self, loc: str) -> Tuple[str, str]:
        return loc.split(", ")

    def compute_errors_all_sets(
        self,
        model_name: str,
        independent_variables: str,
        y_pred_train: ArrayLike,
        y_pred_dev: ArrayLike,
        y_pred_test: ArrayLike,
    ) -> None:
        self.compute_errors(
            model_name, independent_variables, DatasetCategory.TRAINING, y_pred_train
        )
        self.compute_errors(
            model_name, independent_variables, DatasetCategory.DEVELOPMENT, y_pred_dev
        )
        self.compute_errors(
            model_name, independent_variables, DatasetCategory.TEST, y_pred_test
        )

    def compute_errors(
        self,
        model_name: str,
        independent_variables: str,
        set_cat: DatasetCategory,
        y_pred: ArrayLike,
    ) -> None:
        df_metrics = None
        y_true = None

        df_metrics = self.tables[set_cat]
        if df_metrics is None:
            raise ValueError(f"Error table not found for '{set_cat}'")

        y_true = self.y_true[set_cat]
        if y_true is None:
            if y_pred is None:
                return
            raise ValueError(
                f"'y_true' not found for '{set_cat}' while 'y_pred' was specified"
            )

        if np.isscalar(y_pred):
            y_pred = np.full_like(y_true, y_pred)

        if len(y_pred) != len(y_true):
            raise ValueError(
                f"Invalid 'y_pred' length, expected: {len(y_true)} or 1, got: {len(y_pred)}"
            )

        loc = self._to_loc(model_name, independent_variables)

        n = 0
        # MSE
        df_metrics.loc[loc, self._metrics[n]] = metrics.mean_squared_error(
            y_true, y_pred
        )
        n+=1
        df_metrics.loc[loc, self._metrics[n]] = np.average(y_true - y_pred)
        # highest error
        # accuracy
        n+=1
        df_metrics.loc[loc, self._metrics[n]] = metrics.accuracy_score(y_true, y_pred)
        # precision
        n+=1
        df_metrics.loc[loc, self._metrics[n]] = ""
        prec_multi = [
            round(float(x), 2)
            for x in metrics.precision_score(
                y_true, y_pred, average=None, zero_division=0
            )
        ]
        n+=1
        df_metrics.loc[loc, self._metrics[n]] = prec_multi[0]
        n+=1
        df_metrics.loc[loc, self._metrics[n]] = prec_multi[1]
        n+=1
        df_metrics.loc[loc, self._metrics[n]] = prec_multi[2]
        n+=1
        df_metrics.loc[loc, self._metrics[n]] = prec_multi[3]
        n+=1
        df_metrics.loc[loc, self._metrics[n]] = ""
        n+=1
        df_metrics.loc[loc, self._metrics[n]] = metrics.precision_score(
            y_true, y_pred, average="macro", zero_division=0
        )
        # recall
        n+=1
        df_metrics.loc[loc, self._metrics[n]] = ""
        recall_multi = [
            round(float(x), 2)
            for x in metrics.recall_score(y_true, y_pred, average=None)
        ]
        n+=1
        df_metrics.loc[loc, self._metrics[n]] = recall_multi[0]
        n+=1
        df_metrics.loc[loc, self._metrics[n]] = recall_multi[1]
        n+=1
        df_metrics.loc[loc, self._metrics[n]] = recall_multi[2]
        n+=1
        df_metrics.loc[loc, self._metrics[n]] = recall_multi[3]
        n+=1
        df_metrics.loc[loc, self._metrics[n]] = ""
        n+=1
        df_metrics.loc[loc, self._metrics[n]] = metrics.recall_score(
            y_true, y_pred, average="macro"
        )
        # F-1
        n+=1
        df_metrics.loc[loc, self._metrics[n]] = ""
        f1_multi = [
            round(float(x), 2) for x in metrics.f1_score(y_true, y_pred, average=None)
        ]
        n+=1
        df_metrics.loc[loc, self._metrics[n]] = f1_multi[0]
        n+=1
        df_metrics.loc[loc, self._metrics[n]] = f1_multi[1]
        n+=1
        df_metrics.loc[loc, self._metrics[n]] = f1_multi[2]
        n+=1
        df_metrics.loc[loc, self._metrics[n]] = f1_multi[3]
        n+=1
        df_metrics.loc[loc, self._metrics[n]] = ""
        n+=1
        df_metrics.loc[loc, self._metrics[n]] = metrics.f1_score(
            y_true, y_pred, average="macro"
        )
        n+=1
        df_metrics.loc[loc, self._metrics[self.__confusion_matrix_index]] = (
            metrics.confusion_matrix(y_true, y_pred, normalize="true")
        )

    def save_assets(self, table_transpose: bool =True, table_model_name_only: bool =True, table_float_format:str = "{:0.1f}", table_caption_additional: str = None):
        plt.ioff()
        for set_cat, table in self.tables.items():
            if self.y_true[set_cat] is None:
                continue

            confusion_matrices = table.iloc[:, -1]
            tbl = table.iloc[:, :-1]
            if table_model_name_only:
                tbl.index = tbl.index.str.split(',').str[0]
            if table_transpose:
                tbl = tbl.T
            set_name = set_cat.value
            LatexHelpers.save_as_latex_table(
                tbl,
                name=f"{self.dataset_name}_eval_{set_name}",
                caption=f"Evaluation metrics computed on the {set_name} set{table_caption_additional}",
                path=f"{self.assets_path}/tables",
                float_format=table_float_format,
            )
            for j in range(len(confusion_matrices.index)):
                model_name, independent_variables = self._from_loc(
                    confusion_matrices.index[j]
                )
                confusion_matrix = confusion_matrices.iloc[j]
                self.__plot_confusion_matrix(
                    confusion_matrix, model_name, independent_variables, set_cat
                )
                plt.savefig(
                    f"{self.assets_path}/figures/{self.dataset_name}_confusion_matrix_{model_name.replace('"','').replace(' ','_')}_{independent_variables.replace('"','').replace(' ','_')}_{set_name}.png",
                    dpi=300
                )
                plt.close()
        plt.show()

    def __plot_confusion_matrix(
        self,
        confusion_matrix: ArrayLike,
        model_name: str,
        independent_variables: str,
        set_cat: DatasetCategory,
    ) -> None:
        disp = metrics.ConfusionMatrixDisplay(
            confusion_matrix=confusion_matrix,
            display_labels=self.classes,
        )
        disp.plot(values_format=self.confussion_mat_entry_format)
        plt.title(
            f"model:   {model_name}\ndata:      {independent_variables}\ndataset: {set_cat.name}",
            loc="left",
        )

    def get_error_table_for_set(self, set_cat: DatasetCategory) -> pd.DataFrame:
        return self.tables[set_cat]

    def show_confusion_matrix(
        self, model_name: str, independent_variables: str, set_cat: DatasetCategory
    ):
        cm_row = self.tables[set_cat][self._metrics[self.__confusion_matrix_index]]

        loc = self._to_loc(model_name, independent_variables)
        if not loc in cm_row.index:
            raise ValueError(
                f"Model ({model_name}) and indebendent variables ({independent_variables}) combination not found"
            )
        cm = cm_row[loc]
        self.__plot_confusion_matrix(cm, model_name, independent_variables, set_cat)
        plt.show()
