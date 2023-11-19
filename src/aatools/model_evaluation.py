
import numpy as np
import pandas as pd


def metrics_by_threshold(y_true, # Ground truth (correct) target values
                         y_proba, # Estimated probability as returned by a binary classifier
                         n_points:int=100): # Number of points on which to evaluate
    """Returns dataframe with several binary classification metrics as a function of the decision threshold"""
    
    # Calculate tn, fp, fn, tp for different thresholds
    cm_thr = []
    for thr in np.linspace(0,1,100):
        y_pred = np.where(y_proba >= thr, 1, 0)
        tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
        cm_thr.append([thr, tn, fp, fn, tp])
   
    cm_thr_df = pd.DataFrame(cm_thr, columns=['thr', 'tn', 'fp', 'fn', 'tp'])
   
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