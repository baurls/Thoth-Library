#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 12:58:58 2020
@author: Lukas Baur

This framework helps timing program subroutines
"""

#------------------------------------------------------------------------------------------------------ 
        
#---------------------------------------   Standard timing -------------------------------------------- 


#------------------------------------------------------------------------------------------------------ 

import time

class Timer():
    def __init__(self, store_timed_results=True):
        self.active_timer = {}
        self.store_timed_results = store_timed_results
        if store_timed_results:
            self.measured_times = {}
    
    def start(self, identifier):
        self.active_timer[identifier] = time.time()
        return self.active_timer[identifier]

    def stop(self, identifier):
        end_time = time.time()
        start_time = self.active_timer.pop(identifier)
        time_delta = end_time - start_time 
        if self.store_timed_results:
            self.measured_times[identifier] = time_delta
        return time_delta
    
    def time_needed(self, identifier):
        if self.store_timed_results == False:
            raise ValueError("You specified the object not to store timed results.")
        return self.measured_times[identifier]


#------------------------------------------------------------------------------------------------------ 
        
#---------------------------------------   Example usage -------------------------------------------- 


#------------------------------------------------------------------------------------------------------ 
def plot_example_usage():
    #some work simulations
    def sub1():
        for i in range(5000): #do some work
            pass
    def sub2():
        for i in range(10000): #do some work
            pass
        
    
    #run program
    timer = Timer()
    timer.start('whole Programm')
    timer.start('subroutine 1')
    sub1()
    timer.stop('subroutine 1')
    timer.start('subroutine 2')
    sub2()
    timer.stop('subroutine 2')
    timer.stop('whole Programm')
    # get timing results
    for timer_id in ['whole Programm', 'subroutine 1', 'subroutine 2']:
        delta_time = timer.time_needed(timer_id)
        print("time needen for {}: {}s".format(timer_id, delta_time))