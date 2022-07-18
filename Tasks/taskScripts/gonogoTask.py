#!/usr/bin/env python
# Changelog

# CHECK WITH CHARLOTTE IF I'M LOGGING DURATION CORRECTLY

#Import things we need
from psychopy import visual
from psychopy import core, event, gui, data, logging
import time
from psychopy.misc import fromFile
import os, csv
import numpy as np
import numpy.random
import random
from collections import deque

import glob, pygame, sys 
from psychopy.misc import fromFile



############################################# fMRI #############################################################




def setup_input(input_method):
    
    #If input_method is 'keyboard', we don't do anything
    #If input_method is 'serial', we set up the serial port for fMRI responses
    
    if input_method == 'keyboard':
        # Don't do anything
        resp_device = None
    elif input_method == 'serial':
        # Serial - we need to set it up
        import serial
        if sys.platform == 'linux2':
            port = '/dev/ttyS0'
        else:
            port = 'COM1'
        resp_device = serial.Serial(port=port, baudrate=9600)
        resp_device.setTimeout(0.0001)
    else:
        raise Exception('Unknown input method')
    return resp_device

def clear_buffer(input_method, resp_device):

    #Clear whichever buffer is appropriate for our input method

    if input_method == 'keyboard':
        # Clear the keyboard buffer
        event.clearEvents()
    else:
        # Clear the serial buffer
        resp_device.flushInput()

def get_response(input_method, resp_device, timeStamped, myClock):
    #if participants don't respond we will set up a null value so we don't get an error
    thisResp = None
    thisRT = np.nan
    if input_method == 'keyboard':
        for key, RT in event.getKeys(keyList = ['escape', 'q', 'left', 'right', 'space'], timeStamped = timeStamped):
            if key in ['escape','q']:
                
                if trig_collector:
                    trig_collector.endCollection()
                #core.quit()
            else:
                thisResp = key
                thisRT = myClock.getTime()
    else:
        thisResp = resp_device.read(1)
        thisRT = timeStamped.getTime()
        if len(thisResp) == 0:
            thisResp = None
            thisRT = np.nan
        else:
            # Map button numbers to side
            ## Blue == 1, Green == 3
            if thisResp in ['1', '3']:
                thisResp = 'left'
            elif thisResp in ['2', '4']:
                thisResp = 'right'

        # Quickly check for a 'q' response on the keyboard to quit
        for key, RT in event.getKeys(keyList = ['escape', 'q'], timeStamped = timeStamped):
            if key in ['escape', 'q']:
                
                if trig_collector:
                    trig_collector.endCollection()
                #core.quit()
    return thisResp, thisRT


############################################Define all fMRI variables###############################################

#Implement absolute paths in any computer

#def runexp(logpath, myWin, trialnums):
    # global instrTxt1
    # #global myWin
    # global instrTxt2
    # global readyTxt
    # global go_words
    # global nogo_words
    # global sans
    # global input_method
    # global resp_device
    # global f
    # global Part_ID
    # global scrambled_pic
    # global scrambled_word
    #Implement absolute paths in any computer
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
   

    # This needs to be either keyboard or serial - we then setup the response device
    input_method = 'keyboard'
    resp_device = setup_input(input_method)

    #let the script know if we are in the scanner or not (true/false)
    In_scanner = True
    slices_per_vol = 38

    #Create dummy period (time needed for the scanner to collect 2 volumes)
    Dummy_timer = core.CountdownTimer(10)

    ################################## Define all variables experiment ######################################

    #collect participant info, create logfile
    info = {'Subject':'test','Age':'','Gender':['male','female','other']}
    infoDlg = ['Test', '20', "male"]
    #infoDlg = gui.DlgFromDict(info, title = 'Subject details:', order = ['Subject','Age','Gender'])

    # Set the sequence
    orden = 'Sequence: Alpha - A B C'

    #If user clicks OK continue with experiment and create a logfile with their details #else quite experiment
    # if infoDlg.OK: 
    #     logpath = 'log_file/%s_log_GoNoGo.csv' %(info['Subject'])
    #     fmri_logpath = 'log_file/%s_log_GoNoGo_fMRI_log.csv' %(info['Subject'])
    #     f = open(logpath, 'w+') # create log file
    #     f.write('%s_%s_%s\n' %(info['Subject'], info['Age'], info['Gender'])) # write participant info
    #     f.write('%s,\n' %(orden))
    #     f.write('Part_ID, Block, Condition, GO or NO, Item ID, Box Type, Correct Answer, Key, RT, Onset, Duration\n') # write headers for logfiles
    #     fmri_log=open(fmri_logpath, 'w+')#create fMRI logfile
    #     fmri_log.write('%s_%s_%s\n' %(info['Subject'], info['Age'], info['Gender'])) # write participant info
    #     fmri_log.write('Volume,Time\n')
    # else:
    #     print ('User Cancelled')
    #     core.quit()
    
    
    
    
    
    myWin.flip()
    #if participants don't respond we will set up a null value so we don't get an error
    thisResp_go = 'no response'
    thisResp_nogo = 'no response'
    corrAns = ' '
    thisRT_go = np.nan
    thisRT_nogo = np.nan

    # set up a stimulus window
    #myWin = visual.Window(size=(1280, 800), fullscr=False, allowGUI=False,winType='pyglet',
    #            monitor='testMonitor', units ='norm', screen=0, rgb=(1,1,1))

    #set up some fonts. If a list is provided, the first font found will be used.
    sans = ['Helvetica','Gill Sans MT', 'Arial','Verdana'] #use the first font found on this list

    #set up instructions and clock (so you can time stamp duration or trials, RT etc..)
    with open(os.path.dirname(os.path.abspath(__file__)) + "//resources//GoNoGo_Task//GoNoGo_instr_1.txt") as f:
        lines1 = f.read()
    with open(os.path.dirname(os.path.abspath(__file__)) + "//resources//GoNoGo_Task//GoNoGo_instr_2.txt") as f:
        lines2 = f.read()
    instrTxt1 = visual.TextStim(myWin,text=lines1, height = 0.05, color='black')
    # For this task, a series of words and pictures framed by a black box will appear in the centre of the screen. \
    # Your job is to press the left button every time a stimulus appears, except when that stimulus is an animal. Then, don't press anything. \n\
    # \nYou will be given around 1 second to respond to each stimulus, after which time, another one will appear. \n\
    # \nSometimes, instead of words or pictures, you will see a scrambled image framed by a box. In that case, your job is to press the left button \
    # on the keyboard every time a stimulus appear that is more slanted than the one that is normally presented.\n\
    # \n(press the left button to continue)
    #set up instructions and clock (so you can time stamp duration or trials, RT etc..)
    instrTxt2 = visual.TextStim(myWin,text=lines2, height = 0.05, color='black')
    # Before each part of the task begins, you will be informed what type of stimuli you will have to attend to by a cue in red (WORD, PICTURE or BOX).\n\
    # \nPlease give equal importance to SPEED and ACCURACY when completing this task. We would like you to respond as FAST as possible while maintaining a high \
    # level of ACCURACY.\n\
    # \nIf you have any questions, please ask the researcher before we start.\n\
    # \nWhen you are ready to begin the task, please press the left button.
    readyTxt = visual.TextStim(myWin, text = 'The experiment will start shortly.', color='black')
    finishTxt = visual.TextStim(myWin, text = 'End of Experiment!', color='black')

    ######### Set up constant variables outside of loop ############

    # read in csv file with conditions on 
    dataFile = open('StimList.csv', 'r')
    reader = csv.reader(dataFile, delimiter = ',')

    #read in first line of the csv file and assign this to the variable header
    header = dataFile.readline() 

    #strip the header to remove \n from the end and split this line into as many entries as there are columns in the header file (i.e., into each of the columns headers)
    hdr = header.strip().split(';')
    lines = dataFile.readlines() #assign all other information into the variable lines
    # create an empty list in which we can append items from the csv file into
    go_words = []
    nogo_words = []
    go_box = []
    nogo_box = []
    global go_img
    go_img = []
    global nogo_img
    nogo_img = []
    scrambled_word = []
    scrambled_pic = []
    for enum, line in enumerate(lines): # read in row by row from csv file 
        if enum < trialnums:
            data = line.strip().split(',')
            if data[0] != '':
                item1 = data[0] # filename of go word i.e., a string of words denoting my stimulus trials - in the first column of my csv file
                go_words.append(item1)
            if data[1] != '':
                item2 = data[1] # filename of nogo word
                nogo_words.append(item2)
            Block = data[2]
            Condition = data[3]
            if data[4] != '':
                item3 = (data[4])
                go_box.append(item3)
                nogo_box.append(item3)
            if data[5] != '':
                item4 = (data[5])
                go_img.append(str(os.getcwd())+item4)
            if data[6] != '':
                item5 = (str(os.getcwd())+data[6])
                nogo_img.append(item5)
            if data[7] != '':
                item6 = (str(os.getcwd())+data[7])
                scrambled_word.append(item6)
            if data[8] != '':
                item7 = (str(os.getcwd())+data[8])
                scrambled_pic.append(item7)


    #List of numbers we can select from to determine number of consecutive go trials before a no go 
    consecutive_gotrials = [2,3,4,5,6,7,8]
    #length of jitter options in seconds for item and fixation
    jitter_item = [0.75,1,1.25]
    jitter_fixation = [0.5,0.75,1]
    diffs = ['e','h']
    #Participant ID
    Part_ID = info['Subject']
    #create a fixation cross
    fixation = visual.TextStim(myWin,text='+',color='black')
    return instrTxt1, myWin, instrTxt2, readyTxt, sans, resp_device, Part_ID, input_method, nogo_words, go_words, scrambled_pic, scrambled_word, finishTxt



######################################Experiment begins##############################################################

# if In_scanner:
#     import ynicstim.parallel_compat
#     import ynicstim.trigger
    
#     port = '/dev/parport0'
#     p = ynicstim.parallel_compat.getParallelPort(port)
#     ts = ynicstim.trigger.ParallelInterruptTriggerSource(port=p)
#     trig_collector = ynicstim.trigger.TriggerCollector(triggersource=ts, slicespervol=slices_per_vol)

# else:
#     trig_collector = None


def HelpWin(myClock, myWin,dfile):
    global trig_collector
    
    
    

    trig_collector = None
    
    # global instrTxt1
    # #global myWin
    # global instrTxt2
    # global readyTxt
    # global go_words
    # global nogo_words
    # global sans
    # global input_method
    # global resp_device
    # global f
    # global Part_ID
    # global scrambled_pic
    # global scrambled_word
    #Implement absolute paths in any computer
    

    # This needs to be either keyboard or serial - we then setup the response device
    input_method = 'keyboard'
    resp_device = setup_input(input_method)

    #let the script know if we are in the scanner or not (true/false)
    In_scanner = True
    slices_per_vol = 38

    #Create dummy period (time needed for the scanner to collect 2 volumes)
    Dummy_timer = core.CountdownTimer(10)

    ################################## Define all variables experiment ######################################

    #collect participant info, create logfile
    info = {'Subject':'test','Age':'','Gender':['male','female','other']}
    infoDlg = ['Test', '20', "male"]
    #infoDlg = gui.DlgFromDict(info, title = 'Subject details:', order = ['Subject','Age','Gender'])

    # Set the sequence
    orden = 'Sequence: Alpha - A B C'

    #If user clicks OK continue with experiment and create a logfile with their details #else quite experiment
    # if infoDlg.OK: 
    #     logpath = 'log_file/%s_log_GoNoGo.csv' %(info['Subject'])
    #     fmri_logpath = 'log_file/%s_log_GoNoGo_fMRI_log.csv' %(info['Subject'])
    #     f = open(logpath, 'w+') # create log file
    #     f.write('%s_%s_%s\n' %(info['Subject'], info['Age'], info['Gender'])) # write participant info
    #     f.write('%s,\n' %(orden))
    #     f.write('Part_ID, Block, Condition, GO or NO, Item ID, Box Type, Correct Answer, Key, RT, Onset, Duration\n') # write headers for logfiles
    #     fmri_log=open(fmri_logpath, 'w+')#create fMRI logfile
    #     fmri_log.write('%s_%s_%s\n' %(info['Subject'], info['Age'], info['Gender'])) # write participant info
    #     fmri_log.write('Volume,Time\n')
    # else:
    #     print ('User Cancelled')
    #     core.quit()
    
    
    myWin.flip()
    #if participants don't respond we will set up a null value so we don't get an error
    thisResp_go = 'no response'
    thisResp_nogo = 'no response'
    corrAns = ' '
    thisRT_go = np.nan
    thisRT_nogo = np.nan

    # set up a stimulus window
    #myWin = visual.Window(size=(1280, 800), fullscr=False, allowGUI=False,winType='pyglet',
    #            monitor='testMonitor', units ='norm', screen=0, rgb=(1,1,1))

    #set up some fonts. If a list is provided, the first font found will be used.
    sans = ['Helvetica','Gill Sans MT', 'Arial','Verdana'] #use the first font found on this list
    try:
        with open(os.path.dirname(os.path.abspath(__file__)) + "//resources//GoNoGo_Task//GoNoGo_instr_1.txt") as f:
            lines1 = f.read()
        with open(os.path.dirname(os.path.abspath(__file__)) + "//resources//GoNoGo_Task//GoNoGo_instr_2.txt") as f:
            lines2 = f.read()
        with open(os.path.dirname(os.path.abspath(__file__)) + "//resources//GoNoGo_Task//GoNoGo_instr_3.txt") as f:
            lines3 = f.read()
    except:
        with open(os.path.dirname(os.path.abspath(__file__)) + "taskScripts//resources//GoNoGo_Task//GoNoGo_instr_1.txt") as f:
            lines1 = f.read()
        with open(os.path.dirname(os.path.abspath(__file__)) + "taskScripts//resources//GoNoGo_Task//GoNoGo_instr_2.txt") as f:
            lines2 = f.read()
        with open(os.path.dirname(os.path.abspath(__file__)) + "taskScripts//resources//GoNoGo_Task//GoNoGo_instr_3.txt") as f:
            lines3 = f.read()
    instrTxt1 = visual.TextStim(myWin,text=lines1,  color='black')
    # For this task, a series of words and pictures framed by a black box will appear in the centre of the screen. \
    # Your job is to press the left button every time a stimulus appears, except when that stimulus is an animal. Then, don't press anything. \n\
    # \nYou will be given around 1 second to respond to each stimulus, after which time, another one will appear. \n\
    # \nSometimes, instead of words or pictures, you will see a scrambled image framed by a box. In that case, your job is to press the left button \
    # on the keyboard every time a stimulus appear that is more slanted than the one that is normally presented.\n\
    # \n(press the left button to continue)
    #set up instructions and clock (so you can time stamp duration or trials, RT etc..)
    instrTxt2 = visual.TextStim(myWin,text=lines2,  color='black')
    instrTxt3 = visual.TextStim(myWin,text=lines3,  color='black')
    try:
        instrimg = visual.ImageStim(myWin,image=(os.path.dirname(os.path.abspath(__file__)) + "//resources//GoNoGo_Task//Go.jpg"),size=[2,1])
    except:
        instrimg = visual.ImageStim(myWin,image=(os.path.dirname(os.path.abspath(__file__)) + "taskScripts//resources//GoNoGo_Task//Go.jpg"),size=[2,1])
    # Before each part of the task begins, you will be informed what type of stimuli you will have to attend to by a cue in red (WORD, PICTURE or BOX).\n\
    # \nPlease give equal importance to SPEED and ACCURACY when completing this task. We would like you to respond as FAST as possible while maintaining a high \
    # level of ACCURACY.\n\
    # \nIf you have any questions, please ask the researcher before we start.\n\
    # \nWhen you are ready to begin the task, please press the left button.

    readyTxt = visual.TextStim(myWin, text = 'The experiment will start shortly.', color='black')
    finishTxt = visual.TextStim(myWin, text = 'End of Experiment!', color='black')

    ######### Set up constant variables outside of loop ############
    dataFile = open(dfile, 'r')
    # read in csv file with conditions on 
    #dataFile = open('resources/GoNoGo_Task/gonogo_stimuli.csv', 'r')
    reader = csv.reader(dataFile, delimiter = ',')

    #read in first line of the csv file and assign this to the variable header
    header = dataFile.readline() 

    #strip the header to remove \n from the end and split this line into as many entries as there are columns in the header file (i.e., into each of the columns headers)
    hdr = header.strip().split(';')
    lines = dataFile.readlines() #assign all other information into the variable lines
    # create an empty list in which we can append items from the csv file into
    go_words = []
    nogo_words = []
    go_box = []
    nogo_box = []
    global go_img
    go_img = []
    global nogo_img
    nogo_img = []
    scrambled_word = []
    scrambled_pic = []
    for enum, line in enumerate(lines): # read in row by row from csv file 
        if line == '\n':
            continue
        data = line.strip().split(',')
        Block = data[0]
        Condition = data[1]
        if data[2] != '':
            item3 = (data[2])
            go_box.append(item3)
            nogo_box.append(item3)
        if data[3] != '':
            try:
                item6 = (str(os.path.dirname(os.path.abspath(__file__)))+'/resources/GoNoGo_Task/'+data[3])
            except:
                item6 = (str(os.path.dirname(os.path.abspath(__file__)))+'taskScripts/resources/GoNoGo_Task/'+data[3])
            
            scrambled_word.append(item6)
            


    #List of numbers we can select from to determine number of consecutive go trials before a no go 
    consecutive_gotrials = [2,3,4,5,6,7,8]
    #length of jitter options in seconds for item and fixation
    jitter_item = [0.75,1,1.25]
    jitter_fixation = [0.5,0.75,1]
    diffs = ['e','h']
    #Participant ID
    Part_ID = info['Subject']
    #create a fixation cross
    fixation = visual.TextStim(myWin,text='+',color='black')


    # if In_scanner:
    #     import ynicstim.parallel_compat
    #     import ynicstim.trigger

    #     port = '/dev/parport0'
    #     p = ynicstim.parallel_compat.getParallelPort(port)
    #     ts = ynicstim.trigger.ParallelInterruptTriggerSource(port=p)
    #     trig_collector = ynicstim.trigger.TriggerCollector(triggersource=ts, slicespervol=slices_per_vol)

    # else:
    #     trig_collector = None

    

    # Presents a ready screen and waits for participant to press enter
    instrTxt1.draw()
    myWin.flip()
    event.waitKeys(keyList=['return'])
    #present instructions screen
    instrTxt2.draw()
    myWin.flip()
    event.waitKeys(keyList=['return'])
    instrTxt3.draw()
    myWin.flip()
    event.waitKeys(keyList=['return'])
    instrimg.draw()
    myWin.flip()
    event.waitKeys(keyList=['return'])
    myWin.flip()
    

    # Start being ready to get triggers
    if trig_collector:
        trig_collector.start()

    #readyTxt.draw()
    #myWin.flip()
    #event.waitKeys(keyList=['return'])

   

    if trig_collector:
        trig_collector.waitForVolume(5)
    #else:
        #event.waitKeys(keyList=['return'])


    return scrambled_word, scrambled_pic,input_method,resp_device,Part_ID,sans
    #set up a clock from which we can getTime() to measure length of experiment and trials
    #myClock = core.Clock()
    #return myClock



#



###BLOCK C. SCRAMBLED
def Block_C(thisrun, myClock, myWin, writer, resdict, scrambled_word, scrambled_pic, input_method, resp_device, Part_ID, sans, runtime):
    global go_words
    global nogo_words
    global go_box
    global nogo_box
    

    #List of numbers we can select from to determine number of consecutive go trials before a no go 
    consecutive_gotrials = [1,2,3,4,5,6]
    #length of jitter options in seconds for item and fixation
    jitter_item = [0.75,1,1.25]
    jitter_fixation = [0.5,0.75,1]
    #create a fixation cross
    fixation = visual.TextStim(myWin,text='+',color='black')
    scrambled_img = []
    #SPLIT THE MINIBLOCKS HERE
    if thisrun == 1:
        slants = ['h']
    elif thisrun == 2:
        slants = ['h']

    #Cue block 3
    
    #This will wait for 3 seconds
    
    
    #This will wait for 3 seconds
    

    for i in slants:
        diff = i
       
        if thisrun == 1 and diff == 'e':
            cond = 'scrambled words easy'
            for i in scrambled_word:
                scrambled_img.append(i)
        elif thisrun == 1 and diff == 'h':
            cond = 'scrambled pics hard'
            for i in scrambled_pic:
                scrambled_img.append(i)
        elif thisrun == 2 and diff == 'e':
            cond = 'scrambled pics easy'
            for i in scrambled_pic:
                scrambled_img.append(i)
        elif thisrun == 2 and diff == 'h':
            cond = 'scrambled words hard'
            for i in scrambled_word:
                scrambled_img.append(i)
        # Number of go trials in the block
        remaining_trials = 1

        # Keeping a track of how many trials we have completed 
        random.shuffle(scrambled_img)
        
        if len(consecutive_gotrials) == 0:
            consecutive_gotrials = [1,2,3,4,5,6]
        random_gotrials = np.random.choice(consecutive_gotrials, 1, replace=False)
        # As the above line returns a one-value list, we need to select that value so that we have an int to manipulate (this is important for the next line)
        number_gotrials = random_gotrials[0]
        #-I made this, trying to choose one of the three box conditions in the xlsx file at random, with replacement.
        gobox_item = np.random.choice(scrambled_img, number_gotrials, replace=True)
        nogobox_item = np.random.choice(scrambled_img, 1, replace=False)


        # Now we can go through the list line by line and call the stimuli in
        d = 0
    #Start Consecutive Go Trials
        tasktimer = core.MonotonicClock()
        
        while tasktimer.getTime() <= runtime:
            
            
            random_gotrials = np.random.choice(consecutive_gotrials, 1, replace=False)
            # As the above line returns a one-value list, we need to select that value so that we have an int to manipulate (this is important for the next line)
            number_gotrials = random_gotrials[0]
            #-I made this, trying to choose one of the three box conditions in the xlsx file at random, with replacement.
            gobox_item = np.random.choice(scrambled_img, number_gotrials, replace=True)
            nogobox_item = np.random.choice(scrambled_img, 1, replace=False)
            numoftrials = np.random.choice(consecutive_gotrials)
            for i in range(0, len(gobox_item)):
                
                if numoftrials != 0:
                    # Draw fixation cross
                    fixation.draw()
                    rand_jitter_fix = random.choice(jitter_fixation)
                    myWin.flip()
                    core.wait(rand_jitter_fix)
                    rt_clock = core.Clock()
                    # Prepare and draw each stimuli each iteration
                    go_stimulus = visual.ShapeStim(myWin, units='', lineWidth=4, lineColor='black', lineColorSpace='rgb', fillColor=None, fillColorSpace='rgb', vertices=((-0.41, 0.5), (0.59, 0.5), (0.5, -0.5), (-0.5, -0.5)), \
                                                                    closeShape=True, pos=(-0.06, 0), size=1, ori=0.0, opacity=1.0, contrast=1.0, depth=0, interpolate=True, name=None, autoLog=None, autoDraw=False)
                    go_stimulusv = visual.ImageStim(myWin, size=0.44,
                                                image=gobox_item[i],
                                                pos=(0, 0))
                
                    durStim = random.choice(jitter_item)
                    contTrial=True
                    event.clearEvents() #start each trial by clearing event buffer to prevent any previous keys interfering with the current trial
                    rt_clock.reset()
                    Onset = myClock.getTime()
                    resdict['Timepoint'], resdict['Time'], resdict['Auxillary Data']= "Stimulus start", myClock.getTime(), "Type: Go"
                    writer.writerow(resdict)
                    resdict['Timepoint'], resdict['Time'], resdict['Auxillary Data'], resdict['Is_correct'] = None, None,None, None
                    while contTrial and rt_clock.getTime() < durStim:
                        go_stimulusv.draw()
                        go_stimulus.draw()
                        
                        myWin.flip() #IIIII
                        
                        thisResp, thisRT = get_response(input_method, resp_device, myClock, myClock)
                        RT = 0
                        corrAns = 'left'
                        isCorrect = 'noResponse'
                        if thisResp is not None:
                            contTrial = False
                            RT = rt_clock.getTime()
                            isCorrect = int(thisResp == corrAns)
                            if isCorrect == 1:
                                isCorrect = True
                                # resdict['Timepoint'], resdict['Time'], resdict['Auxillary Data'], resdict['Is_correct'] = "Stimulus end", myClock.getTime(), "Type: Go", isCorrect
                                # writer.writerow(resdict)
                                # resdict['Timepoint'], resdict['Time'], resdict['Auxillary Data'], resdict['Is_correct'] = None, None,None, None
                            else:
                                isCorrect = False 
                                
                       
                            
                    while rt_clock.getTime() < durStim:
                        go_stimulusv.draw()
                        go_stimulus.draw()
                        myWin.flip()


                    #Write data into logfile
                    resdict['Timepoint'], resdict['Time'], resdict['Auxillary Data'], resdict['Is_correct'] = "Stimulus end", myClock.getTime(), "Type: Go", isCorrect
                    writer.writerow(resdict)
                    resdict['Timepoint'], resdict['Time'], resdict['Auxillary Data'], resdict['Is_correct'] = None, None,None, None
                    boxtype = 'square'
                    itemid = gobox_item[i].split("\\")
                    itemname = itemid[-1][:-4]
                    
                    #resdict['Timepoint'], resdict['Time'], resdict['Is_correct'] = 'Go_task_start', myClock.getTime(), isCorrect
                    #writer.writerow(resdict)
                    
                    
                    
                    remaining_trials = remaining_trials - 1
                    numoftrials = numoftrials -1
                    
                    
                    
                    continue
                        
            #Start No Go Trial
                # Draw fixation point
                fixation.draw()
                rand_jitter_fix = random.choice(jitter_fixation)
                myWin.flip()
                core.wait(rand_jitter_fix)
                rt_clock = core.Clock()
                
                # Prepare and draw the stimulus
                for line_nogo in nogobox_item:
                        if diff == 'e':
                            nogo_stimulus = visual.ShapeStim(myWin, units='', lineWidth=4, lineColor='black', lineColorSpace='rgb', fillColor=None, fillColorSpace='rgb', vertices=((-0.22, 0.5), (0.78, 0.5), (0.5, -0.5), (-0.5, -0.5)), \
                                                                        closeShape=True, pos=(-0.12, 0), size=1, ori=0.0, opacity=1.0, contrast=1.0, depth=0, interpolate=True, name=None, autoLog=None, autoDraw=False)
                        elif diff == 'h':
                            nogo_stimulus = visual.ShapeStim(myWin, units='', lineWidth=4, lineColor='black', lineColorSpace='rgb', fillColor=None, fillColorSpace='rgb', vertices=((-0.31, 0.5), (0.69, 0.5), (0.5, -0.5), (-0.5, -0.5)), \
                                                                    closeShape=True, pos=(-0.09, 0), size=1, ori=0.0, opacity=1.0, contrast=1.0, depth=0, interpolate=True, name=None, autoLog=None, autoDraw=False)
                        nogo_stimulusv = visual.ImageStim(myWin, size=0.44,
                                            pos=(0, 0), image=nogobox_item[0])
                                            
                        durStim = random.choice(jitter_item)
                        contTrial=True
                        event.clearEvents() #start each trial by clearing event buffer to prevent any previous keys interfering with the current trial
                        rt_clock.reset()
                        Onset = myClock.getTime()
                        resdict['Timepoint'], resdict['Time'], resdict['Auxillary Data'] = "Stimulus start", myClock.getTime(), "Type: NoGo"
                        writer.writerow(resdict)
                        resdict['Timepoint'], resdict['Time'], resdict['Auxillary Data'] = None, None,None
                        while contTrial and rt_clock.getTime() < durStim:
                            nogo_stimulusv.draw()
                            nogo_stimulus.draw()
                            myWin.flip()
                            thisResp, thisRT = get_response(input_method, resp_device, myClock, myClock)
                            RT = 0
                            isCorrect = 'noResponse'
                            if thisResp is not None:
                                contTrial = False
                                isCorrect = False
                                RT = rt_clock.getTime()
                                # resdict['Timepoint'], resdict['Time'], resdict['Auxillary Data'], resdict['Is_correct'] = "Stimulus end", myClock.getTime(), "Type: NoGo",isCorrect
                                # writer.writerow(resdict)
                                # resdict['Timepoint'], resdict['Time'], resdict['Auxillary Data'], resdict['Is_correct'] = None, None,None, None
                            else:
                                isCorrect = True
                                
                                                            
                        while rt_clock.getTime() < durStim:
                            nogo_stimulusv.draw()
                            nogo_stimulus.draw()
                            myWin.flip()

                #Write data into logfile
                        resdict['Timepoint'], resdict['Time'], resdict['Auxillary Data'], resdict['Is_correct'] = "Stimulus end", myClock.getTime(), "Type: NoGo",isCorrect
                        writer.writerow(resdict)
                        resdict['Timepoint'], resdict['Time'], resdict['Auxillary Data'], resdict['Is_correct'] = None, None,None, None
                        if diff == 'e':
                            boxtype = 'easy'
                        elif diff == 'h':
                            boxtype = 'hard'
                        itemid = nogobox_item[0].split("\\")
                        itemname = itemid[-1][:-4]
                        
                        #resdict['Timepoint'], resdict['Time'], resdict['Is_correct'] = 'NoGo_task_start', myClock.getTime(), isCorrect
                       # writer.writerow(resdict)
                        
                        remaining_trials = remaining_trials - 1
                        d = d+1
                        numoftrials = np.random.choice(consecutive_gotrials)


            #This removes the items from the list that you have used (true sampling without replacement) 
                consecutive_gotrials = [ x for x in consecutive_gotrials if x not in random_gotrials]



        # If the while statement is no longer true then do the following
        # else: 
            
        #     # When there's less than 8 trials, we choose a random number to complete +4
        #     print ('last run with %i remaining trials' %(remaining_trials))
        #     random.shuffle(scrambled_img)
        #     #gobox_item = np.random.choice(scrambled_img, (remaining_trials + random.randint(1, 3)), replace=True)
        #     #gobox_item = np.random.choice(scrambled_img)
        #     gobox_item = np.random.choice(scrambled_img, (remaining_trials), replace=True)

        # #Start the last Go trials sequence to reach n 100
        #     for enum, i in enumerate(range(0, len(scrambled_img))):
        #             if enum < numtrials:
        #                 # Draw fixation cross
        #                 fixation.draw()
        #                 rand_jitter_fix = random.choice(jitter_fixation)
        #                 myWin.flip()
        #                 core.wait(rand_jitter_fix)
        #                 rt_clock = core.Clock()
        #                 # Prepare and draw each stimuli each iteration
        #                 go_stimulus = visual.ShapeStim(myWin, units='', lineWidth=4, lineColor='black', lineColorSpace='rgb', fillColor=None, fillColorSpace='rgb', vertices=((-0.41, 0.5), (0.59, 0.5), (0.5, -0.5), (-0.5, -0.5)), \
        #                                                                 closeShape=True, pos=(-0.06, 0), size=1, ori=0.0, opacity=1.0, contrast=1.0, depth=0, interpolate=True, name=None, autoLog=None, autoDraw=False)
        #                 go_stimulusv = visual.ImageStim(myWin, size=0.44,
        #                                             image=scrambled_img[i],
        #                                             pos=(0, 0))
                        
        #                 durStim = random.choice(jitter_item)
        #                 contTrial=True
        #                 event.clearEvents() #start each trial by clearing event buffer to prevent any previous keys interfering with the current trial
        #                 rt_clock.reset()
        #                 Onset = myClock.getTime()
                        
        #                 while contTrial and rt_clock.getTime() < durStim:
        #                     go_stimulusv.draw()
        #                     go_stimulus.draw()
        #                     myWin.flip()
        #                     thisResp, thisRT = get_response(input_method, resp_device, myClock, myClock)
        #                     RT = 0
        #                     corrAns = 'left'
        #                     isCorrect = 'noResponse'
        #                     if thisResp is not None:
        #                         contTrial = False
        #                         RT = rt_clock.getTime()
        #                         isCorrect = int(thisResp == corrAns)
        #                         if isCorrect == 1:
        #                             isCorrect = True
        #                         else:
        #                             isCorrect = False 
        #                 while rt_clock.getTime() < durStim:
        #                     go_stimulusv.draw()
        #                     go_stimulus.draw()
        #                     myWin.flip()

        #                 #Write data into logfile
        #                 boxtype = 'square'
        #                 itemid = scrambled_img[i].split("\\")
        #                 itemname = itemid[-1][:-4]
                        
        #                 resdict['Timepoint'], resdict['Time'], resdict['Is_correct'] = 'Task_End', myClock.getTime(), isCorrect
        #                 writer.writerow(resdict)
                        
        #                 remaining_trials = remaining_trials - 1

        # scrambled_img = []

    # Rest screen goes here
    # resdict['Timepoint'], resdict['Time'], resdict['Auxillary Data'], resdict['Is_correct'] = "Stimulus end", myClock.getTime(), "Type: NoGo",isCorrect
    # writer.writerow(resdict)
    # resdict['Timepoint'], resdict['Time'], resdict['Auxillary Data'], resdict['Is_correct'] = None, None,None, None
    rest_screen = visual.TextStim(myWin, 
                        units='norm',
                        pos=(0, 0), text="5 second rest. The experiment will begin shortly",
                        font=sans, 
                        alignHoriz = 'center',
                        color='black')
    #rest_screen.draw()
    #myWin.flip() 
    #core.wait(5)

def main(logloc, myClock, myWin, writer, resdict, runtime,dfile):
    #instrTxt1, myWin, instrTxt2, readyTxt, sans, resp_device, Part_ID, f, input_method, nogo_words, go_words, scrambled_pic, scrambled_word, fmri_log, finishTxt = runexp(logloc, myWin)
    scrambled_word, scrambled_pic, input_method, resp_device, Part_ID, sans = HelpWin(myClock, myWin,dfile)
    resdict['Timepoint'],resdict['Time'] = 'Go/NoGo Initialized',myClock.getTime()
    writer.writerow(resdict)
    
    ###CALL THE ORDER###
    #DEBUGGER
    #testing (uncomment as needed)
    #diff = 'e'
    #Block_A(diff)
    #Block_B(diff)
    #Block_C(diff)


    #thisrun = 1
    #Block_A(thisrun)
    #Block_B(thisrun)
    #Block_C(thisrun)
    thisrun = 2
    Block_C(thisrun, myClock, myWin, writer, resdict, scrambled_word,scrambled_pic,input_method,resp_device,Part_ID,sans, runtime)
    #Block_B(thisrun)
    #Block_A(thisrun)


    
    resdict['Timepoint'],resdict['Time'] = 'Go/NoGo Finished',myClock.getTime()
    writer.writerow(resdict)
    

    ############################################End Experiment###############################################################
    # If in fMRI mode, store the triggers
    if trig_collector:
        trig_collector.endCollection()
        v_t = trig_collector.getVolumeTimings(myClock)

        # Create a file which has the fMRI timings in
        

    
    myWin.flip()
    fin_time=myClock.getTime()
    
    #event.waitKeys()
    
    

def runexp(logfilelocation, time, myWin, writer,resdict, runtime,dfile,seed):
    writer = writer[0]
    random.seed(a=seed)
    resdict['Timepoint'],resdict['Time'] = 'gonogo START', time.getTime()
    writer.writerow(resdict)
    
    main(logfilelocation, time, myWin, writer, resdict, runtime,dfile)

