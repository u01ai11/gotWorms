import os
import copy
import random

import numpy

from constants import *

from pygaze.display import Display
from pygaze.screen import Screen
from pygaze.keyboard import Keyboard
from pygaze.mouse import Mouse
from pygaze.logfile import Logfile
from pygaze.eyetracker import EyeTracker
import pygaze.libtime as timer

from libmeg import *

#%%

# # # # #
# INITIALISE

# Initialise a new Display instance.
disp = Display()

# Present a start-up screen.
scr = Screen()
scr.draw_text("Loading, please wait...", fontsize=MAIN_FONTSIZE)
disp.fill(scr)
disp.show()



# Open a new log file.
log = Logfile(filename = LOGFILE)
log_det = Logfile(filename = DETAILED_LOGFILE)
log_events = Logfile(filename = EVENT_LOGFILE)
# TODO: Write header.
log.write(["trialnr","left_ang","right_ang", "cue_dir", "targ", "targ_ang", "resp_ang", "perc_diff", "resp_onset", "resp_duration", "iti", "iti_onset", "stim_onset","delay_onset", "cue_onset", "postcue_onset","probe_onset", "prac"])
log_det.write(["trialnr", "timestamp", "angle", "event", "targ_ang", "cue_dir"])
log_events.write(["Trigger", "Timestamp"])
# Initialise the eye tracker.
tracker = EyeTracker(disp)

# Create a new Keyboard instance to process key presses.
kb = Keyboard(keylist=None, timeout=5000)
mouse = Mouse()
mouse.set_visible(visible=False)

# intitliase the MEG interface NI box 
if MEG:
    trigbox = MEGTriggerBox()

# initialise a function 


# trigbox.set_trigger_state(1) <= Example usage 

# btn_list, state = trigbox.get_button_state() <= example usage, needs to be constantly updated during task 

# (0) <= might have to do this



# # # # #
# RANDOMISATION

# Create list of trial dicts.
# One trial should contain the following information:
# - stimulus order (0 for stim0 left and stim1 right, 1 for vice versa)
# - cueside (0 for left, 1 for right)
# - probeside (0 for left, 1 for right)
# - probestim (should follow from stimulus direction and probeside)
    
#%%
trials = []


# everything between 200-255 for events 
# everything below is for response 1-180 where 180 = 0 

# second log file for continous response data => trial number, curr timestamp, curr orientation
# first log file is onset of screens - one line per trial, column for each event (e.g. trial, stim_onset, stim_offset, cue_onset etc., resposne, orientation, error, which stim was probed, blaalaal)



# Create a list of unique trials.
utrials = []
for stimorder in STIM_ORDERS:
    for cue_direction in CUE_DIRECTIONS:
        utrials.append({ \
            'stimorder':        stimorder, \
            'cue_direction':    cue_direction, \
            'probe_direction':  cue_direction, \
            })

# Loop through all repeats.
for i in range(UNIQUE_TRIAL_REPEATS):
    trials.extend(copy.deepcopy(utrials))

# Add stimulus orientations.
n_trials = len(trials)

# Generate uniform distributions on orientations for both stimuli.
stepsize = 180.0 / n_trials
stim0 = numpy.arange(0, 180.0, stepsize).astype(int)
stim1 = numpy.arange(0, 180.0, stepsize).astype(int)
#print(stim0)

# Randomise the stimulus orientations.
random.shuffle(stim0)
random.shuffle(stim1)

# Add all the orientations to the trials.
for i in range(len(trials)):
    trials[i]['stim0'] = stim0[i]
    trials[i]['stim1'] = stim1[i]

# We need jittered ITIs so get a distribution between the max and min given
stepsize = (ITI_RANGE[1] - ITI_RANGE[0]) /n_trials
itis = numpy.arange(ITI_RANGE[0], ITI_RANGE[1], stepsize).astype(int)
for i in range(len(trials)):
    trials[i]['iti'] = itis[i]


# Randomise trial order.
random.shuffle(trials)


#prac trials are just a random selection of 5 of the above trials 
prac_trials = trials[0:4]

#Re-shuffle trials to avoid repeat of the ten first trials
random.shuffle(trials)

#%%

# # # # #
# SCREENS

# Create a screen for each phase in the experiment.

# INSTRUCTIONS
instruction_screens = []
# First screen with text.
inst_scr = Screen()
instructions = \
"""
Welcome to the snake game. 

You will see some snakes on the screen, they will be facing different ways. 

The snakes aren't very good at remembering things, so you must help them. 

Try and remember where they face, then you will have to move them when they
re-appear. 

(Press any button to continue.)
"""
inst_scr.draw_text(instructions, fontsize=MAIN_FONTSIZE, center=True)
instruction_screens.append(inst_scr)

# Second screen with text and images.
inst_scr = Screen()
instructions = \
"""
Let's practice. 

Remember the way this snake is facing! 

When you are ready press a button to continue. 
"""
inst_scr.draw_text(instructions, fontsize=MAIN_FONTSIZE, pos = (DISPCENTRE[0], DISPCENTRE[1]-200))
fpath = os.path.join(RESDIR, STIMNAMES[0] + ".png")
inst_scr.draw_image(fpath, pos=(DISPCENTRE[0], DISPCENTRE[1]+150), scale = 0.7)
inst_scr.screen[2].ori = 100
instruction_screens.append(inst_scr)

# prac screen 1 
inst_scr = Screen()
instructions = \
"""
Can you remember which way the snake faced just now? 

Press the red and green keys in you right hand to turn the snake.
Press the yellow key in your left hand to respond. 
"""
inst_scr.draw_text(instructions, fontsize=MAIN_FONTSIZE, pos = (DISPCENTRE[0], DISPCENTRE[1]-200))
fpath = os.path.join(RESDIR, STIMNAMES[0] + ".png")
inst_scr.draw_image(fpath, pos=(DISPCENTRE[0], DISPCENTRE[1]+150), scale = 0.7)
inst_scr.screen[2].ori = 0
prac_scr = inst_scr

# prac screen 2 
inst_scr = Screen()
instructions = \
"""
Well done - you helped the snake to remember! 

Now we are going to practice with two snakes, 
try and remember which way both of them are going. 

But, you will only be asked to help one of them

Press the key once you have looked at BOTH snakes.
"""
inst_scr.draw_text(instructions, fontsize=MAIN_FONTSIZE, pos = (DISPCENTRE[0], DISPCENTRE[1]-200))
fpath = os.path.join(RESDIR, STIMNAMES[0] + ".png")
inst_scr.draw_image(fpath, pos=(STIMPOS[0][0],STIMPOS[0][1]+200), scale = 0.7)
inst_scr.screen[2].ori = 10
fpath = os.path.join(RESDIR, STIMNAMES[1] + ".png")
inst_scr.draw_image(fpath, pos=(STIMPOS[1][0],STIMPOS[1][1]+200) , scale = 0.7)
inst_scr.screen[3].ori = 145
prac_scr2 = inst_scr

 
print(prac_scr2.screen[1].text)
#prac screen 3 
inst_scr = Screen()
instructions = \
"""
Which way was this snake facing?
"""
inst_scr.draw_text(instructions, fontsize=MAIN_FONTSIZE, pos = (DISPCENTRE[0], DISPCENTRE[1]-200))
fpath = os.path.join(RESDIR, STIMNAMES[1] + ".png")
inst_scr.draw_image(fpath, pos=(STIMPOS[1][0],STIMPOS[1][1]+200) , scale = 0.7)
inst_scr.screen[2].ori = 0
prac_scr3 = inst_scr

#prac screen 4 
# First screen with text.
inst_scr = Screen()
instructions = \
"""
Well Done!

Now we are going to try a few more practices. 

This time you have to do it as fast as you can. 

But make sure to try and be accurate! 

You get a score after each one, 
try and make it as close to 100 as possible. 

(Press any button to continue.)
"""
inst_scr.draw_text(instructions, fontsize=MAIN_FONTSIZE)
prac_scr4 = inst_scr

#prac screen 5 
# Now this is the real version!
inst_scr = Screen()
instructions = \
"""
OK, that is the practice over -- you did really well! 

Now it is time for the main part of the task. 

Remember to try and be as accurate as possible, but don't take too long. 

You will have """+ str(int(n_trials/TRIAL_BREAKS)) +""" breaks in the task.  

(Press any button to continue.)
"""
inst_scr.draw_text(instructions, fontsize=MAIN_FONTSIZE)
prac_scr5 = inst_scr


# STIMULUS
# Create two Screens: One with worm A on the left and B on the right, and one
# vice versa.
stimscr = {}
stim_index = {}
for direction in [0, 1]:
    # Create a screen with two worms.
    stimscr[direction] = Screen()
    # Draw the fixation mark.
    stimscr[direction].draw_fixation(fixtype='cross', pw=XPEN, diameter=XDIAM)
    # Add all the stimuli.
    stim_index[direction] = []
    for i, stimname in enumerate(STIMNAMES):
        # Find the right position.
        if direction == 0:
            pos = STIMPOS[i]
        elif direction == 1:
            pos = STIMPOS[1-i]
        # Construct the path.
        fpath = os.path.join(RESDIR, stimname + ".png")
        # Draw the stimulus.
        stim_index[direction].append(len(stimscr[direction].screen))
        stimscr[direction].draw_image(fpath, pos=pos, scale = 0.7)




# DELAY
# Create a screen with just a fixation mark.
delayscr = Screen()
# Draw the fixation mark.
delayscr.draw_fixation(fixtype='cross', pw=XPEN, diameter=XDIAM)

# CUE
# Create a screen with a retro cue.
cuescr = {}
for direction in [-1, 0, 1]:
    cuescr[direction] = Screen()
    # Neutral.
    if direction == -1:
        cue = CUENAMES[0]
    # Left.
    elif direction == 0:
        cue = CUENAMES[1] 
    # Right.
    elif direction == 1:
        cue = CUENAMES[2] 
    cuescr[direction].draw_fixation(fixtype='cross', pw=XPEN, diameter=XDIAM)
    fpath = os.path.join(RESDIR, cue+".png")
    cuescr[direction].draw_image(fpath, pos=DISPCENTRE, scale = 0.2)

# PRE_RESP 
# Create screens with pre-resonse probe item 


# PROBE
# Create screens for each worm, on each location.
probescr = {}
probe_index = {}
for direction in [0,1]:
    probescr[direction] = {}
    probe_index[direction] = {}
    for i, stimname in enumerate(STIMNAMES):
        # Create a new screen.
        probescr[direction][stimname] = Screen()
        # Draw the fixation mark.
        probescr[direction][stimname].draw_fixation(fixtype='cross', pw=XPEN, diameter=XDIAM)
        # Draw the worm on the correct position.
        fpath = os.path.join(RESDIR, stimname + ".png")
        probe_index[direction] = len(probescr[direction][stimname].screen)
        probescr[direction][stimname].draw_image(fpath, pos=STIMPOS[direction], scale = 0.7)

#FEEDBACK 
feedscr = Screen()
feedtxt = ""
feedscr.draw_text(feedtxt, fontsize=MAIN_FONTSIZE)

#BREAK SCREEN
breakscr = Screen()
breaktxt = \
"""
This is one of your breaks. 

You will have another in """ + str(int(TRIAL_BREAKS)) + \
""" more trials.

PRESS ANY BUTTON TO END THE BREAK
"""
breakscr.draw_text(breaktxt, fontsize=MAIN_FONTSIZE)





# # # # #
# DISPLAY INSTRUCTIONS 

#loop through instruction screens 
for scrn in instruction_screens: 
    timer.pause(100)
    disp.fill(scrn); 
    disp.show()
    btn_pressed = False  
    if MEG: # if MEG repeatedly loop until button state changes
        trigbox.wait_for_button_press()

    else: 
        mouse.get_clicked()


#now show the first practice screen 
disp.fill(prac_scr)
timer.pause(500) # pause so snake does not appear to be instantly moving
disp.show()

target_ang = 100
start_time = timer.get_time()
time_at_target = 0; 
time_last = 0
time_now = 0
time_trial = 0
correct = True; 
end_press = False
while (time_at_target < 0.2 and time_trial < 10000 and end_press == False):
    # get current time 
    time_now = timer.get_time()
    #since start
    time_trial = time_now - start_time
    if (time_trial >= 10000): #if timeout then we didn't get this right
        correct = False; 
    # duration of the last frame 
    time_frame = time_now - time_last 
    # Poll the input device.
    
    if MEG:
        btn_list, state = trigbox.get_button_state(button_list = [LEFT_BUT, RIGHT_BUT, MAIN_BUT]) # get button states 
        # we need to replicate the get_pressed() pygame functionality 
        button_states = [False, False] # list of bools 
        if state[0] != 0: # if left button is not 0
            button_states[0] = True
        if state[1] != 0: # if right button is not 0 
            button_states[-1] = True 
        if state[2] != 0:
            end_press = True
        key, presstime = kb.get_key(keylist=['q', 'f', 'j'], timeout=1, flush=False)


    else:
        key, presstime = kb.get_key(keylist=['q', 'f', 'j'], timeout=1, flush=False)
        button_states = mouse.get_pressed()
    # Break loop on 'q' press.
    if key == 'q':
        log.close()
        tracker.close()
        disp.close()
        raise Exception('DEBUG KILL')
    # Rotate the stimulus accordingly.
    if  button_states[0]:
        pre_clamp = prac_scr.screen[2].ori - 1
        prac_scr.screen[2].ori = clamp_angle(int(pre_clamp))
    elif button_states[-1]:
        pre_clamp = prac_scr.screen[2].ori +1
        prac_scr.screen[2].ori = clamp_angle(int(pre_clamp))
    # if at target time add the length of this frame 
    angle = prac_scr.screen[2].ori
    # reduce the angle  
    angle =  angle % 360; 
    #force it to be the positive remainder, so that 0 <= angle < 360  
    angle = (angle + 360) % 360;  
    #force into the minimum absolute value residue class, so that -180 < angle <= 180  
    if (angle > 180):
        angle -= 360;  
    if target_ang - 30 <= abs(angle) <= target_ang + 30:
        time_at_target += time_frame
    print(time_at_target, angle, target_ang)
    # Update the display.
    disp.fill(prac_scr)
    t1 = disp.show()
    #time at this frame 
    time_last = timer.get_time()

end_press = False
# Second practice screen 

if (correct == False):
    prac_scr2.screen[1].text = \
    """
    You ran out of time! Try and find the direction faster!

    Now we are going to practice with two snakes, 
    try and remember which way both of them are going. 

    But, you will only be asked to help one of them

    Press the key once you have looked at BOTH snakes.
    """
disp.fill(prac_scr2)

timer.pause(500) # pause so loads of clicks don't go through
disp.show()

if MEG: # if MEG repeatedly loop until button state changes
    trigbox.wait_for_button_press()

else: 
    mouse.get_clicked()

# Third practice screen 
disp.fill(prac_scr3)
timer.pause(500) # pause so snake does not appear to be instantly moving
disp.show()
target_ang = 90
start_time = timer.get_time()
time_at_target = 0; 
time_last = 0
time_now = 0
time_trial = 0
correct = True;
while (time_at_target < 0.2 and time_trial < 10000 and end_press == False):
    # get current time 
    time_now = timer.get_time()
    # duration of the last frame 
    time_frame = time_now - time_last 
    #duration of trial
    time_trial = time_now - start_time
    if (time_trial > 10000):
        correct = False; 
    if MEG:
        btn_list, state = trigbox.get_button_state(button_list = [LEFT_BUT, RIGHT_BUT, MAIN_BUT]) # get button states 
        # we need to replicate the get_pressed() pygame functionality 
        button_states = [False, False] # list of bools 
        if state[0] != 0: # if left button is not 0
            button_states[0] = True
        if state[1] != 0: # if right button is not 0 
            button_states[-1] = True 
        if state[2] != 0:
            end_press = True 

        key, presstime = kb.get_key(keylist=['q', 'f', 'j'], timeout=1, flush=False)

    else:
        key, presstime = kb.get_key(keylist=['q', 'f', 'j'], timeout=1, flush=False)
        button_states = mouse.get_pressed()
    # Break loop on 'q' press.
    if key == 'q':
        log.close()
        tracker.close()
        disp.close()
        raise Exception('DEBUG KILL')
    # Rotate the stimulus accordingly.
    if  button_states[0]:
        pre_clamp = prac_scr3.screen[2].ori - 1
        prac_scr3.screen[2].ori = clamp_angle(int(pre_clamp))
    elif button_states[-1]:
        pre_clamp = prac_scr3.screen[2].ori +1
        prac_scr3.screen[2].ori = clamp_angle(int(pre_clamp))
    # if at target time add the length of this frame
    angle= prac_scr3.screen[2].ori 
    # reduce the angle  
    angle =  angle % 360; 
    #force it to be the positive remainder, so that 0 <= angle < 360  
    angle = (angle + 360) % 360;  
    #force into the minimum absolute value residue class, so that -180 < angle <= 180  
    if (angle > 180):
        angle -= 360;  
    if target_ang - 30 <= abs(angle) <= target_ang + 30:
        time_at_target += time_frame
    print(time_at_target)
    # Update the display.
    disp.fill(prac_scr3)
    t1 = disp.show()
    #time at this frame 
    time_last = timer.get_time()


if (correct == False):
    prac_scr2.screen[1].text = \
    """
    You Ran out of time, try to respond faster!

    Now we are going to try a few more practices. 

    This time you have to do it as fast as you can. 

    But make sure to try and be accurate! 

    You get a score after each one, 

    try and make it as close to 100 as possible. 

    (Press any button to continue.)
    """

# Fourth practice screen 
disp.fill(prac_scr4)
timer.pause(500) # pause so loads of clicks don't go through
disp.show()


if MEG: # if MEG repeatedly loop until button state changes
    trigbox.wait_for_button_press()
else: 
    mouse.get_clicked()

# # # # #
# RUN PRACTICE TRIALS 

# Loop through all trials.
for trialnr, trial in enumerate(prac_trials):

    # PREPARE
    # If there is a neutral cue, randomly choose the probe direction.
    if trial['cue_direction'] == -1:
        trial['probe_direction'] = random.choice([0,1])
    # Compute the probed stimulus.
    if trial['stimorder'] == 0:
        probed_stim = STIMNAMES[trial['probe_direction']]
    elif trial['stimorder'] == 1:
        probed_stim = STIMNAMES[1 - trial['probe_direction']]
    
    #print(trial['stim0'])
    # Rotate stimuli to orientation.
    #stimscr[0 or 1].screem[]

    stimscr[trial['stimorder']].screen[stim_index[trial['stimorder']][0]].ori = trial['stim0'] #left
    stimscr[trial['stimorder']].screen[stim_index[trial['stimorder']][1]].ori = trial['stim1'] # right 
    
    # Optional drift check.
    if (trialnr > 0) and (trialnr % DRIFT_CHECK_FREQ == 0):
        tracker.drift_correction()

    # Start eye tracking.
    tracker.start_recording()
    
    # TODO: Log trial specifics.
    tracker.log("")

    #Draw them on to the screen 

    
    # RUN
    # Inter-trial-interval.
    disp.fill(delayscr)
    iti_onset = disp.show()

    if MEG: # log 201: ITI onset 
        trigbox.set_trigger_state(201, RET_ZERO)
        log_events.write([str(trialnr), str(timer.get_time()), "0", "201", "0", "0"])

    timer.pause(trial['iti'])

    
    # Present memory array
    disp.fill(stimscr[trial['stimorder']])
    stim_onset = disp.show()

    if MEG: # log 202: stim onset 
        trigbox.set_trigger_state(202, RET_ZERO)
        log_events.write([str(trialnr), str(timer.get_time()), "0", "202", "0", "0"])

    timer.pause(STIM_DURATION)
    
    # Present delay screen.
    disp.fill(delayscr)
    precue_delay_onset = disp.show()

    if MEG: # log 203: delay onset
        trigbox.set_trigger_state(203, RET_ZERO)
        log_events.write([str(trialnr), str(timer.get_time()), "0", "203", "0", "0"])

    timer.pause(MAINTENANCE_DURATION)
    
    # Present cue.
    disp.fill(cuescr[trial['cue_direction']])
    cue_onset = disp.show()

    if MEG: # log 250-252: cue onset 
        # trigger based on left right or neutral 
        if trial['cue_direction'] == 0: #left
            cue_trig = 250
        if trial['cue_direction'] == 1: # right
            cue_trig = 251
        if trial['cue_direction'] == -1: # neutral 
            cue_trig = 252
        trigbox.set_trigger_state(cue_trig, RET_ZERO)
        log_events.write([str(trialnr), str(timer.get_time()), "0", str(cue_trig), "0", "0"])

    timer.pause(CUE_DURATION)
    
    
    # Present delay screen.
    disp.fill(delayscr)
    postcue_delay_onset = disp.show()

    if MEG: # log 205: postcue onset 
        trigbox.set_trigger_state(205, RET_ZERO)
        log_events.write([str(trialnr), str(timer.get_time()), "0", "205", "0", "0"])
    
    # Reset stimulus orientation.
    probescr[trial['probe_direction']][probed_stim].screen[probe_index[trial['probe_direction']]].ori = 90
    timer.pause(POSTCUE_DURATION)
    

    # Present probe screen.
    disp.fill(probescr[trial['probe_direction']][probed_stim])
    probe_onset = disp.show()

    if MEG: # log 260-261: probe onset 

        #
        print(trial['probe_direction'])
        if trial['probe_direction'] == 0: # Left
            probe_trig = 240
        elif trial['probe_direction'] == 1: #Right
            probe_trig = 241

        trigbox.set_trigger_state(probe_trig, RET_ZERO)
        log_events.write([str(trialnr), str(timer.get_time()), "0", str(probe_trig), "0", "0"])

    # Flush the keyboard.
    kb.get_key(keylist=None, timeout=1, flush=True)

    #Move stimulus according to input.
    t1 = copy.copy(probe_onset) # timer 
    resp_started = False; 
    resp_len = 0 
    resp_onset = 0 
    currang = 0 
    tarang = 0
    end_press = False
    
    while (t1 - probe_onset < RESPONSE_TIMEOUT and end_press == False):
        if MEG:
            btn_list, state = trigbox.get_button_state(button_list = [LEFT_BUT, RIGHT_BUT, MAIN_BUT]) # get button states 
            # we need to replicate the get_pressed() pygame functionality 
            button_states = [False, False] # list of bools 
            if state[0] != 0: # if left button is not 0
                button_states[0] = True
            if state[1] != 0: # if right button is not 0 
                button_states[-1] = True 
            if state[2] != 0:
                end_press = True 

            key, presstime = kb.get_key(keylist=['q', 'f', 'j'], timeout=1, flush=False)


        else:
            key, presstime = kb.get_key(keylist=['q', 'f', 'j'], timeout=1, flush=False)
            button_states = mouse.get_pressed()
        # Break loop on 'q' press.
        if key == 'q':
            log.close()
            tracker.close()
            disp.close()
            raise Exception('DEBUG KILL')
        # Rotate the stimulus accordingly.
        if key == 'f' or button_states[0]:
            if resp_started == False:
                resp_started = True 
                resp_onset = copy.copy(t1) - probe_onset #time stamp of response onset
                if MEG: # log 207: resp onset 
                    trigbox.set_trigger_state(207, RET_ZERO)
                    log_events.write([str(trialnr), str(timer.get_time()), "0", "207", "0", "0"]) 

            pre_clamp = probescr[trial['probe_direction']][probed_stim].screen[probe_index[trial['probe_direction']]].ori -1
            #print(clamp_angle(pre_clamp))
            probescr[trial['probe_direction']][probed_stim].screen[probe_index[trial['probe_direction']]].ori = clamp_angle(int(pre_clamp))
            resp_len = copy.copy(t1) - probe_onset - resp_onset 
        elif key == 'j' or button_states[-1]:
            if resp_started == False:
                resp_started = True 
                resp_onset = copy.copy(t1) - probe_onset#time stamp of response onset

                if MEG: # log 207: resp onset 
                    trigbox.set_trigger_state(207, RET_ZERO)
                    log_events.write([str(trialnr), str(timer.get_time()), "0", "207", "0", "0"]) 

            pre_clamp = probescr[trial['probe_direction']][probed_stim].screen[probe_index[trial['probe_direction']]].ori +1
            #print(clamp_angle(pre_clamp))
            probescr[trial['probe_direction']][probed_stim].screen[probe_index[trial['probe_direction']]].ori = clamp_angle(int(pre_clamp))
            resp_len = copy.copy(t1) - probe_onset - resp_onset
        # Update the display.
        disp.fill(probescr[trial['probe_direction']][probed_stim])
        #log_det.write(["trialnr", "timestamp", "angle", "event", "targ_ang", "cue_dir"])
        #write to log file detailed 
        currang = probescr[trial['probe_direction']][probed_stim].screen[probe_index[trial['probe_direction']]].ori
        if currang > 180:
            currang = currang - 180 
        tarang = stimscr[trial['stimorder']].screen[stim_index[trial['stimorder']][trial['probe_direction']]].ori
        log_det.write([str(trialnr), str(t1 - probe_onset), str(currang), "0", str(tarang), str(timer.get_time())])
        t1 = disp.show() #update timestamp



    respAng = probescr[trial['probe_direction']][probed_stim].screen[probe_index[trial['probe_direction']]].ori

    # remember 180 is the degree of movement, so convert anything above 180 
    print ('resp angle raw' + str(respAng))
    if respAng > 180: 
        respAng = respAng - 180

    print ('resp angle after' + str(respAng))
    #print(trial['stimorder'])
    #print(trial['probe_direction'])
    targAng = stimscr[trial['stimorder']].screen[stim_index[trial['stimorder']][trial['probe_direction']]].ori
    print('target angle' + str(targAng))
    #targAng = stimscr[direction].screen[stim_index[direction][0]].ori
   
    ## Present feedback.
    #Calculate difference score
    a = float(90 - abs(abs(respAng - targAng) - 90)); 
    #a = respAng - targAng
    #a = (a + 180) % 360 - 180
    feedscore = numpy.round(100 - ((a/90)*100))

    #present text
    feedscr.clear()

    feedtxt = str(int(feedscore)) + " Points"
    #feedtxt2 = " Worms until next break: " + str((TRIAL_BREAKS - trialnr % TRIAL_BREAKS)-1) 

    feedscr.draw_text(feedtxt, fontsize=40, colour=RED2GREEN[int(numpy.round(feedscore))-1])
    #feedscr.draw_text(feedtxt2, fontsize = MAIN_FONTSIZE, pos = (DISPCENTRE[0], DISPCENTRE[1] + DISPSIZE[0]*0.2), center=True)
    
    ##LOG THE TRIAL 
    #log.write(["trialnr","left_ang","right_ang", "cue_dir", "targ", "targ_ang", "resp_ang", "perc_diff", "resp_onset", "resp_duration", "prac"])
    log.write([str(trialnr),str(trial['stim0']),str(trial['stim1']), str(trial['cue_direction']), str(trial['probe_direction']), str(targAng), str(respAng), str(feedscore), str(resp_onset), str(resp_len), str(trial['iti']),str(iti_onset), str(stim_onset), str(precue_delay_onset), str(cue_onset), str(postcue_delay_onset), str(probe_onset),"1"])

    #draw and wait 
    disp.fill(feedscr)
    feed_onset = disp.show()

    if MEG: # log 208: feedback onset
        trigbox.set_trigger_state(208, RET_ZERO)
        log_events.write([str(trialnr), str(timer.get_time()), "0", "208", "0", "0"]) 

    timer.pause(FEED_DURATION)
    # Stop recording eye movements.
    tracker.stop_recording()

# Fourth practice screen 
disp.fill(prac_scr5)
timer.pause(500) # pause so loads of clicks don't go through
disp.show()
if MEG: # if MEG repeatedly loop until button state changes
    trigbox.wait_for_button_press()
else: 
    mouse.get_clicked()


block_scores = [0]

total_score = 0
# # # # #
# RUN TRIALS

# Loop through all trials.
for trialnr, trial in enumerate(trials):

    if trialnr % TRIAL_BREAKS == 0:
        print('breaktime')
        
        #BREAK SCREEN
        breakscr = Screen()
        breaktxt = \
        """
        This is one of your breaks. 
        
        You will have another in """ + str(int(TRIAL_BREAKS)) + " more trials"\
        """ 
        
        PRESS ANY BUTTON TO END THE BREAK
        """
        breakscr.draw_text(breaktxt, fontsize=MAIN_FONTSIZE)
        #calculate progress fraction 
        prg = trialnr/len(trials)

        #draw fill with proportion
        breakscr.draw_rect(colour = 'green', x=DISPSIZE[0]*0.1, y=DISPCENTRE[1]+200, w=(DISPSIZE[0]*0.8)*prg, h=99, pw=1, fill=True)
        #draw empty square 
        breakscr.draw_rect(x=DISPSIZE[0]*0.1, y=DISPCENTRE[1]+200, w=DISPSIZE[0]*0.8, h=100, pw=1)
        #write trials left 
        breakscr.draw_text(str(int(len(trials)-10)) + " worms left", fontsize=MAIN_FONTSIZE, pos=(DISPCENTRE[0], DISPCENTRE[1]+300))
        #Write total score
        breakscr.draw_text("Your Points: " + str(int(total_score)), fontsize=50, pos=(DISPCENTRE[0], DISPCENTRE[1]-300), colour='green')
        disp.fill(breakscr)
        start_break = disp.show()

        timer.pause(500) # pause so loads of clicks don't go through

        if MEG: # if MEG repeatedly loop until button state changes
            trigbox.wait_for_button_press()
        else: 
            mouse.get_clicked()
    
    block_scores = [];
    # PREPARE
    # If there is a neutral cue, randomly choose the probe direction.
    if trial['cue_direction'] == -1:
        trial['probe_direction'] = random.choice([0,1])
    # Compute the probed stimulus.
    if trial['stimorder'] == 0:
        probed_stim = STIMNAMES[trial['probe_direction']]
    elif trial['stimorder'] == 1:
        probed_stim = STIMNAMES[1 - trial['probe_direction']]
    
    #print(trial['stim0'])
    # Rotate stimuli to orientation.
    stimscr[trial['stimorder']].screen[stim_index[trial['stimorder']][0]].ori = trial['stim0']
    stimscr[trial['stimorder']].screen[stim_index[trial['stimorder']][1]].ori = trial['stim1']
    #Draw them on to the screen 

    # Optional drift check.
    if (trialnr > 0) and (trialnr % DRIFT_CHECK_FREQ == 0):
        tracker.drift_correction()

    # Start eye tracking.
    tracker.start_recording()
    
    # TODO: Log trial specifics.
    tracker.log("")
    
    # RUN
    # Inter-trial-interval.
    disp.fill(delayscr)
    iti_onset = disp.show()

    if MEG: # log 201: ITI onset 
        trigbox.set_trigger_state(201, RET_ZERO)
        log_events.write([str(trialnr), str(timer.get_time()), "0", "201", "0", "0"])

    timer.pause(trial['iti'])

    
    # Present memory array
    disp.fill(stimscr[trial['stimorder']])
    stim_onset = disp.show()

    if MEG: # log 202: stim onset 
        trigbox.set_trigger_state(202, RET_ZERO)
        log_events.write([str(trialnr), str(timer.get_time()), "0", "202", "0", "0"])

    timer.pause(STIM_DURATION)
    
    # Present delay screen.
    disp.fill(delayscr)
    precue_delay_onset = disp.show()

    if MEG: # log 203: delay onset
        trigbox.set_trigger_state(203, RET_ZERO)
        log_events.write([str(trialnr), str(timer.get_time()), "0", "203", "0", "0"])

    timer.pause(MAINTENANCE_DURATION)
    
    # Present cue.
    disp.fill(cuescr[trial['cue_direction']])
    cue_onset = disp.show()

    if MEG: # log 250-252: cue onset 
        # trigger based on left right or neutral 
        if trial['cue_direction'] == 0: #left
            cue_trig = 250
        if trial['cue_direction'] == 1: # right
            cue_trig = 251
        if trial['cue_direction'] == -1: # neutral 
            cue_trig = 252
        trigbox.set_trigger_state(cue_trig, RET_ZERO)
        log_events.write([str(trialnr), str(timer.get_time()), "0", str(cue_trig), "0", "0"])

    timer.pause(CUE_DURATION)
    
    # Present delay screen.
    disp.fill(delayscr)
    postcue_delay_onset = disp.show()

    if MEG: # log 205: postcue onset 
        trigbox.set_trigger_state(205, RET_ZERO)
        log_events.write([str(trialnr), str(timer.get_time()), "0", "205", "0", "0"])


    # Reset stimulus orientation.
    probescr[trial['probe_direction']][probed_stim].screen[probe_index[trial['probe_direction']]].ori = 90
    
    timer.pause(POSTCUE_DURATION)
    
    # Present probe screen.
    disp.fill(probescr[trial['probe_direction']][probed_stim])
    probe_onset = disp.show()

    if MEG: # log 240-241: probe onset 

        #
        if trial['probe_direction'] == 0: #Left
            probe_trig = 240
        if trial['probe_direction'] == 1: # Right
            probe_trig = 241
        trigbox.set_trigger_state(probe_trig, RET_ZERO)
        log_events.write([str(trialnr), str(timer.get_time()), "0", str(probe_trig), "0", "0"])


    # Flush the keyboard.
    kb.get_key(keylist=None, timeout=1, flush=True)
    #Move stimulus according to input.
    t1 = copy.copy(probe_onset) # timer 
    resp_started = False; 
    resp_len = 0 
    resp_onset = 0 
    currang = 0 
    tarang = 0
    end_press = False
    
    while (t1 - probe_onset < RESPONSE_TIMEOUT and end_press == False):
        if MEG:
            btn_list, state = trigbox.get_button_state(button_list = [LEFT_BUT, RIGHT_BUT, MAIN_BUT]) # get button states 
            # we need to replicate the get_pressed() pygame functionality 
            button_states = [False, False] # list of bools 
            if state[0] != 0: # if left button is not 0
                button_states[0] = True
            if state[1] != 0: # if right button is not 0 
                button_states[-1] = True 
            if state[2] != 0:
                end_press = True 

            key, presstime = kb.get_key(keylist=['q', 'f', 'j'], timeout=1, flush=False)


        else:
            key, presstime = kb.get_key(keylist=['q', 'f', 'j'], timeout=1, flush=False)
            button_states = mouse.get_pressed()

        key, presstime = kb.get_key(keylist=['q', 'f', 'j'], timeout=1, flush=False)

        # Break loop on 'q' press.
        if key == 'q':
            log.close()
            tracker.close()
            disp.close()
            raise Exception('DEBUG KILL')
        # Rotate the stimulus accordingly.
        if key == 'f' or button_states[0]:
            if resp_started == False:
                resp_started = True 
                resp_onset = copy.copy(t1) - probe_onset #time stamp of response onset 
                if MEG: # log 207: resp onset 
                    trigbox.set_trigger_state(207, RET_ZERO)
                    log_events.write([str(trialnr), str(timer.get_time()), "0", "207", "0", "0"]) 
            pre_clamp = probescr[trial['probe_direction']][probed_stim].screen[probe_index[trial['probe_direction']]].ori -1
            #print(clamp_angle(pre_clamp))
            probescr[trial['probe_direction']][probed_stim].screen[probe_index[trial['probe_direction']]].ori = clamp_angle(int(pre_clamp))
            resp_len = copy.copy(t1) - probe_onset - resp_onset 
        elif key == 'j' or button_states[-1]:
            if resp_started == False:
                resp_started = True 
                resp_onset = copy.copy(t1) - probe_onset#time stamp of response onset 
                if MEG: # log 207: resp onset 
                    trigbox.set_trigger_state(207, RET_ZERO)
                    log_events.write([str(trialnr), str(timer.get_time()), "0", "207", "0", "0"]) 
            pre_clamp = probescr[trial['probe_direction']][probed_stim].screen[probe_index[trial['probe_direction']]].ori +1
            #print(clamp_angle(pre_clamp))
            probescr[trial['probe_direction']][probed_stim].screen[probe_index[trial['probe_direction']]].ori = clamp_angle(int(pre_clamp))
            resp_len = copy.copy(t1) - probe_onset - resp_onset
        # Update the display.
        disp.fill(probescr[trial['probe_direction']][probed_stim])
        #log_det.write(["trialnr", "timestamp", "angle", "event", "targ_ang", "cue_dir"])
        #write to log file detailed 
        currang = probescr[trial['probe_direction']][probed_stim].screen[probe_index[trial['probe_direction']]].ori
        if currang > 180: 
            currang= currang - 180
        tarang = stimscr[trial['stimorder']].screen[stim_index[trial['stimorder']][trial['probe_direction']]].ori
        log_det.write([str(trialnr), str(t1 - probe_onset), str(currang), "0", str(tarang), str(trial['cue_direction'])])
        t1 = disp.show() #update timestamp



    respAng = probescr[trial['probe_direction']][probed_stim].screen[probe_index[trial['probe_direction']]].ori

    # remember 180 is the degree of movement, so convert anything above 180 
    print ('resp angle raw' + str(respAng))
    if respAng > 180: 
        respAng = respAng - 180

    print ('resp angle after' + str(respAng))
    #print(trial['stimorder'])
    #print(trial['probe_direction'])
    targAng = stimscr[trial['stimorder']].screen[stim_index[trial['stimorder']][trial['probe_direction']]].ori
    print('target angle' + str(targAng))
    #targAng = stimscr[direction].screen[stim_index[direction][0]].ori
   
    ## Present feedback.
    #Calculate difference score
    a = float(90- abs(abs(respAng - targAng) - 90)); 
    #a = respAng - targAng
    #a = (a + 180) % 360 - 180
    ##feedscore = numpy.round(100 - (((abs(a)/90)*100) ),1)
    feedscore = numpy.round(100 - ((a/90)*100))
    total_score += feedscore
    #present text
    feedscr.clear()
    
    feedtxt = str(int(feedscore)) + " Points"
    feedtxt2 = " Worms until next break: " + str(int((TRIAL_BREAKS - trialnr % TRIAL_BREAKS)-1)) 

    feedscr.draw_text(feedtxt, fontsize=40, colour=RED2GREEN[int(numpy.round(feedscore))-1])
    feedscr.draw_text(feedtxt2, fontsize = MAIN_FONTSIZE, pos = (DISPCENTRE[0], DISPCENTRE[1] + DISPSIZE[0]*0.2), center=True)
    
    block_scores.append(int(feedscore))
    ##LOG THE TRIAL 
    #log.write(["trialnr","left_ang","right_ang", "cue_dir", "targ", "targ_ang", "resp_ang", "perc_diff", "resp_onset", "resp_duration", "prac"])
    log.write([str(trialnr),str(trial['stim0']),str(trial['stim1']), str(trial['cue_direction']), str(trial['probe_direction']), str(targAng), str(respAng), str(feedscore), str(resp_onset), str(resp_len),str(trial['iti']), str(iti_onset), str(stim_onset), str(precue_delay_onset), str(cue_onset), str(postcue_delay_onset), str(probe_onset),"0"])

    #draw and wait 
    disp.fill(feedscr)
    feed_onset = disp.show()
    if MEG: # log 208: feedback onset
        trigbox.set_trigger_state(208, RET_ZERO)
        log_events.write([str(trialnr), str(timer.get_time()), "0", "208", "0", "0"]) 
    timer.pause(FEED_DURATION)
    # Stop recording eye movements.
    tracker.stop_recording()


# # # # #
# CLOSE
    
# Close the log file.
log.close()
log_det.close()
# Close connection to the eye tracker.
tracker.close()

# Present an ending screen.
scr = Screen()
scr.draw_text("That's the end of the game \n Well Done \n You scored: " + str(total_score) , fontsize=MAIN_FONTSIZE)
disp.fill(scr)
disp.show()
kb.get_key(keylist=None, timeout=None, flush=True)

# Close the display.
disp.close()
