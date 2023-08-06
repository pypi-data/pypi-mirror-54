
from patsy import dmatrices
from scipy.optimize import curve_fit
from scipy.stats import chi2
from sklearn.metrics import roc_curve
from statsmodels.stats.outliers_influence import variance_inflation_factor
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm


# Complete
class Interval():
    '''A connected 1-d Interval.'''

    def __init__(self, start, stop = None):
        '''(Interval, args[, number]) -> None

        Initialize an Interval.

        Possible start:
        1) one number num: initializes (-inf, num]; 
            if num == np.inf, then it initializes (-inf, inf).
        2) [num0, num1]: initializes [num0, num1] if num0 <= num1;
            if num1 == np.inf, then it initializes [num0, inf).
        3) (num0, num1): initializes (num0, num1) if num0 <= num1
        
        If both start and end are specified, then it initializes 
        (start, stop] given start <= stop. If stop == np.inf, 
        then this initializes (start, inf).

        >>> int1 = Interval(.45)
        >>> int1
        (-inf, 0.45]
        >>> int2 = Interval([.96, 1.03])
        >>> int2
        [.96, 1.03]
        >>> int3 = Interval((2.1, 5))
        >>> int3
        (2.1, 5)
        >>> int4 = Interval(2.1, 5)
        >>> int4
        (2.1, 5]
        '''

        if stop is None:
            if isinstance(start, (float, int)):
                ep = int(start) if isinstance(start, bool) else start
                self.__lower = -np.inf
                self.__upper = ep
                self.loweropen = True
                self.upperopen = True if ep == np.inf else False
            elif isinstance(start, (list, tuple)):
                assert len(start) == 2, \
                    "The length of an argument must be 2, not " +\
                    str(len(start)) + "."
                assert isinstance(start[0], (float, int)) and \
                    isinstance(start[1], (float, int)), \
                    'If two endpoints are given, then both points ' +\
                    'must be a number. Currently, they are of ' +\
                    str(type(start[0])) + ' and ' +\
                    str(type(start[1])) + '.'
                assert start[0] <= start[1], \
                    "Numbers in iterables must be ordered."
                self.__lower = int(start[0]) if isinstance(start[0], bool)\
                    else start[0] 
                self.__upper = int(start[1]) if isinstance(start[1], bool)\
                    else start[1]
                self.loweropen = False if isinstance(start, list) else True
                self.upperopen = False if isinstance(start, list) else True
            else:
                msg = "Interval is initialized with a number, list, or " +\
                    "tuple; don't know how to initialize " +\
                    str(type(start)) + "."
                raise TypeError(msg)
        else:
            assert isinstance(start, (float, int)) and \
                isinstance(stop, (float, int)), \
                'If two endpoints are given, then both points ' +\
                'must be a number. Currently, they are of ' +\
                '{0} and {1}.'.format(type(start), type(stop))
            assert start <= stop, \
                'The given endpoints are ' + str(start) +\
                ' and ' + str(stop) + ', in that order. ' +\
                'Change the order of the two and try again.'
            ep0 = int(start) if isinstance(start, bool) else start
            ep1 = int(stop) if isinstance(stop, bool) else stop
            self.__lower = ep0
            self.__upper = ep1
            self.loweropen = True
            self.upperopen = True if stop == np.inf else False

    def __contains__(self, item):
        a = self.get_lower()
        b = self.get_upper()
        if isinstance(item, (float, int)):
            if item < a:
                return False
            elif item == a:
                return False if self.loweropen else True
            elif a < item < b:
                return True
            elif item == b:
                return False if self.upperopen else True
            else:
                return False
        elif isinstance(item, Interval):
            c = item.get_lower()
            d = item.get_upper()
            if a > c or b < d:
                return False
            elif a < c and b > d:
                return True
            else:
                if c == a:
                    if self.loweropen and not item.loweropen:
                        return False
                    else:
                        if d < b:
                            return True
                        else:
                            if self.upperopen and not item.upperopen:
                                return False
                            else:
                                return True
                else:
                    if self.upperopen and not item.upperopen:
                        return False
                    else:
                        return True
        elif isinstance(item, (list, tuple)):
            return Interval(item) in self
        else:
            return False

    def __repr__(self):
        return str(self)

    def __str__(self):
        left = '(' if self.loweropen else '['
        right = ')' if self.upperopen else ']'
        result = left + '{0}, {1}' + right
        return result.format(self.__lower, self.__upper)

    def get_lower(self):
        return self.__lower

    def get_upper(self):
        return self.__upper

    def set_lower(self, value):
        assert isinstance(value, (float, int)), \
            "A lower bound of Interval must be a number, not " +\
            str(type(value)) + "."
        value = int(value) if isinstance(value, bool) else value
        assert value <= self.__upper, \
            "lower bound <= upper bound not satisfied. " +\
            "Your value is " + str(value) + ", whereas the " +\
            "upper bound is " + str(self.__upper) + "."
        self.__lower = value

    def set_upper(self, value):
        assert isinstance(value, (float, int)), \
            "An upper bound of Interval must be a number, not " +\
            str(type(value)) + "."
        value = int(value) if isinstance(value, bool) else value
        assert value >= self.__lower, \
            "upper bound >= lower bound not satisfied. " +\
            "Your value is " + str(value) + ", whereas the " +\
            "lower bound is " + str(self.__lower) + "."
        self.__upper = value
class Pipe():
    '''A class that enables you to Pipe.'''

    def __init__(self, obj):
        '''
        Initialize the function piping mechanism.
        '''

        self.obj = obj

    def __repr__(self):
        '''
        Print the representation of self.
        '''

        return str(self.obj)

    def collect(self):
        '''
        Collect the result of piping.
        '''

        return self.obj

    def pipe(self, func, *args, **kwargs):
        '''
        Pipe.
        '''
    
        return Pipe(func(self.obj, *args, **kwargs))
def add_intercept(data, int_name = 'Intercept', loc = 0, inplace = False):
    '''(pd.DataFrame[, str, int, bool]) -> pd.DataFrame
    
    Precondition: 
    1. -(len(data.columns) + 1) <= loc <= len(data.columns)
    2. int_name not in data.columns
    
    Add the column of 1s with the name int_name to data at the 
    specified loc. data is mutated if inplace is True (False by default).
    '''
    
    all_cols_before_intercept = list(data.columns)
    assert int_name not in all_cols_before_intercept, \
        '{0} already exists in data. Try different int_name.'\
        .format(int_name)
    assert -(len(data.columns) + 1) <= loc <= len(data.columns), \
        'loc must be in between {0} and {1}. Current loc is {2}.'\
        .format(-(len(data.columns) + 1), len(data.columns), loc)
    if loc < 0:
        loc += len(data.columns) + 1
    if inplace:
        data.insert(loc, int_name, 1)
    else:
        data_cp = data.copy()
        data_cp.insert(loc, int_name, 1)
        return data_cp
def additive_terms(terms):
    '''([str]) -> str

    Return the additive terms of the formula with terms.

    >>> additive_terms(['a', 'b', 'c'])
    'a + b + c'
    '''

    return ''.join(map(lambda x: x + ' + ', terms))[:-3]
def dcast(data, formula, value_var = None):
    '''(pd.DataFrame, str[, str]) -> pd.DataFrame
    
    Return the grouped DataFrame based on data and formula. If value_var
    is specified, then it is used to populate the output DataFrame; if
    not specified, then it is guessed from data and formula.
    '''
    
    all_cols = list(data.columns)
    indices_input = []
    indices = formula[:(formula.index('~'))].split('+')
    if len(indices) == 1:
        indices = indices[0].strip()
        indices_input.append(data[indices])
        cols_used = [indices]
    else:
        indices = list(map(lambda x: x.strip(), indices))
        for ind in indices:
            indices_input.append(data[ind])
        cols_used = indices[:]
        
    cols_input = []
    cols = formula[(formula.index('~') + 1):].split('+')
    if len(cols) == 1:
        cols = cols[0].strip()
        cols_input.append(data[cols])
        cols_used.append(cols)
    else:
        cols = list(map(lambda x: x.strip(), cols))
        for c in cols:
            cols_input.append(data[c])
        cols_used.extend(cols)
        
    value_col = list(set(all_cols).difference(set(cols_used)))
    assert len(value_col) == 1 or value_var is not None, \
        'value column ambiguous; should be one of: {0}'.format(value_col)
    if len(value_col) == 1:
        value_col = value_col[0]
    elif value_var is not None:
        value_col = value_var
    
    return pd.crosstab(
        index = indices_input, 
        columns = cols_input,
        values = data[value_col],
        aggfunc = lambda x: x
    )
def determine_type(actual, pred, p_thres):
    '''(np.array, np.array, float) -> np.array
    
    Determine classification types ('tpn', 'fp', or 'fn') using 
    actual, pred, and p_thres.
    '''
    
    def classifier(y, yhat):
        if ((y == 0) & (yhat == 0)) | ((y == 1) & (yhat == 1)):
            return 'tpn'
        elif (y == 0) & (yhat == 1):
            return 'fp'
        else:
            return 'fn'
    classified = pred > p_thres
    result = np.array(list(map(classifier, actual, classified)))
    
    return result
def dist_to_point(X, point):
    '''(pd.DataFrame or np.array, np.array) -> float or np.array
    
    Precondition: X.shape[1] == len(point)
    
    Calculate the distance from each row of X to the point.
    '''
    
    X = X.values if 'pandas' in str(type(X)) else X
    return np.array(list(map(lambda row: np.linalg.norm(row - point), X)))
def fft_curve(tt, yy, only_sin = False):
    '''(array-like, array-like, bool) -> {str: number, lambda, or tuple}
    
    Estimate sin + cos curve of yy through the input time sequence tt, 
    and return fitting parameters "amp", "omega", "phase", "offset",
    "freq", "period", and "fitfunc". Set only_sin = True to fit only a
    sine curve.
    
    Reference: https://stackoverflow.com/questions/16716302/how-do-i-fit-a-sine-curve-to-my-data-with-pylab-and-numpy
    '''
    
    tt = np.array(tt)
    yy = np.array(yy)
    assert len(set(np.diff(tt))) == 1, \
        'tt does not have an uniform spacing.'
    ff = np.fft.fftfreq(len(tt), (tt[1] - tt[0])) # assume uniform spacing
    Fyy = abs(np.fft.fft(yy))
    # excluding the zero frequency "peak", which is related to offset
    guess_freq = abs(ff[np.argmax(Fyy[1:]) + 1])
    guess_amp = np.std(yy) * 2. ** 0.5
    guess_offset = np.mean(yy)
    guess = [
        guess_amp, 
        2. * np.pi * guess_freq, 
        0., 
        guess_offset      
    ]
    def sinfunc(t, A_1, w_1, p_1, c): 
        return A_1 * np.sin(w_1 * t + p_1) + c    
    if only_sin:
        guess = np.array(guess)
        popt, pcov = curve_fit(sinfunc, tt, yy, p0 = guess)
        A_1, w_1, p_1, c = popt
        fitfunc = lambda t: sinfunc(t, A_1, w_1, p_1, c)
        A_2, w_2, p_2 = 0, 0, 0
    else:
        def curve(t, A_1, w_1, p_1, c, A_2, w_2, p_2):
            return sinfunc(t, A_1, w_1, p_1, c) +\
                A_2 * np.cos(w_2 * t + p_2)
        guess.extend([
            guess_amp, 
            2. * np.pi * guess_freq, 
            0.
        ])
        guess = np.array(guess) / 2
        popt, pcov = curve_fit(curve, tt, yy, p0 = guess)
        A_1, w_1, p_1, c, A_2, w_2, p_2 = popt
        fitfunc = lambda t: curve(t, A_1, w_1, p_1, c, A_2, w_2, p_2)
    
    return {
        "amp": [A_1, A_2], 
        "omega": [w_1, w_2], 
        "phase": [p_1, p_2], 
        "offset": c,
        "fitfunc": fitfunc, 
        "maxcov": np.max(pcov), 
        "rawres": (guess, popt, pcov)
    }
def gauss_seidel(y, B = None, theta = None, lambd = None, max_iter = 50, 
                 eps = 1e-08):
    '''(1d-array[, 2d-array, 1d-array, float, int, float]) -> 
        {str: np.array and str: number}

    Preconditions:
    1. If B is None, then lambd must not be None and lambd > 0, as well as
        len(y) >= 5.
    2. If B is not None, then B must be either strictly diagonally
        dominant, symmetric positive definite, or both.
    3. If theta is not None, then len(y) == len(theta).
    4. eps > 0
    5. max_iter >= 1

    Approximate theta that solves the linear equation y = B @ theta,
    where len(y) == n and B is n-by-n, using the Gauss-Seidel method. 
    If B is specified, then lambd is ignored; if B is not specified, 
    then lambd must be positive and be specified since the following 
    B will be used in the equation:

    >>> n = len(y) # must be at least 5
    >>> B_lambd = np.zeros(n ** 2).reshape(n, n)
    >>> B_lambd[0, [0, 1, 2]] = [1, -2, 1]
    >>> B_lambd[1, [0, 1, 2, 3]] = [-2, 5, -4, 1]
    >>> for j in range(2, n - 2):
    ...     B_lambd[j, [j - 2, j - 1, j, j + 1, j + 2]] = [1, -4, 6, -4, 1]
    ...   
    >>> B_lambd[n - 2, [-4, -3, -2, -1]] = [1, -4, 5, -2] 
    >>> B_lambd[n - 1, [-3, -2, -1]] = [1, -2, 1]
    >>> B_lambd = lambd * B_lambd
    >>> B = B_lambd + np.identity(n)

    If theta is None, then the initial guess starts with theta = y.
    '''

    assert eps > 0, 'eps must be positive. Current value: ' + str(eps)
    max_iter = int(max_iter)
    assert max_iter >= 1, \
        'max_iter must be at least 1. Current value: ' + str(max_iter)
    y = np.array(y)
    n = len(y)
    if B is None:
        msg = 'If B is None, then lambd must be '
        assert lambd is not None, msg + 'specified.'
        assert lambd > 0, msg + 'positive. Current lambd == ' + str(lambd)
        assert n >= 5, \
            'If B is None, then len(y) must be at least 5. ' +\
            'Currently, len(y) == ' + str(n) + '.'
        B_lambd = np.zeros(n ** 2).reshape(n, n)
        B_lambd[0, [0, 1, 2]] = [1, -2, 1]
        B_lambd[1, [0, 1, 2, 3]] = [-2, 5, -4, 1]
        for j in range(2, n - 2):
            B_lambd[j, [j - 2, j - 1, j, j + 1, j + 2]] = [1, -4, 6, -4, 1]
        B_lambd[n - 2, [-4, -3, -2, -1]] = [1, -4, 5, -2] 
        B_lambd[n - 1, [-3, -2, -1]] = [1, -2, 1]
        B_lambd = lambd * B_lambd
        B = B_lambd + np.identity(n)
    else:
        B = np.array(B).copy()
        assert B.shape == (n, n), \
            'B.shape == {0}, not {1}'.format(B.shape, (n, n))
        if (abs(B).sum(axis = 0) - 2 * abs(B).diagonal() < 0).all():
            pass
        elif (abs(B).sum(axis = 1) - 2 * abs(B).diagonal() < 0).all():
            pass
        else:
            msg2 =\
                'B given is neither strictly diagonally dominant ' +\
                'nor symmetric positive definite.'
            if (B.T == B).all():
                try:
                    np.linalg.cholesky(B)
                except:
                    raise ValueError(msg2)
            else:
                raise ValueError(msg2)
    LD = np.tril(B)
    U = B - LD
    if theta is None:
        theta = y.copy()
    else:
        theta = np.array(theta)
        assert len(y) == len(theta), \
            'If the initial theta is specified, then the length ' +\
            'of theta must be the same as y. Currently, ' +\
            'len(y) == {0} != {1} == len(theta)'.format(len(y), len(theta))
    iteration = 0
    errors = [np.linalg.norm(B @ theta - y)]
    no_conv = True
    while no_conv:
        theta = np.linalg.inv(LD) @ (y - (U @ theta))
        errors.append(np.linalg.norm(B @ theta - y))
        iteration += 1
        if errors[-1] < eps or iteration == max_iter:
            no_conv = False
    errors = np.array(errors)

    return {'y': y, 'theta': theta, 'niters': iteration, 'errors': errors}
def get_p_thres(roc_tbl, criterion = None):
    '''(returning pd.DataFrame of produce_roc_table[, [str, number]]) 
        -> float
    
    Precondition: criterion in [('tpr', x), ('fpr', y)]
    for some 0 < x < 1 and 0 < y < 1 (criterion need not be a tuple).
    
    Return the probability threshold from roc_tbl based on criterion.
    By default, the function returns the threshold that yields the
    minimum distance from the roc curve to the point (fpr, tpr) = (0, 1).
    If criterion == ('tpr', x) for some 0 < x < 1, then it returns a
    probability threshold that achieves the true positive rate of at
    least x and has the minimum false positive rate; 
    if criterion == ('fpr', y) for some 0 < y < 1, then it returns a
    probability threshold that achieves the false positive rate of at
    most y and has the maximum true positive rate.
    '''
    
    if criterion is None:
        dtp = roc_tbl['dist_to_optimal_point']
        p_thres = roc_tbl\
            .loc[lambda x: x['dist_to_optimal_point'] == np.min(dtp)]\
            ['thresholds']\
            .values[0]
    else:
        msg = 'If criterion is specified, '
        assert len(criterion) == 2, \
            msg + 'the length of criterion must be 2, not ' +\
            str(len(criterion)) + '.'
        assert type(criterion) != str, \
            msg + 'then it must be an array-like object, not a string.'
        assert criterion[0] in ['fpr', 'tpr'], \
            msg + 'then the first element must be exactly one of ' +\
            '"fpr" or "tpr", not ' + str(criterion[0]) + '.'
        type1 = str(type(criterion[1]))
        assert 'float' in type1 or 'int' in type1, \
            msg + 'then the second element must be a number, not ' +\
            type1 + '.'
        assert 0 < criterion[1] < 1, \
            msg + 'then the second element must be a number on the ' +\
            'interval (0, 1), not ' + str(criterion[1]) + '.'
        if criterion[0] == 'tpr':
            # Optimal p_thres is values[0], but it sometimes does not 
            # result in a desired tpr. This is because produce_roc_table()
            # uses sklearn roc_curve with drop_intermediate = True, and
            # a very small change (around a scale of 1e-09) in the 
            # threshold affects tpr. values[1] is less optimal, but always 
            # achieves the desired tpr.
            p_thres = roc_tbl\
                .loc[lambda x: x['tpr'] >= criterion[1]]\
                ['thresholds']\
                .values[1]
        else:
            # Optimal p_thres is values[-1], but values[-2] is used
            # by the same reasoning as above.
            p_thres = roc_tbl\
                .loc[lambda x: x['fpr'] <= criterion[1]]\
                ['thresholds']\
                .values[-2]
    
    return p_thres
def get_response(mod):
    '''(sm.GLMResultsWrapper) -> str

    Get the name of response column of mod.
    '''

    summary_str = str(mod.summary())
    response = summary_str[
        summary_str.index('Dep. Variable'):\
        summary_str.index('No. Observations:')
    ].strip()

    return response[14:].strip()
def hsm(x, tau = .5):
    '''(pd.Series, float) -> float
    
    Precondition: 0 < tau < 1
    
    Estimate the mode of x by the half sample mode method.
    '''
    
    n = len(x)
    x = x.sort_values()
    m = int(np.ceil(tau * n)) if tau <= .5 else int(np.floor(tau * n))
    m1 = int(m - 1)
    x2 = x[(m - 1):n]
    x1 = x[0:(n - m1)]
    k = np.arange(1, n - m1 + 1)
    k = k[x2.values - x1.values == min(x2.values - x1.values)]
    k = np.random.choice(k, 1)[0] if len(k) > 1 else k[0]
    x = x[int(k - 1):int(k + m1)]
    r = x.mean() if len(x) <= 2 else hsm(x, tau = tau)
    
    return r
def kde(x, samples, **kwargs):
    '''(float or *iterable, *iterable[, arguments of KDEUnivariate]) 
        -> np.array
    
    Return the value of kernel density estimate evaluated at x. kde is
    fitted using samples.
    '''
    
    dens = sm.nonparametric.KDEUnivariate(samples)
    dens.fit(**kwargs)
    
    return dens.evaluate(x)
def kde_mult(X, samples, **kwargs):
    '''(*iterable, *iterable[, arguments of KDEMultivariate]) -> np.array

    Precondition: number of columns of X == number of columns of samples

    Return the value of multidimensional kde evaluated at each row of X.
    kde is fitted using samples.
    '''
    
    vt = 'c' * X.shape[1]
    dens_M = sm.nonparametric.KDEMultivariate(
        samples, var_type = vt, **kwargs
    )
    
    return dens_M.pdf(X)
def logarithmic_scoring(mod, data, get_sum = True):
    '''(sm.GLMResultsWrapper, pd.DataFrame[, bool]) -> float
    
    Return the logarithmic scoring of mod onto the data, computed as
    y * log(phat) + (1 - y) * log(1 - phat). The higher, the better. 
    Set get_sum = True to get 
    sum(y * log(phat) + (1 - y) * log(1 - phat)) instead of a vector.
    '''
    
    summary_str = str(mod.summary())
    response = summary_str[
        summary_str.index('Dep. Variable'):\
        summary_str.index('No. Observations:')
    ].strip()
    response = response[14:].strip()
    assert response in data.columns, \
        'response "' + response + '" does not exist in data. Needs one.'

    features = list(mod.conf_int().index)
    ys = data[response].values
    phats = mod.predict(data[features]).values
    result = ys * np.log(phats) + (1 - ys) * np.log(1 - phats)
    
    return sum(result) if get_sum else result
def plot_op(mod, response, num_breaks = None, breaks = None, 
            xlab = 'Predicted Probability', 
            ylab = 'Observed Proportion'):
    '''(sm.GLMResultsWrapper, array-like[, int, np.array, str, str]) 
        -> None

    Plot the grouped observed proportions vs. predicted probabilities
    of mod that used `response` argument as the reponse. 
    Specify `num_breaks` to divide linear predictors into that much of 
    intervals of equal length.
    Specify `breaks` to have different bins for linear predictors; 
    `num_breaks` is ignored if `breaks` is specified. 
    '''

    logit = lambda p: np.log(p / (1 - p))
    predprob = mod.predict()
    linpred = logit(predprob)
    if breaks is None:
        if num_breaks is None:
            num_breaks = int(len(response) / 50)
        breaks = np.unique(
            np.quantile(linpred, np.linspace(0, 1, num = num_breaks + 1))
        )
    bins = pd.cut(linpred, breaks)
    df =\
        pd.DataFrame({
            'y': response, 
            'count': 1,
            'predprob': predprob,
            'bins': bins
        })\
        .groupby('bins')\
        .agg(
            y = ('y', 'sum'),
            counts = ('count', 'sum'),
            ppred = ('predprob', 'mean')
        )\
        .dropna()
    df['se_fit'] = np.sqrt(df['ppred'] * (1 - df['ppred']) / df['counts'])
    df['ymin'] = df['y'] / df['counts'] - 2 * df['se_fit']
    df['ymax'] = df['y'] / df['counts'] + 2 * df['se_fit']
    x = np.linspace(min(df['ppred']), max(df['ppred']))
    plt.scatter(df['ppred'], df['y'] / df['counts'])
    plt.vlines(
        df['ppred'], df['ymin'], df['ymax'], 
        alpha = .3, color = '#1F77B4'
    )
    plt.xlabel(xlab)
    plt.ylabel(ylab)
    plt.plot(x, x, color = '#FF7F0E', alpha = .4)
    plt.show()
def produce_roc_table(mod, train):
    '''(sm.GLMResultsWrapper, pd.DataFrame) -> pd.DataFrame
    
    Remarks: 
    1. train must be the data that is used to fit mod.
    2. Regardless of whether response is specified or not, train
    must contain the endogenous variable used to fit mod:
        + 2.1. If response is None, then the function assumes that 
               train has Dep. Variable specified in mod.summary() with
               exactly the same name.
        + 2.2. If response is specified, then the function assumes that 
               the endogenous variable with the same name as the 
               specified response value is one of the columns of train,
               and is used to fit mod.
    
    Return DataFrame that contains informations of fpr, tpr, and the
    corresponding probability thresholds based on mod and train.
    '''
    
    response = get_response(mod)
    actuals_train = train[response]
    preds_train = mod.predict()
    fpr, tpr, threses = roc_curve(actuals_train, preds_train)
    roc_tbl = pd.DataFrame({'fpr': fpr, 'tpr': tpr, 'thresholds': threses})
    dtp = dist_to_point(roc_tbl[['fpr', 'tpr']], np.array([0, 1]))
    roc_tbl['dist_to_optimal_point'] = dtp    
    
    return roc_tbl


# In development
def anova(*args):
    '''(sm.GLMResultsWrappers) -> pd.DataFrame

    Return the LRT results of models given to *args. If more than two
    models are given, then sequential LRT results are returned.
    '''

    result = {
        'Resid. Df': [],
        'Resid. Dev': [],
        'Df': [''],
        'Deviance': [''],
        'Pr(>Chi)': ['']
    }
    models = [*args]
    responses = []
    fmlrs = []
    assert len(models) != 1, \
        'Functionality not yet available for only one model; ' +\
        'need at least two.'
    if len(models) > 1:
        for mod in models:
            result['Resid. Df'].append(mod.df_resid)
            result['Resid. Dev'].append(mod.deviance)
        mod_pairs =\
            [tuple(models[i:(i + 2)]) for i in range(len(models) - 1)]
        for mod0, mod1 in mod_pairs:
            result['Df'].append(mod0.df_resid - mod1.df_resid)
            result['Deviance'].append(mod0.deviance - mod1.deviance)
            result['Pr(>Chi)'].append(
                1 - chi2.cdf(
                    mod0.deviance - mod1.deviance, 
                    df = mod0.df_resid - mod1.df_resid
                )
            )
    else:
        pass # for now

    return pd.DataFrame(result)
def classify_terbin(mod_terbin, data):
    '''(return value of terbin_model(), pd.DataFrame) 
        -> {str: np.array and/or str: pd.DataFrame}

    Compute the probability for each observations of data, and classify
    according to mod_terbin.
    '''

    # Check: does data have all features of mod_ternary and mod_binary?
    data_cols = data.columns
    ter_features = mod_terbin['mod_ternary'][2].columns
    bin_response = mod_terbin['mod_binary'][1].name
    bin_features = mod_terbin['mod_binary'][2].columns
    assert set(ter_features).issubset(set(data_cols)), \
        'data does not have all the features of mod_ternary. ' +\
        'The following are missing: ' +\
        str(list(set(ter_features).difference(set(data_cols))))
    assert set(bin_features).issubset(set(data_cols)), \
        'data does not have all the features of mod_binary. ' +\
        'The following are missing: ' +\
        str(list(set(bin_features).difference(set(data_cols))))

    # Check: does data have a binary response column?
    # If no, just return the classification result.
    # If yes, then return classification result and case counts
    data_has_bin_response = bin_response in data.columns

    # Predict types: fn, fp, or tpn
    types = Pipe(lambda row: ['fn', 'fp', 'tpn'][np.argmax(row)])\
        .pipe(
            map, 
            mod_terbin['mod_ternary'][0]\
                .predict(data[ter_features])\
                .values
        )\
        .pipe(list)\
        .pipe(np.array)\
        .collect()

    # Predict probabilities
    probs = mod_terbin['mod_binary'][0].predict(data[bin_features]).values

    # Classify using different probability thresholds
    types_probs = np.array(list(zip(types, probs)))
    p_threses = {
        'fn': mod_terbin['p_threses'][0], 
        'tpn': mod_terbin['p_threses'][1],
        'fp': mod_terbin['p_threses'][2]
    }

    result = np.array(list(map(
        lambda row: float(row[1]) > p_threses[row[0]], 
        types_probs
    )))
    result = np.array(list(map(int, result)))

    if not data_has_bin_response:
        return {
            'predicted_types': types,
            'result': result,
            'p_threses': mod_terbin['p_threses']
        }
    else:
        actuals = data[bin_response].values
        total_neg = np.sum(actuals == 0)
        total_pos = len(actuals) - total_neg
        tn = sum((actuals == 0) & (result == 0))
        fp = total_neg - tn
        tp = sum((actuals == 1) & (result == 1))
        fn = total_pos - tp
        case_counts = pd.DataFrame({
            'class': [0, 0, 1, 1],
            'classified': [0, 1, 0, 1],
            'class_total': [total_neg, total_neg, total_pos, total_pos],
            'counts': [tn, fp, fn, tp]
        })
        case_counts['perc'] =\
            np.array([tn, fp, fn, tp]) /\
            np.array([total_neg, total_neg, total_pos, total_pos])
        accuracy = (tp + tn) / (total_pos + total_neg)
        return {
            'predicted_types': types,
            'result': result,
            'counts': case_counts,
            'accuracy': accuracy,
            'p_threses': mod_terbin['p_threses']
        }
def count_cases(mod, data, train = None, p_thres = None, criterion = None):
    '''(sm.GLMResultsWrapper or return value of terbin_model(), 
        pd.DataFrame, 
        [pd.DataFrame , float, [str, number]]) 
        -> pd.DataFrame

    Precondition: 
    1. response of mod consists of 0s and 1s.
    2. data contains the response column specified by mod
    3. data contains all or more feature columns of mod, including the
    intercept if applicable.
    4. train must be specified if mod is of class GLMResultsWrapper
    5. 0 < p_thres < 1

    Count the number of true negatives, false positives, false negatives,
    and true positives in data classified by mod and p_thres; train must
    be the dataset that is used to fit mod. If p_thres is None, then 
    it uses the probability threshold that yields the minimum distance 
    between the ROC curve and the point (fpr, tpr) = (0, 1); if p_thres is
    specified, then criterion (used as an argument of get_p_thres()) is 
    ignored. If mod is not of class sm.GLMResultsWrapper, then every
    argument except mod and data are ignored.
    '''
    
    if 'GLMResultsWrapper' in str(type(mod)):
        assert train is not None, \
            'If a given mod is of class GLMResultsWrapper, then ' +\
            'train must be specified.'

        # Get the (binary) response column; len('Dep. Variable') == 14
        summary_str = str(mod.summary())
        response = summary_str[
            summary_str.index('Dep. Variable'):\
            summary_str.index('No. Observations:')
        ].strip()
        response = response[14:].strip()
        
        # Checks
        all_features_of_data = set(data.columns)
        assert response in all_features_of_data, \
            'data does not have the response: "' + response + '".'   
        all_features_of_data.remove(response) # leave only predictors
        mod_features = mod.cov_params().columns
        mod_features_set = set(mod_features)
        assert mod_features_set.issubset(all_features_of_data), \
            'data does not have all the features used in mod; data ' +\
            'requires the following: {0}'\
            .format(
                list(mod_features_set.difference(all_features_of_data))
            )
        mod_features = list(mod_features)
        
        # Compute p_thres if not specified
        actuals = data[response].values
        preds = mod.predict(data[mod_features]).values    
        if p_thres is None: # p_thres must come from train, not data
            roc_tbl = produce_roc_table(mod, train, response)
            p_thres = get_p_thres(roc_tbl, criterion)
        classifieds = preds > p_thres
        classifieds = np.array(list(map(int, classifieds)))
        
        # Binary classification result
        total_neg = np.sum(actuals == 0)
        total_pos = len(actuals) - total_neg
        tn = sum((actuals == 0) & (classifieds == 0))
        fp = total_neg - tn
        tp = sum((actuals == 1) & (classifieds == 1))
        fn = total_pos - tp
        result = pd.DataFrame({
            'class': [0, 0, 1, 1],
            'classified': [0, 1, 0, 1],
            'class_total': [total_neg, total_neg, total_pos, total_pos],
            'counts': [tn, fp, fn, tp]
        })
        result['perc'] =\
            np.array([tn, fp, fn, tp]) /\
            np.array([total_neg, total_neg, total_pos, total_pos])
        accuracy = (tp + tn) / (total_pos + total_neg)
        
        return {
            'counts': result, 
            'accuracy': accuracy,
            'p_thres': p_thres
        }
    else:
        result = classify_terbin(mod, data)
        del result['result']
        return result
def drop1(mod, train, show_progress = True):
    '''(sm.GLMResultsWrapper, pd.DataFrame) -> pd.DataFrame

    Conduct a LRT of mod minus one feature vs. mod for every feature
    used in mod, trained by train.
    '''

    response = get_response(mod)
    assert response in train.columns, \
        'response "' + response + '" does not exist in train. Needs one.'

    int_name = ''
    all_features = list(mod.conf_int().index)
    for col in all_features:
        if (train[col] == 1).all():
            int_name += col
            break
    assert int_name != '', \
        'An intercept column does not exist in train. Needs one.'
    all_features_minus_int = all_features[:]
    all_features_minus_int.remove(int_name)

    result = {
        'Removed': ['<none>'],
        'Df': [''],
        'Deviance': [mod.deviance],
        'AIC': [mod.aic],
        'LRT': [''],
        'Pr(>Chi)': [''],
        '': ['']
    }
    for item in all_features_minus_int:
        afmi = all_features_minus_int[:]
        afmi.remove(item)
        if show_progress:
            print('LRT: mod - {0} vs. mod'.format(item))
        mod_minus1_features = [int_name] + afmi
        mod_1dropped = sm.GLM(
            train[response],
            train[mod_minus1_features],
            family = sm.families.Binomial()
        )\
        .fit()
        aov = anova(mod_1dropped, mod)
        result['Removed'].append(item)
        result['Df'].append(aov['Df'][1])
        result['Deviance'].append(aov['Resid. Dev'][0])
        result['AIC'].append(mod_1dropped.aic)
        result['LRT'].append(aov['Deviance'][1])
        p_val = aov['Pr(>Chi)'][1]
        result['Pr(>Chi)'].append(p_val)
        sig = ''
        if p_val <= .001:
            sig += '***'
        elif p_val <= .01:
            sig += '** '
        elif p_val <= .05:
            sig += '*  '
        elif p_val <= .1:
            sig += '.  '
        result[''].append(sig)

    return pd.DataFrame(result)
def model_by_lrt(mod, train, pval_thres = .05, show_progress = True):
    '''(sm.GLMResultsWrapper, pd.DataFrame[, float, bool])
        -> sm.GLMResultsWrapper

    Precondition: 0 < pval_thres < 1

    Sequentially remove a feature that has a maximum p-value from 
    drop1(mod, train), trained by train, until every feature has a
    p-value less that pval_thres. Return sm.GLMResultsWrapper object 
    that only contains such features. Set show_progress = True to see 
    the removal process.
    '''

    assert 0 < pval_thres < 1, \
        'pval_thres argument must be between 0 and 1, not ' +\
        str(pval_thres) + '.'

    response = get_response(mod)
    assert response in train.columns, \
        'response "' + response + '" does not exist in train. Needs one.'

    features = list(mod.conf_int().index)
    drop1_result = drop1(mod, train, show_progress)
    not_all_less_than_thres =\
        not (drop1_result.iloc[1:, :]['Pr(>Chi)'] < pval_thres).all()
    if not not_all_less_than_thres:
        return mod
    i = 0
    while not_all_less_than_thres:
        i += 1
        ordered = drop1_result.iloc[1:, :]\
            .sort_values('Pr(>Chi)', ascending = False)
        to_remove = ordered['Removed'].values[0]
        pval_of_removed = ordered['Pr(>Chi)'].values[0]
        if show_progress:
            msg = 'Iteration {0}: removed {1} (p-val: {2})'
            msg = msg.format(i, to_remove, pval_of_removed)
            print(msg)
        features.remove(to_remove)
        mod_new = sm.GLM(
            train[response],
            train[features],
            family = sm.families.Binomial()
        )\
        .fit()
        print(anova(mod_new, mod)) if show_progress else ''
        drop1_result =\
            drop1(mod_new, train[[response] + features], show_progress)
        not_all_less_than_thres =\
            not (drop1_result.iloc[1:, :]['Pr(>Chi)'] < pval_thres).all()

    return mod_new
def model_by_vif(mod, train, vif_thres = 5, show_progress = True):
    '''(sm.GLMResultsWrapper, pd.DataFrame[, float, bool]) 
        -> {str: sm.GLMResultsWrapper and str: {str: float}}
    
    Precondition: vif_thres > 0
    
    Sequentially remove a feature that has a maximum VIF from mod,
    trained by train, until every feature has a VIF less than vif_thres. 
    Return sm.GLMResultsWrapper object that only contains such features.
    Set show_progress = True to see the removal process.
    '''
    
    assert vif_thres > 0, \
        "vif_thres argument must be positive, not " + str(vif_thres) + "."

    # Remove response
    response = get_response(mod)
    all_cols = list(train.columns)
    if response in all_cols:
        all_cols.remove(response)
        X = train.loc[:, all_cols]
    else:
        X = train
    
    # Let Intercept be the first predictor
    int_name = ''
    for c in all_cols:
        if (X[c].values == 1).all(): # Try to find Intercept
            int_name += c
            break
    if int_name == '': # Intercept column doesn't exist; make one
        int_name += 'Intercept'
        assert int_name not in X.columns, \
            '"Intercept", the column in train that ' +\
            'is NOT the column of 1s and yet uses the name ' +\
            '"Intercept", already exists in train. User inspection ' +\
            'is required.'
        X[int_name] = 1
        all_cols2 = [int_name]
        all_cols2.extend(all_cols)
        all_cols = all_cols2
        X = X.loc[:, all_cols]
    all_cols.remove(int_name)
    
    # X = train minus response
    # i.e. X.columns = [Intercept, *features]
    # all_cols: train.columns minus response minus Intercept
    # i.e. all_cols = [*features]
    vifs = dict(zip(
        (c for c in all_cols),
        (variance_inflation_factor(X.values, j) \
         for j in range(1, X.values.shape[1])) # except Intercept
    ))
    not_all_vifs_less_than_thres =\
        not (np.array(list(vifs.values())) < vif_thres).all()
    i = 0
    while not_all_vifs_less_than_thres:
        i += 1
        current_max = max(vifs.values())
        k_to_remove = ''
        for k, v in vifs.items():
            if v == current_max:
                k_to_remove += k
                break
        v_removed = vifs.pop(k_to_remove) # same as current_max
        if show_progress:
            msg = 'Iteration {0}: removed {1} (VIF: {2})'\
                .format(i, k_to_remove, v_removed)
            print(msg)
        del X[k_to_remove]
        all_cols.remove(k_to_remove)
        vifs = dict(zip(
            (c for c in all_cols),
            (variance_inflation_factor(X.values, j) \
             for j in range(1, X.values.shape[1]))
        ))
        not_all_vifs_less_than_thres =\
            not (np.array(list(vifs.values())) < vif_thres).all()  
    
    features = [int_name]
    features.extend(all_cols)
    if show_progress:
        msg2 = 'Features used: {0}'.format(features)
        print(msg2)
    mod_reduced =\
        sm.GLM(
            train[response],
            train.loc[:, features],
            family = sm.families.Binomial()
        )\
        .fit()
    
    return {'model': mod_reduced, 'vifs': vifs}
def model_matrix(data, formula):
    '''(pd.DataFrame, str) -> pd.DataFrame

    Design data according to formula.
    '''
    
    name_df =\
        lambda df: pd.DataFrame(df, columns = df.design_info.column_names)
    response, features = dmatrices(formula, data)
    response = name_df(response)
    features = name_df(features)
    response_name = response.columns[0]
    features.insert(0, response_name, response)
    
    return features
def mutate(data, colname, lambd = None, lambd_df = None):
    '''(pd.DataFrame, str[, (str, function), function]) -> pd.DataFrame
    
    Add a column named as the value of colname that is obtained by lambd 
    or lambd_df. lambd is a tuple of str and function that is applied for 
    each element in a selected Series of df; lambd_df is a function that 
    applies to the entire df. If lambd is specified, then lambd_df is 
    ignored.
    
    >>> df = pd.DataFrame({
            'basiscol': ['aba', 'bba', 'cce'], 
            'extra': [1, 2, 3]
        })
    >>> df1 =\\
    ...     mutate(
    ...         df, 
    ...         'newcolname', 
    ...         ('basiscol', lambda x: x[:2])
    ...     )
    ...
    >>> df2 =\\
    ...     mutate(
    ...         df, 
    ...         'newcolname', 
    ...         lambd_df = lambda x: x['basiscol'].apply(lambda y: y[:2])
    ...     )
    ...
    >>> df1.equals(df2)
    True
    '''

    df_cp = data.copy()
    assert not (lambd is None and lambd_df is None), \
        'Either one of lambd or lambd_df has to be specified.'
    if lambd is not None:
        df_cp[colname] = df_cp[lambd[0]].apply(lambd[1])
    elif lambd_df is not None:
        df_cp[colname] = lambd_df(df_cp)

    return df_cp
def plot_rl(mod, num_breaks = None, breaks = None, 
            xlab = 'Linear predictor', 
            ylab = 'Deviance residuals'):
    '''(sm.GLMResultsWrapper[, int, np.array, str, str]) -> None

    Plot the means of grouped residuals vs. linear predictors of mod. 
    Specify `num_breaks` to divide linear predictors into that much of 
    intervals of equal length.
    Specify `breaks` to have different bins for linear predictors; 
    `num_breaks` is ignored if `breaks` is specified.
    '''

    logit = lambda p: np.log(p / (1 - p))
    residuals = mod.resid_deviance
    linpred = logit(mod.predict())
    if breaks is None:
        if num_breaks is None:
            num_breaks = int(len(residuals) / 50)
        breaks = np.unique(
            np.quantile(linpred, np.linspace(0, 1, num = num_breaks + 1))
        )
    bins = pd.cut(linpred, breaks)
    df = pd.DataFrame(
        {'residuals': residuals, 'linpred': linpred, 'bins': bins}
    )
    df = df.groupby('bins')\
        .agg(
            residuals = ('residuals', 'mean'), 
            linpred = ('linpred', 'mean')
        )

    plt.scatter(df['linpred'], df['residuals'])
    plt.xlabel(xlab)
    plt.ylabel(ylab)
    plt.show()
def terbin_model(mod, train, p_thres = None, criterion = None, 
                 ter_features = None, train_ter = None, **kwargs):
    '''(sm.GLMResultsWrapper, pd.DataFrame
        [, number, (str, float), [str], pd.DataFrame,
        arguments to sm.MNLogit.fit(...)]) 
        -> {str: results}
    
    Precondition:
    1. mod is fitted using train.
    2. train contains the response column specified in mod.summary().
    3. 0 < p_thres < 1
    4. set(ter_features).issubset(set(train.columns)) if train_ter is None\
        else set(ter_features).issubset(set(train_ter.columns))
    
    Fit a compounded model, or a terbin (ternary-binary) model, based on
    mod and train. 
    
    * If p_thres is None, then it uses the probability threshold that 
    yields the minimum distance between the ROC curve and the point 
    (fpr, tpr) = (0, 1); if p_thres is specified, then criterion 
    (used as an argument of get_p_thres()) is ignored.
    * Specify ter_features to fit a multinomial logit model using those 
    features. If not specified, then the same formula as mod is used.
    * If train_ter is specified, then this training set is used to fit a
    multinomial logit model. If not specified, then train works as 
    train_ter.
    '''
    
    # Get the (binary) response column; len('Dep. Variable') == 14
    response = get_response(mod)
    
    # Checks
    all_features_of_train = set(train.columns)
    assert response in all_features_of_train, \
        'train does not have the response "' + response + '" specified ' +\
        'in mod.'
    all_features_of_train.remove(response) # leave only predictors
    mod_features = mod.cov_params().columns # features used in mod
    mod_features_set = set(mod_features)
    assert mod_features_set.issubset(all_features_of_train), \
        'train does not have all the features used in mod; train ' +\
        'requires the following: {0}'\
        .format(list(mod_features_set.difference(all_features_of_train)))
    mod_features = list(mod_features)
    if ter_features is not None:
        if train_ter is None:
            assert set(ter_features).issubset(set(train.columns)), \
            'ter_features must be a subset of train.columns if ' +\
            'train_ter is not specified. train.columns requires ' +\
            'the following: ' +\
            str(list(set(ter_features).difference(set(train.columns))))
        else:
            assert set(ter_features).issubset(set(train_ter.columns)), \
            'ter_features must be a subset of train_ter.columns if ' +\
            'both train_features and train_ter are specified. ' +\
            'train_ter.columns requires the following: ' +\
            str(list(set(ter_features).difference(set(train_ter.columns))))
    else:
        ter_features = mod_features
    train_ter = train if train_ter is None else train_ter

    # Compute p_thres if not specified  
    if p_thres is None:
        roc_tbl = produce_roc_table(mod, train)
        p_thres = get_p_thres(roc_tbl, criterion)
    
    # Ternary model
    actuals = train[response].values
    preds = mod.predict(train[mod_features]).values  
    response_ter = determine_type(actuals, preds, p_thres)
    mod_ter =\
        sm.MNLogit(response_ter, train_ter[ter_features])\
        .fit(**kwargs)
    
    # Get p_thres_fn and p_thres_fp
    p_thres_fn = np.quantile(
        mod.predict(train.loc[response_ter == 'fn', mod_features]), 
        .1
    )
    p_thres_fp = np.quantile(
        mod.predict(train.loc[response_ter == 'fp', mod_features]),
        .9
    )

    return {
        'mod_ternary': [mod_ter, response_ter, train_ter[ter_features]],
        'mod_binary': [mod, train[response], train[mod_features]],
        'p_threses': np.array([p_thres_fn, p_thres, p_thres_fp])
    }
