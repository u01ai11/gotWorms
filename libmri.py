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
# Last update: 2018-11-21

import copy
import time

import nidaqmx
from nidaqmx.constants import LineGrouping


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
        
        # Create a list with all short-hand button names.
        self._button_list = ["B1", "B2", "B3", "B4"]
        # Set all the channel names for the buttons.
        self._button_channels = "port0/line1:4"
                
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
                                state is a list of the associated Booleans.
        """
        
        # Create a new Task to listen in on the button channels.
        with nidaqmx.Task() as task:
            # Add the digital input (di) channels.
            task.di_channels.add_di_chan( \
                "%s/%s" % (self._dev, self._button_channels), \
                line_grouping=LineGrouping.CHAN_PER_LINE)
            # Get a single sample from the digital input channels.
            state = task.read(number_of_samples_per_channel=1, \
                timeout=0.001)
        
        # Unwrap state, which is a list of lists of samples.
        # Example: [[False], [False], [False], [False], [False]]
        # We want instead: [False, False, False, False, False]
        for i, b in enumerate(state):
            state[i] = b[0]

        # Select all buttons if no specific ones are requested.
        if button_list is None:
            return copy.deepcopy(self._button_list), state

        # Return only the requested buttons.
        else:
            l = []
            for b in button_list:
                if b not in self._button_list:
                    raise Exception("ERROR: Unknown button '%s'; available buttons: %s" \
                        % (b, self._button_list))
                i = self._button_list.index(b)
                l.append(state[i])
            return button_list, l
    
    
    def wait_for_sync(self, timeout=10.0):
        
        """
        """
        
        # Get the starting time.
        t0 = time.time()

        # Create a new Task to listen in on the button channels.
        with nidaqmx.Task() as task:
            # Add the digital input (di) channels.
            task.di_channels.add_di_chan("%s/%s" % \
                (self._dev_name, self._scan_chan))

            # Loop until a signal or a timeout happens.
            triggered = False
            timed_out = False
            while not triggered and not timed_out:
                # Get a single sample from the digital input channels.
                state = task.read(number_of_samples_per_channel=1, timeout=1.0)
                t1 = time.time()
                # Check the sample (turns False when triggered).
                if not state[0]:
                    triggered = True
                    break
                # Check the time.
                if t1 - t0 > timeout:
                    timed_out = True
        
        return t1, triggered, timed_out
    
    
    def wait_for_button_press(self, allowed=None, timeout=None):
        
        """Waits for a button press.
        
        Keyword Arguments
        
        allowed             -   List of strings with allowed button names, or
                                None to allow all buttons. Default = None
        
        timeout             -   Float or int that indicates the timeout in
                                seconds. If no button is pressed within the
                                timeout, this function will return. The
                                timeout can be None, meaning no timeout will
                                occur. Default = None
        
        Returns

        button, time        -   button is a string that indicates the pressed
                                button's name (only the first-pressed button
                                is counted), or None if no button was pressed
                                before a timeout occured.
                                time is a float value that reflects the time
                                in seconds at the time the button press was
                                detected.
        """
        
        # Get the indices of the allowed buttons.
        if allowed is not None:
            allow = []
            for b in allowed:
                if b not in self._button_list:
                    raise Exception("ERROR: Unknown button '%s'; available buttons: %s" \
                        % (b, self._button_list))
                allow.append(self._button_list.index(b))
        else:
            allow = range(len(self._button_list))

        # Get the starting time.
        t0 = time.time()
        t1 = time.time()
        
        # Create a new Task to listen in on the button channels. Using a with
        # statement will automatically close the Task if an error happens
        # during execution, leaving the NI box in a better state.
        with nidaqmx.Task() as task:

            # Add the digital input (di) channels.
            task.di_channels.add_di_chan( \
                "%s/%s" % (self._dev, self._button_channels), \
                line_grouping=LineGrouping.CHAN_PER_LINE)
            # Start the task (this will reduce timing inefficience when
            # calling the task.read function).
            task.start()

            # Run until a timeout or a button press occurs.
            button = None
            pressed = False
            while not pressed and t1 - t0 < timeout:

                # Get a single sample from the digital input channels.
                state = task.read(number_of_samples_per_channel=1, \
                    timeout=0.001)
                # Get a timestamp for the sample.
                t1 = time.time()

                # Check whether any of the allowed buttons were pressed.
                for i in allow:
                    if state[i][0]:
                        pressed = True
                        button = self._button_list[i]
                        break
            
            # Stop the task.
            task.stop()
                
        return button, t1
        
        
        
        
