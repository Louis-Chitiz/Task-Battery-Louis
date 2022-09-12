#from src.library import *
import os
import codecs
import sys
import random
from psychopy import core, event, logging, visual, data
import time
import re
from pyglet.window import key

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
    PATH = os.path.dirname(os.path.abspath(__file__)) + "//resources//ESQ//ESQ_instr.txt"
    
    with codecs.open(PATH, 'r', encoding='utf8') as f:
        input_data = f.read()

    text = parse_instructions(input_data)

    return text

class my_instructions(object):
    '''
    show instruction and wait for trigger
    '''
    def __init__(self, window, settings, instruction_txt, ready_txt, instruction_size, instruction_font, instruction_color, parseflag):
        self.window = window
        self.settings = settings
        self.env = settings['env']
        self.instruction_txt = load_instruction(instruction_txt)
        self.ready_txt = load_instruction(ready_txt)[0]
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
        with open('instructions/You_instr.txt') as f:
            lines = f.read()
        instext = lines

        
        # substitue keys in the instruction text before displaying the instruction        
        if self.parseflag == 1:
            self.parse_inst()
        self.display.setText(instext)
        self.display.draw()
        self.window.flip()
        
        event.waitKeys(keyList=['return'])

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


def get_settings(env, ver):
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
    '''Return a dictionary of settings based on
    the specified environment, given by the parameter
    env. Can also specify whether or not to use testing settings.

    Include keypress counter balancing
    '''
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

def runexp(filename, timer, win, writers, resdict, runtime,dfile,seed,movietype=None):
    random.seed()
    rs = random.randint(0,10000)
    random.seed(a=rs)
    writera = writers[0]
    writerb = writers[1]
    if movietype != None:
        resdict['Assoc Task'] = movietype
    instr_path = './taskScripts/resources/ESQ/'  # path for instructions
    instr_name = '_instr.txt' # filename (preceded by subtask name) for instructions
    begin_name = 'begin_instr.txt' # beginning text, if no instruction is needed for second run
    ready_name = 'wait_trigger.txt' # instruction: wait trigger screen
    exp_end_name = 'taskend_instr.txt' # instruction: wait trigger screen
    ESQ_name = 'ESQ_instr.txt'
    end_name = 'end_instr.txt'
    trial_setup_path = '.' # path for trial setup
    fixed_ESQ_name = os.path.dirname(os.path.abspath(__file__)) + '//resources//ESQ//ESQ_Questions.csv' # experience sampling questions - fixed

    win.flip() 
    
    instruction_parameter = dict([
                ('inst_size', 34), # size/height of the instruction
                ('inst_color', 'black'), # color of the instruction
                ('inst_font', 'sans'), # color of the instruction
                ])

    INFO = {
            'Experiment': 'Task2019',  # compulsory: name of program, used for trial definition in ./parameter/~.csv
            'Subject': '001',  # compulsory
            'Version': ['A', 'B'],  # counterbalance the fixation color
            'Run': '1',  # compulsory
            #'Subtask': ['Self', 'Other'],  # start the task with block for Self or Other
            'Subtask': ['Word', 'Picture', 'You', 'Friend', 'Go', 'NoGo'],  # start the task with block for Image or Word
            'Environment': ['lab', 'mri'],  # mri version can be tested on a normal stimuli delivery pc
            'ESQuestion': ['ES', 'No ES'], # with or without experience sampling
            }
    ready_txt = instr_path + ready_name

    #experiment_info = subject_info(INFO)
    settings = get_settings(
                        env='lab',
                        ver='A')
    #Experiment = Paradigm(escape_key='esc', color=0
    #                          )#window_size=settings['window_size'])
        # hide mouse


    ESQ_txt = instr_path + ESQ_name
    ESQ_msg = my_instructions(
            window=win, settings=settings,
            instruction_txt=ESQ_txt, ready_txt=ready_txt, 
            instruction_size=instruction_parameter['inst_size'], instruction_font=instruction_parameter['inst_font'],
            instruction_color='black', parseflag=0)
    with open(os.path.dirname(os.path.abspath(__file__)) + "//resources//ESQ//ESQ_instr.txt") as f:
        lines = f.read()
    ESQ_msg.display.setText(lines)
    ESQ_msg.display.draw()
    ESQ_msg.window.flip()
        
    event.waitKeys(keyList=['return'])
    #ESQ_msg.show()
    win.flip()

    ES_fixed = data.TrialHandler(nReps = 1, method = 'sequential', trialList = data.importConditions(fixed_ESQ_name), name = 'Questionnaire') 
    #ES_random = data.TrialHandler(nReps = 1, method = 'random', trialList = data.importConditions(random_ESQ_name), name = 'Questionnaire')

    # Note: this is the order of the output header, very specific, just to conform with others
    ESQ_key = ['Participant_number', 'Questionnaire_startTime', 'Questionnaire_endTime', 'TrialDuration', 'Focus', 'Future', 'Past', 'Self', 'Other', 'Emotion', 'Modality', 'Detailed', 'Deliberate', 'Problem', 'Diversity', 'Intrusive', 'Source', 'Arousal', 'Tense', 'Uncertainty']            

    ratingScale = visual.RatingScale(win, low=1, high=10, markerStart=4.5,
            precision=10, tickMarks=[1, 10], markerColor='black', textColor='black', lineColor='black',acceptPreText='Use the left and right arrow keys',acceptSize=3
            )
    QuestionText = visual.TextStim(win, color = 'black', text = None , anchorHoriz = 'center', anchorVert= 'top')
    scale_high = visual.TextStim(win, text=None,  wrapWidth=None,color='black', pos=(0.5,-0.5))
    scale_low = visual.TextStim(win, text=None, wrapWidth=None, color='black',pos=(-0.5,-0.5))
    random.shuffle(ES_fixed.trialList)
    

    #       get each question from Questionnaire:
    for enum, i in enumerate(range(0,len(ES_fixed.trialList))):
        
    #for enum, i in enumerate(range(0,1)):     #Shortened
        #if i < len(ES_fixed.trialList):
        event.clearEvents()
        if i < len(ES_fixed.trialList):
            question = ES_fixed.next()
            resdict['Timepoint'], resdict['Time'], resdict['Experience Sampling Question'] = 'ESQ', timer.getTime(), str(question['Label'] + "_start")
            writera.writerow(resdict)

            resdict['Timepoint'], resdict['Time'],resdict['Experience Sampling Question'],resdict['Experience Sampling Response'], resdict['Auxillary Data'] = None,None,None,None,None
        ratingScale.noResponse = True
        rand = random.randrange(1,10,1)
        ratingScale.markerStart = rand
        keyState=key.KeyStateHandler()

        win.winHandle.push_handlers(keyState)

        pos = ratingScale.markerStart
        inc=0.1
        ratingScale.noResponse = True

        while ratingScale.noResponse:  #key 4 not pressed
            if keyState[key.LEFT] is True:
                pos -= inc
            elif keyState[key.RIGHT] is True:
                pos += inc
            if pos > 9:
                pos = 9
            elif pos < 0:
                pos = 0

            ratingScale.setMarkerPos(pos)
            QuestionText.setText(question['Questions'])
            QuestionText.draw()
            scale_high.setText(question['Scale_high'])
            scale_low.setText(question['Scale_low'])
            scale_high.draw()
            scale_low.draw()
            ratingScale.draw()
            win.flip()
        time.sleep(1)
        responded = ratingScale.getRating()

        resdict['Timepoint'], resdict['Time'], resdict['Experience Sampling Question'], resdict['Experience Sampling Response'],resdict['Auxillary Data'] = 'ESQ', timer.getTime(), str(question['Label'] + "_response"), responded, str("Marker Started at " + str(rand +1))
        
        writera.writerow(resdict)
        writerb.writerow(resdict)
        
        resdict['Timepoint'], resdict['Time'],resdict['Experience Sampling Question'],resdict['Experience Sampling Response'], resdict['Auxillary Data'] = None,None,None,None,None
    

    
    
    




    end_txt = instr_path + end_name
    end_msg = my_instructions(
            window=win, settings=settings,
            instruction_txt=end_txt, ready_txt=ready_txt, 
            instruction_size=instruction_parameter['inst_size'], instruction_font=instruction_parameter['inst_font'],
            instruction_color=instruction_parameter['inst_color'], parseflag=0)
    


