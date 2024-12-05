from typing import List
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
        self.confussion_mat_entry_format = confussion_mat_entry_format

        if y_true_train is None or y_true_dev is None or y_true_test is None:
            raise ValueError("all arguments must be set to non-null values")

        self.y_true = {
            DatasetCategory.TRAINING: y_true_train,
            DatasetCategory.DEVELOPMENT: y_true_dev,
            DatasetCategory.TEST: y_true_test,
        }
        self.classes = classes

        self._metrics = [
            "MSE",
            "average error",
            "highest error",
            "accuracy",
            "precision (multiclass)",
            "precision (micro)",
            "precision (macro)",
            "recall (multiclass)",
            "recall (micro)",
            "recall (macro)",
            "$F_1$ (multiclass)",
            "$F_1$ (micro)",
            "$F_1$ (macro)",
            "confusion matrix",
        ]

        self.tables = {
            DatasetCategory.TRAINING: pd.DataFrame(columns=self._metrics),
            DatasetCategory.DEVELOPMENT: pd.DataFrame(columns=self._metrics),
            DatasetCategory.TEST: pd.DataFrame(columns=self._metrics),
        }

    def metrics(self) -> List[str]:
        return self._metrics

    def compute_errors_all_sets(
        self,
        model_name: str,
        y_pred_train: ArrayLike,
        y_pred_dev: ArrayLike,
        y_pred_test: ArrayLike,
    ) -> None:
        self.compute_errors(model_name, DatasetCategory.TRAINING, y_pred_train)
        self.compute_errors(model_name, DatasetCategory.DEVELOPMENT, y_pred_dev)
        self.compute_errors(model_name, DatasetCategory.TEST, y_pred_test)

    def compute_errors(
        self, model_name: str, set: DatasetCategory, y_pred: ArrayLike
    ) -> None:

        df_metrics = None
        y_true = None

        df_metrics = self.tables[set]
        if df_metrics is None:
            raise ValueError(f"Error table not found for '{set}'")

        y_true = self.y_true[set]
        if y_true is None:
            raise ValueError(f"'y_true' not found for '{set}'")

        if np.isscalar(y_pred):
            y_pred = np.full_like(y_true, y_pred)

        if len(y_pred) != len(y_true):
            raise ValueError(
                f"Invalid 'y_pred' length, expected: {len(y_true)} or 1, got: {len(y_pred)}"
            )

        # MSE
        df_metrics.loc[model_name, self._metrics[0]] = metrics.mean_squared_error(
            y_true, y_pred
        )
        df_metrics.loc[model_name, self._metrics[1]] = np.average(y_true - y_pred)
        # highest error
        er = y_true - y_pred
        mx = np.max(er)
        mn = np.min(er)
        df_metrics.loc[model_name, self._metrics[2]] = int(mn if abs(mn) > mx else mx)
        # accuracy
        df_metrics.loc[model_name, self._metrics[3]] = metrics.accuracy_score(
            y_true, y_pred
        )
        # precision
        df_metrics.loc[model_name, self._metrics[4]] = [
            round(float(x), 2)
            for x in metrics.precision_score(
                y_true, y_pred, average=None, zero_division=0
            )
        ]
        df_metrics.loc[model_name, self._metrics[5]] = metrics.precision_score(
            y_true, y_pred, average="micro", zero_division=0
        )
        df_metrics.loc[model_name, self._metrics[6]] = metrics.precision_score(
            y_true, y_pred, average="macro", zero_division=0
        )
        # recall
        df_metrics.loc[model_name, self._metrics[7]] = [
            round(float(x), 2)
            for x in metrics.recall_score(y_true, y_pred, average=None)
        ]
        df_metrics.loc[model_name, self._metrics[8]] = metrics.recall_score(
            y_true, y_pred, average="micro"
        )
        df_metrics.loc[model_name, self._metrics[9]] = metrics.recall_score(
            y_true, y_pred, average="macro"
        )
        # F-1
        df_metrics.loc[model_name, self._metrics[10]] = [
            round(float(x), 2) for x in metrics.f1_score(y_true, y_pred, average=None)
        ]
        df_metrics.loc[model_name, self._metrics[11]] = metrics.f1_score(
            y_true, y_pred, average="micro"
        )
        df_metrics.loc[model_name, self._metrics[12]] = metrics.f1_score(
            y_true, y_pred, average="macro"
        )
        df_metrics.loc[model_name, self._metrics[-1]] = metrics.confusion_matrix(
            y_true, y_pred, normalize="true"
        )

    def save_assets(self):
        plt.ioff()
        for ds_type, table in self.tables.items():
            confusion_matrices = table.iloc[:, -1]
            tbl = table.iloc[:, :-1].T
            set_name = ds_type.value
            LatexHelpers.save_as_latex_table(
                tbl,
                name=f"{self.dataset_name}_eval_{set_name}",
                caption=f"Evaluation metrics computed on the {set_name} set",
                path=f"{self.assets_path}/tables",
            )
            for j in range(len(confusion_matrices.index)):
                model_name = confusion_matrices.index[j]
                confusion_matrix = confusion_matrices.iloc[j]
                disp = metrics.ConfusionMatrixDisplay(
                    confusion_matrix=confusion_matrix, display_labels=self.classes
                )
                disp.plot(values_format=self.confussion_mat_entry_format)
                plt.title(
                    f"Confusion matrix for {model_name} model on the {set_name} set"
                )
                plt.savefig(
                    f"{self.assets_path}/figures/{self.dataset_name}_confusion_matrix_{model_name.replace('"','').replace(' ','_')}_{set_name}.png"
                )
                plt.close()
        plt.show()

    def get_error_table_for_set(self, set: DatasetCategory) -> pd.DataFrame:
        return self.tables[set]
    