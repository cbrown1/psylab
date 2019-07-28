import numpy as np


def rms_error(data, groupby, data_col, rms_col_title='rms'):
    """
    rms_error takes a pandas dataframe, and computes rms error
    based on the levels in the column names specified in groupby

    For each group, a mean will be computed and subtracted from each score.
    Then, the rms (root-mean-square) of all the difference scores will be
    computed, which is the square-root of the mean of the squared differences.

    Parameters
    ----------
    data : pandas dataframe
        The dataframe
    groupby : list of str
        A list of column names to sort data on, in the same form that you
        would pass to pd.groupby
    data_col : str
        The name of the column on which to compute the rms values
    rms_col_title : str
        The name to assign to the newly created rms data column. Default = 'rms'

    Returns
    -------
    new_data : pandas dataframe
        Will contain rms error values along with the groupby variables

    Example
    -------
    >>> a = pd.DataFrame({'proc': [1,1,1, 2,2,2, 3,3,3], 'scores': [4,5,6, 2,5,7, 0,5,10]})
    >>> rms_error(a,['proc'],'scores')
       proc       rms
    0     1  0.816497
    1     2  2.449490
    2     3  4.082483
    >>> np.sqrt(np.mean(np.square((-1,0,1)))) # Mean-diff scores for [4,5,6]
    0.81649658092772603
    >>> np.sqrt(np.mean(np.square((-3,0,3)))) # Mean-diff scores for [2,5,8]
    2.4494897427831779
    >>> np.sqrt(np.mean(np.square((-5,0,5)))) # Mean-diff scores for [0,5,10]
    4.0824829046386304
    """

    data_diff_fun = lambda data: data - data.mean()
    new_data = data.copy()
    new_data['diff'] = data.groupby(groupby).transform(data_diff_fun)[data_col]
    new_data['diff_sq'] = new_data['diff']**2
    new_data = new_data.groupby(groupby).agg(np.mean).reset_index()
    new_data[rms_col_title] = np.sqrt(new_data['diff_sq'])

    return new_data[groupby].join(new_data[rms_col_title])

