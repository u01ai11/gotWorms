"""play with some worms"""
from psychopy import core, visual, gui, data, event
from psychopy.tools.filetools import fromFile, toFile
import numpy
import random
import pyglet

#flag to avoid annoying UI things when developing
debug = True

""" Set up things to start with """
if debug != True:
    try:  # try to get a previous parameters file
        expInfo = fromFile('lastParams.pickle')
    except:  # if not then set up some
        
        expInfo = {}
        from psychopy import gui
        myDlg = gui.Dlg(title="got Worms?")
        myDlg.addText('Subject info')
        myDlg.addField('ID:')
        myDlg.addField('Session:')
        ok_data = myDlg.show()  # show dialog and wait for OK or Cancel
        if myDlg.OK:  # or if ok_data is not None
            print(ok_data)
            expInfo = {'id': ok_data[0], 'session': ok_data[1]}
        else:
            print('user cancelled')
        

    expInfo['dateStr'] = data.getDateStr()  # add the current time

    # make a text file to save data
    fileName = 'data/'+'gotWorms_'+ '_' + expInfo['id']+'_' + expInfo['dateStr']
    dataFile = open(fileName+'.csv', 'w')  # a  csv

    # Write header information to the csv
    dataFile.write('trial,worm_1,worm_2,angle_1,angle_2\n')

#instantiate our window 
win = visual.Window(allowGUI=True,
                    monitor='Dell_external', units='deg', fullscr=True, screen=0)

#set up for listening to keypresses 
key = pyglet.window.key
keyboard = key.KeyStateHandler()
win.winHandle.push_handlers(keyboard)

#set up list of colours for colour space 
red_to_green = ["#FF0000", "#FC0100", "#F90200", "#F70300", "#F40500", "#F20600", "#EF0700", "#EC0900", "#EA0A00", "#E70B00", "#E50C00", "#E20E00", "#E00F00", "#DD1000", "#DA1200", "#D81300", "#D51400", "#D31500", "#D01700", "#CE1800", "#CB1900", "#C81B00", "#C61C00", "#C31D00", "#C11F00", "#BE2000", "#BC2100", "#B92200", "#B62400", "#B42500", "#B12600", "#AF2800", "#AC2900", "#AA2A00", "#A72B00", "#A42D00", "#A22E00", "#9F2F00", "#9D3100", "#9A3200", "#973300", "#953500", "#923600", "#903700", "#8D3800", "#8B3A00", "#883B00", "#853C00", "#833E00", "#803F00", "#7E4000", "#7B4100", "#794300", "#764400", "#734500", "#714700", "#6E4800", "#6C4900", "#694A00", "#674C00", "#644D00", "#614E00", "#5F5000", "#5C5100", "#5A5200", "#575400", "#555500", "#525600", "#4F5700", "#4D5900", "#4A5A00", "#485B00", "#455D00", "#425E00", "#405F00", "#3D6000", "#3B6200", "#386300", "#366400", "#336600", "#306700", "#2E6800", "#2B6A00", "#296B00", "#266C00", "#246D00", "#216F00", "#1E7000", "#1C7100", "#197300", "#177400", "#147500", "#127600", "#0F7800", "#0C7900", "#0A7A00", "#077C00", "#057D00", "#027E00", "#008000"]
"""Instructions"""
#Screen 1
message1 = visual.TextStim(win, pos=[0,3],text="We are going to play a game with some worms!")
message2 = visual.TextStim(win, pos=[0,-3],text="You are going to see some worms, like the one below")
exampleWorm = visual.ImageStim(win, image='resources/wormy_green.png',pos=[0, -10])
message3 = visual.TextStim(win, pos=[0, -5], text='Press the button to continue')
message1.draw()
message2.draw()
exampleWorm.draw()
win.flip()#to show our newly drawn 'stimuli'
#pause until there's a keypress
event.waitKeys()

#Screen 2 
message1 = visual.TextStim(win, pos=[0,3],alignHoriz='center',text="The aim of the game is to remember the ANGLE of the worms")
message2 = visual.TextStim(win, pos=[0,-3],alignHoriz='center',text="You will see two worms like the ones here/ Press any button to continue")
left_worm = visual.ImageStim(win, image='resources/wormy.png',pos=[-15, 0], color= 'green', ori=180, size=[10,3])
right_worm = visual.ImageStim(win, image='resources/wormy.png',pos=[+15, 0], color='red', ori=220, size=[10,3])
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
left_worm = visual.ImageStim(win, image='resources/wormy.png',pos=[-15, 0], color= 'green', ori=180, size=[10,3])
right_worm = visual.ImageStim(win, image='resources/wormy.png',pos=[+15, 0], color='red', ori=220, size=[10,3])
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
resp_duration = 5

#pre trial interval
cross = visual.TextStim(win, pos=[0,0], text="+", color='white') #just show cross
cross.draw()
win.flip()
core.wait(1.0) #wait for a second 

# memory encoding phase 
left_targ = visual.ImageStim(win, image='resources/wormy.png',pos=[-15, 0], color= left_col, ori=left_ori, size=[10,3]) #add stimuli 
right_targ = visual.ImageStim(win, image='resources/wormy.png',pos=[+15, 0], color= right_col, ori=right_ori, size=[10,3])

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
    resp_targ = visual.ImageStim(win, image='resources/wormy.png',pos=[-15, 0], color= left_col, ori=resp_start, size=[10,3]) #stimuli at starting position
    correct_angle = left_ori
elif target == 1: #draw right as response target 
    resp_targ = visual.ImageStim(win, image='resources/wormy.png',pos=[+15, 0], color=right_col, ori=resp_start, size=[10,3]) #stimuli at starting position
    correct_angle = right_ori

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
    
    resp_targ.ori = resp_targ.ori % 360 # normalise between 0 and 360
    
    #Now update the timer and adjust wedge
    fraction = resp_clock.getTime()/resp_duration
    timer_wedge.visibleWedge = [0, (365*fraction)]
    timer_wedge.draw()
    
    cross.draw() # fixation cross
    win.flip() # show this frame
    
    #check for exit 
    if resp_clock.getTime() >= resp_duration:

        animating = False
    

#Feedback
resp_angle = resp_targ.ori; #record the angle of response from the last shown frame 
diff = resp_angle - correct_angle # how far off was it, sine gives the direction 
feed = round(((360 - abs(diff))/360)*100)

message1 = visual.TextStim(win, pos=[0,2],alignHoriz='center',text="Your Accuracy Was:")
message2 = visual.TextStim(win, pos=[0,-2],alignHoriz='center',text=str(feed) +"%", color=red_to_green[int(feed)])
message1.draw()
message2.draw()

cross.draw()
win.flip()#to show our newly drawn 'stimuli'
#pause until there's a keypress
event.waitKeys()




 