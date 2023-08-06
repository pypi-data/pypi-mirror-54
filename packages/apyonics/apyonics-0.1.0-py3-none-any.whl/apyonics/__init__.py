import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from .client import *

def add_to_dataset(ds,sample):
    """Add a sample to a dataset.

    Parameters
    ----------
    ds : pandas.DataFrame
        Dataset to be augmented
    sample : dict
        Sample to add to the dataset, 
        must have a value for each column in the dataset

    Returns
    -------
    new_ds : pandas.DataFrame
        The input dataset with the new sample included
    """
    ds_cols = list(ds.columns)
    samp_cols = sample.keys()
    for col in samp_cols:
        if not col in ds_cols:
            sample.pop(col)
    samp_cols = sample.keys()
    for col in ds_cols:
        if not col in samp_cols:
            raise KeyError('sample does not contain an entry for {}'.format(col))
    new_ds = ds.append(sample,ignore_index=True,verify_integrity=True)
    return new_ds

def save_dataset(ds,filepath):
    """Save a dataset to a local file.

    Parameters
    ----------
    ds : pandas.DataFrame
        Dataset to be saved
    filepath : str
        Path to a local csv file where the dataset should be saved
    """
    ds.to_csv(filepath,index_label='id')
    
def plot_logreg_cfs(results,show=False):
    """Plot the results of logistic regression combinatoric feature selection

    Parameters
    ----------
    results : dict
        Dict of results, for example, client.get_logreg_combo_results(0)['results']
    show : bool
        Determines whether or not the figure should be displayed

    Returns
    -------
    fig : matplotlib.figure.Figure
        matplotlib Figure object containing the rendered plot
    """
    fig = plt.figure()
    n_feats_list = list(results.keys())
    n_feats = np.sort(np.array(n_feats_list))
    f1 = [results[nf]['best_f1'] for nf in n_feats]
    prec = [results[nf]['best_precision'] for nf in n_feats]
    rec = [results[nf]['best_recall'] for nf in n_feats]
    acc = [results[nf]['best_accuracy'] for nf in n_feats]
    plt.plot(n_feats,f1)
    plt.plot(n_feats,prec)
    plt.plot(n_feats,rec)
    plt.plot(n_feats,acc)
    plt.legend(['f1','precision','recall','accuracy'])
    plt.title('best performance metrics over all combinations')
    plt.xlabel('number of features')
    plt.ylabel('performance metrics')
    if show: plt.show()
    return fig

