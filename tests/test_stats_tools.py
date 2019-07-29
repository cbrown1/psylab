# -*- coding: utf-8 -*-

import numpy as np
import numpy.testing as np_testing
import pandas as pd
import psylab


def test_anova_between():
    # F values taken from
    # http://davidmlane.com/hyperstat/factorial_ANOVA.html
    ref = np.array([273.03754266, 535.15358362, 246.41638225, 141.54266212,
        55.29010239,  60.31399317,   7.89078498,          np.nan,
                np.nan])

    d = psylab.tools.stats_tools.dataview.from_csv("tests/data/hyperstat_3f_between.csv", dv="dv")
    # Or: an = d.anova_between()
    an = psylab.tools.stats_tools.anova_between(d.data)

    np_testing.assert_allclose(an.f, ref)
    return


def test_anova_within():
    # F values taken from
    # http://davidmlane.com/hyperstat/within-subjects.html
    ref = np.array([33., 24.81818182, 3., np.nan, np.nan, np.nan, np.nan, np.nan])

    d = psylab.tools.stats_tools.dataview.from_csv("tests/data/hyperstat_2f_within.csv", dv="dv")
    an = psylab.tools.stats_tools.anova_within(d.data)

    np_testing.assert_allclose(an.f, ref)
    return


def test_anova_table():

    ref = """source                ss        df        ms         f         p
Task           1000.0000    1.0000 1000.0000  273.0375    0.0000  ***
Age            1960.0000    1.0000 1960.0000  535.1536    0.0000  ***
Stim            902.5000    1.0000  902.5000  246.4164    0.0000  ***
Task*Age        518.4000    1.0000  518.4000  141.5427    0.0000  ***
Task*Stim       202.5000    1.0000  202.5000   55.2901    0.0000  ***
Age*Stim        220.9000    1.0000  220.9000   60.3140    0.0000  ***
Task*Age*Stim    28.9000    1.0000   28.9000    7.8908    0.0084  **
error           117.2000   32.0000    3.6625
total          4950.4000   39.0000
"""

    d = psylab.tools.stats_tools.dataview.from_csv("tests/data/hyperstat_3f_between.csv", dv="dv")
    an = d.anova_between()
    table = psylab.tools.stats_tools.anova_table(an)
    assert ref == table
    return


def test_pairwise():

    ref = [('Task[0],Age[1],Stim[1] -- Task[0],Age[1],Stim[0]', -34.00000000000001, 6.117916422272445e-10)]

    d = psylab.tools.stats_tools.dataview.from_csv("tests/data/hyperstat_3f_between.csv", dv="dv")

    ci = d.indices_from_comparison([
    [{'Task':['1'],'Age':['C'], 'Stim':['W']},{'Task':['1'],'Age':['C'], 'Stim':['P']}],
    ])
    c = psylab.tools.stats_tools.pairwise_comparisons(d.data,ci, correction=psylab.tools.stats_tools.bonferroni, factors=["Task", "Age", "Stim"])
    assert ref == c
    return


def test_pairwise_table():

    ref = """                                      Comparison:          Mean Diff;                      p
Task[0],Age[0],Stim[1] -- Task[0],Age[0],Stim[0]: -5.828933915240022; 0.00039203885258633193
"""
    d = psylab.tools.stats_tools.dataview.from_csv("tests/data/hyperstat_3f_between.csv", dv="dv")
    an = d.anova_between()

    ci = d.indices_from_comparison([
    [{'Task':['1'],'Age':['A'], 'Stim':['W']},{'Task':['1'],'Age':['A'], 'Stim':['P']}],
    ])
    c = psylab.tools.stats_tools.pairwise_comparisons(d.data,ci, correction=psylab.tools.stats_tools.bonferroni, factors=["Task", "Age", "Stim"])
    t = psylab.tools.stats_tools.pairwise_table(c)
    assert ref == t
    return


def test_dataview_ivs():

    ref = ('size', 'color')
    d = psylab.tools.stats_tools.dataview.from_csv("tests/data/small_2x3.csv", dv="score")
    assert ref == d.ivs
    return


def test_dataview_dv():

    ref = 'score'
    d = psylab.tools.stats_tools.dataview.from_csv("tests/data/small_2x3.csv", dv="score")
    assert ref == d.dv
    return


def test_dataview_design():

    ref = {'color': ('blue', 'red'), 'score': None, 'size': ('small', 'med', 'large')}
    d = psylab.tools.stats_tools.dataview.from_csv("tests/data/small_2x3.csv", dv="score")
    assert ref == d.design
    return


def test_dataview_filter_ivs():

    ref = {'color': (), 'score': None, 'size': ('small', 'med', 'large')}
    # Get only 1 variable
    d = psylab.tools.stats_tools.dataview.from_csv("tests/data/small_2x3.csv", "score", ['size'])
    assert ref == d.design
    return



def test_dataview_view_data():

    ref = np.array([4.49000003, 5.13000002])
    # Get only specified variable levels
    d = psylab.tools.stats_tools.dataview.from_csv("tests/data/three.csv", dv="dv")
    v = d.view({'a':['a1'],'b':['b1','b2']})
    np_testing.assert_allclose(ref, v.mean)
    return


def test_dataview_view_looks():

    d = psylab.tools.stats_tools.dataview.from_csv("tests/data/1f_within.csv", dv="dv")
    # No multiple-looks var
    v1 = d.view({'a':[]})
    # With multiple-looks var
    v2 = d.view({'a':[]},looks='s')

    # Means are the same
    np_testing.assert_allclose(v1.mean, v2.mean)
    # But n's are different, since 3 scores per subject, per treatment
    np_testing.assert_allclose(v2.n * 3, v1.n)
    return


def test_rau():
    ref = np.array([-0.23      ,  0.06905584,  0.20094416,  0.30875477,  0.40642244,
        0.5       ,  0.59357756,  0.69124523,  0.79905584,  0.93094416,
        1.23      ])
    data = np.linspace(0, 1, 11)
    rdata = psylab.tools.stats_tools.rau(data)
    np_testing.assert_allclose(ref, rdata)
    return


def test_rms_error():
    ref = np.array([0.81649658, 2.05480467, 4.0824829 ])
    data = pd.DataFrame({'proc': [1,1,1, 2,2,2, 3,3,3], 'scores': [4,5,6, 2,5,7, 0,5,10]})
    rmse = psylab.tools.stats_tools.rms_error(data,['proc'],'scores')
    np_testing.assert_allclose(ref, rmse['rms'].values)
    return


def test_cumr2():
    ref = np.array([       np.nan, 1.        , 1.        , 1.        , 1.        ,
       1.        , 0.98463115, 0.97339205, 0.96969697, 0.97013614])
    x = np.linspace(1,10,10)
    y = np.concatenate((np.linspace(1,5,5), np.linspace(6,14,5)))
    r2 = psylab.tools.stats_tools.cumr2(x,y)
    np_testing.assert_allclose(ref, r2)
    return

