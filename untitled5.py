# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 15:11:36 2018

@author: stim22user
"""

from libmeg import *
trig = MEGTriggerBox()
output = trig.wait_for_button_press(allowed=["Rg"])
print(output)