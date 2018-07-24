"""play with some worms"""
from psychopy import core, visual, gui, data, eventfrom psychopy.tools.filetools import fromFile, toFileimport numpy, random

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

#instantiate our window win = visual.Window(allowGUI=True,                    monitor='testMonitor', units='deg', fullscr=True)

"""Instructions"""
#Screen 1message1 = visual.TextStim(win, pos=[0,+3],text='We are going to play a game with some worms!')message2 = visual.TextStim(win, pos=[0,-3],    text="You are going to see some worms, like the one below")
exampleWorm = visual.ImageStim(win, image='stim/wormy_green.png',pos=[0, -4])
message3 = visual.TextStim(win, pos=[0, -5], text='Press the button to continue')message1.draw()message2.draw()
exampleWorm.draw()win.flip()#to show our newly drawn 'stimuli'#pause until there's a keypressevent.waitKeys()

#Screen 2 
message1 = visual.TextStim(win, pos=[0,+3],text='You will see two worms, like the ones below')
message2 = visual.TextStim(win, pos=[0,+2],text='The game is to remember the angle of the worms')
left_worm = visual.ImageStim(win, image='stim/wormy_green.png',pos=[0, 3])
right_worm = visual.ImageStim(win, image='stim/wormy_red.png',pos=[0, 2])
message1.draw()
message2.draw()
left_worm.draw()
right_worm.draw()
win.flip()#to show our newly drawn 'stimuli'
#pause until there's a keypress
event.waitKeys()