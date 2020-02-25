#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 15:24:13 2020
@author: Lukas Baur

TODO future: group into the following types
- Discrete random variables
    - X∼Bernoulli(p)    ! DONE
    - X∼Binomial(n,p)
    - X∼Geometric(p)
    - X∼Poisson(λ)
- Continuous random variables
    - X∼Uniform(a,b)    ! DONE
    - X∼Exponential(λ)  ! DONE
    - X∼Normal(μ,σ²)    ! DONE
    - X∼K-Erlang(λ)     ! DONE
    - X∼SymTriange(a,b) ! DONE
    - X∼Ramp(a,off)     ! DONE
"""


# local file
import rngStream
import numpy as np

class Distribution:
    def sketch(self, samples=100000, bins=100):
        import matplotlib.pyplot as plt
        
        plt.hist([self.X() for _ in range(samples)], bins=bins, density=True)
        plt.title("f(x) for " + str(self))
        plt.show()

#------------------------------------------------------------------------------------------------------ 
        
#------------------------------------   Discrete random variables -------------------------------- 

#                                        X ∈ {E1, E2, ..., En}

#------------------------------------------------------------------------------------------------------ 


class BernoulliDistribution(Distribution):
    """
    X ∈ {0,1}
    p(X = 1) = p
    p(X = 0) = 1-p
    """
    def __init__(self, p=0.5):
        self.p = p
        self.unigen = UniformDistribution()  
    
    def __str__(self):
        return "X∼Bernoulli({})".format(self.p)
        
 
    def X(self):
        return 1 if self.unigen.X() < self.p else 0
    

#------------------------------------------------------------------------------------------------------ 
        
#------------------------------------   Continuous random variables -------------------------------- 

#                                             X ∈ [a, b]

#------------------------------------------------------------------------------------------------------ 







class UniformDistribution(Distribution):
    def __init__(self, name="UniGenDist01", lower=0.0, upper=1.0):
        self.range = upper - lower
        self.upper = upper
        self.lower = lower
        self.unigen = rngStream.RngStream(name)
    
    def __str__(self):
        return "X~U({},{})".format(self.lower, self.upper)
        
    def get_random_U01(self):
        return self.unigen.RandU01()
 
    def X(self):
        u = (self.unigen.RandU01() * self.range) + self.lower
        return u

class NormalDistribution(Distribution):
    def __init__(self,mean=0, var=1):
        self.random_values = []
        self.var = var
        self.std = var**0.5
        self.mean = mean
        self.unigen = UniformDistribution()        
        
    def __str__(self):
        return "X~N({},{})".format(self.mean, self.var)

    def X(self):
        if len(self.random_values) == 0:
            self.__generate_new_random_variables()
        return self.random_values.pop()

    def __generate_new_random_variables(self):
        U_1 = self.unigen.X()
        U_2 = self.unigen.X()
        X_1 = (-2 * np.log(U_1))**0.5 * np.cos(2 * np.pi * U_2)
        X_2 = (-2 * np.log(U_1))**0.5 * np.sin(2 * np.pi * U_2)
        # scale
        X_1 *= self.std 
        X_2 *= self.std
        # shift
        X_1 += self.mean
        X_2 += self.mean

        self.random_values.append(X_1)
        self.random_values.append(X_2)
        

class ExponentialDistribution(Distribution):
    def __init__(self,lam):
        self.lam = lam
        self.lam_inv = 1/lam
        self.unigen = UniformDistribution()        
        
    def __str__(self):
        return "X~Exp({})".format(self.lam)

    def X(self):
       return -self.lam_inv * np.log(self.unigen.X())


class KErlangDistribution(Distribution):
    def __init__(self,lam,k):
        self.lam = lam
        self.k = k
        self.expgen = ExponentialDistribution(lam)        
        
    def __str__(self):
        return "X~{}-Erlang({})".format(self.k, self.lam)

    def X(self):
        x_sum = self.expgen.X()
        for _ in range(self.k-1):
            x_sum += self.expgen.X()
        return x_sum

class SymmetricTriangleDistribution(Distribution):
# f(x):          o 
#              o | o
#            o   .   o
#          o     |     o
#        o       .       o
#      o         |         o
# ___o___________.___________o_______
#    |<----r---->|           |
#    |                       |
#    lower                   upper
    
    def __init__(self,lower, upper):
        self.upper = upper
        self.lower = lower
        self.r = (upper - lower)/2
        self.unigen = UniformDistribution()        
        
    def __str__(self):
        return "X~SymTriangle([{},{}])".format(self.lower, self.upper)

    def X(self):
       return self.r *(self.unigen.X() + self.unigen.X()) + self.lower
   
  
class RampDistribution(Distribution):
# f(x):                      o 
#                        o   |
#                    o       |
#                o           |
#            o               |
#        o                   |
# ___o_______________________|_______
#    |<----------a---------->|
#    |                       
#    offset                   
    
    def __init__(self,a, offset=0):
        self.a = a
        self.offset = offset
        self.unigen = UniformDistribution()        
        
    def __str__(self):
        return "X~Ramp({}, offset={})".format(self.a, self.offset)

    def X(self):
       return self.offset + (self.unigen.X() ** 0.5) * self.a
   
    
    
    
    
    
    
    
    
#------------------------------------------------------------------------------------------------------ 
        
#------------------------------------   Playgroud ----------------------------------------------------- 

#------------------------------------------------------------------------------------------------------ 


def plot_distrubutions():
    
    import matplotlib.pyplot as plt
    
    dists = [RampDistribution(3,5), 
             SymmetricTriangleDistribution(-3,8), 
             BernoulliDistribution(0.2), 
             ExponentialDistribution(3),
             KErlangDistribution(0.1,2)
            ]
    for dist in dists:
        dist.sketch()
        
#uncomment to test
#plot_distrubutions() 