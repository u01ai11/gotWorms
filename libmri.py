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


class MRITriggerBox:
    
    def __init__(self, device="Dev1"):
        
        """Initialises the MRI Trigger Box. Note that the button box buttons'
        names and channels are hard-coded into the initialisation function.
        The same is true for the scanner pulse channel.

        Keyword Arguments
        
        device              -   String indicating the name of the device.
                                Don't mess with this unless you know what
                                you're doing. Default = "Dev1"
        """
        
        # Channel for scanner pulse.
        self._scan_chan = "port0/line0"
        
        # Create a dict with all short-hand button names and associated ports.
        self._button_list = ["B1", "B2", "B3", "B4"]
        self._buttons = { \
            "B1":   "port0/line1", \
            "B2":   "port0/line2", \
            "B3":   "port0/line3", \
            "B4":   "port0/line4", \
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
        print("Scanner pulse: %s" % (self._scan_chan))
        print("Buttons: %s" % (self._buttons))
    
    
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
    
    
    def wait_for_sync(self, timeout=10.0):
        
        # Get the starting time.
        t0 = time.time()
        # Create a new Task to listen in on the button channels.
        with nidaqmx.Task() as task:
            # Loop until a signal or a timeout happens.
            triggered = False
            timed_out = False
            while not triggered and not timed_out:
                # Add the digital input (di) channels.
                task.di_channels.add_di_chan("%s/%s:1" % \
                    (self._dev_name, self._scan_chan))
                # Get a single sample from the digital input channels.
                state = task.read(number_of_samples_per_channel=1, timeout=1.0)
                t = time.time()
                # Check the sample.
                if state:
                    triggered = True
                # Check the time.
                if t - t0 > timeout:
                    timed_out = True
        
        return t, triggered, timed_out
        
        
        
        
