#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
# MRC CBU PYTHON MEG WRAPPER
#
# This library is intended to allow for easy communication between our
# experiment and the MEG setup at the MRC Cognition and Brain Sciences Unit.
# It is based on the MATLAB class for doing the same thing by Tibor Auer and
# Johan Carlin (https://github.com/MRC-CBU/megsync/blob/master/MEGSynchClass.m)
# The implementation is intended for the CBU setup only, and uses the custom
# National Instruments setup in the MEG lab.
#
# Author: Edwin Dalmaijer
# Email: Edwin.Dalmaijer@mrc-cbu.cam.ac.uk
# Date: 2018-10-24
# Last update: 2018-10-24

import time
import nidaqmx


class MEGTriggerBox:
    
    def __init__(self, device="Dev1"):
        
        """Initialises the MEG Trigger Box. Note that the button box buttons'
        names and channels are hard-coded into the initialisation function.
        The same is true for the trigger channels.

        Keyword Arguments
        
        device              -   String indicating the name of the device.
                                Don't mess with this unless you know what
                                you're doing. Default = "Dev1"
        """
        
        # Create a dict with all short-hand button names and associated ports.
        self._button_list = ["S3", "S4", "S5", "S6", "S7"]
        self._buttons = { \
            "S3":   "port0/line1", \
            "S4":   "port0/line2", \
            "S5":   "port0/line3", \
            "S6":   "port0/line4", \
            "S7":   "port0/line0", \
            }
        
        # Create a dict with all the trigger names and associated ports.
        n_trigger_channels = 8
        self._trigger_list = range(n_trigger_channels)
        self._triggers = {}
        for i in self._trigger_list:
            self._triggers[i] = "port2/line%d" % (i)
        
        # INITIALISE
        print("\nInitialising connection to the NI box...")
        # Initialise the system.
        system = nidaqmx.system.System.local()
        # Present the available devices.
        print("\tAvailable NI devices:")
        for dev_name in system.devices:
            print("\t\t%s" % (dev_name))
        # Connect to the passed device.
        self._dev_name = device
        self._dev = system.devices[self._dev_name]
        
        print("\nConnection established with '%s'!" % (self._dev_name))
        print("\tDevice: %s" % (self._dev))
        print("\tDriver version: %s" % (system.driver_version))
        print("\nChannel details:")
        print("Buttons: %s" % (self._buttons))
        print("Triggers: %s" % (self._triggers))
    
    
    def get_button_state(self, button_list=None):
        
        """Returns a single sample from the button channels.
        
        Keyword Arguments
        
        button_list         -   List of button names, or None to automatically
                                poll all the buttons. Default = None
        
        Returns
        
        button_list, state  -   button_list is a list of all button names, and
                                state is a list of the associated values.
        """
        
        if button_list is None:
            button_list = self._button_list[:]
        
        # Create a new Task to listen in on the button channels.
        with nidaqmx.Task() as task:
            # Add the digital input (di) channels.
            for butt in button_list:
                task.di_channels.add_di_chan("%s/%s:1" % \
                    (self._dev_name, self._buttons[butt]))
            # Get a single sample from the digital input channels.
            state = task.read(number_of_samples_per_channel=1, \
                timeout=1.0)
        
        return button_list, state
    
    
    def set_trigger_state(self, value):
        
        """Sets the current trigger states to an 8-bit value.
        
        Arguments
        
        value               -   Unsigned 8-bit integer value, i.e. an int
                                between 0 and 255. Passing anything else, even
                                a float, will result in an Exception.
        
        Returns
        
        t                   -   Time of the trigger being sent, clocked
                                directly after the write function returns
                                (based on time.time).
        """
        
        # Input sanity checks.
        if value < 0 or value > 255 or type(value) != int:
            raise Exception("ERROR: Invalid value '%s' (type=%s); please use an unsigned 8-bit integer!" \
                % (value, type(value)))
        
        # Compute the binary value associated with the current value. The
        # result is a string with length 8.
        binary = bin(value)[1:].replace('b', '').zfill(8)
        
        # Convert the binary into input that the NI API can understand. This
        # needs to be in the form of a list of lists, with each list 
        # corresponding to a channel, and the content of each list
        # corresponding to a single sample or a list of samples.
        output = []
        for val in list(binary):
            output.append([val])
        
        # Create a new Task to listen in on the button channels.
        with nidaqmx.Task() as task:
            # Add the digital output (do) channels.
            for trigger in self._trigger_list:
                task.di_channels.add_do_chan("%s/%s:1" % \
                    (self._dev_name, self._trigger_list[trigger]))
            # Write a single sample to each channel.
            task.write(list(binary), timeout=1.0)
            t = time.time()
        
        return t
        
        
        
