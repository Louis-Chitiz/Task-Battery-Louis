#This file was created by Louis Chitiz with edits from Ian Goodall-Halliwell.
from psychopy import visual, core, monitors, event, sound, gui, logging
import os
import time
import csv
import sys, os, errno # to get file system encoding (used in setDir())
import numpy as np
import random
from collections import OrderedDict
import pandas as pd


#Change this to the path where you store the stimuli folders for the 2-back
PATH = "taskScripts/resources/TwoBack_Task/blocks/"
STIMPATH = "taskScripts/resources/TwoBack_Task/WM Stimuli/"
#This is a list of pre-generated blocks. See the block_generator scripts for how I created them.
BLOCKS = ['faces_B','scenes_B']

def runexp1(timer, win, writer, resultdict, data, runtime,dataver):
    stimuli_file = data

    expr_time = 2 # formal experiment, it is 1.45
    choi_time = 2  # formal experiment, it is 1.45
    blank_time = 0.1   # display a blank screen
    timelimit_deci = 2 # equal to the choi_time 1.45 (check)
    trial_time = expr_time + choi_time + blank_time  # each trial is 3s

    pretrialFixDur = 15.00;  # in seconds previous four fixation is 15s
    posttrialFixDur = 16.00; # in seconds the final fixation is 16s

    instru_key     = ['return','escape']
    choie_key_list = ['left','right','escape']  # 1 == left, 2 == right

    # window related
    # windows
    # assign the monitor name
    monitor_name = 'HP ProOne 600'

    # instruction, position height
    word_pos = (0,0.3)
    choice_left_pos =(-0.5,-0.5)
    choice_right_pos =(0.5,-0.5)

    ### define functions

    #write to resultdict
    def resultdictWriter(timepoint,timer,writer, iscorrect=None):
        
        #print(dataver)
        resultdict['Timepoint'], resultdict['Time'], resultdict['Is_correct'],resultdict["Auxillary Data"] = timepoint, timer.getTime(), iscorrect,dataver
        writer.writerow(resultdict)
        resultdict['Timepoint'], resultdict['Time'],resultdict["Auxillary Data"] = None,None,None

    # get the current directory of this script - correct
    def get_pwd():
        global curr_dic
        curr_dic = os.path.dirname(sys.argv[0])  # U:/task_fMRI_Experiment/exp_March
        return curr_dic

    def shutdown ():
        win.close()
        core.quit()

    # Open a csv file, read through from the first row   # correct
    def load_conditions_dict(conditionfile):

    #load each row as a dictionary with the headers as the keys
    #save the headers in its original order for data saving

    # csv.DictReader(f,fieldnames = None): create an object that operates like a regular reader 
    # but maps the information in each row to an OrderedDict whose keys
    # are given by the optional fieldnames parameter.

        with open(os.path.join(os.getcwd(), conditionfile)) as csvfile:
            reader = csv.DictReader(csvfile)
            trials = []

            for row in reader:
                trials.append(row)
        
        # save field names as a list in order
            fieldnames = reader.fieldnames  # filenames is the first row, which used as keys of trials

        return trials, fieldnames   # trial is a list, each element is a key-value pair. Key is the 
                                    # header of that column and value is the corresponding value               


    # set up the window
    # fullscr: better timing can be achieved in full-screen mode
    # allowGUI: if set to False, window will be drawn with no frame and no buttons to close etc...

    def set_up_window(window=win): 
        mon = monitors.Monitor(monitor_name)
        mon.setDistance (114)
        win = window
        win.mouseVisible = False
        return win

    # prepare the content on the screen
    # removed height from function
    def prep_cont(line, pos):
        line_text = visual.TextStim(win, line, color='black', pos=pos, bold=True)
        return line_text

    # prepares the image stimulus for the trial to be displayed
    def prep_image(imgfldr, image, pos, path=STIMPATH):
        #path is the folder containing the stimuli for the task,
        #imagefolder is the folder containing the stimuli from the block,
        #image is the name of the exact stimulus being presented.
        imstim = visual.ImageStim(win,image = os.path.join(path,imgfldr,image), pos=pos)
        return imstim 
        
    # display each trial on the screen at the appropriate time
    def run_stimuli(stimuli_file, runtime):
        # read the stimuli  # re-define, not use numbers, but use keywords
            
        all_trials, headers = load_conditions_dict(conditionfile=stimuli_file)
        headers += ['i_trial_onset','trial_onset','choice_onset','blank_r_onset', 'RT', 'correct','KeyPress']   
        
        # prepare fixation and blank screen for drawing
        fixa = prep_cont('+',word_pos)
        blank = prep_cont(' ',word_pos)

        #prepare trial choices for drawing
        choice_l = prep_cont('SAME AS 2-BACK', choice_left_pos)
        choice_r = prep_cont('NOT SAME AS 2-BACK', choice_right_pos)
    
        # write the fixation time into the fixation.csv file    
        fixa_numth = 1  
        blockfixa_onset_abs = 0
        #f.write('%f,%.2f\n'% (fixa_numth, blockfixa_onset_abs))
        # draw the first long fixation and flip the window 

        fixa.draw()
        resultdictWriter('fixation cross', timer,writer)
        timetodraw = core.monotonicClock.getTime()
        #        
        while core.monotonicClock.getTime() < (timetodraw - (1/120.0)):
            pass
        
        run_onset = win.flip()  # this is when the real experiment starts and the run starts
        
        
        timetodraw = run_onset + pretrialFixDur
        # while core.monotonicClock.getTime() < (timetodraw - (1/120.0)):
        #     pass
        
        count = 1 # initiaze count
        curtime = core.Clock()
        for trial in all_trials:
            fixa.draw()
            win.flip()
            time.sleep(2)
            if curtime.getTime() < runtime:
                
                #''' trial is a ordered dictionary. The key is the first raw of the stimuli csv file'''
                expression = prep_image(trial['stimulus type'],trial['image'],word_pos)
                # choice = prep_cont(trial['choice'][0:4],choice_right_pos)
                # choice_right = prep_cont(trial['choice'][len(trial['choice'])-4::],choice_left_pos)

                # display stimulus and choices - the start of a new trial
                expression.draw()
                choice_l.draw()
                choice_r.draw()
                resultdictWriter('2-back Trial Start',timer,writer)
                resultdictWriter('Choice presented',timer,writer)
                # ideal_trial_onset = float( pretrialFixDur) +float(run_onset) + float( trial['expr_onset'])
                # timetodraw = ideal_trial_onset
                # while core.monotonicClock.getTime() < (timetodraw - (1/120.0)):
                #     pass
                trial_onset = win.flip()  # when expression is displayed, this is the trial onset
                timetodraw = trial_onset + expr_time
                # while core.monotonicClock.getTime() < (timetodraw - (1/120.0)):
                #         pass
                event.clearEvents()
                #choice_onset = win.flip()
                keys = event.waitKeys(maxWait = timelimit_deci, keyList =['left','right'],timeStamped = True)
                fixa.draw()
                win.flip()
                resultdictWriter('Choice made',timer,writer)
                
                
                # display choice and ask subjects to press the button 1 or 2


                # If subjects do not press the key within maxwait time, RT is the timilimit and key is none and it is false
                if keys is None:
                    RT = 'None'
                    keypress = 'None'
                    correct = 'False'

            # If subjects press the key, record which key is pressed, RT and whether it is right
                elif type(keys) is list:
                    if keys[0][0]=='escape':
                        shutdown()
                    
                    else:
                        keypress = keys[0][0]
                        RT = keys[0][1] - trial_onset  
                        if trial["correct_ans"] == '1':
                            trial["correct_ans"] = 'left'
                        if trial["correct_ans"] == '2':
                            trial["correct_ans"] = 'right'
                        correct = (keys[0][0]==trial['correct_ans']) 
                        trial['RT']=RT
                        trial['correct'] = correct
                        trial['KeyPress'] = keypress
                        
                        #resultdictWriter('2-back Trial End',timer,writer, correct)

            
                # trial['i_trial_onset'] = float( pretrialFixDur) + float( trial['expr_onset'])
                trial['trial_onset']   = trial_onset - run_onset
                #trial['choice_onset']  = choice_onset - run_onset
                trial['RT'] = RT
                trial['correct'] = correct
                trial['KeyPress'] = keypress

                resultdictWriter('2-back Trial End',timer,writer, correct)
        
                count+=1 # the number-th trials that are displaying
            else:
                return

    # -----------------------------------------------------------------------------------------------------------------------------------------------
    # call the functions defined
    # get the current directory
    curr_dic = get_pwd()

    # set up the window to display the instruction
    win = set_up_window()

    # read the instruction
    #instruct()

    # generate the jitter list for the fixation and probe
    # know the number of trials
    #trials, fieldnames = load_conditions_dict(stimuli_file)

    text_inst = visual.TextStim(win=win, name='text_4',
        text='You may now stop.',
        font='Open Sans',
        pos=(0, 0), height=0.1, wrapWidth=None, ori=0.0, 
        color='black', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    # show the instruction
    # instruct(curr_dic,instruct_figure)
    with open("taskScripts/resources/TwoBack_Task/instr1.txt") as f:
        lines1 = f.read()
    with open("taskScripts/resources/TwoBack_Task/instr2.txt") as f:
        lines2 = f.read()
    with open("taskScripts/resources/TwoBack_Task/instr3.txt") as f:
        lines3 = f.read()
        
        for i, cur in enumerate([lines1,lines2,lines3]):
            text_inst.setText(cur)
            text_inst.draw()
            win.flip()
            event.waitKeys(keyList=['return'])

    resultdictWriter('2-back Task Start',timer,writer)


    # run the stimuli
    run_stimuli(stimuli_file, runtime)

    ## end of the experiment
    #end_exp()
    resultdictWriter('2-back Task End',timer,writer)

def runexp(filename, timer, win, writer, resdict, runtime,dfile, seed):
    #print()
    writer = writer[0]
    random.seed(a=seed)
    if dfile.split("_")[-1].split(".")[0] == "0":
        blocktype = "scenes_A"
    elif dfile.split("_")[-1].split(".")[0] == "1":
        blocktype = "scenes_B"
    # else:
    #     print("else")
        
    #     blocktype = random.choice(BLOCKS)
    cwd = os.getcwd()
    block = random.choice(os.listdir(os.path.join(PATH,blocktype)))
    data = os.path.join(PATH, blocktype, block)
    dataver = data.split("/")[-1].split("_")[0]
    #resultdict = {'Timepoint': None, 'Time': None, 'Is_correct': None, 'Experience Sampling Question': None, 'Experience Sampling Response':None, 'Task' : None, 'Task Iteration': None, 'Participant ID': None,'Response_Key':None, 'Auxillary Data': None}
    #timer = core.Clock()
    runexp1(timer, win, writer, resdict,  data, runtime,dataver)
    return dataver