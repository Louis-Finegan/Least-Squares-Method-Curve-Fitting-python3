
"""
File will apply least square method to curve fit
1. linear
2. exponential
3. power
4. limited exponential
5. logistic
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

    # Linearization
    def linearization(self, exponential: bool, linear: bool, power: bool) -> np.ndarray:
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
    def systemsolver(self, X: np.ndarray, Y: np.ndarray) -> tuple:
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
    def curve_fit_linear(self, a: float, b: float) -> np.ndarray:
        return a*self.Xdata + b

    # uses (a, b) from systemsolver() to output numpy array of the modelled exponential data
    # exponential curve fit
    def curve_fit_exp(self, a: float, b: float) -> np.ndarray:
        c = np.exp(b)
        return c*np.exp(a*self.Xdata)

    # uses (a, b) from systemsolver() to output numpy array of the modelled power (mononomial) data
    # power curve fit
    def curve_fit_power(self, a: float, b: float) -> np.ndarray:
        c = np.exp(b)
        return c*(self.Xdata)**a

class curve_fit_guess_limit:
    def __init__(self, Xdata: np.ndarray, Ydata: np.ndarray, limit: float) -> None:
        self.Xdata = Xdata
        self.Ydata = Ydata
        self.limit = limit

    # transforms the Ydata to a linear projection
    def linearization(self, limited_exponential: bool, logistic: bool) -> np.ndarray:
        if limited_exponential == True and logistic == False:
            return np.log((self.limit - self.Ydata)/(self.limit - self.Ydata[0]))
        elif limited_exponential == False and logistic == True:
            return np.log((self.limit/self.Ydata - 1)/(self.limit/self.Ydata[0] - 1))
        else:
            print('Only one of the 2 bools should be TRUE.')

    # Will calculate -k (inverse logistic/exponential growth rate) values from the system defined 
    # in systemsolver() where b=0 and a = -k 
    def systemsolver_guess_limit(self, Y: np.ndarray) -> tuple:
        return np.sum(self.Xdata * Y)/np.sum(self.Xdata**2), np.sum(Y)/np.sum(self.Xdata)

    # uses k = -a from systemsolver_guess_limit() to output numpy array of the modelled logistic data
    # logistic curve fit
    def curve_fit_logistic(self, k: float) -> np.ndarray:
        return self.limit/(1 + (self.limit/self.Ydata[0] - 1)*np.exp(-k*self.Xdata))

    # uses k = -a from systemsolver_guess_limit() to output numpy array of the modelled limited exponential data
    # limited exponential curve fit
    def curve_fit_limited_exp(self, k: float) -> np.ndarray:
        return self.limit + (self.Ydata[0] - self.limit)*np.exp(-k*self.Xdata)

class curve_fit_limit:

    def __init__(self, Ydata: np.ndarray, min_val: float, max_val: float, sep: float) -> None:
        self.min_val = min_val
        self.max_val = max_val
        self.sep = sep
        self.Xdata = np.arange(min_val, max_val, sep)
        self.Ydata = Ydata


    # will return -> (X, Y)
    def linearization(self, limited_exponential: bool, logistic: bool) -> np.ndarray:
        if limited_exponential == True and logistic == False:
            return np.delete(self.Ydata, len(self.Ydata)-1), np.delete(self.Ydata, 0)
        elif limited_exponential == False and logistic == False:
            pass
        else:
            print('Only one of the 2 bools should be TRUE.')

    # Will calculate k (inverse logistic/exponential growth rate) and limit values from the system defined 
    # in systemsolver() where limit=(1-a)/b and a = -ln(a)/sep
    def systemsolver_limited(self, X: np.ndarray, Y: np.ndarray) -> tuple:
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

        k = -np.log(a)/self.sep
        limit = (1- a)/b
        return k, limit

    # uses k and limit from systemsolver_limit() to output numpy array of the modelled logistic data
    # logistic curve fit
    def curve_fit_logistic(self, limit: float, k: float) -> np.ndarray:
        return limit/(1 + (limit/self.Ydata[0] - 1)*np.exp(-k*self.Xdata))

    # uses k and limit from systemsolver_limit() to output numpy array of the modelled limited exponential data
    # limited exponential curve fit
    def curve_fit_limited_exp(self, limit: float, k: float) -> np.ndarray:
        return limit + (self.Ydata[0] - limit)*np.exp(-k*self.Xdata)