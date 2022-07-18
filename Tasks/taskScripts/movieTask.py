#Written by Brontë McKeown and Theodoros Karapanagiotidis
from matplotlib.pyplot import pause
from psychopy import visual 

from psychopy import gui, data, core,event
from taskScripts import ESQ
import os.path


import random

###################################################################################################
def runexp(filename, timer, win, writer, resdict, runtime,dfile,seed):
    writera = writer[1]
    writer = writer[0]
    random.seed(seed)
    
    resdict['Timepoint'], resdict['Time'] = 'Movie Task Start', timer.getTime()
    writer.writerow(resdict)
    resdict['Timepoint'], resdict['Time'] = None,None
    
    

    

    # user can update instructions for task here if required.
    instructions = """You will be presented with several video clips. These clips are rated 15 and contain extreme violence, aggression and bad language. If you find these types of clips distressing, please do not participate in this study. 
    \nIf at any point, you become distressed and would like to stop the task, please inform the experimenter. You will not be penalised for withdrawing from the study. 
    \nAt the end of each task block, you will be asked to rate several statements about the ongoing thoughts you experienced during that block. 
    \nPress enter or return to begin the experiment meow."""

    # user can update start screen text here if required. 
    start_screen = "The experiment is about to start. Press return to continue."


    
    # create text stimuli to be updated for start screen instructions.
    stim = visual.TextStim(win, "", color = [-1,-1,-1], wrapWidth = 1300, units = "pix", height=40)

    # update text stim to include instructions for task. 
    stim.setText(instructions)
    stim.draw()
    win.flip()
    # Wait for user to press enter to continue. 
    event.waitKeys(keyList=(['return']))

    # update text stim to include start screen for task. 
    stim.setText(start_screen)
    stim.draw()
    win.flip()
    
    # Wait for user to press enter to continue. 
    event.waitKeys(keyList=(['return']))
    
    
    
    # Create two lists, one with the control videos, and one with action videos
    # Videos are sorted based on their file name
    list_of_videos = os.listdir(os.path.join(os.getcwd(), 'taskScripts//resources//Movie_Task//videos'))
    
    #I've been trying to do randomize the selection of the videos but can't get it to work, basically just fucking around w trying to
    #code random.shuffle ??? anyways i took it out bc otherwise it'll break. hopefully u see the vision
    
    # Write when it's initialized
    resdict['Timepoint'], resdict['Time'] = 'Movie Init', timer.getTime()
    writer.writerow(resdict)
    resdict['Timepoint'], resdict['Time'] = None,None
    
    # Create two different lists of videos for trial 1 and trial 2. 
    
    trialvideo = os.path.join(os.getcwd(), 'taskScripts//resources//Movie_Task//videos') + "/" + list_of_videos[filename-1]


    
    
    
    # Pick the video to show based on the trial version, we are just going to pick the one at the top of the list
    
        
    
    
    # present film using moviestim
    resdict['Timepoint'], resdict['Time'] = 'Movie Start', timer.getTime()
    writer.writerow(resdict)
    resdict['Timepoint'], resdict['Time'] = None,None
    
    #bruh this shit ain't working wtf
     
    mov = visual.MovieStim3(win, trialvideo, size=(1920, 1080), flipVert=False, flipHoriz=False, loop=False)
    expClock = core.Clock()
    timelimit = 10
    while mov.status != visual.FINISHED:
        if expClock.getTime() > timelimit: 
            mov.pause()
            ESQ.runexp(None,timer,win,[writer,writera],resdict,None,None,None)
            mov.play()
            expClock.reset()
            timelimit = 10000000
            #break

        mov.draw()
        win.flip()

    
    
    
    resdict['Timepoint'], resdict['Time'] = 'Movie End', timer.getTime()
    writer.writerow(resdict)
    resdict['Timepoint'], resdict['Time'] = None,None
