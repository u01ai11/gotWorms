# Some text here to explain the experiment.
#
# Version 1 (2018-07-26)

import os

# DISPLAY SETTINGS
# Display back-end ('pygame' or 'psychopy').
# NOTE: Use PsychoPy, as we're doing PsychoPy-specific stuff with orientations.
DISPTYPE = 'psychopy'
# Display resolution (match with your computer screen!).
DISPSIZE = (1440, 900)
DISPCENTRE = (DISPSIZE[0]//2, DISPSIZE[1]//2)
# Foreground and background colour.
FGC = (  0,   0,   0)
BGC = (128, 128, 128)
# Screen size in centimeters (measure your screen!).
# TODO: Measure this in the lab.
SCREENSIZE = (30.0, 20.0)
# Screen-to-participant distance in centimeters.
# TODO: Measure in lab.
SCREENDIST = 62.0
#colour vector for green to red feedback 
#set up list of colours for colour space 
RED2GREEN= ["#FF0000", "#FC0100", "#F90200", "#F70300", "#F40500", "#F20600", "#EF0700", "#EC0900", "#EA0A00", "#E70B00", "#E50C00", "#E20E00", "#E00F00", "#DD1000", "#DA1200", "#D81300", "#D51400", "#D31500", "#D01700", "#CE1800", "#CB1900", "#C81B00", "#C61C00", "#C31D00", "#C11F00", "#BE2000", "#BC2100", "#B92200", "#B62400", "#B42500", "#B12600", "#AF2800", "#AC2900", "#AA2A00", "#A72B00", "#A42D00", "#A22E00", "#9F2F00", "#9D3100", "#9A3200", "#973300", "#953500", "#923600", "#903700", "#8D3800", "#8B3A00", "#883B00", "#853C00", "#833E00", "#803F00", "#7E4000", "#7B4100", "#794300", "#764400", "#734500", "#714700", "#6E4800", "#6C4900", "#694A00", "#674C00", "#644D00", "#614E00", "#5F5000", "#5C5100", "#5A5200", "#575400", "#555500", "#525600", "#4F5700", "#4D5900", "#4A5A00", "#485B00", "#455D00", "#425E00", "#405F00", "#3D6000", "#3B6200", "#386300", "#366400", "#336600", "#306700", "#2E6800", "#2B6A00", "#296B00", "#266C00", "#246D00", "#216F00", "#1E7000", "#1C7100", "#197300", "#177400", "#147500", "#127600", "#0F7800", "#0C7900", "#0A7A00", "#077C00", "#057D00", "#027E00", "#008000"]



# FILES AND FOLDERS
# Auto-detect folders.
DIR = os.path.dirname(os.path.abspath(__file__))
DATADIR = os.path.join(DIR, 'data')
RESDIR = os.path.join(DIR, 'resources')
# Check whether these folders exist.
if not os.path.isdir(DATADIR):
    os.mkdir(DATADIR)
if not os.path.isdir(RESDIR):
    raise Exception("ERROR: Missing the 'resources' directory at this directory:\n'%s'" \
        % (RESDIR))

# EXPERIMENT SETTINGS
# Stimulus order: 0 for A left and B right; 1 for vice versa.
STIM_ORDERS = [0]
# Cue direction: -1 for neutral (=both), 0 for left, 1 for right.
CUE_DIRECTIONS = [-1, 0, 1]
# Number of times the unique combinations of stim order and cue direction are
# run.
UNIQUE_TRIAL_REPEATS = 40

# TIMING
# Duration of the stimulus presentation in milliseconds.
STIM_DURATION = 992
# Duration of the blank screen between stimulus and cue (ms).
MAINTENANCE_DURATION = 992
# Duration of the cue.
CUE_DURATION = 492
# Duration of the blank screen between cue and probe.
POSTCUE_DURATION = 992
# Probe timeout duration.
RESPONSE_TIMEOUT = 4992
# feedback duration
FEED_DURATION = 1992
# STIMULUS SETTINGS
# Names of the stimuli.
STIMNAMES = ["plain_snek_b", "plain_snek_y"]
# Potential positions of the stimuli.
STIMPOS = [ \
    (int(DISPCENTRE[0]-DISPSIZE[0]*0.2), DISPCENTRE[1]), \
    (int(DISPCENTRE[0]+DISPSIZE[0]*0.2), DISPCENTRE[1]), \
    ]

TRIAL_BREAKS = 10
# EYE TRACKER SETTINGS
# Brand of the eye tracker.
TRACKERTYPE = 'eyelink'
DUMMYMODE = True
# Number of trials between each drift check.
DRIFT_CHECK_FREQ = 20

#Clamp angle 

def clamp_angle(input):

	if input >= 360:
		return input - 360
	elif input <= 0:
		return 360 + input 
	else:
		return input



