#Written by Brontë McKeown and Theodoros Karapanagiotidis
from psychopy import visual 
from psychopy.visual import MovieStim 
from psychopy import gui, data, core,event
import csv
import time
from time import localtime, strftime, gmtime
from datetime import datetime
import os.path
import pyglet 
import pandas as pd
from itertools import groupby
import random
############### Section for filmlist randomisation ################################################

# read in filmlist csv which is sorted according to condition (cert and uncert)
#df = pd.read_csv(os.path.join(os.getcwd(),'resources//Movie_Task//csv//sorted_filmList.csv'))

# separate the dataframe into conditions (cert and uncert)
# cert = df['cert']
# uncert = df['uncert']

# def randomisation(df1,df2):
#     """Returns randomised list for 1st dataframe given
#     1st film is always determined by condition required
#     The remaining films are randomly presented but there are never more
#     than two consecutive conditions"""
#     max_count = 1


#     while max_count == 1:
#         x_bad = []
#         # randomly select one film from each condition which will go first in the list
#         x_1 = df1.sample(n=1)
        
#         # drop the randomly selected films from each condition list
#         x_cert = df1.drop(x_1.keys()[0])
        
#         # put together remaining lists minus each film already taken out for a and b
#         # randomise these lists
#         x_remaining = pd.concat([x_cert,df2])
#         x_random = x_remaining.sample(n=7)
        
#         # put together first item of a list with rest of randomised a list
#         x_complete = pd.concat([x_1,x_random])
        
#         # rest indices so that the final a and b lists can be put together to write to 
#         # csv file
#         x_final = x_complete.reset_index(drop= True)
        
#         # convert dataframe to list
#         x_list = x_final.values.tolist()
        
#         # only retain cert and uncert from filename
#         for i in range(len(x_list)):
#             x_list[i] = x_list[i].split('/')[1].split('_')[0]
        
#         # checks how many times condition is placed consecutively 
#         x_check = [[i, sum(1 for i in group)] for i, group in groupby(x_list)]

#         # check if any condition appears > twice consecutively in x_check list.
#         if any(i[1] > 2 for i in x_check):
#             #print (x_check)
#             # if any condition appears > twice consecutively, continues loop.
#             print ('Conditions not met, reshuffling.')
#         else:
#             # if conditions don't appear > twice consecutively, breaks loop.
#             #print (x_check)
#             print ('Conditions met, finished.')
#             max_count = 0
#     return x_final

# # call randomisation function for a and b lists
# a_final = randomisation(cert,uncert)
# b_final = randomisation(uncert,cert)

# # put together final a and b lists to write to csv file
# df_final = pd.concat([a_final,b_final],axis = 1)

# # rename column headers to be a and b instead of 0 and 1
# df_final.columns=['a','b']

# # save a and b lists concatanated to csv file without indexes
# df_final.to_csv('csv\\filmList.csv', index = False)

###################################################################################################
def runexp(filename, timer, win, writer, resdict, runtime,dfile,seed):
# kill switch for Psychopy3
    random.seed(seed)
    resdict['Timepoint'], resdict['Time'] = 'Movie Task Start', timer.getTime()
    writer.writerow(resdict)
    resdict['Timepoint'], resdict['Time'] = None,None
    df = pd.read_csv(dfile)
    # call globalKeys so that whenever user presses escape, quit function called
    

    # user should set cwd to the experiment directory.
    #os.chdir('R:\\Task_SGT\\Bronte\\movie_study_2.0')
    # user should set directory for output files to be stored. 
    #save_path= 'R:\\Task_SGT\\Bronte\\movie_study_2.0\\output\\questionnaire'

    # user can update instructions for task here if required.
    instructions = """You will be presented with several video clips. These clips are rated 15 and contain extreme violence, aggression and bad language. If you find these types of clips distressing, please do not participate in this study. 
    \nIf at any point, you become distressed and would like to stop the task, please inform the experimenter. You will not be penalised for withdrawing from the study. 
    \nAt the end of each task block, you will be asked to rate several statements about the ongoing thoughts you experienced during that block. 
    \nTo rate these statements, hold 1 to move the marker left along the slider and hold 2 to move the marker right along the slider. When you are happy with your selection, please press 4 to move on to the next statement. 
    \nPress return to begin the experiment."""

    # user can update start screen text here if required. 
    start_screen = "The experiment is about to start. Press return to continue."


    # use trialhandler to sequentially present films listed in filmlist csv file. 
    #filmDict = data.TrialHandler(nReps = 1, method = 'sequential', trialList = data.importConditions('taskScripts//resources//Movie_Task//csv//filmList.csv'), name = 'filmList') 

    # create white window for stimuli to be presented on throughout task. 
    # win = visual.Window(size=[1024, 768], color=[1,1,1,], monitor="testMonitor", fullscr= True, allowGUI = False)
    # create text stimuli to be updated for start screen instructions.
    stim = visual.TextStim(win, "", color = [-1,-1,-1], wrapWidth = 1300, units = "pix", height=40)

    # update text stim to include instructions for task. 
    stim.setText(instructions)
    stim.draw()
    win.flip()
    # Wait for user to press 1 to continue. 
    event.waitKeys(keyList=(['return']))

    # update text stim to include start screen for task. 
    stim.setText(start_screen)
    stim.draw()
    win.flip()
    # Wait for user to press 5 to continue. 
    event.waitKeys(keyList=(['return']))
    control = []
    action = []
    try:
        for a in os.listdir(os.path.join(os.getcwd(), 'taskScripts//resources//Movie_Task//videos')):
            v = a.split("_")[0]
            if v == "control":
                control.append(a)
            if v == "action":
                action.append(a)
    
        # start a clock right before the experiment starts
        filmlista = []
        filmlistb = []
        random.shuffle(control)
        random.shuffle(action)
        resdict['Timepoint'], resdict['Time'] = 'Movie Init', timer.getTime()
        writer.writerow(resdict)
        resdict['Timepoint'], resdict['Time'] = None,None
        
        for en, m in enumerate(control):
            m = os.path.join(os.getcwd(), 'taskScripts//resources//Movie_Task//videos//' + m)
            r = os.path.join(os.getcwd(), 'taskScripts//resources//Movie_Task//videos//' + action[en])
            filmlista.append(m)
            
            filmlistb.append(r)
    
        
    
        filmlist = random.choice([filmlista,filmlistb])
        tasktime = core.Clock()
        tasktime.reset()

        if filename == 1:
            filmlist = filmlista[0]
        if filename == 2:
            filmlist = filmlistb[0]
            
        
        # loop through each film stored in filmDict created above using trialhandler. 
        
            # store trial start time for later use in calculating trial duration. 
        start =time.time()

        # store when the video started to later store in outputfile, this videoStart uses clock created at start of experiment. 
        videoStart = tasktime.getTime()
        # present film using moviestim
        resdict['Timepoint'], resdict['Time'] = 'Movie Start', timer.getTime()
        writer.writerow(resdict)
        resdict['Timepoint'], resdict['Time'] = None,None
        mov = visual.MovieStim3(win, filmlist, size=(1920, 1080), flipVert=False, flipHoriz=False, loop=False)

        while mov.status != visual.FINISHED:
            mov.draw()
            win.flip()
    except:
        
        for a in os.listdir(os.path.join(os.getcwd(), 'resources//Movie_Task//videos')):
            v = a.split("_")[0]
            if v == "control":
                control.append(a)
            if v == "action":
                action.append(a)
        filmlista = []
        filmlistb = []
        random.shuffle(control)
        random.shuffle(action)
        resdict['Timepoint'], resdict['Time'] = 'Movie Init', timer.getTime()
        writer.writerow(resdict)
        resdict['Timepoint'], resdict['Time'] = None,None

        for en, m in enumerate(control):
            m = os.path.join(os.getcwd(), 'resources//Movie_Task//videos//' + m)
            r = os.path.join(os.getcwd(), 'resources//Movie_Task//videos//' + action[en])
            filmlista.append(m)
            
            filmlistb.append(r)
    
        
    
        filmlist = random.choice([filmlista,filmlistb])
        tasktime = core.Clock()
        tasktime.reset()

        if filename == 1:
            filmlist = filmlista[0]
        if filename == 2:
            filmlist = filmlistb[0]
            
        
        # loop through each film stored in filmDict created above using trialhandler. 
        
            # store trial start time for later use in calculating trial duration. 
        start =time.time()

        # store when the video started to later store in outputfile, this videoStart uses clock created at start of experiment. 
        videoStart = tasktime.getTime()
        # present film using moviestim
        resdict['Timepoint'], resdict['Time'] = 'Movie Start', timer.getTime()
        writer.writerow(resdict)
        resdict['Timepoint'], resdict['Time'] = None,None
        mov = visual.MovieStim3(win, filmlist, size=(1920, 1080), flipVert=False, flipHoriz=False, loop=False)

        while mov.status != visual.FINISHED:
            mov.draw()
            win.flip()
    # store when the video ends to later store in outputfile, this videoEnd uses clock created at start of experiment. 
    videoEnd = tasktime.getTime()
    resdict['Timepoint'], resdict['Time'] = 'Movie End', timer.getTime()
    writer.writerow(resdict)
    resdict['Timepoint'], resdict['Time'] = None,None
    # If statement to either present break screen or end screen
    # nextTrial = filmDict.getFutureTrial(n=1) # fixes error for end screen 
    # if nextTrial is None or nextTrial[videoCondition] == None:
    #     # when the video has ended, call thought_probes function to present probes and rating scale
    #     thought_probes(film[videoCondition], part_number,1) 
    # else:
    #     thought_probes(film[videoCondition], part_number)

    # outputfile.flush()
