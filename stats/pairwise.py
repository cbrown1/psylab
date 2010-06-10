import numpy as np
from scipy import stats

def bonferroni(p,k):
    # Ref: http://books.google.com/books?id=3jpvrEhozGgC&pg=PA70
    return p*k

def sidak(p,k):
    # Ref: http://books.google.com/books?id=3jpvrEhozGgC&pg=PA70
    return 1.0 - (1.0 - p)**k

def paired_diff_test(data, comparisons, correction=bonferroni,
                     factors=None,
                     levels=None):
    """Compute a table of pairwise comparisons.

    Parameters:
    -----------
    data : numpy.ndarray
        Representation of the experimental data.

    comparisons : list or tuple
        A list of pairs of the form `(ii,jj)`, where `ii` and `jj` are lists of
        advanced indices used to pull samples out of `data`.

    correction : function
        The correction function to adjust for multiplicity of tests.

    factors : list or tuple
        String of human-readable factor names.

    Returns:
    --------
    result : list
        
    """

    if factors is None: #If factors aren't specified
        num_factors = len(data.shape) - 1
        if num_factors <= 26: # If the factor dimensions can be mapped to
                                 # letters of the alphabet...
            factors = [x for x in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[:num_factors]]
        else: # just give them indexed dummy names
            factors = tuple("F%s" % (i) for i in xrange(len(data.shape)-1))

    def samplename(indices):
        index = tuple(tuple(sorted(set(y))) for y in zip(*indices))

        name = []
        # This is broken if level names are actually passed
        for i in xrange(len(index)-1):
            case = index[i]
            if case[0] == Ellipsis:
                pass
            elif len(case) == 1:
                name.append("%s[%d]" % (factors[i], index[i][0]))
            else:
                if index[i] == tuple(xrange(index[i][0],index[i][-1]+1)):
                    name.append("%s[%d:%d]" % 
                                (factors[i], index[i][0],index[i][-1]+1))
                else:
                    name.append("%s[%s]" % 
                                (factors[i],
                                 (",".join(map(str, index[i])))))
        return ",".join(name)

    k = len(comparisons)
    result = []
    for x in comparisons:
        ii,jj = x

        comp_str = " -- ".join(map(samplename, (ii,jj)))

        sample_a = []
        for i in ii:
            sample_a.extend(data[i].flatten())
        sample_a = np.array(sample_a)

        sample_b = []
        for j in jj:
            sample_b.extend(data[j].flatten())
        sample_b = np.array(sample_b)

        t,p = stats.ttest_ind(sample_a, sample_b)
        adjp = correction(p,k)
        result.append((comp_str, t, adjp))
    return result
