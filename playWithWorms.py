"""play with some worms"""
from psychopy import core, visual, gui, data, eventfrom psychopy.tools.filetools import fromFile, toFileimport numpy
import random
import pyglet

#flag to avoid annoying UI things when developing
debug = True

""" Set up things to start with """
if debug != True:
    try:  # try to get a previous parameters file        expInfo = fromFile('lastParams.pickle')    except:  # if not then set up some
                expInfo = {}
        from psychopy import gui        myDlg = gui.Dlg(title="got Worms?")        myDlg.addText('Subject info')        myDlg.addField('ID:')
        myDlg.addField('Session:')        ok_data = myDlg.show()  # show dialog and wait for OK or Cancel        if myDlg.OK:  # or if ok_data is not None            print(ok_data)
            expInfo = {'id': ok_data[0], 'session': ok_data[1]}        else:            print('user cancelled')
        
    expInfo['dateStr'] = data.getDateStr()  # add the current time

    # make a text file to save data    fileName = 'data/'+'gotWorms_'+ '_' + expInfo['id']+'_' + expInfo['dateStr']    dataFile = open(fileName+'.csv', 'w')  # a  csv

    # Write header information to the csv    dataFile.write('trial,worm_1,worm_2,angle_1,angle_2\n')

#instantiate our window win = visual.Window(allowGUI=True,                    monitor='Dell_external', units='deg', fullscr=True, screen=0)

#set up for listening to keypresses 
key = pyglet.window.key
keyboard = key.KeyStateHandler()
win.winHandle.push_handlers(keyboard)

"""Instructions"""
#Screen 1message1 = visual.TextStim(win, pos=[0,3],text="We are going to play a game with some worms!")message2 = visual.TextStim(win, pos=[0,-3],text="You are going to see some worms, like the one below")
exampleWorm = visual.ImageStim(win, image='stim/wormy_green.png',pos=[0, -10])
message3 = visual.TextStim(win, pos=[0, -5], text='Press the button to continue')message1.draw()message2.draw()
exampleWorm.draw()win.flip()#to show our newly drawn 'stimuli'#pause until there's a keypressevent.waitKeys()

#Screen 2 
message1 = visual.TextStim(win, pos=[0,3],alignHoriz='center',text="The aim of the game is to remember the ANGLE of the worms")
message2 = visual.TextStim(win, pos=[0,-3],alignHoriz='center',text="You will see two worms like the ones here/ Press any button to continue")
left_worm = visual.ImageStim(win, image='stim/wormy.png',pos=[-15, 0], color= 'green', ori=180, size=[10,3])
right_worm = visual.ImageStim(win, image='stim/wormy.png',pos=[+15, 0], color='red', ori=220, size=[10,3])
message1.draw()
message2.draw()
left_worm.draw()
right_worm.draw()
win.flip()#to show our newly drawn 'stimuli'
#pause until there's a keypress
event.waitKeys()

#Screen 3 
message1 = visual.TextStim(win, pos=[0,3],alignHoriz='center',text="There will be a cross in the middle of the screen, try and concentrate on this, and only look at the worms out of the sides of your eyes")
message2 = visual.TextStim(win, pos=[0,-3],alignHoriz='center',text="Press any button to continue")
cross = visual.TextStim(win, pos=[0,0], text="+", color='white')
message1.draw()
message2.draw()
cross.draw()
win.flip()
event.waitKeys()

#Screen 4 
message1 = visual.TextStim(win, pos=[0,3],alignHoriz='center',text="You'll see the worms for a bit, try and remember which way they are pointing ")
message2 = visual.TextStim(win, pos=[0,-3],alignHoriz='center',text="Then the worms will disappear, and only one will be shown. Move the worm to it's starting position using the F and J keys! Press any button to try a practice")
left_worm = visual.ImageStim(win, image='stim/wormy.png',pos=[-15, 0], color= 'green', ori=180, size=[10,3])
right_worm = visual.ImageStim(win, image='stim/wormy.png',pos=[+15, 0], color='red', ori=220, size=[10,3])
message1.draw()
message2.draw()
left_worm.draw()
right_worm.draw()
cross.draw()
win.flip()#to show our newly drawn 'stimuli'
#pause until there's a keypress
event.waitKeys()

""" Two Target Trial """
#variables 
left_col = 'red'
right_col = 'green'
left_ori = 0
right_ori = 90
target = 0
delay = 2
encoding_duration = 2
resp_start = random.randint(1,360)
resp_duration = 10

#pre trial interval
cross = visual.TextStim(win, pos=[0,0], text="+", color='white') #just show cross
cross.draw()
win.flip()
core.wait(1.0) #wait for a second 

# memory encoding phase 
left_targ = visual.ImageStim(win, image='stim/wormy.png',pos=[-15, 0], color= left_col, ori=left_ori, size=[10,3]) #add stimuli 
right_targ = visual.ImageStim(win, image='stim/wormy.png',pos=[+15, 0], color= right_col, ori=right_ori, size=[10,3])

left_targ.draw()#draw 
right_targ.draw()
cross.draw()
win.flip()#display
core.wait(encoding_duration)#wait for eocoding time 

#delay phase 
cross = visual.TextStim(win, pos=[0,0], text="+", color='white') #just show cross
cross.draw()
win.flip()
core.wait(delay) #wait for delay 


#response phase 
if target == 0: #draw left as response_target
    resp_targ = visual.ImageStim(win, image='stim/wormy.png',pos=[-15, 0], color= left_col, ori=resp_start, size=[10,3]) #stimuli at starting position
elif target == 1: #draw right as response target 
    resp_targ = visual.ImageStim(win, image='stim/wormy.png',pos=[+15, 0], color=right_col, ori=resp_start, size=[10,3]) #stimuli at starting position

timer_wedge = visual.RadialStim(win, tex='sqrXsqr', size=5, 
    visibleWedge=[0, 0], radialCycles=0, angularCycles=0, interpolate=False)  
##we need an animation loop for allowing the rotation of the stuff 
resp_clock = core.Clock() # begining of response window 
animating = True; #animating flag 
while animating == True: 
    #Deal with rotation of the response object
    if keyboard[key.F]:# if f key rotate the worm left 
        resp_targ.ori -= 1 
    if keyboard[key.J]: #if j key rorate the worm right
        resp_targ.ori += 1
    resp_targ.draw() # draw the newly rotated target
    
    #Now update the timer and adjust wedge
    fraction = resp_clock.getTime()/resp_duration
    timer_wedge.visibleWedge = [0, (365*fraction)]
    timer_wedge.draw()
    
    cross.draw() # fixation cross
    win.flip() # show this frame
    
    #check for exit 
    if resp_clock.getTime() >= resp_duration:
        animating = False
    

resp_angle = resp_targ.ori; #record the angle 







 