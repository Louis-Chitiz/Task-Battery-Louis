# -*- coding: utf-8 -*-
"""
Created on Mon Mar  5 14:48:51 2018

@author: xw1365
"""
''' This is a script to run the blocked and mixed experiment.
Instruction:
In this experiment, participants will be asked to match words based on their features - colour,size or shape.\n" + "  \n" +  
The feature will change on each trial and will be indicated by the top word on the screen.\n" +  
Subjects need to determine whether the probe and target shares the same feature.

The script will create a folder called data_FeatureMatchingExperiment under the folder of the script
Capture the info of each subject - experiment time, ID, name
Generate a csv file for each subject
Store the data in that csv file, inclduing the info about each trial, fixa_onset,offset, clue_onset,offset and so on.

Trial num =
Run num =
Trial time = 
Run time = 
'''
from psychopy import visual, core, monitors, event, sound, gui, logging
from psychopy.hardware import keyboard
from datetime import datetime
from random import shuffle
import os
import time
import csv
import sys, os, errno # to get file system encoding (used in setDir())
import numpy as np
import random
from collections import OrderedDict,deque
from psychopy.hardware import keyboard

# Experiment constants

def runexp(logfile, expClock, win, writer, resultdict, runtime,dfile,seed):
    writer = writer[0]
    random.seed(a=seed)
    # Experiment constants
    instruct_file = 'semantic_relation_instru.csv' 
    rest_file = 'semantic_relation_judgement_rest.csv'

    #stimuli_file = 'feature_matching_stimuli_exp_test.csv'
    expName = 'Reading_and_Memory_Recall_Task'  # the experiment name
    data_folder = 'data' + '_' +  expName  # make a directory to store data
    stimuli_name = 'sem_stim_run'
    fixa_name = 'sem_fixa_run'
    # assign the monitor name
    monitor_name = 'HP ProOne 600'

    # window size = x, y
    win_size_x = 800
    win_size_y = 600

    # window background color
    win_bg_col = (1.0,1.0,1.0) # background color is white
    changed_col = (-1,-1,-1) # response color is red
    win_text_col = (-1,-1,-1)  # text color is black

    # instruction, position height (font size)
    instru_pos = (0,0) # (0,0) indicates the central position
    clue_pos = (0,0)
    fixa_pos = (0,0)
    word_pos = (0,0)
    question_pos = (0,0)

    instru_h = 62
    text_h = 62
    task_h = 62

    num_skip_trials = 1  # the number of trials that can be skipped, used for testing the scirpt

    words_num = 15

    # have a rest parameters
    rest_num = 100 # after every rest_num, subjects can have a rest
    rest_time = 2 # subjects can have a break for rest_time

    num_trials = 30 # total trial numbers of each run 


    # presentation time of clue and probe
    clue_time = 2
    task_instr_time = 1
    word_time = 0.6
    sen_time = 9
    question_duration = 4
    rating_time = 12

    # response time 
    #timelimit_deci = 3
    # define functions

    # get the current directory of this script - correct
    def get_pwd():
        global curr_dic
        curr_dic = os.path.dirname(sys.argv[0])  # U:/task_fMRI_Experiment/exp_March
        return curr_dic

    # make a folder in the current directory used to store data  - correct
  

    def generate_jitter_list(trial_num,start,stop):
        '''
        trial_num is the number of trials, which means how many random jitter you need to generate
        start and stop is used to return a random interger N sucha that a <=N <= b.
        start = 20
        stop = 30

        is not necessary in this exp
        '''
        jitter_list = []
        for i in range(trial_num):
            jitter_time = random.randint(start,stop)/10.0
            jitter_list.append(jitter_time)
        jitter_sum  = sum(jitter_list)
        jitter_mean = jitter_sum/float(len(jitter_list))

        return jitter_list,jitter_sum,jitter_mean

    # quit functions  - to allow subjects to quit the experiment  - correct
    def shutdown ():
        win.close()
        core.quit()

    # get the participants info, initialize the screen and create a data file for this subject
    def info_gui(expName):
        # Set up a dictionary in which we can store our experiment details
        expInfo={}
        expInfo['expname'] =expName
        # Create a string version of the current year/month/day hour/minute
        expInfo['expdate']=datetime.now().strftime('%Y%m%d_%H%M')
        expInfo['subjID']='a'
        expInfo['subjName']='b'
        expInfo['run']=''

        # Set up our input dialog
        # Use the 'fixed' argument to stop the user changing the 'expname' parameter
        # Use the 'order' argumennt to set the order in which to display the fields
        dlg = gui.DlgFromDict(expInfo,title='input data', fixed = ['expname','expdate'],order =['expname','expdate','subjID','subjName','run'])

        #if not dlg.OK:
            #print ('User cancelled the experiment')
            #core.quit()

    # creates a file with a name that is absolute path + info collected from GUI
        #filename = data_folder + os.sep + '%s_%s_%s_%s.csv' %(expInfo['subjID'], expInfo['subjName'], expInfo['expdate'], expInfo['run'])
        stimuli_file = dfile
        #fixa_file = fixa_name + expInfo['run']+'.csv'
        return expInfo, filename,stimuli_file,fixa_file
    # to avoid overwrite the data. Check whether the file exists, if not, create a new one and write the header.
    # Otherwise, rename it - repeat_n
    # correct
    # def write_file_not_exist(filename):
    #     repeat_n = 1
    #     while True:
    #         if not os.path.isfile(filename):
    #             f = open(filename,'w')
    #            # f.write(header)
    #             break
    #         else:
    #             #filename = data_folder + os.sep + '%s_%s_%s_repeat_%s.csv' %(expInfo['subjID'], expInfo['subjName'], expInfo['expdate'],str(repeat_n))
    #             repeat_n = repeat_n + 1


    # Open a csv file, read through from the first row   # correct
    def load_conditions_dict(conditionfile):

    #load each row as a dictionary with the headers as the keys
    #save the headers in its original order for data saving

    # csv.DictReader(f,fieldnames = None): create an object that operates like a regular reader 
    # but maps the information in each row to an OrderedDict whose keys
    # are given by the optional fieldnames parameter.

        with open(conditionfile) as csvfile:
            reader = csv.DictReader(csvfile)
            trials = []

            for row in reader:
                trials.append(row)

        # save field names as a list in order
            fieldnames = reader.fieldnames  # filenames is the first row, which used as keys of trials

        return trials, fieldnames   # trial is a list, each element is a key-value pair. Key is the 
                                    # header of that column and value is the corresponding value

    # Create the log file to store the data of the experiment 
    # create the header


    # def write_header(filename, header):
    #     with open (filename,'a') as csvfile:
    #         fieldnames = header
    #         data_file = csv.DictWriter(csvfile,fieldnames=fieldnames,lineterminator ='\n')
    #         data_file.writeheader()

    #write each trial
    # def write_trial(filename,header,trial):
    #     with open (filename,'a') as csvfile:
    #         fieldnames = header
    #         data_file = csv.DictWriter(csvfile,fieldnames=fieldnames,lineterminator ='\n')
    #         data_file.writerow(trial)


    def read_fix_from_csv(fixa_file):

        """
        read random fixation file from fixa_file and shuffle and write them in a list
        fixa_file is the random fixa time file
        argument:sem_fixa_run1.csv, sem_fixa_run2.csv,sem_fixa_run3.csv,sem_fixa_run4.csv

        """

        f = open(fixa_file,'r')    
        fixa_list = []   

        for line in f.readlines():
            line = line.strip()     
            line = float(line)
            fixa_list.append(line)

        #random.shuffle(fixa_list)

        return fixa_list , sum(fixa_list)


    # set up the window
    # fullscr: better timing can be achieved in full-screen mode
    # allowGUI: if set to False, window will be drawn with no frame and no buttons to close etc...

    def set_up_window(): 
        mon = monitors.Monitor(monitor_name)
        mon.setDistance (114)
        win = visual.Window([win_size_x,win_size_y],fullscr = False, monitor = mon,allowGUI = True, winType = 'pyglet', units="pix",color=win_bg_col)
        win.mouseVisible = False  # hide the mouse
        return win

    # read the content in the csv or text file
    # def read_cont (filename):
    #     f = open(filename,'r')
    #     return f

    # prepare the content on the screen - content is text
    def prep_cont(line, pos):
        line_text = visual.TextStim(win,line,color = win_text_col,pos = pos)
        return line_text

    # display the content on the screen
    def disp_instr_cont(line):
        line.draw()
        win.flip()
        keys = event.waitKeys(keyList =['return','escape'])

        if keys[0][0]=='escape':
            shutdown()

    def instruct():
        """
        path is where the instruct figure stored
        instruct_figure is the name of instruct_figure
        """
        instruction_1 = visual.ImageStim(win,image = 'instruction_1.jpg',pos = (0,0))
        instruction_2 = visual.ImageStim(win,image = 'instruction_2.png',pos = (0,0))
        instruction_1.draw()
        win.flip()
        event.waitKeys(keyList=['return','escape','space'],timeStamped = True)
        instruction_2.draw()
        win.flip()
        event.waitKeys(keyList=['return','escape','space'],timeStamped = True)
        keys = event.waitKeys(keyList =['return','escape'])
        if keys[0][0]=='escape':
            shutdown()

    def trigger_exp():

        trigger = prep_cont('experiment starts soon',instru_pos)
        trigger.draw()
        win.flip()

    def ready():

        trigger = prep_cont('experiment soon',instru_pos,instru_h)
        trigger.draw()
        ready_onset = win.flip()
        return ready_onset

    def end_exp():

        trigger = prep_cont('End of Experiment',instru_pos )
        trigger.draw()
        end_onset = win.flip()
        keys = event.waitKeys(keyList =['return'],timeStamped = True)
        
        
        return end_onset

    # read the rest
    # def rest():
    #     f = read_cont(rest_file)
    #     for line in f.readlines():
    #         line.split('\n')
    #         line_text = prep_cont(line,instru_pos,text_h)
    #         disp_instr_cont(line_text) 

    # display each trial on the screen at the appropriate time
    def run_stimuli(stimuli_file,fixa_list, timer, resultdict, writer):
        resultdict['Timepoint'], resultdict['Time'] = "Reading start", timer.getTime()
        writer.writerow(resultdict)
        resultdict['Timepoint'], resultdict['Time'] = None,None

        """
        stimuli file is sem_stim_runi.csv file, including the stimuli for each run

        fixa_list is a list, including random jittered fixation time for each trial

        """
        # read the stimuli  # re-define, not use numbers, but use keywords
        all_trials, headers = load_conditions_dict(conditionfile=stimuli_file)
        headers += ['trial_pres_num','fixa1_onset', 'fixa1_durat', 'clue_onset', 'clue_durat', 'task_onset','task_durat','word1_onset', 'word2_onset','word3_onset','word4_onset', 'word5_onset','word6_onset',
        'word7_onset','word8_onset','word9_onset','word10_onset','word11_onset','word12_onset','word13_onset','word14_onset','word15_onset', 'word_time','fixa2_onset', 'fixa2_durat','question1_onset','question1_offset','rating1','rating1_RT','question2_onset','question2_offset',
        'rating2','rating2_RT','question3_onset','question3_offset','rating3','rating3_RT','ori_press_word','press_word','press_word_offset','RT', 'correct','KeyPress'] 

        # read the fixation duration
    #    all_fixa, fixa_headers = load_conditions_dict(conditionfile=fixa_file)
        # open the result file to write the heater

        #write_header(filename,headers) 

    #    
    #    
        #shuffle(all_trials) #- 
        trial_pres_num = 1 # initialize a counter (so that we can have mini-blocks of 10)
        fixa_num = 0          
        rating_num = 0

        #trigger the scanner
        trigger_exp()

        #event.waitKeys(keyList=['return'], timeStamped=True)
        #  remind the subjects that experiment starts soon.
        #ready()
        #core.wait(9)  # 3 TRs
        run_onset = win.flip() 
        text_inst = visual.TextStim(win=win, name='text_4',
            text='You may now stop.',
            font='Open Sans',
            pos=(0, 0), height=0.1, wrapWidth=None, ori=0.0, 
            color='black', colorSpace='rgb', opacity=None, 
            languageStyle='LTR',
            depth=0.0);
        try:
            with open(os.path.join(os.getcwd(),"taskScripts/resources/Reading_Task/instructions.txt")) as f:
                lines1 = f.read()
        except:
            with open(os.path.join(os.getcwd(),"resources/Reading_Task/instructions.txt")) as f:
                lines1 = f.read()
        
        for i, cur in enumerate([lines1]):
            text_inst.setText(cur)
            text_inst.draw()
            win.flip()
            time.sleep(1)
            event.waitKeys(keyList=['return'])

        trialtimer = core.MonotonicClock()
        
        for enum, trial in enumerate(all_trials):
            if trialtimer.getTime() < runtime:       
                
                #''' trial is a ordered dictionary. The key is the first raw of the stimuli csv file'''

                # prepare fixation, clue, probe and target for dispaly
                fixa  = prep_cont(trial['fixa'],fixa_pos)
                clue  = prep_cont(trial['clue'],fixa_pos)
                #task = trial['task']
                Rating1 = prep_cont(trial['Question1'],clue_pos)
                Rating2 = prep_cont(trial['Question2'],clue_pos)
                Rating3 = prep_cont(trial['Question3'],clue_pos)

                # write all the words to a sentence list
                sen_list = []

                for i in range (1,16):
                    word = trial['word'+str(i)]
                    sen_list.append(word)
                resultdict['Timepoint'], resultdict['Time'], resultdict['Auxillary Data'] = "Reading trial start", timer.getTime(), sen_list
                writer.writerow(resultdict)
                resultdict['Timepoint'], resultdict['Time'], resultdict['Auxillary Data'] = None,None,None
                


                # draw fixation and flip the window
                fixa.draw()

                if trial_pres_num == 1:
                    timetodraw = run_onset
                else:
                    fixa_sum = 0
                    for fixa_index in range(0,fixa_num,1):
                        fixa_sum+=fixa_list[fixa_index]
                    timetodraw = run_onset + fixa_sum + (clue_time + task_instr_time + sen_time)*(trial_pres_num -1) + (rating_time*rating_num)

                while core.monotonicClock.getTime() < (timetodraw - (1/120.0)):
                    pass
                fixa1_onset = win.flip()
                #print ('fixa1_onset', fixa1_onset)

                # draw clue and filp the window
                border = visual.Rect(win, width = 500, fillColor = 'white', lineColor = 'black',pos = (0,0))

                words_onset = []

                if trial['trial type'] == 'catch trial':

                    random_i = random.randint (0,words_num-1)  # randomly choose a number between 1 and 15

                    trial['ori_press_word'] = sen_list[random_i]

                    for word_index in range(15):

                        word = sen_list[word_index]

                        if word_index == random_i:

                            word = visual.TextStim(win,text = word,color = changed_col,pos = clue_pos)
                        else:
                            word = visual.TextStim(win,text = word,color = win_text_col,pos = clue_pos)

                        word.draw()

                        timetodraw = fixa1_onset + fixa_list[fixa_num] + clue_time + task_instr_time + word_time * word_index

                        event.clearEvents()

                        while core.monotonicClock.getTime() < (timetodraw - (1/120.0)):
                            pass

                        word_onset = win.flip()

                        keys = event.waitKeys(maxWait = word_time-0.05,keyList=['1','2'],timeStamped = True)

                        word.draw()
                        win.flip()

                        if type(keys) is list:
                            trial['press_word'] = sen_list[word_index]
                            trial['KeyPress'] = keys[0][0]
                            trial['RT'] = keys[0][1] - word_onset
                            trial['correct'] = 'True'
                            trial['press_word_offset'] = keys[0][1] - run_onset

                            word.draw()
                            win.flip()

                        words_onset.append(word_onset)

                    

                else:
                    for word_index in range(15):
                        word_text = sen_list[word_index]
                        word = visual.TextStim(win,text = word_text,color = win_text_col,pos = clue_pos)
                        word.draw()
                        timetodraw = fixa1_onset + fixa_list[fixa_num] + clue_time + task_instr_time + word_time * word_index
                        while core.monotonicClock.getTime() < (timetodraw - (1/120.0)):
                            pass
                        word_onset = win.flip()
                        words_onset.append(word_onset)
                time.sleep(1)



                resultdict['Timepoint'], resultdict['Time'] = "Reading trial ended", timer.getTime()

                writer.writerow(resultdict)

                resultdict['Timepoint'], resultdict['Time'] = None,None




                # draw ratings for reading and memory recall trials
                if trial['task'] != 'xxxxxxxx':
                    continue
                    # draw fixation between sentences and ratings and flip the window
                    fixa.draw()
                    timetodraw = fixa1_onset + fixa_list[fixa_num] + clue_time + task_instr_time + sen_time
                    while core.monotonicClock.getTime() < (timetodraw - (1/120.0)):
                        pass
                    fixa2_onset = win.flip()

                    trial['fixa2_onset'] = fixa2_onset - run_onset
                    trial['fixa2_durat'] = fixa_list[fixa_num+1]

                    # draw first question for rating and save it 
                    ratingScale = visual.RatingScale(win, maxTime = 4, low = 1, high = 7, markerStart=4, tickMarks = [1,2,3,4,5,6,7], textColor='Black', leftKeys='1', rightKeys = '2', acceptPreText='Please select your rating', acceptKeys= '4', acceptText='accept?', acceptSize = 2.0, marker='slider', stretch=2,scale = None)#,tickHeight=1.5)

                    timetodraw = fixa1_onset + fixa_list[fixa_num] + clue_time + task_instr_time + sen_time + fixa_list[fixa_num+1]
                    while core.monotonicClock.getTime() < (timetodraw - (1/120.0)):
                        pass
                    question1_onset = core.monotonicClock.getTime()
                    # present the rating scale:
                    while ratingScale.noResponse:
                        Rating1.draw()
                        ratingScale.draw()
                        question1_offset = win.flip()
                        if event.getKeys(['escape']):
                            core.quit()
                        # a response was made, so save it on each iteration
                    trial['question1_onset'] = question1_onset - run_onset
                    trial['question1_offset'] = question1_offset - run_onset
                    trial['rating1'] = ratingScale.getRating()
                    trial['rating1_RT'] = ratingScale.getRT()    
                    # reset the scale to its original state for the next iteration:
                    ratingScale.reset()

                    # draw second question for rating and save it 
                    timetodraw = fixa1_onset + fixa_list[fixa_num] + clue_time + task_instr_time + sen_time + fixa_list[fixa_num +1] + question_duration
                    while core.monotonicClock.getTime() < (timetodraw - (1/120.0)):
                        pass
                    question2_onset = core.monotonicClock.getTime()
                    # present the rating scale:
                    while ratingScale.noResponse:
                        Rating2.draw()
                        ratingScale.draw()
                        question2_offset = win.flip()
                        if event.getKeys(['escape']):
                            core.quit()
                        # a response was made, so save it on each iteration
                    trial['question2_onset'] = question2_onset - run_onset
                    trial['question2_offset'] = question2_offset - run_onset
                    trial['rating2'] = ratingScale.getRating()
                    trial['rating2_RT'] = ratingScale.getRT()
                    # reset the scale to its original state for the next iteration:
                    ratingScale.reset()

                    # draw third question for rating and save it 
                    timetodraw = fixa1_onset + fixa_list[fixa_num] + clue_time + task_instr_time + sen_time + fixa_list[fixa_num +1] + question_duration*2
                    while core.monotonicClock.getTime() < (timetodraw - (1/120.0)):
                        pass
                    question3_onset = core.monotonicClock.getTime()
                    # present the rating scale:
                    while ratingScale.noResponse:
                        Rating3.draw()
                        ratingScale.draw()
                        question3_offset = win.flip()
                        if event.getKeys(['escape']):
                            core.quit()
                        # a response was made, so save it on each iteration
                    trial['question3_onset'] = question3_onset - run_onset
                    trial['question3_offset'] = question3_offset - run_onset
                    trial['rating3'] = ratingScale.getRating()
                    trial['rating3_RT'] = ratingScale.getRT()
                    # reset the scale to its original state for the next iteration:
        #            ratingScale.reset()

                    #write_trial(filename,headers,trial) 
                trial['trial_pres_num'] = trial_pres_num
                trial['fixa1_onset'] = fixa1_onset - run_onset
                trial['fixa1_durat']= fixa_list[fixa_num]
                #trial['clue_onset'] = clue_onset - run_onset
                trial['clue_durat'] = clue_time
                #trial['task_onset'] = task_onset - run_onset
                trial['task_durat'] = task_instr_time
                trial['word_time'] = word_time
                trial['word1_onset'] = words_onset[0] - run_onset
                trial['word2_onset'] = words_onset[1] - run_onset
                trial['word3_onset'] = words_onset[2] - run_onset
                trial['word4_onset'] = words_onset[3] - run_onset
                trial['word5_onset'] = words_onset[4] - run_onset
                trial['word6_onset'] = words_onset[5] - run_onset
                trial['word7_onset'] = words_onset[6] - run_onset
                trial['word8_onset'] = words_onset[7] - run_onset
                trial['word9_onset'] = words_onset[8] - run_onset
                trial['word10_onset'] = words_onset[9] - run_onset
                trial['word11_onset'] = words_onset[10] - run_onset
                trial['word12_onset'] = words_onset[11] - run_onset
                trial['word13_onset'] = words_onset[12] - run_onset
                trial['word14_onset'] = words_onset[13] - run_onset
                trial['word15_onset'] = words_onset[14] - run_onset

                trial_pres_num +=1 # the number-th presentnted trial
                #write_trial(filename,headers,trial)     # calls the function that writes csv output

                if trial['task'] != 'xxxxxxxx':
                    fixa_num+=2 # the number-th fixation
                else:
                    fixa_num+=1 # the number-th fixation

                if trial['task'] != 'xxxxxxxx':
                    rating_num += 1 # the number of rating time

    # -----------------------------------------------------------------------------------------------------------------------------------------------
    # call the functions defined
    # get the current directory
    curr_dic = get_pwd()

    # make a directory – data to store the generated data
    #makedir(data_folder)
    expInfo={}
    expInfo['expname'] =expName
        # Create a string version of the current year/month/day hour/minute
    expInfo['expdate']=datetime.now().strftime('%Y%m%d_%H%M')
    expInfo['subjID']='a'
    expInfo['subjName']='b'
    expInfo['run']=''
    # record subjects info and create a csv file with the info about subjects
    filename, stimuli_file, fixa_file = 'testdataread.csv', dfile ,os.path.dirname(os.path.abspath(__file__))+ "//resources//Reading_Task//sem_fixa_run.csv"

    # if the data does not exist, create one, otherwise,  rename one –filename-repeat-n
    #write_file_not_exist(filename)

    # set up the window to display the instruction
    #win = set_up_window()

    # read the instruction
    # instruct()

    # generate the jitter list for the fixation and probe
    # know the number of trials
    trials, fieldnames = load_conditions_dict(stimuli_file)
    trials_num = len(trials)

    fixa_list,total_fixa_time = read_fix_from_csv(fixa_file)


    # sets a local clock that will be used to store timing information synced with the scanner
    
      

    # run the stimuli
    run_stimuli(stimuli_file,fixa_list, expClock, resultdict, writer)

    # end of the experiment
    #end_onset = end_exp()

    #print ('end onset',end_onset)



    # Experiment()   



    
    
# Experiment()   
