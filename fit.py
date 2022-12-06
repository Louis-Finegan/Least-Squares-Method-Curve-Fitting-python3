
"""
File will apply least square method to curve fit
1. linear
2. exponential
3. power
"""

import numpy as np
import matplotlib.pyplot as plt

#Determinant
def det(Array):
    # Must be 2x2 Matrix
    # Must be a column of rows
    return Array[0, 0]*Array[1, 1] - Array[0, 1]*Array[1, 0]

class curve_fit:
    def __init__(self, Xdata: np.ndarray, Ydata: np.ndarray) -> None:
        self.Xdata = Xdata
        self.Ydata = Ydata

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

    # X, Y = log_data(...)
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
        print('determinant is {}'.format(det(array)))
        if det(array) == 0:
            print('Matrix is not invertible and the equation cannot be solved')
            return
        else:
            arrayinv = np.zeros((2, 2))
            arrayinv[0, 0] = (1/det(array))*array[1, 1]
            arrayinv[0, 1] = (-1/det(array))*array[0, 1]
            arrayinv[1, 0] = (-1/det(array))*array[1, 0]
            arrayinv[1, 1] = (1/det(array))*array[0, 0]
            #print('Inverse of array', arrayinv)

        a = arrayinv[0, 0]*vec[0] + arrayinv[0, 1]*vec[1]
        b = arrayinv[1, 0]*vec[0] + arrayinv[1, 1]*vec[1]

        return a, b

    def curve_fit_linear(self, a: float, b: float):
        return a*self.Xdata + b

    def curve_fit_exp(self, a: float, b: float):
        c = np.exp(b)
        return c*np.exp(a*self.Xdata)

    def curve_fit_power(self, a: float, b: float):
        c = np.exp(b)
        return c*(self.Xdata)**a

class curve_fit_limited:
    def __init__(self, Xdata: np.ndarray, Ydata: np.ndarray) -> None:
        self.Xdata = Xdata
        self.Ydata = Ydata

    def transformation_Guess_limit(self):
        pass

    def systemsolver_Guess_limit(self, X: np.ndarray, Y: np.ndarray):
        pass

    
