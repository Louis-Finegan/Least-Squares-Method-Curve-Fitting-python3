
"""
File will apply least square method to curve fit
1. linear
2. exponential
3. power
"""

import numpy as np

#Determinant
def det(Array):
    # Must be 2x2 Matrix
    # Must be a column of rows
    return Array[0, 0]*Array[1, 1] - Array[0, 1]*Array[1, 0]

class curve_fit:
    def __init__(self, Xdata: np.ndarray, Ydata: np.ndarray) -> None:
        self.Xdata = Xdata
        self.Ydata = Ydata

    # transforms the Ydata to a linear projection
    def log_data(self, exponential: bool, linear: bool, power: bool):
        # will take the log of the data
        if exponential == True and linear == False and power == False:
            return self.Xdata, np.log(self.Ydata)
        elif exponential == False and linear == True and power == False:
            return self.Xdata, self.Ydata
        elif exponential == False and linear == False and power == True:
            return np.log(self.Xdata), np.log(self.Ydata)
        else:
            print('Only one of the 3 bools should be TRUE.')

    # X, Y = log_data()
    # will calculate (a, b) to get the parameters to fit each curve
    def systemsolver(self, X: np.ndarray, Y: np.ndarray):
        array = np.zeros((2, 2))
        array[0, 0] = np.sum(X**2)
        array[0, 1] = np.sum(X)
        array[1, 0] = np.sum(X)
        array[1, 1] = len(X)

        vec = np.zeros(2)
        vec[0] = np.sum(X.dot(Y))
        vec[1] = np.sum(Y)

        # Must determine the inverse of array
        if det(array) == 0:
            print('Matrix is not invertible and the equation cannot be solved')
            return
        else:
            arrayinv = np.zeros((2, 2))
            arrayinv[0, 0] = (1/det(array))*array[1, 1]
            arrayinv[0, 1] = (-1/det(array))*array[0, 1]
            arrayinv[1, 0] = (-1/det(array))*array[1, 0]
            arrayinv[1, 1] = (1/det(array))*array[0, 0]

        a = arrayinv[0, 0]*vec[0] + arrayinv[0, 1]*vec[1]
        b = arrayinv[1, 0]*vec[0] + arrayinv[1, 1]*vec[1]

        return a, b

    # uses (a, b) from systemsolver() to output numpy array of the modelled linear data
    # linear curve fit
    def curve_fit_linear(self, a: float, b: float):
        return a*self.Xdata + b

    # uses (a, b) from systemsolver() to output numpy array of the modelled exponential data
    # exponential curve fit
    def curve_fit_exp(self, a: float, b: float):
        c = np.exp(b)
        return c*np.exp(a*self.Xdata)

    # uses (a, b) from systemsolver() to output numpy array of the modelled power (mononomial) data
    # power curve fit
    def curve_fit_power(self, a: float, b: float):
        c = np.exp(b)
        return c*(self.Xdata)**a

class curve_fit_guess_limit:
    def __init__(self, Xdata: np.ndarray, Ydata: np.ndarray, limit: float) -> None:
        self.Xdata = Xdata
        self.Ydata = Ydata
        self.limit = limit

    # transforms the Ydata to a linear projection
    def transformation_guess_limit(self, limited_exponential: bool, logistic: bool) -> np.ndarray:
        if limited_exponential == True and logistic == False:
            return np.log((self.limit - self.Ydata)/(self.limit - self.Ydata[0]))
        elif limited_exponential == False and logistic == True:
            return np.log((self.limit/self.Ydata - 1)/(self.limit/self.Ydata[0] - 1))
        else:
            print('Only one of the 2 bools should be TRUE.')

    # Will calculate -k (inverse logistic growth rate) values from the system defined in systemsolver() where b=0 and a = -k 
    def systemsolver_guess_limit(self, Y: np.ndarray) -> tuple:
        return np.sum(self.Xdata * Y)/np.sum(self.Xdata**2), np.sum(Y)/np.sum(self.Xdata)

    # uses (a) from systemsolver_guess_limit() to output numpy array of the modelled logistic data
    # logistic curve fit
    def curve_fit_logistic(self, a: float) -> np.ndarray:
        return self.limit/(1 + (self.limit/self.Ydata[0] - 1)*np.exp(a*self.Xdata))

    # uses (a) from systemsolver_guess_limit() to output numpy array of the modelled limited exponential data
    # limited exponential curve fit
    def curve_fit_limited_exp(self, a: float) -> np.ndarray:
        return self.limit + (self.Ydata[0] - self.limit)*np.exp(a*self.Xdata)
