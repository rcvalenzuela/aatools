
import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix, roc_curve


def metrics_by_threshold(y_true: pd.Series,
                         y_proba: pd.Series) -> pd.DataFrame:
    """Compute binary classification metrics as a function of the decision threshold.

    The returned metrics are the precision, recall, accuracy, F1-score, specificity and Matthews correlation coefficient
    
    See the [design rationale](./explanation/model-evaluation.md) for why this implementation was chosen.

    Args:
        y_true: Ground truth (correct) target values
        y_proba: Estimated probability as returned by a binary classifier

    Returns:
        A `pandas.DataFrame` listing the value of each metric at the corresponding decision thresholds
    """

    # Compute fpr and tpr at different threhsholds
    fpr, tpr, cm_thr = roc_curve(y_true, y_proba)

    # Compute the number of elements in each class
    n_neg = np.sum(y_true == 0)
    n_pos = np.sum(y_true == 1)


    cm_thr_df = pd.DataFrame({'thr':cm_thr})
    cm_thr_df['fp'] = fpr * n_neg
    cm_thr_df['tp'] = tpr * n_pos
    cm_thr_df['tn'] = n_neg - cm_thr_df['fp']
    cm_thr_df['fn'] = n_pos - cm_thr_df['tp']

    ## Calculation of metrics

    cm_thr_df['precision'] = cm_thr_df['tp'] / (cm_thr_df['tp'] + cm_thr_df['fp'])
    cm_thr_df['recall'] = cm_thr_df['tp'] / (cm_thr_df['tp'] + cm_thr_df['fn'])
    cm_thr_df['accuracy'] = (cm_thr_df['tp'] + cm_thr_df['tn']) / (cm_thr_df['tp'] + cm_thr_df['fn'] + cm_thr_df['fp'] + cm_thr_df['tn'])
    cm_thr_df['f1'] = (2*cm_thr_df['tp']) / (2*cm_thr_df['tp'] + cm_thr_df['fn'] + cm_thr_df['fp'])
    cm_thr_df['specificity'] = cm_thr_df['tn'] / (cm_thr_df['tn'] + cm_thr_df['fp'])
    
    # Matthews correlation coefficient
    num_mcc = (cm_thr_df['tp'] * cm_thr_df['tn']) - (cm_thr_df['fp'] * cm_thr_df['fn'])
    subrad_mcc = ((cm_thr_df['tp'] + cm_thr_df['fp']) *
                  (cm_thr_df['tp'] + cm_thr_df['fn']) *
                  (cm_thr_df['tn'] + cm_thr_df['fp']) *
                  (cm_thr_df['tn'] + cm_thr_df['fn']))
    cm_thr_df['mcc'] = num_mcc / np.sqrt(subrad_mcc)

    return cm_thr_df
