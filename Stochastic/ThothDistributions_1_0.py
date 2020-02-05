#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 15:24:13 2020
@author: Lukas Baur

TODO future: group into the following types
- Discrete random variables
    - X∼Bernoulli(p) 
    - X∼Binomial(n,p)
    - X∼Geometric(p)
    - X∼Poisson(λ)
- Continuous random variables
    - X∼Uniform(a,b)      ! DONE
    - X∼Exponential(lambda)
    - X∼Normal(mu,var)    ! DONE
"""


# local file
import rngStream
import numpy as np


class UniformDistribution:
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

class NormalDistribution:
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