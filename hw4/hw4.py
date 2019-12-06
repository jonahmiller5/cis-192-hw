'''
Name: Jonah Miller
PennKey: jonahmil
Hours of work required: 5
'''

'''
In all functions below, the keyword "pass" is used to
indicate to the interpreter that the corresponding codeblock
is empty. This is necessary in order for the interpreter
not to consider empty code blocks as syntax errors.
You will replace each of these "pass" keywords by your
code completing the function as described in the comments.
'''

import numpy as np


class DataProcessor():
    def __init__(self, X):
        '''
        The initialization function should save the
        data set X and any other relevant information
        args:
            X: an n-by-d matrix of n data instances
            and d variables per instance
        ret: None
        Outcome: self.X must contain the data set
        '''
        if not isinstance(X, np.ndarray):
            return

        self.X = X

    def remove_nans(self):
        '''
        This function must remove all instances (rows)
        containing at least one missing value (np.nan)
        args: None
        ret: None
        Outcome: the dataset must contain no NaNs
        '''
        if not isinstance(self.X, np.ndarray):
            return

        X_nans = np.isnan(self.X)
        found_index = np.any(X_nans, axis=1)
        found_index = np.invert(found_index)
        self.X = self.X[found_index]

    def standardize(self):
        '''
        This function standardizes the data set so that
        each variable (column) has zero mean and standard
        deviation one
        args: None
        ret: None
        Outcome: the data set is standardized
        '''
        if not isinstance(self.X, np.ndarray):
            return

        mean = np.mean(self.X, axis=0)
        stdev = np.std(self.X, axis=0)

        mean[stdev == 0] = 0
        stdev[stdev == 0] = 1

        self.X = (self.X - mean) / stdev

    def clip(self, min_val=-np.inf, max_val=np.inf):
        '''
        This function clips the data set to the thresholds
        given by min_val and max_val
        args:
            min_val: the minimum value any element in the
            data set may have
            max_val: the maximum value any element in the
            data set may have
        ret: None
        Outcome: the data set is clipped
        '''
        if not isinstance(self.X, np.ndarray):
            return
        if not (isinstance(min_val, int) and isinstance(max_val, int)):
            return
        if max_val < min_val:
            return

        if min_val == max_val:
            self.X = max_val
        else:
            self.X[self.X < min_val] = min_val
            self.X[self.X > max_val] = max_val

    def scale(self, min_val=-1, max_val=1):
        '''
        This function linearly scales the data set so that
        each variable has the specified min and max values
        args:
            min_val: same as for clip
            max_val: same as for clip
        ret: None
        Outcome: Each variable (column) is linearly scaled
        and has maximum and minimum values as specified
        '''
        if not isinstance(self.X, np.ndarray):
            return
        if not (isinstance(min_val, int) and isinstance(max_val, int)):
            return
        if max_val < min_val:
            return

        if max_val == min_val:
            self.X = max_val
        else:
            original_min = np.min(self.X)
            original_max = np.max(self.X)

            self.X = ((max_val-min_val)*(self.X-original_min) /
                      (original_max-original_min)) + min_val


def main():
    '''
    Use this for testing! Make sure to be thorough and test for
    corner cases.
    '''
    X = np.random.randn(10, 10) * 10
    nan_mask = np.random.rand(10, 10) > 0.98
    # print(nan_mask)
    X[nan_mask] = np.nan
    X[0] = np.nan
    X[:, 0] = 0.5
    dp = DataProcessor(None)
    dp = DataProcessor(X)
    dp.remove_nans()
    # print(dp.X)
    dp.standardize()
    # print(dp.X)
    # print(dp.X)
    dp.clip(-1, 1)
    # print(dp.X)
    dp.scale(-3, 5)
    # print(dp.X)


if __name__ == '__main__':
    '''
    This calls the function main() when executing python3 hw4.py
    '''
    main()
