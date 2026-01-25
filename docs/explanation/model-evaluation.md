# Model evaluation

## metrics-by-threshold

Computes the precision, recall, accuracy, F1-score, specificity and Matthews correlation coefficient for all the thresholds possible from the given dataset.

We use scikit-learn's [roc_curve](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.roc_curve.html) function to compute the [false positive rate](https://en.wikipedia.org/wiki/False_positive_rate) and [true positive rate](https://en.wikipedia.org/wiki/Sensitivity_and_specificity) at different decision thresholds. Together with this we also know the number of element is the positive class $P$ and the number of elements in the negstive class $N$.

To compute each of the metrics we first compute the values of TP, FN, FP and TN at each threshold and then use standard formulas.

$$
\begin{align*}
TP &= TPR \cdot P \\
FN &= P - TP \\
FP &= FPR \cdot N \\
TN &= N - FP
\end{align*}
$$


### Recall

It is given, identical to TPR. It is defined as

$$
TPR = \frac{TP}{P}
$$

we can compute $TP = TPR \cdot P$.

### Precision

Precision is given as,
$$
\text{Precision} = \frac{TP}{TP + FP}
$$

The false positive rate is given by:
$$
FPR = \frac{FP}{N}
$$
which implies we can compute $FP = FPR \cdot N$. 

### Accuracy



### F1-score

### Specificity

### Matthews correlation coefficient
