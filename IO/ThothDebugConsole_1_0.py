#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 25 20:21:12 2020
@author: Lukas Baur

This framework should help outputting and debugging using output levels.
(level of abstraction)
"""

#------------------------------------------------------------------------------------------------------ 
        
#---------------------------------------   Standard output -------------------------------------------- 


#------------------------------------------------------------------------------------------------------ 


class DebugOutputFormatter():
    """
    debug_level ∈ [1,10], decribes the proirity
        1    = gets printed every time (even productive)
        2-3  = gets printed for advanced output (productive)
        4-6  = detailed outputs, helpful for debugging and in extreme cases for productive
        7-8  = for debugging purposes, high level implementation output
        9-10 = for debugging purposes, (very) low level implementation output
    """
    def __init__(self, debug_level=10, output_length=60, fill_line=' ', var_field_length=25):
        self.debug_level = debug_level
        self.output_length = output_length
        self.fill_line = fill_line
        self.var_field_length = var_field_length
    
    def __str__(self):
        return "<DebugOutputFormatter object, output_level:{}>".format(self.debug_level)
    
    def __print_if_level_fit(self, text, prio):
        if prio <= self.debug_level:
            print(text)
        
    def info(self, value, debug_level, info_key="[INFO]", align="r"):
        """
        value       = the message
        debug_level = output level 
        [info_key]  = label frame for output 
        [align]     = either "r", "l", "rx" or "lx" where x is an integer
        """
        
        DEFAULT_RIGHT_INTENDENT = 0
        DEFAULT_LEFT_INTENDENT = 3
        KEY_TO_VALUE_INTENDENT = 2
        fill_line = self.fill_line
        
        if align[0] == 'r':
            intendent = DEFAULT_RIGHT_INTENDENT
            if len(align) > 1:
                intendent = int(str(align[1:]))
            right = intendent
            left = max(self.output_length - right - KEY_TO_VALUE_INTENDENT- len(str(info_key)) - len(str(value)) , 0)
            output = "{}{}{}{}{}".format(left*fill_line, value, KEY_TO_VALUE_INTENDENT*fill_line, info_key, right*fill_line) 
        elif align[0] == 'l':
            intendent = DEFAULT_LEFT_INTENDENT  
            if len(align) > 1:
                intendent = int(str(align[1:]))
            left = intendent
            right = max(self.output_length - left - KEY_TO_VALUE_INTENDENT -len(str(info_key)) - len(str(value)) , 0)
            output = "{}{}{}{}{}".format(left*fill_line, info_key, KEY_TO_VALUE_INTENDENT*fill_line, value, right*fill_line) 
        else:
            raise ValueError("align can only take values 'l', 'r', 'lx' or 'rx' where x is an integer")
            
        self.__print_if_level_fit(output, debug_level)
        
    def var(self, varname, value, debug_level):
        """
        varname     = description of the variable
        value       = value of the variable
        debug_level = output level 
        
        a variable is per default left-aligned
        """
        
        DEFAULT_INTENDENT = 3
        fill_line = self.fill_line

        left = DEFAULT_INTENDENT 
        space = max(self.var_field_length - left - len(str(varname)) -1, 0)
        right = max(self.output_length - left -space -len(str(varname)) -1 - len(str(value)), 0)
        output = "{}{}:{}{}{}".format(left*fill_line, varname, space*fill_line, value, right*fill_line) 
      
        
        self.__print_if_level_fit(output, debug_level)
        
    
    def chapter(self, chaptername, nr, seperator="=", align='c', prio=None, debug_level=1):
        """
        chaptername = description of output title
        nr          = current chapter number
        align       = "c"  (center) or 
                      "lx" (left,  x times indented) or 
                      "rx" (right, x times indented)
        prio        = defines an automatic indentend (for non-center align only, if no align defined 'left' is choosen)
        """
        DEFAULT_INTENDENT = 3
        PRIO_INTENDENT_STEP_SIZE= 2
        
        rest_length = self.output_length - 3 - len(str(nr)) - len(chaptername)
        rest_seperators = int( rest_length / len(str(seperator)) ) 
        
        
        if prio != None:
            if align=='c':
                align = 'l'
            if len(align) > 1:
                intendent = int(align[1:])
                intendent += PRIO_INTENDENT_STEP_SIZE * int(prio)
            else:
                intendent = PRIO_INTENDENT_STEP_SIZE * int(prio)
            align = align[0] + str(intendent)
        
        if align == 'c':
            left = int(rest_seperators / 2)  
            right = rest_seperators - left
        elif align[0] == 'l':
            intendent = int(align[1:]) if len(align) > 1 else DEFAULT_INTENDENT
            left = intendent  
            right = rest_seperators - left
        elif align[0] == 'r':
            intendent = int(align[1:]) if len(align) > 1 else DEFAULT_INTENDENT
            right = intendent 
            left = rest_seperators - right
        else:
            raise ValueError("align can only take values 'c', 'lx', 'rx' where x is an integer")
                
        output = "{} {} {} {}".format(left*seperator, chaptername, nr, right*seperator) 
        self.__print_if_level_fit(output, debug_level)
        
    def empty(self, debug_level):
        self.__print_if_level_fit("", debug_level)
        
        
        
def print_example_code():
    dof = DebugOutputFormatter()

    dof.chapter("Question", "4", prio=1)
    dof.chapter("Question", "4.1", prio=2)
 
    dof.var("y", 7, 1)
    dof.var("List lst", [1,292,2,1], 1)
    
    
    dof.chapter("Question", "4.2", prio=2)
    dof.chapter("Question", "4.2.1", prio=3)
    dof.var("x", hex(4), 1)
    dof.var("boolean", True, 1)
    

    dof.chapter("Question", "5")
    dof.info("wichtig", 1)
    dof.info("also very important", 1)

#print_example_code()