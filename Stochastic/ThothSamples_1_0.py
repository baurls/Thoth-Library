#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 13:25:58 2020

@author: Lukas Baur
"""

import numpy as np

class Estimator():
    
    def __init__(self, n):
        self.samples = np.zeros(n)
        self.i = 0 #next index to fill value in
        
    def process_next_val(self, value):
        self.samples[self.i] = value
        self.i += 1
        
    def all_samples(self):
        return self.samples[0:self.i]
    
    def mean(self):
        return np.mean(self.all_samples())
    
    def var(self):
        return np.var(self.all_samples(), ddof=1)
    
    def std(self):
        return np.std(self.all_samples(), ddof=1)
    
    def ci(self, tolerance):
        """
        GIVEN:   1) n samples
                 2) tolerance (often: 0.05 or 0.01)
        RETUN:   μ ± halfwidth
    
        e.g. tolerance=0.05 means:
            P(μ* ∈ [μ-halfwidth,μ+halfwidth] )  = 1- 0.05
            P(μ-halfwidth ≤ μ* ≤ μ+half_width)  = 1- 0.05
        """
        z_gamma = CiUtil.zgamma(tolerance)
        half_width = (z_gamma * self.std()) / (self.i ** 0.5)
        
         # return (μ, half_width)
        return ConfidenceInterval(self.mean(), half_width, z_gamma=z_gamma, std=self.std(), n=self.i)
     
    def good_n_estimate(self, delta=0.05, eps=(0.05,'rel')):
        '''
            Make predictoin how large n shoud be, such that
            μ* = μ  ± eps        (absolute case)
            μ* = μ  * (1 ± eps)  (realtive case)
            with probability 1-delta
        '''
        eps_val  = eps[0]
        eps_type = eps[1]
        params = CiUtil.EstParams(delta, eps_val, eps_type)
        return CiUtil.n_that_fits_CI(params, self)
    
#------------------------------------------------------------------------------------------------------ 
        
#------------------------------------   Confidence Interval Management -------------------------------- 

#------------------------------------------------------------------------------------------------------ 



class ConfidenceInterval:
    def __init__(self, mean, halfwidth, z_gamma=None, std=None, n=None):
        self.mean = mean
        self.halfwidth = halfwidth
        self.z_gamma = z_gamma
        self.std=std
        self.n=n
        
    def __str__(self, output_precision=4):
        mean = np.round(self.mean, decimals=output_precision)
        halfwidth = np.round(self.halfwidth, decimals=output_precision)
        return "[CI:{} ± {}]".format(mean, halfwidth)
       
        
    

class CiUtil:
    
    class EstParams:
        """
          delta = P(mean outside of CI) (e.g. 0.05 means 95% guarantee within CI)
          eps_type = 'rel' or 'abs  
          eps = halfwidth of CI (in rel or abs)
          
          example: CiUtil.EstParams(0.05, 2, 'abs')
          example: CiUtil.EstParams(0.05, 0.1, 'rel') 
        """
        def __init__(self, delta, eps, eps_type):
            self.delta = delta
            if eps_type == 'rel':
                self.rel_eps = eps
                self.has_relative_eps = True
            elif eps_type == 'abs':
                self.abs_eps= eps
                self.has_relative_eps = False
            else:
                raise ValueError("No such eps type available: {}. Choose 'abs' or 'rel'".format(eps_type))
                
            
            
#
#                                       o o
#                                   o        o
#                                o              o
#                             o                    o
#                           o                        o 
#                         o |                        | o
#                      o    |       1 - delta        |    o
#                  o        |                        |        o
#             o             |                        |              o
#      o        0.5*delta   |                        |    0.5*delta      o
#o__________________________|________________________|________________________o
#   
#
#  gamma = (0.5*delta) + (1 - delta)
#        = 1 - 0.5*delta
#
    
    zgamma_loockup = {   0.6    : 0.253, 
                         0.7    : 0.524, 
                         0.8    : 0.842,
                         0.9    : 1.282, 
                         0.9333 : 1.501, 
                         0.95   : 1.645,   #0.1    = 10% 
                         0.96   : 1.751, 
                         0.9667 : 1.834, 
                         0.975  : 1.960,   #0.05  = 5% 
                         0.98   : 2.054,   #0.04  = 4% 
                         0.9833 : 2.127, 
                         0.9875 : 2.241,   #0.025 = 2.5%
                         0.99   : 2.326,   #0.02  = 2%
                         0.9917 : 2.395, 
                         0.9928 : 2.501,   
                         0.995  : 2.576    # 0.01 = 1%
                      }   
    
    def zgamma(delta):
        gamma = 1-(delta/2)
        discrete_gamma = np.round(gamma, decimals=4)
        if discrete_gamma not in CiUtil.zgamma_loockup:
            raise ValueError('The delta value (=' + str(delta)+ ') for the confidence interval is not supported.')
        z_gamma = CiUtil.zgamma_loockup[discrete_gamma]
        return z_gamma
    
    def n_that_fits_CI(estParams, estimator):
            """
            Returns a n, such that:
                P(μ* ∈ [μ ± eps] )  = 1 - delta
                
            example 1    
                delta=0.05, eps=3 (abs) means:
                choose n s.t. P(μ* ∈ [μ-3,μ+3])   = 0.05
                              P(μ-3 ≤ μ* ≤ μ+3)  = 0.05
            example 2    
                delta=0.05, eps=0.03 (rel) means:
                choose n s.t. P(μ in [μ'-(0.03μ'),μ'+(0.03μ')])  = 0.05
                              P(0.97μ'<= μ <= 1.03μ')            = 0.05
            """
            
            numerator = estimator.var() * (CiUtil.zgamma(estParams.delta) ** 2.0) 
            if estParams.has_relative_eps:
                # Relative eps
                # Estimate μ to within ±μ*eps with probabilty (1-delta)
                denumerator =  ((estParams.rel_eps**2) * (estimator.mean()**2))   
            else:
                # Absolute eps
                # Estimate μ to within ±eps with probabilty (1-delta)
                denumerator =  (estParams.abs_eps**2) 
            return numerator  /  denumerator
        
    
    
#------------------------------------------------------------------------------------------------------ 
        
#-------------------------------------------    Example usages   -------------------------------------- 

#------------------------------------------------------------------------------------------------------ 
"""
est = Estimator(4)
est.process_next_val(124.2)
est.process_next_val(128.3)
est.process_next_val(100.9)
print(est.ci(0.02))

k1 = CiUtil.n_that_fits_CI(CiUtil.EstParams(delta=0.05, eps=0.01, eps_type='abs'), est)
print(k1)
k2 = CiUtil.n_that_fits_CI(CiUtil.EstParams(0.05, 3.1, 'abs'), est)
print(k2)
"""
