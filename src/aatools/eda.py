
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def plot_univariate_continuous(df:pd.DataFrame, # Data
                               var:str, # Variable to plot
                               var_name:str, # Variable name
                               ax): # Axes on which to draw the plot
   
    ## Calculate the quantiles
    df_plot = df[[var]].copy()
    df_plot['qcut'] = pd.qcut(df_plot[var], [0, 0.25, 0.75, 1], labels=['1st', 'iqr', '4th'])
   
    # Define the palette
    # color palette as dictionary
    palette = {"1st":"silver",
               "iqr":"gold",
               "4th":"silver"}
   
    # Create a density plot
    sns.histplot(data=df_plot,
                 x=var,
                 stat='percent',
                 ax=ax,
                 hue='qcut',
                 multiple='stack',
                 palette=palette)
   
   
    # Remove legend
    ax.get_legend().remove()
   
    # Add a vertical line at the mean
    var_mean = df[var].mean()
   
    ax.axvline(var_mean)
   
    # Add labels
    ax.set_xlabel(var_name, fontfamily='Century Gothic', fontsize=16)
    ax.set_ylabel('Percent', fontfamily='Century Gothic', fontsize=16)
   
    # Set tick font size
    for label in (ax.get_xticklabels() + ax.get_yticklabels()):
        label.set_name('Century Gothic')
        label.set_size(12)
   
    return ax


def plot_univariate_nominal(df:pd.DataFrame, # Data
                            var:str, # Variable to plot
                            var_name:str, # Variable name
                            ax): # Axes on which to draw the plot
    pass


def rr_corr(df:pd.DataFrame, # Data
            ratio_vars:list): # Columns in `df` with ratio variables
    """
    Correlation between all pairs of ratio variables in `df`
    
    Uses the `corr` method of `pandas.DataFrame` 
    """
    
    # Extract ratio variables
    df_corr = df[ratio_vars].copy()
    
    # Calculate the correlation between ratio features in the dataset
    df_corr = df.corr()
    
    # Reshape into a table removing redundant pairs
    df_corr = df_corr.where(np.triu(np.ones(df_corr.shape), 1).astype(bool))
    df_corr = df_corr.stack().reset_index()
    df_corr.columns = ['feat_1', 'feat_2', 'value']
    df_corr['metric'] = "Pearson correlation coefficient"
    
    # Absolute value of correlation is used since we only search for association
    df_corr['assoc_strength'] = df_corr['value'].abs()
    df_corr['assoc_strength'] = pd.cut(df_corr['assoc_strength'], 
                                       bins=[0, 0.2, 0.5, 1], 
                                       labels=['weak', 'moderate', 'strong'])
    
    return df_corr.sort_values('assoc_strength', ascending=False)


def strength_of_assoc(df:pd.DataFrame, # Data
                      ratio_vars:list=None, # Columns in `df` with ratio variables
                      ordinal_vars:list=None, # Columns in `df` with ordinal variables
                      nominal_vars:list=None, # Columns in `df` with nominal variables
                      binary_vars:list=None): # Columns in `df` with binary variables
    # Initialize results dataframe
    soa_df = []
    
    ## Calculate strength of association between different variables
    # Ratio - Ratio
    if ratio_vars:
        soa_df.append(rr_corr(df, ratio_vars))
    
    # Ratio - Ordinal
    # Ratio - Nominal
    # Ratio - Binary
    # Ordinal - Ordinal
    # Ordinal - Nominal
    # Ordinal - Binary
    # Nominal - Nominal
    # Nominal - Binary
    # Binary - Binary
    
    return pd.concat(soa_df)


def rb_corr(df:pd.DataFrame, # Data
            ratio_vars:list, # Columns in `df` with ratio variables
            binary_vars:list): # Columns in `df` with 2-level nominal variables (i.e. binary)
    
    bin_feat = df[binary_vars].copy()


def ro_corr(df:pd.DataFrame, # Data
            ratio_vars:list, # Columns in `df` with ratio variables
            ordinal_vars:list): # Columns in `df` with ordinal variables
    """
    
    All the ordinal variables must have an ordered category dtype
    """
    for ov in ordinal_vars:
        if not df[ov].cat.ordered:
            raise TypeError(f'{ov} is not ordered')
    
    kendall_tau = []
    for rv,ov in zip(ratio_vars, ordinal_vars):
        kendall_tau.append(stats.kendalltau(df[rv], df[ov]))
    
    return kendall_tau


def soa_graph(cdf:pd.DataFrame, # A dataframe as output by `ratio_corr`
               min_strength:str='strong'): # Threshold for high correlation
    
    # Filter values below min_strength (weak < moderate < strong)
    if min_strength == 'strong':
        filter_list = ['strong']
    elif min_strength == 'moderate':
        filter_list = ['moderate', 'strong']
    else:
        filter_list = ['weak', 'moderate', 'strong']
    
    high_soa = cdf[cdf.assoc_strength.isin(filter_list)].copy()
    
    # Sort for visualization
    high_soa = high_soa.sort_values(['assoc_strength', 'feat_1', 'feat_2'], ascending=False)
    
    # Generate the graph
    soa_graph = nx.from_pandas_edgelist(high_soa, 'feat_1', 'feat_2')
    for node in soa_graph.nodes():
        soa_graph.nodes[node]['label'] = node
            
    return high_soa, soa_graph


def continuous_mi(df:pd.DataFrame): # Data
    
    # Keep only numeric variables
    num_df = df.select_dtypes(include=[np.number]).copy()
    
    # Define the variables
    feats = num_df.columns.to_list()
    
    # Initialize
    dfs = list()
    
    for feat in feats:
        # Define columns to use
        subset_feat = feats.copy()
        #subset_feat.remove(feat)
        X = num_df[subset_feat].copy()
        y = num_df[feat].ravel()
        
        mi_Xy = skfl.mutual_info_regression(X, y)
        
        dfi = pd.DataFrame(data={'feat_1':subset_feat, 'feat_2':feat, 'mutual_info':mi_Xy})
        dfs.append(dfi)
        
    return pd.concat(dfs)    