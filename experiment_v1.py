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


# # # # #
# INITIALISE

# Initialise a new Display instance.
disp = Display()

# Present a start-up screen.
scr = Screen()
scr.draw_text("Loading, please wait...", fontsize=24)
disp.fill(scr)
disp.show()

# Open a new log file.
log = Logfile()
# TODO: Write header.

# Initialise the eye tracker.
tracker = EyeTracker(disp)

# Create a new Keyboard instance to process key presses.
kb = Keyboard(keylist=None, timeout=5000)
mouse = Mouse()


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
inst_scr.draw_text(instructions, fontsize=24)
instruction_screens.append(inst_scr)

# Second screen with text and images.
inst_scr = Screen()
instructions = \
"""
Let's practice. 

Remember the way this snake is facing! 

When you are ready press a button to continue. 
"""
inst_scr.draw_text(instructions, fontsize=24, pos = (DISPCENTRE[0], DISPCENTRE[1]-200))
fpath = os.path.join(RESDIR, STIMNAMES[0] + ".png")
inst_scr.draw_image(fpath, pos=(DISPCENTRE[0], DISPCENTRE[1]+150), scale = 0.7)
inst_scr.screen[2].ori = 100
instruction_screens.append(inst_scr)

# prac screen 1 
inst_scr = Screen()
instructions = \
"""
Can you remember which way the snake faced just now? 

Press the keys in front of you to move the snake to
his position
"""
inst_scr.draw_text(instructions, fontsize=24, pos = (DISPCENTRE[0], DISPCENTRE[1]-200))
fpath = os.path.join(RESDIR, STIMNAMES[0] + ".png")
inst_scr.draw_image(fpath, pos=(DISPCENTRE[0], DISPCENTRE[1]+150), scale = 0.7)
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
inst_scr.draw_text(instructions, fontsize=24, pos = (DISPCENTRE[0], DISPCENTRE[1]-200))
fpath = os.path.join(RESDIR, STIMNAMES[0] + ".png")
inst_scr.draw_image(fpath, pos=(STIMPOS[0][0],STIMPOS[0][1]+200), scale = 0.7)
inst_scr.screen[2].ori = 100
fpath = os.path.join(RESDIR, STIMNAMES[1] + ".png")
inst_scr.draw_image(fpath, pos=(STIMPOS[1][0],STIMPOS[1][1]+200) , scale = 0.7)
inst_scr.screen[3].ori = 200
prac_scr2 = inst_scr

#prac screen 3 
inst_scr = Screen()
instructions = \
"""
Which way was this snake facing?
"""
inst_scr.draw_text(instructions, fontsize=24, pos = (DISPCENTRE[0], DISPCENTRE[1]-200))
fpath = os.path.join(RESDIR, STIMNAMES[1] + ".png")
inst_scr.draw_image(fpath, pos=(STIMPOS[1][0],STIMPOS[1][1]+200) , scale = 0.7)
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

You get a score after each one, try and make it as close
to 100 as possible. 

(Press any button to continue.)
"""
inst_scr.draw_text(instructions, fontsize=24)
prac_scr4 = inst_scr

# STIMULUS
# Create two Screens: One with worm A on the left and B on the right, and one
# vice versa.
stimscr = {}
stim_index = {}
for direction in [0, 1]:
    # Create a screen with two worms.
    stimscr[direction] = Screen()
    # Draw the fixation mark.
    stimscr[direction].draw_fixation(fixtype='cross', pw=3, diameter=8)
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
delayscr.draw_fixation(fixtype='cross', pw=3, diameter=8)

# CUE
# Create a screen with a retro cue.
cuescr = {}
for direction in [-1, 0, 1]:
    cuescr[direction] = Screen()
    # Neutral.
    if direction == -1:
        cue = '<>'
    # Left.
    elif direction == 0:
        cue = '<'
    # Right.
    elif direction == 1:
        cue = '>'
    cuescr[direction].draw_text(cue, fontsize=42)

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
        probescr[direction][stimname].draw_fixation(fixtype='cross', pw=3, diameter=8)
        # Draw the worm on the correct position.
        fpath = os.path.join(RESDIR, stimname + ".png")
        probe_index[direction] = len(probescr[direction][stimname].screen)
        probescr[direction][stimname].draw_image(fpath, pos=STIMPOS[direction], scale = 0.7)

#FEEDBACK 
feedscr = Screen()
feedtxt = ""
feedscr.draw_text(feedtxt, fontsize=24)




# # # # #
# RANDOMISATION

# Create list of trial dicts.
# One trial should contain the following information:
# - stimulus order (0 for stim0 left and stim1 right, 1 for vice versa)
# - cueside (0 for left, 1 for right)
# - probeside (0 for left, 1 for right)
# - probestim (should follow from stimulus direction and probeside)
trials = []

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
stepsize = 360.0 / n_trials
stim0 = numpy.arange(0, 360.0, stepsize).astype(int)
stim1 = numpy.arange(0, 360.0, stepsize).astype(int)
#print(stim0)
# Randomise the stimulus orientations.
random.shuffle(stim0)
random.shuffle(stim1)

# Add all the orientations to the trials.
for i in range(len(trials)):
    trials[i]['stim0'] = stim0[i]
    trials[i]['stim1'] = stim1[i]

# Randomise trial order.
random.shuffle(trials)



# # # # #
# DISPLAY INSTRUCTIONS 

#loop through instruction screens 
for scrn in instruction_screens: 
    timer.pause(100)
    disp.fill(scrn); 
    disp.show()
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
while (time_at_target < 0.5):
    # get current time 
    time_now = timer.get_time()
    # duration of the last frame 
    time_frame = time_now - time_last 
    # Poll the input device.
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
    if target_ang - 10 <= prac_scr.screen[2].ori <= target_ang + 10:
        time_at_target += time_frame
    print(time_at_target)
    # Update the display.
    disp.fill(prac_scr)
    t1 = disp.show()
    #time at this frame 
    time_last = timer.get_time()

# Second practice screen 
disp.fill(prac_scr2)
timer.pause(500) # pause so loads of clicks don't go through
disp.show()
mouse.get_clicked()

# Third practice screen 
disp.fill(prac_scr3)
timer.pause(500) # pause so snake does not appear to be instantly moving
disp.show()
target_ang = 200
start_time = timer.get_time()
time_at_target = 0; 
time_last = 0
time_now = 0
while (time_at_target < 0.5):
    # get current time 
    time_now = timer.get_time()
    # duration of the last frame 
    time_frame = time_now - time_last 
    # Poll the input device.
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
    if target_ang - 10 <= prac_scr3.screen[2].ori <= target_ang + 10:
        time_at_target += time_frame
    print(time_at_target)
    # Update the display.
    disp.fill(prac_scr3)
    t1 = disp.show()
    #time at this frame 
    time_last = timer.get_time()


# Fourth practice screen 
disp.fill(prac_scr4)
timer.pause(500) # pause so loads of clicks don't go through
disp.show()
mouse.get_clicked()


# # # # #
# RUN TRIALS

# Loop through all trials.
for trialnr, trial in enumerate(trials):
    
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

    
    # RUN
    # TODO: Inter-trial-interval.
    
    # TODO: Optional drift check.
    if (trialnr > 0) and (trialnr % DRIFT_CHECK_FREQ == 0):
        tracker.drift_correction()

    # Start eye tracking.
    tracker.start_recording()
    
    # TODO: Log trial specifics.
    tracker.log("")
    
    # Present memory array
    disp.fill(stimscr[trial['stimorder']])
    stim_onset = disp.show()
    timer.pause(STIM_DURATION)
    
    # Present delay screen.
    disp.fill(delayscr)
    precue_delay_onset = disp.show()
    timer.pause(MAINTENANCE_DURATION)
    
    # Present cue.
    disp.fill(cuescr[trial['cue_direction']])
    cue_onset = disp.show()
    timer.pause(CUE_DURATION)
    
    # Present delay screen.
    disp.fill(delayscr)
    postcue_delay_onset = disp.show()
    timer.pause(POSTCUE_DURATION)
    
    # Present probe screen.
    disp.fill(probescr[trial['probe_direction']][probed_stim])
    probe_onset = disp.show()

    # Flush the keyboard.
    kb.get_key(keylist=None, timeout=1, flush=True)

    # TODO: Move stimulus according to input.
    t1 = copy.copy(probe_onset)
    while t1 - probe_onset < RESPONSE_TIMEOUT:
        # Poll the input device.
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
            pre_clamp = probescr[trial['probe_direction']][probed_stim].screen[probe_index[trial['probe_direction']]].ori -1
            #print(clamp_angle(pre_clamp))
            probescr[trial['probe_direction']][probed_stim].screen[probe_index[trial['probe_direction']]].ori = clamp_angle(int(pre_clamp))
        elif key == 'j' or button_states[-1]:
            pre_clamp = probescr[trial['probe_direction']][probed_stim].screen[probe_index[trial['probe_direction']]].ori +1
            #print(clamp_angle(pre_clamp))
            probescr[trial['probe_direction']][probed_stim].screen[probe_index[trial['probe_direction']]].ori = clamp_angle(int(pre_clamp))
        # Update the display.
        disp.fill(probescr[trial['probe_direction']][probed_stim])
        t1 = disp.show()

    # TODO: Log trial input.
    respAng = probescr[trial['probe_direction']][probed_stim].screen[probe_index[trial['probe_direction']]].ori
    #print(trial['stimorder'])
    #print(trial['probe_direction'])
    targAng = stimscr[trial['stimorder']].screen[stim_index[trial['stimorder']][trial['probe_direction']]].ori
    #targAng = stimscr[direction].screen[stim_index[direction][0]].ori
   
    ## Present feedback.
    #Calculate difference score
    a = respAng - targAng
    a = (a + 180) % 360 - 180
    feedscore = numpy.round(100 - (((abs(a)/360)*100) *2),1)

    #present text
    feedscr.clear()
    feedtxt = str(feedscore) + " %"
    feedscr.draw_text(feedtxt, fontsize=25, colour=RED2GREEN[int(numpy.round(feedscore))-1])

    #draw and wait 
    disp.fill(feedscr)
    feed_onset = disp.show()
    timer.pause(FEED_DURATION)
    # Stop recording eye movements.
    tracker.stop_recording()


# # # # #
# CLOSE

# Present a start-up screen.
scr = Screen()
scr.draw_text("Loading, please wait...", fontsize=24)
disp.fill(scr)
disp.show()

# Close the log file.
log.close()

# Close connection to the eye tracker.
tracker.close()

# Close the display.
disp.close()
