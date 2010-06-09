import numpy as np
import csv
from itertools import product
from pal.nan import mean as nanmean

class Dataset:
    def __init__(self, csv_path, dv, subject):
        self.design = {}
        self.group_indices = {}
        self.level_indices = {}
        self.ivs = None
        self.dv = dv
        self.subject = subject
        self.rawdata = None
        self.data = None

        # Get the first line of the .csv containing experimental data, which is
        # assumed to be a row of labels for each column.
        file_data = csv.reader(open(csv_path))
        csv_labels = file_data.next()

        tmparr = np.rec.fromrecords([tuple(x) for x in file_data],
                                    names=csv_labels)

        self.ivs = [x for x in csv_labels if x != dv]

        # Characterize the semantic structure of the experiment
        for v in self.ivs:
            self.design[v] = []
            for entry in tmparr[v]:
                if entry not in self.design[v]:
                    self.design[v].append(entry)

        # Compute mappings from:
        #     Treatment groups to indices (`group_indices`)
        #     Levels within groups to indices (`level_indices`)
        i = 0
        for g in self.ivs:
            self.group_indices[g] = i
            i += 1

            j = 0
            for l in self.design[g]:
                self.level_indices[(g,l)] = j
                j += 1

        treatments = tuple(product(*tuple(self.design[x] for x in self.ivs)))

        # Read data from .csv and partition up to repeated measures
        partitions = {}
        for t in tmparr:
            tk = tuple([t[n] for n in self.ivs])
            if tk not in partitions:
                partitions[tk] = [np.float64(t[dv])]
            else:
                partitions[tk] = partitions[tk] + [np.float64(t[dv])]

        newshape = [len(set(tmparr[n])) for n in tmparr.dtype.names if n != dv]
        newshape.append(max([len(x) for x in partitions.values()]))
        newshape = tuple(newshape)

        self.rawdata = np.zeros(shape=newshape) * np.nan

        for k in partitions:
            gk = tuple(zip(self.ivs, k))

            index = tuple([self.level_indices[k0] for k0 in gk])
            index = [Ellipsis for dimension in self.rawdata.shape]
            for k0 in gk:
                index[self.group_indices[k0[0]]] = self.level_indices[k0]
            index = tuple(index)

            for i in xrange(len(partitions[k])):
                self.rawdata[index][i] = partitions[k][i]

        tmp = np.ones(shape=self.rawdata.shape)
        
        # Generate the keys that will let us extract the last dimensions.
        # i.e., for an array of shape: 
        #     (a_1, ... a_(k-1), a_k),
        # we should get all possible tuples of the shape:
        #     (b_1, ..., b_(k-1), Ellipsis)
        # Where b_1 is in range(a_1),
        #       b_2 is in range(a_2),
        #         ...
        #       b_(k-1) is in range(a_(k-1))
        keys = [x for x in apply(product,
                                 map(range,
                                     self.rawdata.shape[:-1]) + [[Ellipsis]])]

        newshape = self.rawdata.shape[:-1] + (1,)
        self.data = np.ones(shape=newshape)
        for k in keys:
            k2 = k[:-1] + (0,)
            self.data[k2] = nanmean(self.rawdata[k])

    def view(self, var_dict):
        t = [Ellipsis for i in self.data.shape]
        for var in var_dict:
            i = self.group_indices[var]
            k = tuple([self.level_indices[(var,x)] for x in var_dict[var]])
            t[i] = k
        t = tuple(t)

        # Account for fact that the advanced index:
        #   ((0,1),(0,1,2),(0,1))
        # is not equivalent to the advanced index:
        #   (Ellipsis,Ellipsis,Ellipsis)
        def fixtuple(t):
            fixed = []
            for i in xrange(len(t)):
                if t[i] is Ellipsis:
                    fixed.append(Ellipsis)
                elif len(t[i]) == self.data.shape[i]:
                    fixed.append(Ellipsis)
                else:
                    fixed.append(t[i])
            return tuple(fixed)

        return self.data[fixtuple(t)]

class DatasetView:
    def __init__(self, dat, vars=None):
        # Stats
        self.data = None
        self.treatments = None

        self.mean = None
        self.sd = None
        self.se = None
        self.n = None

        # Extract data we care about, as indicated by vars
        # This breaks indexing in a way that is a huge pain
        if vars is None:
            self.data = dat.data
            self.treatments = np.array([str(x) for x in 
                                        product(*[dat.design[x] for x in dat.ivs])])
            vars = dat.design
        else:
            self.data = dat.view(vars)
            self.treatments = np.array([str(x) for x in
                                        product(*vars.values())])

        self.n = np.ones(shape=self.treatments.shape)
        self.mean = np.ones(shape=self.treatments.shape)
        self.sd = np.ones(shape=self.treatments.shape)
        self.se = np.ones(shape=self.treatments.shape)

        def index_from_tuple(t):
            index = [Ellipsis] * len(self.data.shape)

            for i in xrange(len(dat.ivs)):
                group = dat.ivs[i]
                j = dat.group_indices[group]
                index[j] = dat.level_indices[(group,t[i])]
            return tuple(index)

        for i in xrange(len(self.treatments)):
            t = eval(self.treatments[i])
            j = index_from_tuple(t)
            jdata = np.array([x for x in dat.data[j].flatten() if not np.isnan(x)])
            print "jdata",jdata

            n = len(jdata)
            mean = jdata.mean()
            sd = jdata.std()
            se = sd / np.sqrt(n)
            
            self.n[i] = n
            self.mean[i] = mean
            self.sd[i] = sd
            self.se[i] = se
