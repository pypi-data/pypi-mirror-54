import numpy as np
from math import isnan

class svtnn:
    '''
        Single Valued Triangular Neutrosophic Number
        alpha: used to calculate truth
        gamma: used to calculate indeterminacy
        beta: used to calculate falsity
        a1: lower
        a2: median
        a3: upper
    '''

    def __init__(self, a1, a2, a3, alpha, theta, beta):
        self.a1 = a1
        self.a2 = a2
        self.a3 = a3
        self.alpha = alpha
        self.theta = theta
        self.beta = beta
        
    def truth_value_at(self, x):
        '''
            truth value of svtnn at point/value x
        '''
        if self.a1 <= x < self.a2:
            if isnan(self.alpha * ((x - self.a1)/(self.a2 - self.a1))):
                return 0
            else:
                return self.alpha * ((x - self.a1)/(self.a2 - self.a1))
        elif self.a2 == x :
            if isnan(self.alpha):
                return 0
            else:
                return self.alpha
        elif self.a2 < x <= self.a3:
            if isnan(self.alpha * ((self.a3 - x)/(self.a3 - self.a2))):
                return 0
            else:
                return self.alpha * ((self.a3 - x)/(self.a3 - self.a2))
        else:
            return 0
        
    def indeterminacy_value_at(self, x):
        '''
            indeterminacy value of svtnn at point/value x
        '''
        if self.a1 <= x < self.a2:
            if isnan((self.a2 - x + self.theta * (x - self.a1))/(self.a2 - self.a1)):
                return 1
            else:
                return ((self.a2 - x + self.theta * (x - self.a1))/(self.a2 - self.a1))
        elif self.a2 == x:
            if isnan(self.theta):
                return 1
            else:
                return self.theta
        elif self.a2 < x <= self.a3:
            if isnan(((x - self.a2 + self.theta * (self.a3 - x))/(self.a3 - self.a2))):
                return 1
            else:
                return ((x - self.a2 + self.theta * (self.a3 - x))/(self.a3 - self.a2))
        else:
            return 1
        
    def false_value_at(self, x):
        '''
            false value of svtnn at point/value x
        '''
        if self.a1 <= x < self.a2:
            if isnan(((self.a2 - x + self.beta * (x - self.a1))/(self.a2 - self.a1))):
                return 1
            else:
                return ((self.a2 - x + self.beta * (x - self.a1))/(self.a2 - self.a1))
        elif self.a2 == x:
            if isnan(self.beta):
                return 1
            else:
                return self.beta
        elif self.a2 < x <= self.a3:
            if isnan(((x - self.a2 + self.beta * (self.a3 - x))/(self.a3 - self.a2))):
                return 1
            else:
                return ((x - self.a2 + self.beta * (self.a3 - x))/(self.a3 - self.a2))
        else:
            return 1
        
    def inverse(self):
        return svtnn(1/self.a1 if self.a1 != 0 else 0, 
                     1/self.a2 if self.a2 != 0 else 0, 
                     1/self.a3 if self.a3 != 0 else 0, 
                     self.alpha, self.theta, self.beta)
    
    def __add__(self, other):
        if type(other) == type(self):
            return svtnn(self.a1 + other.a1,
                         self.a2 + other.a2,
                         self.a3 + other.a3,
                         min(self.alpha, other.alpha),
                         max(self.theta, other.theta),
                         max(self.beta, other.beta)
                        )
    
    def __sub__(self, other):
        if type(other) == type(self):
            return svtnn(self.a1 - other.a1,
                         self.a2 - other.a2,
                         self.a3 - other.a3,
                         min(self.alpha, other.alpha),
                         max(self.theta, other.theta),
                         max(self.beta, other.beta)
                        )
    
    def __mul__(self, other):
        if type(other) == type(2) or type(other) == type(2.):
            if other > 0:
                return svtnn(other * self.a1,
                             other * self.a2,
                             other * self.a3,
                             self.alpha,
                             self.theta,
                             self.beta
                            )
            elif other < 0:
                return svtnn(other * self.a3,
                             other * self.a2,
                             other * self.a1,
                             self.alpha,
                             self.theta,
                             self.beta
                            )
        if type(other) == type(self):
            if self.a3 > 0 or other.a3 > 0:
                return svtnn(self.a1 * other.a1,
                             self.a2 * other.a2,
                             self.a3 * other.a3,
                             min(self.alpha, other.alpha),
                             max(self.theta, other.theta),
                             max(self.beta, other.beta)
                            )
            if self.a3 < 0 and other.a3 > 0:
                return svtnn(self.a1 * other.a3,
                             self.a2 * other.a2,
                             self.a3 * other.a1,
                             min(self.alpha, other.alpha),
                             max(self.theta, other.theta),
                             max(self.beta, other.beta)
                            )
            if self.a3 < 0 or other.a3 < 0:
                return svtnn(self.a3 * other.a3,
                             self.a2 * other.a2,
                             self.a1 * other.a1,
                             min(self.alpha, other.alpha),
                             max(self.theta, other.theta),
                             max(self.beta, other.beta)
                            )
    
    def __truediv__(self, other):
        if type(other) == type(2) or type(other) == type(2.):
            if other > 0 :
                return svtnn(self.a1 / other,
                             self.a2 / other,
                             self.a3 / other,
                             self.alpha,
                             self.theta,
                             self.beta)
            elif other < 0 :
                return svtnn(self.a3 / other,
                             self.a2 / other,
                             self.a1 / other,
                             self.alpha,
                             self.theta,
                             self.beta
                            )
        if type(other) == type(self):
            if self.a3 > 0 and other.a3 > 0:
                return svtnn(self.a1 / other.a3,
                             self.a2 / other.a2,
                             self.a3 / other.a3,
                             min(self.alpha, other.alpha),
                             max(self.theta, other.theta),
                             max(self.beta, other.beta)
                            )
            if self.a3 < 0 and other.a3 > 0:
                return svtnn(self.a3 / other.a3,
                             self.a2 / other.a2,
                             self.a1 / other.a1,
                             min(self.alpha, other.alpha),
                             max(self.theta, other.theta),
                             max(self.beta, other.beta)
                            )
            if self.a3 < 0 and other.a3 < 0:
                return svtnn(self.a3 / other.a3,
                             self.a2 / other.a2,
                             self.a1 / other.a1,
                             min(self.alpha, other.alpha),
                             max(self.theta, other.theta),
                             max(self.beta, other.beta)
                            )
                
            
    
    def __div__(self, other):
        self.__truediv__(self, other)
    
    def deneutrosophy(self):
        # return abs( ( (self.a1 + self.a2 + self.a3) / 3) + ( self.alpha - self.theta - self.beta ) )
        return abs(pow(self.a1 * self.a2 * self.a3, (self.alpha + self.theta + self.beta) / 9))
    
    def __repr__(self):
        return f'<<{round(self.a1,2)}, {round(self.a2,2)}, {round(self.a3,2)}>,{round(self.alpha,2)}, {round(self.theta,2)}, {round(self.beta,2)}>'

    
    
    def plot_me(self):
        #TODO
        pass