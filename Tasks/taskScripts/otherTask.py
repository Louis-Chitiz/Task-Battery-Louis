# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 11:47:22 2019

"""
from genericpath import exists
import os
import sys
import random
from psychopy import core, event, logging, visual, data
import time
import codecs
import csv
import re
import numpy as np
import winsound

#from src.library import *
#instr_txt = './instructions/exp_instr.txt'  # instruction: start of experiment
instr_path = './instructions/'  # path for instructions
instr_name = '_instr.txt' # filename (preceded by subtask name) for instructions
begin_name = 'begin_instr.txt' # beginning text, if no instruction is needed for second run
ready_name = 'wait_trigger.txt' # instruction: wait trigger screen
exp_end_name = 'taskend_instr.txt' # instruction: wait trigger screen
ESQ_name = 'ESQ_instr.txt'
end_name = 'end_instr.txt'
trial_setup_path = './resources/' # path for trial setup
fixed_ESQ_name = './resources/ESQ/ESQ_Questions.csv'

def quitEXP(endExpNow):
    if endExpNow:
        
        core.quit()

def get_keyboard(timer, respkeylist, keyans):
    '''
    Get key board response
    '''
    Resp = None
    KeyResp = None
    KeyPressTime = np.nan
    keylist = ['escape'] + respkeylist

    for key, time in event.getKeys(keyList=keylist, timeStamped=timer):
        if key in ['escape']:
            quitEXP(True)
        else:
            KeyResp, KeyPressTime = key, time
    # get what the key press means
    if KeyResp:
        Resp = keyans[respkeylist.index(KeyResp)]
    return KeyResp, Resp, KeyPressTime


def Get_Response(clock, duration, respkeylist, keyans, beepflag):
    
    respRT = np.nan
    KeyResp = None
    Resp = None
    KeyPressTime = np.nan

    event.clearEvents() # clear the keyboard buffer
    #myclock = core.Clock() # start a clock for this response trial
    resp_start  = clock.getTime()

    while KeyResp is None and (clock.getTime() <= resp_start + duration):
        
        # get key press and then disappear
        KeyResp, Resp, KeyPressTime = get_keyboard(
            clock, respkeylist, keyans)

    # get reaction time and key press
    if not np.isnan(KeyPressTime):
        respRT = KeyPressTime - resp_start
    else:
        KeyResp, Resp = 'None', 'None'
        if beepflag == 0:
            winsound.Beep(1000, 100)  # make a beep if no response is made
    
    return resp_start, KeyResp, Resp, KeyPressTime, respRT

class Display_Image_act(object):
    '''
    show image in the screen at x,y
    '''
    def __init__(self, window, image, pos_x, pos_y):
        '''Initialize a text stimulus.
        Args:
        window - The window object
        image - image to display
        size - attributes of the image
        pos_x, pos_y - x,y position, 0,0 is the centre
        '''
        self.window = window
        #self.window = image
        self.display = visual.ImageStim(self.window, image=image,
#                size=[size_x, size_y], 
                pos=[pos_x, pos_y]
                ) #object to display instructions

    def show(self, clock):
        self.display.draw()
        self.window.flip()
        start_trial = clock.getTime()

        return start_trial

class Display_Text(object):
    '''
    show text in the screen at x,y
    '''
    def __init__(self, window, text, size, color, font, pos_x, pos_y):
        '''Initialize a text stimulus.
        Args:
        window - The window object
        text - text to display
        size, color, font - attributes of the text
        pos_x, pos_y - x,y position, 0,0 is the centre
        '''
        self.window = window
        self.text = text
        self.display = visual.TextStim(
                window, text=text, font=font,
                #name='instruction',
                pos=[pos_x, pos_y],  wrapWidth=1100,
                color='black'
                ) #object to display instructions

    def show(self, clock):
        self.display.draw()
        self.window.flip()
        start_trial = clock.getTime()

        return start_trial

def parse_instructions(input_data):
    '''
    parse instruction into pages
    page break is #
    '''

    text = re.findall(r'([^#]+)', input_data) # match any chars except for #

    return text

def load_instruction(PATH):
    '''
    load and then parse instrucition
    return a list
    '''

    PATH = ("./resources/Self_Task/Self_instr.txt")
    with codecs.open(PATH, 'r', encoding='utf8') as f:
        input_data = f.read()

    text = parse_instructions(input_data)

    return text


class my_instructions(object):
    '''
    show instruction and wait for trigger
    '''
    def __init__(self, window, settings, instruction_txt, ready_txt, instruction_size, instruction_font, instruction_color, parseflag,writer,resdict, timer):
        self.window = window
        self.writer = writer
        self.settings = settings
        self.resdict = resdict
        self.timer = timer
        self.env = settings['env']
        #self.instruction_txt = load_instruction(instruction_txt)
        #self.ready_txt = load_instruction(ready_txt)[0]
        self.display = visual.TextStim(
                window, text='default text', font=instruction_font,
                name='instruction', color='black')#,
                #pos=[-50,0], height=instruction_size, wrapWidth=1100)
                #color=instruction_color
                #) #object to display instructions
        self.parseflag = parseflag

    def parse_inst(self):

        

        return self.instruction_txt

    def showf(self):
        try:
            with open(os.path.join(os.getcwd(),"taskScripts/resources/Other_Task/Other_instr1.txt")) as f:
                lines1 = f.read()
            with open(os.path.join(os.getcwd(),"taskScripts/resources/Other_Task/Other_instr2.txt")) as f:
                lines2 = f.read()
            with open(os.path.join(os.getcwd(),"taskScripts/resources/Other_Task/Other_instr3.txt")) as f:
                lines3 = f.read()
        except:
            with open(os.path.join(os.getcwd(),"resources/Other_Task/Other_instr1.txt")) as f:
                lines1 = f.read()
            with open(os.path.join(os.getcwd(),"resources/Other_Task/Other_instr2.txt")) as f:
                lines2 = f.read()
            with open(os.path.join(os.getcwd(),"resources/Other_Task/Other_instr3.txt")) as f:
                lines3 = f.read()
        
        for i, cur in enumerate([lines1,lines2,lines3]):
            self.display.setText(cur)
            self.display.draw()
            self.window.flip()
            event.waitKeys(keyList=['return'])

        
        # substitue keys in the instruction text before displaying the instruction        
   
        

        self.resdict['Timepoint'] = "Self_Task_Start"
        self.resdict['Time'] = self.timer.getTime()
        
        self.writer.writerow(self.resdict)
        self.resdict['Timepoint'], self.resdict['Time'], self.resdict['Response_Key'] = None, None, None 

    def waitTrigger(self, trigger_code):
        # wait for trigger in mri environment
        self.display.setText(self.ready_txt)
        self.display.draw()
        self.window.flip()

        if self.env == 'lab':
            core.wait(0)
        elif self.env == 'mri':
            event.waitKeys(keyList=[trigger_code])
        else: # not supported
            raise Exception('Unknown environment setting')

def load_trials(infile):
    '''
    load each row as a dictionary with the headers as the keys
    save the headers in its original order for data saving
    '''
    
    
    with codecs.open(infile, 'r', encoding='utf8') as f:
        reader = csv.DictReader(f)
        trials = []

        for enum, row in enumerate(reader):
            trials.append(row)

        # save field names as a list in order
        fieldnames = reader.fieldnames

    return trials, fieldnames


def get_trial_generator(subtask, version, run_no):
#def get_trial_generator(subtask, version):
    '''
    get the list of parameters (stimuli) from the .csv 
    '''
    
    trial_path = trial_setup_path + subtask + '_' + version + str(run_no) + '.csv'   
    trialpool, trialhead = load_trials(trial_path)
    
#    if ESQuestion == 'ES':
#        question2, _ = load_conditions_dict(random_ESQ_name)       
        #exp_sample_generator = stimulus_ExpSample(question2)
#        question1, _ = load_conditions_dict(fixed_ESQ_name)
#        questions = question1 + question2
    
    return trialpool, trialhead

def get_settings(env, ver):
    '''Return a dictionary of settings based on
    the specified environment, given by the parameter
    env. Can also specify whether or not to use testing settings.

    Include keypress counter balancing
    '''
    BASE = {
    'test': False,
    'mouse_visible': False,
#    'logging_level': logging.INFO
    'logging_level': logging.ERROR,
    }

    # Laboratory setting
    LAB = {
        'env': 'lab',  # Enviroment name
        #'window_size': 'full_screen',
        #'window_size': (1280, 720),
        'window_size': 'full_screen',
        'input_method': 'keyboard'
        }

    MRI = {
        'env': 'mri',
        'window_size': 'full_screen',
        'input_method': 'serial',
    }

    # experiment specific vesion related setting
    VER_A = {
            'txt_color': 'black',
            'rec_keys': ['left', 'right'],
            'rec_keyans': ['Yes', 'No'],
            }

    VER_B = {
            'txt_color': 'black',
            'rec_keys': ['left', 'right'],
            'rec_keyans': ['Yes', 'No'],
            }

    VER_A_MRI = {
                'rec_keys': ['1', '2'],
                'loc_keys': ['6', '7']
                }

    VER_B_MRI = {
                'rec_keys': ['6', '7'],
                'loc_keys': ['1', '2']
                }
    # Start with the base settings
    settings = BASE


    if env == 'lab':
        settings.update(LAB)

        # display and key press counter balancing
        if ver == 'A':
            settings.update(VER_A)
        elif ver == 'B':
            settings.update(VER_B)
        else:
            raise ValueError('Version "{0}" not supported.'.format(ver))

    elif env == 'mri':
        settings.update(MRI)
        # display and key press counter balancing
        if ver == 'A':
            settings.update(VER_A_MRI)
        elif ver == 'B':
            settings.update(VER_B_MRI)
        else:
            raise ValueError('Version "{0}" not supported.'.format(ver))

    else:
        raise ValueError('Environment "{0}" not supported.'.format(env))


    return settings




def run_experiment(timer, win, writer, resdict, runtime, dfiles):
    
    ##########################################
    # collect participant info
    ##########################################
    #experiment_info = subject_info()

    ##########################################
    # Setup
    ##########################################
    #
    # set up enviroment variables and generators
    settings = get_settings(
                    env='lab',
                    ver='A')
    
    ####################
    ### ************ ###
    # programmatically change the number for stimuli for go-nogo task
    ####################
    #if experiment_info['Subtask'] in ['Go', 'NoGo']:
    trial_parameter['num_stim'] = 1
    trial_parameter['beep_flag'] = 1
    #del settings['rec_keys'][1]
    #del settings['rec_keyans'][1]
    settings['rec_keyans'][0] = 'Go'
    Stim_min[0] = 3000
    Stim_max[0] = 5000
    ISI_min[0] = 500
    ISI_max[0] = 500
    ISI_step[0] = 500
    ####################
    ### ****end***** ###
    ####################
    
    # set up the trial conditions
    #trials, headers=get_trial_generator("You", 'A', 1)
    trials, headers = load_trials(dfiles)
    # setup the trial header, used for logging info
    temp = list(trials[1].items())
    mycount = 0
    for i in range (0, len(headers)):
        if temp[i][1] != 'NA':
            trial_output[headers[i]]=temp[mycount][1]
        mycount += 1
    trial_output_headers = list(trial_output.keys()) + list(trial_response.keys())
    
    
    # set log file
    #logloc = 'rando.csv'
    #event_logger(settings['logging_level'], logloc)

    # create experiment 
    #Experiment = Paradigm(escape_key='esc', color=0
    #                      )#window_size=settings['window_size'])
    #win = visual.Window(allowGUI=True, units='pix')
    # hide mouse
    event.Mouse(visible=False)

    ##########################################
    # Set & display instructions
    ##########################################
    # display instruction for first run
    myparse=0
    #if experiment_info['Run'] == '1':
    instr_txt = instr_path + 'Friend' + instr_name
    myparse=1
    # skip instruction in other runs (just press return)
    #else:
        #instr_txt = instr_path + begin_name
    ready_txt = instr_path + ready_name
    instructions_run = my_instructions(
        window=win, settings=settings,
        instruction_txt=instr_txt, ready_txt=ready_txt, 
        instruction_size=instruction_parameter['inst_size'], instruction_font=instruction_parameter['inst_font'],
        instruction_color='black', parseflag=myparse, writer=writer, resdict=resdict, timer=timer)

#    if experiment_info['Run'] == '1':
    instructions_run.showf()
    win.flip()
    trialtimer = core.Clock()
    trialtimer.reset()
#    else:
#        pass

    
    # setup the fixation cross, assume to be displayed at the same position at the origin 
    fixation = Display_Text(window=win, text=trial_parameter['IS'], 
                            size=trial_parameter['IS_size'], color=trial_parameter['IS_color'], 
                            font=trial_parameter['IS_font'], pos_x=0, pos_y=0)
    #exp_end_txt = instr_path + exp_end_name
    #exp_end_msg = my_instructions(
        #window=win, settings=settings,
        #instruction_txt=exp_end_txt, ready_txt=ready_txt, 
        #instruction_size=instruction_parameter['inst_size'], instruction_font=instruction_parameter['inst_font'],
        #instruction_color=instruction_parameter['inst_color'], parseflag=0)

#    exp_end_txt = load_instruction(instr_path + exp_end_name)
#    exp_end_msg = visual.TextStim(win, text=exp_end_txt, font=instruction_parameter['inst_font'],
#                              name='instruction', pos=[-50,0], 
#                              height=instruction_parameter['inst_size'], wrapWidth=1100,
#                              color=instruction_parameter['inst_color'])    


#     ##########################################
#     # Running the experiment
#     ##########################################

    # wait trigger if this this in MRI environment (checked inside the function)
    
    trial_parameter['num_stim'] = 2

    for trialcount in range(0, len(trials)):
 #   for trialcount in range(0, 1):

        for i in range (0, len(trial_output_headers)):
            if trial_output_headers[i] not in list(trial_response.keys()):
                trial_output[trial_output_headers[i]]=trials[trialcount][trial_output_headers[i]]

        trial_response['trialstart_time'] = timer.getTime()
#        print(trialcount, trials[trialcount]['Trial_No'], trials[trialcount]['Type'])
        # get current trial from trials read from file
        trial_stim = [trials[trialcount]['Stim1']]
        trial_stim_F1 = [trials[trialcount]['Stim1_F1']]
        trial_stim_F2 = [trials[trialcount]['Stim1_F2']]
        if trial_parameter['num_stim'] > 1:
            trial_stim = trial_stim + [trials[trialcount]['Stim2']]
            trial_stim_F1 = trial_stim_F1 + [trials[trialcount]['Stim2_F1']]
            trial_stim_F2 = trial_stim_F2 + [trials[trialcount]['Stim2_F2']]
        if trial_parameter['num_stim'] > 2:
            trial_stim = trial_stim + [trials[trialcount]['Stim3']]
            trial_stim_F1 = trial_stim_F1 + [trials[trialcount]['Stim3_F1']]
            trial_stim_F2 = trial_stim_F2 + [trials[trialcount]['Stim3_F2']]
        if trial_parameter['num_stim'] > 3:
            trial_stim = trial_stim + [trials[trialcount]['Stim4']]
            trial_stim_F1 = trial_stim_F1 + [trials[trialcount]['Stim4_F1']]
            trial_stim_F2 = trial_stim_F2 + [trials[trialcount]['Stim4_F2']]
            

        
        # display 1-4 stimuli in defined in the current trial
        for stimcount in range(0, trial_parameter['num_stim']):
                       
            #######################################################
            # display fixation - before stim (skip if this is set to 0)
            if ISI_min[stimcount] != 0: # not to display IS if ISI_min is set to 0
                mytime = fixation.show(timer)
                if ISI_min[stimcount] == ISI_max[stimcount]:
                    myduration=ISI_min[stimcount]
                else:
                    myduration=random.randrange(ISI_min[stimcount], ISI_max[stimcount]+1, ISI_step[stimcount])
                core.wait(myduration/1000)

            #######################################################
            # set the current stimulus positions, x, y defined by F1[0], and text feature defined by F1[1]
            mytext=trial_stim[stimcount]
            mypos_x = 0;
            mypos_y = 0;
            for i in range (0, len(trial_stim_F1[stimcount])):
                if i == 0:  # set position
                    if trial_stim_F1[stimcount][i] == 'L':
                        mypos_x = mypos_x - trial_parameter['pos_x_gap']
                    elif trial_stim_F1[stimcount][i] == 'R':
                        mypos_x = mypos_x + trial_parameter['pos_x_gap']
                    if trial_stim_F1[stimcount][i] == 'B':
                        mypos_y = mypos_y - trial_parameter['pos_y_gap']
                    elif trial_stim_F1[stimcount][i] == 'T':
                        mypos_y = mypos_y + trial_parameter['pos_y_gap']
                elif i == 1 or i == 2:    # set text characteristics
                    if trial_stim_F1[stimcount][i] == 'U':
                        mytext = trial_stim[stimcount].upper()
                    elif trial_stim_F1[stimcount][i] == 'L':
                        mytext = trial_stim[stimcount].lower()
                    elif trial_stim_F1[stimcount][i] == 'S':
                        mytext = list(trial_stim[stimcount])
                        random.shuffle(mytext)
                        mytext = ''.join(mytext)
                    

            #######################################################
            # setup the current stimulus for display, text or image

            if trial_parameter['Stim_Image_Type'] in trial_stim[stimcount]:  # for image display
#                trial_parameter['StimImage_size_x'], size_y=trial_parameter['StimImage_size_y'] = cv.GetSize(trial_stim[stimcount])
                cur_stim = Display_Image_act(window=win, image=trial_stim[stimcount], 
#                                          size_x=trial_parameter['StimImage_size_x'], size_y=trial_parameter['StimImage_size_y'], 
                                          pos_x=mypos_x, pos_y=mypos_y)
            else:
                cur_stim = Display_Text(window=win, text=mytext, 
                                        size=trial_parameter['StimTxt_size'], color=trial_parameter['StimTxt_color'], 
                                        font=trial_parameter['StimTxt_font'], pos_x=mypos_x, pos_y=mypos_y)
                cur_stimL = visual.TextStim(win=win,text='No', pos=(-.8,0), color='black')
                cur_stimR = visual.TextStim(win=win,text='Yes', pos=(.8,0), color='black')
            #######################################################
            # display the current stimulus-text 
            if Stim_min[stimcount] == 9999:    # not to display yet (if 999), wait read the next stimuli first (need more codings)
                print('Do nothing now')
            else:
                
                if trialtimer.getTime() >= runtime:
                    
                    if stimcount == 0:
                        return
                mytime = cur_stim.show(timer)

                # calculate the duration time
                if Stim_min[stimcount] == Stim_max[stimcount] or Stim_step[stimcount] == 0:
                    myduration=Stim_min[stimcount]
                    if stimcount == 1:
                        resdict['Timepoint'] = str("Start_of_" + trial_stim[1])
                        resdict['Time'] = mytime
                        writer.writerow(resdict) 
                        resdict['Timepoint'], resdict['Time'] = None, None
                    
                else:
                    myduration=random.randrange(Stim_min[stimcount], Stim_max[stimcount]+1, Stim_step[stimcount])
                
                # if this is the last trial, wait for key press OR when duration for this stim lapses
                if stimcount == trial_parameter['num_stim'] -1:
                    cur_stimL.setAutoDraw(True)
                    cur_stimR.setAutoDraw(True)
                    cur_stim.show(timer)
                    trial_response['keystart_time'], trial_response['resp_key'], trial_response['response'], trial_response['keypress_time'], trial_response['key_RT'] = Get_Response(timer, myduration/1000, settings['rec_keys'], settings['rec_keyans'], trial_parameter['beep_flag'])
                    if trial_parameter['resp_stay'] == 0:  # stay until duration
                        cur_stimL.setAutoDraw(False)
                        cur_stimR.setAutoDraw(False)
                        win.flip()  # clear the window
                        #core.wait(myduration/1000 - trial_response['key_RT']) # wait for duration
                    
                    for i in range(0, len(list(trial_response.keys()))):
                        trial_output[list(trial_response.keys())[i]]=list(trial_response.items())[i][1]

                    # write response to data file
                    #write_csv(logloc, trial_output_headers, trial_output)
                    resdict['Timepoint'] = str("End_of_" + trial_stim[1])
                    resdict['Time'] = timer.getTime()
                    resdict['Response_Key'] = trial_response['resp_key']
                    writer.writerow(resdict) 
                    resdict['Timepoint'], resdict['Time'], resdict["Response_Key"] = None, None, None

                # else, it is NOT the last stimuli in trial, wait for presentation of the stimuli
                else:
                    core.wait(myduration/1000) # wait for dura
                    
    
    #write_csv(logloc, trial_output_headers, trial_output)    
    
    ##########################################
    # Finishing the experiment
    ##########################################
        
    # ending message
    #exp_end_msg.show()
#    exp_end_msg.draw()
#    win.flip()
#    event.waitKeys(keyList=['return'])

    logging.flush()
    # change output files to read only
    
    # quit

    ##########################################
    # Running the Experience Sampling Questionnarire
    ##########################################
#     if experiment_info['ESQuestion'] == 'ES':

#         ESQ_txt = instr_path + ESQ_name
#         ESQ_msg = my_instructions(
#                 window=win, settings=settings,
#                 instruction_txt=ESQ_txt, ready_txt=ready_txt, 
#                 instruction_size=instruction_parameter['inst_size'], instruction_font=instruction_parameter['inst_font'],
#                 instruction_color=instruction_parameter['inst_color'], parseflag=0)
#         ESQ_msg.show()
        
#         ES_fixed = data.TrialHandler(nReps = 1, method = 'sequential', trialList = data.importConditions(fixed_ESQ_name), name = 'Questionnaire') 
#         ES_random = data.TrialHandler(nReps = 1, method = 'random', trialList = data.importConditions(random_ESQ_name), name = 'Questionnaire')
        
#         # Note: this is the order of the output header, very specific, just to conform with others
#         ESQ_key = ['Participant_number', 'Questionnaire_startTime', 'Questionnaire_endTime', 'TrialDuration', 'Focus', 'Future', 'Past', 'Self', 'Other', 'Emotion', 'Modality', 'Detailed', 'Deliberate', 'Problem', 'Diversity', 'Intrusive', 'Source', 'Arousal', 'Tense', 'Uncertainty']            
    
#         ratingScale = visual.RatingScale(win, low=1, high=10, markerStart=4.5,
#                 precision=10, tickMarks=[1, 10],
#                 leftKeys='1', rightKeys='2', acceptKeys='4')
#         QuestionText = visual.TextStim(win, color = 'white', text = None , alignHoriz = 'center', alignVert= 'top', height=34)
#         scale_high = visual.TextStim(win, text=None, height=34, wrapWidth=1100, pos=[300,-150],color='white', font=sans)
#         scale_low = visual.TextStim(win, text=None, height=34, wrapWidth=1100, pos=[-300,-150],color='white', font=sans)
#         thisRunDict = {'Participant_number': experiment_info['Subject']}
#         thisRunDict['Questionnaire_startTime'] = 0
    
# #       get each question from Questionnaire:
#         for i in range(0, len(ES_fixed.trialList + ES_random.trialList)):
#             time.sleep(1)
#             if i < len(ES_fixed.trialList):
#                 question = ES_fixed.next()
#             else:
#                 question = ES_random.next()
#             ratingScale.noResponse = True
#             keyState=key.KeyStateHandler()
#             win.winHandle.push_handlers(keyState)

#             pos = ratingScale.markerStart
#             inc=0.1
#             while ratingScale.noResponse:  #key 4 not pressed
#                 if keyState[key._1] is True:
#                     pos -= inc
#                 elif keyState[key._2] is True:
#                     pos += inc
#                 if pos > 9:
#                     pos = 9
#                 elif pos < 0:
#                     pos = 0
            
#                 ratingScale.setMarkerPos(pos)
#                 QuestionText.setText(question['Questions'])
#                 QuestionText.draw()
#                 scale_high.setText(question['Scale_high'])
#                 scale_low.setText(question['Scale_low'])
#                 scale_high.draw()
#                 scale_low.draw()
#                 ratingScale.draw()
#                 win.flip()

#             responded = ratingScale.getRating()
#             thisRunDict[ str(question['Label'] )] = str(responded) 

#         thisRunDict['Questionnaire_endTime'] = 0
#         thisRunDict['TrialDuration'] = thisRunDict['Questionnaire_endTime'] - thisRunDict['Questionnaire_startTime']
#         filename = experiment_info['DataFile'].replace('.csv', 'endQs.csv')
# #        write_csv(filename, thisRunDict.keys(), thisRunDict)
#         write_csv(filename, ESQ_key, thisRunDict)




        # end_txt = instr_path + end_name
        # end_msg = my_instructions(
        #         window=win, settings=settings,
        #         instruction_txt=end_txt, ready_txt=ready_txt, 
        #         instruction_size=instruction_parameter['inst_size'], instruction_font=instruction_parameter['inst_font'],
        #         instruction_color=instruction_parameter['inst_color'], parseflag=0)
        # end_msg.show()

    ##########################################
    # Finishing
    ##########################################

    

    #win.close()
    #core.quit()


def runexp(filename, timer, win, writer, resdict, runtime,dfile,seed):
    writer = writer[0]
    random.seed(a=seed)
    global instruction_parameter
    global trial_output
    global ISI_min
    global ISI_max
    global Stim_max
    global Stim_min
    global trial_parameter
    
    global ISI_step
    global trial_response
    global trigger_code
    global Stim_step
    

   
    # get input for dictionary defining the environment & trials to run
    

    # set dictionary for instructions in running each trial
    instruction_parameter = dict([
            ('inst_size', 34), # size/height of the instruction
            ('inst_color', 'black'), # color of the instruction
            ('inst_font', 'sans'), # color of the instruction
            ])

    # set dictionary for parameters in running each trial
    trial_parameter = dict([
            ('IS', '+'),  # symbol to display durint ISI)
            ('IS_size', 44), # size/height of the fixation
            ('IS_color', 'black'), # color of the fixation
            ('IS_font', 'sans'), # color of the fixation
            ('StimTxt_size', 64), # size/height of the stimulus text
            ('StimTxt_color', 'black'), # color of the stimulus text
            ('StimTxt_font', 'sans'), # color of the stimulus text
            # the following two are not used ... but the actual size, for the moment
            ('StimImage_size_x', 300), # size x of stimulus image
            ('StimImage_size_y', 300), # size x of stimulus image
            ('Stim_Image_Type', '.bmp'), # include those Subtask that show images
            ('pos_x_gap', 400), # gap to add / subtract to make the presentation towards left or Right from origin (0,0)
            ('pos_y_gap', 220), # gap to add / subtract to make the presentation towardsTop or Bottom from origin (0,0)
            ('num_stim', 2), # number of stimulus within one trial.. max=4 ... check if programme below update this
            ('resp_stay', 0), # should the screen stay until after receiving response input, 0=yes, 1=no
            ('beep_flag', 1), # should there be a beep sound if no response is received, 0=yes, 1=no
            ])


    # set the response set for each trial
    trial_response = dict([
            ('trialstart_time', 0),  # trial start time)
            ('keystart_time', 0),  # trial start time)
            ('resp_key', None), # size/height of the fixation
            ('response', 999), # nth response in the response key list, currently set to [yes, no]
            ('keypress_time', 0), # nth response in the response key list, currently set to [0:yes, 1:no]
            ('key_RT', 0), # Reaction Time 
            ])

    # initialize the output for writing to csv
    trial_output = {}

    # set dictionary for min/max/step duration for ISI presented before the each stimuli (max 4) 
    # IMPORTANT -- these are set for ms ... while clock time is in seconds -- remember to divide by 1000
    # Note:  if any of the ISI_min is set to 0, no IS is displayed.
    ISI_min = dict([
            (0, 500), # before stim1
            (1, 500), # before stim2
            (2, 0), # before stim3
            (3, 0), # before stim4
            ])

    ISI_max = dict([
            (0, 500), # before stim1
            (1, 500), # before stim2
            (2, 0), # before stim3
            (3, 0), # before stim4
            ])

    ISI_step = dict([
            (0, 0), # before stim1
            (1, 500), # before stim2
            (2, 0), # before stim3
            (3, 0), # before stim4
            ])

    # set dictionary for min/max/step duration for stimuli presentation (max 4) 
    # not working -- If Stim_min is set to 99999, the current stim is displayed with the upcoming stimuli (meaning 2 stimuli displayed together)
    Stim_min = dict([
            (0, 800), # before stim1
            (1, 5500), # before stim2
            (2, 0), # before stim3
            (3, 0), # before stim4
            ])

    Stim_max = dict([
            (0, 800), # before stim1
            (1, 5500), # before stim2
            (2, 0), # before stim3
            (3, 0), # before stim4
            ])

    Stim_step = dict([
            (0, 0), # before stim1
            (1, 0), # before stim2
            (2, 0), # before stim3
            (3, 0), # before stim4
            ])

    # MRI related settings
    dummy_vol = 0
    tr = 2
    trigger_code = '5'
    
    run_experiment(timer, win, writer, resdict, runtime,dfile)


##########################################
# This is the main programme
##########################################
# now run this thing


