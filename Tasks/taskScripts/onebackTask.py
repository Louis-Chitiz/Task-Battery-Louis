    # -*- coding: utf-8 -*-
import os
import sys
from typing_extensions import runtime
from psychopy import core, event, logging, visual
#from src.experiment import (event_logger, Paradigm, fixation_cross,
#                                    Text, Question, get_stim_screen, responsescreen, instructions,
#                                subject_info)
#from src.fileIO import read_only, write_csv
#from settings import *
#from src.experiment import instructions as instr
from psychopy import core, data, gui, visual, event, logging
from pyglet.window import key


import os
from random import uniform, shuffle, randrange

import numpy as np

sans = ['Arial','Gill Sans MT', 'Helvetica','Verdana'] #use the first font found on this list
import codecs
import csv
import os
import re
import stat
from collections import OrderedDict


def create_dir(directory):
    '''

    create a directory if it doesn't exist.

    '''
    if not os.path.exists(directory):
        os.makedirs(directory)


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

    with codecs.open(PATH, 'r', encoding='utf8') as f:
        input_data = f.read()

    text = parse_instructions(input_data)

    return text


def load_conditions_dict(conditionfile):
    '''
    load each row as a dictionary with the headers as the keys
    save the headers in its original order for data saving
    '''

    with codecs.open(conditionfile, 'r', encoding='utf8') as f:
        reader = csv.DictReader(f)
        trials = []

        for row in reader:
            trials.append(row)

        # save field names as a list in order
        fieldnames = reader.fieldnames

    return trials, fieldnames


'''settings.py
Define global and environment-specific settings here.
'''
# there's a bug in datastructure so don't change the next two lines
BLOCK_TIME = 12
BLOCK_GO_N = 16

# set the two features we used for making the stimulus
shape = ['square', 'triangle', 'circle']
# texture = ['dot', 'solid', 'stripe']

# locate path of experiment specification related files
condition_path = None  # set later by subject info input
trialheader_path = os.path.dirname(os.path.abspath(__file__)) +'//resources//ZeroBack_Task//TrialHeaders.csv'
trialspec_path = os.path.dirname(os.path.abspath(__file__)) +'//resources//ZeroBack_Task//TrialSpecifications.csv'
stimulus_dir = os.path.dirname(os.path.abspath(__file__)) +'//resources//ZeroBack_Task//stimuli//'
exp_questions_path = './stimuli/ES_questions.csv'

# column name of trial type names in TrialSpecifications.csv
trialspec_col = 'trial_type'

# task instruction
instr_txt1 = os.path.dirname(os.path.abspath(__file__)) + "//resources//OneBack_Task//exp_instr_es1.txt" 
instr_txt2 = os.path.dirname(os.path.abspath(__file__)) + "//resources//OneBack_Task//exp_instr_es2.txt" 
instr_txt3 = os.path.dirname(os.path.abspath(__file__)) + "//resources//OneBack_Task//exp_instr_es3.txt" 

# wait trigger screen
ready_txt = os.path.dirname(os.path.abspath(__file__)) +  "//resources//ZeroBack_Task//wait_trigger.txt" 


from psychopy import logging
from psychopy.platform_specific import win32
#from src.fileIO import write_csv, create_headers, load_conditions_dict
#from src.datastructure.stimulus import stimulus_onefeat, stimulus_ExpSample
#from src.datastructure.datastructure import *
#from src.datastructure import trial_library

from random import shuffle, randint, uniform, choice
from itertools import product


class ExpSample(object):
    '''
    generate a experience sampling trial detail

    trial_spec: dict
        trial specification

    lst_header: list
        headers for generating dictionary to store trial details

    '''
    def __init__(self, trial_spec, lst_header):
        self.trial_spec = trial_spec
        self.lst_header = lst_header

    def generate_trial(self, stimulus_generator, last_trial):
        '''
        a generater that creates trials

        stimulus_generator: generator
            stimulus generator
            the output of the generator is a list of dictionaries
            the header of the dictionaries are
            "Item", "Question", "Scale_low", "Scale_high"

        last_trial: dict
            the previous trial; some trials need this information
            if it's a experience sampling question,
            zero-back or no-go trial, None type is accepted

        output

        dict_rows: a list of dict
            a list of trials in dictionary

        trial_time: a list of float
            total time of each trial, for counter

        '''
        items = next(stimulus_generator.generate())

        dict_rows = []
        trial_time = []
        for item in items:

            dict_row = {key: None for key in self.lst_header}
            dict_row['TrialIndex'] = None
            dict_row['Condition'] = None

            dict_row['TrialType'] = self.trial_spec['trial_type']
            dict_row['fix_duration'] = uniform(self.trial_spec['fix_t_min'], self.trial_spec['fix_t_max'])
            dict_row['stim_duration'] =self.trial_spec['trial_t_total'] - dict_row['fix_duration']

            dict_row['stimPicLeft'] = item['Scale_low']
            dict_row['stimPicRight'] =  item['Scale_high']
            rand_marker_start = round(uniform(1, 10), 1)
            dict_row['Ans'] = str(rand_marker_start)

            dict_row['stimPicMid'] = item['Item']

            dict_rows.append(dict_row)
            trial_time.append(self.trial_spec['trial_t_total'])

        yield dict_rows, trial_time

class NoGo(object):
    '''
    generate a one back trial detail

    trial_spec: dict
        trial specification

    lst_header: list
        headers for generating dictionary to store trial details

    '''
    def __init__(self, trial_spec, lst_header):

        self.trial_spec = trial_spec
        self.lst_header = lst_header

    def generate_trial(self, stimulus_generator, last_trial):
        '''
        a generater that creates trials

        stimulus_generator: generator
            stimulus generator

        last_trial: dict
            the previous trial; some trials need this information
            if it's a zero-back or no-go trial, None type is accepted

        output

        dict_row: dict
            a trail in dictionary

        t: float
            total time of this trial, for counter

        '''
        dict_row = {key: None for key in self.lst_header}
        item_list = next(stimulus_generator.generate())

        dict_row['TrialIndex'] = None
        dict_row['Condition'] = None

        dict_row['TrialType'] = self.trial_spec['trial_type']
        dict_row['fix_duration'] = uniform(self.trial_spec['fix_t_min'],self.trial_spec['fix_t_max'])
        dict_row['stim_duration'] =self.trial_spec['trial_t_total'] - dict_row['fix_duration']

        dict_row['stimPicLeft'] = item_list[0]
        dict_row['stimPicRight'] = item_list[1]
        dict_row['stimPicMid'] = None
        dict_row['Ans'] = 'NA'

        yield dict_row, self.trial_spec['trial_t_total']



class ZeroBack(object):
    '''
    generate a zero back trial detail

    trial_spec: dict
        trial specification

    lst_header: list
        headers for generating dictionary to store trial details

    '''
    def __init__(self, trial_spec, lst_header):
        self.trial_spec = trial_spec
        self.lst_header = lst_header

    def generate_trial(self, stimulus_generator, last_trial):
        '''
        a generater that creates trials

        stimulus_generator: generator
            stimulus generator

        last_trial: dict
            the previous trial; some trials need this information
            if it's a zero-back or no-go trial, None type is accepted

        output

        dict_row: dict
            a trail in dictionary

        self.trial_spec['trial_t_total']: float
            total time of this trial, for counter

        '''
        dict_row = {key: None for key in self.lst_header}
        item_list = next(stimulus_generator.generate())

        dict_row['TrialIndex'] = None
        dict_row['Condition'] = None

        dict_row['TrialType'] = self.trial_spec['trial_type']
        dict_row['fix_duration'] = uniform(self.trial_spec['fix_t_min'],self.trial_spec['fix_t_max'])
        dict_row['stim_duration'] =self.trial_spec['trial_t_total'] - dict_row['fix_duration']

        dict_row['stimPicLeft'] = item_list[0]
        dict_row['stimPicRight'] = item_list[1]
        dict_row['Ans'] = choice(['left', 'right'])

        if dict_row['Ans'] == 'left':
            dict_row['stimPicMid'] = dict_row['stimPicLeft']
        else:
            dict_row['stimPicMid'] = dict_row['stimPicRight']

        yield dict_row,self.trial_spec['trial_t_total']


class OneBack(object):
    '''
    generate a one back recall trial detail

    trial_spec: dict
        trial specification

    lst_header: list
        headers for generating dictionary to store trial details
    '''
    def __init__(self, trial_spec, lst_header):
        self.trial_spec = trial_spec
        self.lst_header = lst_header

    def generate_trial(self, last_trial, stimulus_generator):
        '''
        a generater that creates trials

        stimulus_generator: generator
            stimulus generator

        last_trial: dict
            the previous trial; some trials need this information
            if it's a zero-back or no-go trial, None type is accepted

        output

        dict_row: dict
            a trail in dictionary

        self.trial_spec['trial_t_total']: float
            total time of this trial, for counter

        '''
        dict_row = {key: None for key in self.lst_header}

        dict_row['TrialIndex'] = None
        dict_row['Condition'] = None

        dict_row['TrialType'] = self.trial_spec['trial_type']
        dict_row['fix_duration'] = uniform(self.trial_spec['fix_t_min'], self.trial_spec['fix_t_max'])
        dict_row['stim_duration'] =self.trial_spec['trial_t_total'] - dict_row['fix_duration']

        dict_row['stimPicLeft'] = '?'
        dict_row['stimPicRight'] = '?'

        dict_row['Ans'] = choice(['left', 'right'])

        if dict_row['Ans'] == 'left':
            dict_row['stimPicMid'] = last_trial['stimPicLeft']
        else:
            dict_row['stimPicMid'] = last_trial['stimPicRight']

        yield dict_row,self.trial_spec['trial_t_total']

class ZeroBackRecog(object):
    '''
    generate a zero back trial detail

    trial_spec: dict
        trial specification

    lst_header: list
        headers for generating dictionary to store trial details

    '''
    def __init__(self, trial_spec, lst_header):
        self.trial_spec = trial_spec
        self.lst_header = lst_header

    def generate_trial(self, stimulus_generator, last_trial):
        '''
        a generater that creates trials

        stimulus_generator: generator
            stimulus generator

        last_trial: dict
            the previous trial; some trials need this information
            if it's a zero-back or no-go trial, None type is accepted

        output

        dict_row: dict
            a trail in dictionary

        self.trial_spec['trial_t_total']: float
            total time of this trial, for counter

        '''
        dict_row = {key: None for key in self.lst_header}
        item_list = next(stimulus_generator.generate())

        dict_row['TrialIndex'] = None
        dict_row['Condition'] = None

        dict_row['TrialType'] = self.trial_spec['trial_type']
        dict_row['fix_duration'] = uniform(self.trial_spec['fix_t_min'],self.trial_spec['fix_t_max'])
        dict_row['stim_duration'] =self.trial_spec['trial_t_total'] - dict_row['fix_duration']

        dict_row['stimPicLeft'] = item_list[0]
        dict_row['stimPicRight'] = item_list[1]
        null = filter(lambda x: x not in item_list, stimulus_generator.stimuli)[0]

        dict_row['Ans'] = choice(['yes', 'no'])

        if dict_row['Ans'] == 'yes':
            dict_row['stimPicMid'] = choice(item_list)
        else:
            dict_row['stimPicMid'] = null

        yield dict_row,self.trial_spec['trial_t_total']


class OneBackRecog(object):
    '''
    generate a one back recall trial detail

    trial_spec: dict
        trial specification

    lst_header: list
        headers for generating dictionary to store trial details
    '''
    def __init__(self, trial_spec, lst_header):
        self.trial_spec = trial_spec
        self.lst_header = lst_header

    def generate_trial(self, last_trial, stimulus_generator):
        '''
        a generater that creates trials

        stimulus_generator: generator
            stimulus generator

        last_trial: dict
            the previous trial; some trials need this information
            if it's a zero-back or no-go trial, None type is accepted

        output

        dict_row: dict
            a trail in dictionary
        self.trial_spec['trial_t_total']: float
            total time of this trial, for counter

        '''
        dict_row = {key: None for key in self.lst_header}
        # create a equal chance to get a present/absent target in the pre trial
        item_list = [last_trial['stimPicLeft'], last_trial['stimPicRight']]


        dict_row['TrialType'] = self.trial_spec['trial_type']
        dict_row['fix_duration'] = uniform(self.trial_spec['fix_t_min'], self.trial_spec['fix_t_max'])
        dict_row['stim_duration'] =self.trial_spec['trial_t_total'] - dict_row['fix_duration']

        dict_row['stimPicLeft'] = '?'
        dict_row['stimPicRight'] = '?'

        null= filter(lambda x: x not in item_list, stimulus_generator.stimuli)[0]

        dict_row['Ans'] = choice(['yes', 'no'])

        if dict_row['Ans'] == 'yes':
            dict_row['stimPicMid'] = choice(item_list)
        else:
            dict_row['stimPicMid'] = null

        yield dict_row,self.trial_spec['trial_t_total']

class Recognition(object):
    '''
    generate a one back recognition trial detail

    trial_spec: dict
        trial specification

    lst_header: list
        headers for generating dictionary to store trial details
    '''
    def __init__(self, trial_spec, lst_header):
        self.trial_spec = trial_spec
        self.lst_header = lst_header

    def generate_trial(self, last_trial, stimulus_generator):
        '''
        a generater that creates trials

        stimulus_generator: generator
            stimulus generator

        last_trial: dict
            the previous trial; some trials need this information
            if it's a zero-back or no-go trial, None type is accepted

        output

        dict_row: dict
            a trail in dictionary

        self.trial_spec['trial_t_total']: float
            total time of this trial, for counter

        '''
        dict_row = {key: None for key in self.lst_header}

        dict_row['TrialIndex'] = None
        dict_row['Condition'] = None

        dict_row['TrialType'] = self.trial_spec['trial_type']
        dict_row['fix_duration'] = uniform(self.trial_spec['fix_t_min'], self.trial_spec['fix_t_max'])
        dict_row['stim_duration'] =self.trial_spec['trial_t_total'] - dict_row['fix_duration']

        # decide to preserve left or right
        for f1 in stimulus_generator.feature1:
            if f1 not in [last_trial['stimPicLeft'][0], last_trial['stimPicRight'][0]]:
                distract_feature1 = f1
        for f2 in stimulus_generator.feature2:
            if f2 not in [last_trial['stimPicLeft'][1], last_trial['stimPicRight'][1]]:
                distract_feature2 = f2
        distractor = (distract_feature1, distract_feature2)

        if choice(['left', 'right']) == 'left':
            dict_row['stimPicLeft'] = last_trial['stimPicLeft']
            dict_row['stimPicRight'] = distractor
            dict_row['stimPicMid'] = '?'
            dict_row['Ans'] = 'yes'

        else:
            dict_row['stimPicLeft'] = distractor
            dict_row['stimPicRight'] = last_trial['stimPicRight']
            dict_row['stimPicMid'] = '?'
            dict_row['Ans'] = 'no'
        yield dict_row,self.trial_spec['trial_t_total']


class ZeroBack_feature(object):
    '''
    generate a zero back trial detail

    trial_spec: dict
        trial specification

    lst_header: list
        headers for generating dictionary to store trial details
    '''
    def __init__(self, trial_spec, lst_header):
        self.trial_spec = trial_spec
        self.lst_header = lst_header

    def generate_trial(self, stimulus_generator, last_trial):
        '''
        a generater that creates trials

        stimulus_generator: generator
            stimulus generator

        last_trial: dict
            the previous trial; some trials need this information
            if it's a zero-back or no-go trial, None type is accepted

        output

        dict_row: dict
            a trail in dictionary

        self.trial_spec['trial_t_total']: float
            total time of this trial, for counter

        '''
        dict_row = {key: None for key in self.lst_header}
        item_list = next(stimulus_generator.generate())

        dict_row['TrialIndex'] = None
        dict_row['Condition'] = None

        dict_row['TrialType'] = self.trial_spec['trial_type']
        dict_row['fix_duration'] = uniform(self.trial_spec['fix_t_min'], self.trial_spec['fix_t_max'])
        dict_row['stim_duration'] =self.trial_spec['trial_t_total'] - dict_row['fix_duration']

        dict_row['stimPicLeft'] = item_list[0]
        dict_row['stimPicRight'] = item_list[1]

        target_item = choice(item_list)
        target_feat = choice(target_item)

        # decide to preserve left or right
        # they all the items on screen can only share on feature
        if target_feat in stimulus_generator.feature1:
            for f2 in stimulus_generator.feature2:
                if f2 not in [dict_row['stimPicLeft'][1], dict_row['stimPicRight'][1]]:
                    distract_feature2 = f2
            dict_row['stimPicMid'] = (target_feat, distract_feature2)
        else:
            for f1 in stimulus_generator.feature1:
                if f1 not in [dict_row['stimPicLeft'][0], dict_row['stimPicRight'][0]]:
                    distract_feature1 = f1
            dict_row['stimPicMid'] = (distract_feature1, target_feat)

        if dict_row['stimPicLeft'] == target_item:
            dict_row['Ans'] = 'left'
        else:
            dict_row['Ans'] = 'right'

        yield dict_row,self.trial_spec['trial_t_total']


class OneBack_feature(object):
    '''
    generate a one back trial detail

    trial_spec: dict
        trial specification

    lst_header: list
        headers for generating dictionary to store trial details
    '''
    def __init__(self, trial_spec, lst_header):
        self.trial_spec = trial_spec
        self.lst_header = lst_header

    def generate_trial(self, last_trial, stimulus_generator):
        '''
        a generater that creates trials

        stimulus_generator: generator
            stimulus generator
        last_trial: dict
            the previous trial; some trials need this information
            if it's a zero-back or no-go trial, None type is accepted

        output

        dict_row: dict
            a trail in dictionary
        self.trial_spec['trial_t_total']: float
            total time of this trial, for counter

        '''
        dict_row = {key: None for key in self.lst_header}

        dict_row['TrialIndex'] = None
        dict_row['Condition'] = None

        dict_row['TrialType'] = self.trial_spec['trial_type']
        dict_row['fix_duration'] = uniform(self.trial_spec['fix_t_min'], self.trial_spec['fix_t_max'])
        dict_row['stim_duration'] =self.trial_spec['trial_t_total'] - dict_row['fix_duration']

        dict_row['stimPicLeft'] = '?'
        dict_row['stimPicRight'] = '?'

        target_item = choice([last_trial['stimPicLeft'], last_trial['stimPicRight']])
        target_feat = choice(target_item)
        # decide to preserve left or right

        if target_feat in stimulus_generator.feature1:
            for f2 in stimulus_generator.feature2:
                if f2 not in [last_trial['stimPicLeft'][1], last_trial['stimPicRight'][1]]:
                    distract_feature2 = f2
            dict_row['stimPicMid'] = (target_feat, distract_feature2)

        else:
            for f1 in stimulus_generator.feature1:
                if f1 not in [last_trial['stimPicLeft'][0], last_trial['stimPicRight'][0]]:
                    distract_feature1 = f1
            dict_row['stimPicMid'] = (distract_feature1, target_feat)

        if last_trial['stimPicLeft'] == target_item:
            dict_row['Ans'] = 'left'
        else:
            dict_row['Ans'] = 'right'

        yield dict_row,self.trial_spec['trial_t_total']


class Recognition_feature(object):
    '''
    generate a one back trial detail

    trial_spec: dict
        trial specification

    lst_header: list
        headers for generating dictionary to store trial details

    '''
    def __init__(self, trial_spec, lst_header):
        self.trial_spec = trial_spec
        self.lst_header = lst_header

    def generate_trial(self, last_trial, stimulus_generator):
        '''
        a generater that creates trials

        stimulus_generator: generator
            stimulus generator

        last_trial: dict
            the previous trial; some trials need this information
            if it's a zero-back or no-go trial, None type is accepted

        output

        dict_row: dict
            a trail in dictionary

        self.trial_spec['trial_t_total']: float
            total time of this trial, for counter

        '''
        dict_row = {key: None for key in self.lst_header}

        dict_row['TrialIndex'] = None
        dict_row['Condition'] = None

        dict_row['TrialType'] = self.trial_spec['trial_type']
        dict_row['fix_duration'] = uniform(self.trial_spec['fix_t_min'], self.trial_spec['fix_t_max'])
        dict_row['stim_duration'] =self.trial_spec['trial_t_total'] - dict_row['fix_duration']
        # decide to preserve left or right
        for f1 in stimulus_generator.feature1:
            if f1 not in [last_trial['stimPicLeft'][0], last_trial['stimPicRight'][0]]:
                distract_feature1 = f1
        for f2 in stimulus_generator.feature2:
            if f2 not in [last_trial['stimPicLeft'][1], last_trial['stimPicRight'][1]]:
                distract_feature2 = f2
        distractor = (distract_feature1, distract_feature2)

        if choice(['left', 'right']) == 'left':

            target_item = last_trial['stimPicLeft']
            target_feat = choice(target_item)

            if target_feat in stimulus_generator.feature1:
                dict_row['stimPicLeft'] = (target_feat, last_trial['stimPicRight'][1])

            else:
                dict_row['stimPicLeft'] = (last_trial['stimPicRight'][0], target_feat)

            dict_row['stimPicRight'] = distractor
            dict_row['stimPicMid'] = '?'
            dict_row['Ans'] = 'left'

        else:
            target_item = last_trial['stimPicRight']
            target_feat = choice(target_item)

            if target_feat in stimulus_generator.feature1:
                dict_row['stimPicRight'] = (target_feat, last_trial['stimPicLeft'][1])

            else:
                dict_row['stimPicRight'] = (last_trial['stimPicLeft'][0], target_feat)

            dict_row['stimPicLeft'] = distractor
            dict_row['stimPicMid'] = '?'
            dict_row['Ans'] = 'right'

        yield dict_row,self.trial_spec['trial_t_total']


class stimulus_ExpSample(object):
    '''
    experience sampling stimulus generator
    save features and generate stimuli

    features: list, dictionaries of questions

    '''
    def __init__(self, features):
        '''split questions into two sets'''
        self.q_focus = [features[0]]  # the focus question stays at the top
        self.q_others = features[1:]

    def generate(self):
        '''yield self.stimuli'''
        shuffle(self.q_others)
        yield self.q_focus + self.q_others


class stimulus_twofeat(object):
    '''
    double feature stimulus generator

    save features and genenrate stimuli pair

    feature1, feature2 : list, features of stimulus

    '''
    def __init__(self, feature1, feature2):
        self.feature1 = feature1
        self.feature2 = feature2

    def generate(self):
        '''
        generate a pair of stimuli with no shared feature

        '''
        shuffle(self.feature1)
        shuffle(self.feature2)
        item_left = (self.feature1[0], self.feature2[0])
        item_right = (self.feature1[1], self.feature2[1])

        yield [item_left, item_right]


class stimulus_twofeat_mix(object):
    '''
    double feature stimulus generator with mixed congurency
    The stimulis pair can share one feature or no feature.

    save features and genenrate stimuli pair

    feature1, feature2 : list, features of stimulus

    '''
    def __init__(self, feature1, feature2):
        self.feature1 = feature1
        self.feature2 = feature2
        self.stimuli = list(product(self.feature1, self.feature2))

    def generate(self):
        '''
        generate a pair of stimuli

        '''
        shuffle(self.stimuli)
        item_left = self.stimuli[0]
        item_right = self.stimuli[1]

        yield [item_left, item_right]


class stimulus_onefeat(object):
    '''
    single feature stimulus generator

    save features and genenrate stimuli
    features: list, features of stimuli

    '''
    def __init__(self, features):
        self.stimuli = features

    def generate(self):
        '''
        generate a pair of stimuli with no shared features

        '''

        shuffle(self.stimuli)
        yield [self.stimuli[0], self.stimuli[1]]


def tup2str(dir_path, tuple_stim, filesuffix):
    '''
    trun tuple to a string (filename)
    the filename must look like:
        feature1_feature2.png

    dir_path: str
        example: './stimulus/'

    tuple_stim: tuple
        stimulus, ('feature1', 'feature2')

    filesuffix: str
        expample '.png'

    return
        str, example: './stimulus/feature1_feature2.png'
    '''
    return dir_path + ('_').join(tuple_stim) + filesuffix


class experiment_parameters(object):
    '''
    save basic parameter, late pass to trial_builder

    block_length: float
        the length of a condition block, must be 1.5 * n

        default as 1.5 minutes

    block_go_n: int
        the number of catch trials (of any kind) in a block
        must be 6 * n
        default as 6

    runs: int
        the number of time to go through a set of conditions

    '''
    def __init__(self, block_length=1.5, block_go_n=6, runs=1):
        self.block_length = block_length
        self.block_go_n = block_go_n
        self.blocks = []
        self.conditions = []
        self.headers = None
        self.runs = runs

    def load_conditions(self, condition_path):
        '''

        load all the conditions for building a block

        condition_path
            path to the condition file
        '''

        conditions, _ = load_conditions_dict(condition_path)

        # conditions = []
        # with codecs.open(condition_path, 'r', encoding='utf8') as f:
        #     reader = csv.reader(f)
        #     for cond in reader:
        #         conditions.append(cond[0])
        self.conditions = conditions

    def load_header(self, trialheader_path):
        _, header = load_conditions_dict(trialheader_path)
        self.headers = header

    def create_counter(self):
        '''
        create:
        a counter in seconds for task length
        a list of counters for the number of catch trial type 1 to n
       '''
        time = self.block_length * 60
        trial_library_n = len(self.conditions[0]) - 1
        go_n = [self.block_go_n / trial_library_n] * trial_library_n
        return time, go_n


class trial_finder(object):
    '''
    find and create trials accroding to the trial specification
    later pass to trial_bulder

    trialspec_path: a path to the trial specification file
    trialspec_col: the column name directing to the trial specification info

    '''
    def __init__(self, trialspec_path, trialspec_col):
        self.trialspec_path = trialspec_path
        self.trialspec_col = trialspec_col

    def get(self, trial_type):
        '''
        get the trial by keyword 'trial_type'
        only the supporting ones works!

        trial_type: str

        '''
        
        with codecs.open(self.trialspec_path, 'r', encoding='utf8') as f:
            reader = csv.DictReader(f)
            #loop through csv list
            for row in reader:

                # first convert strings to float
                for item in row.keys():
                    row[item] = str2float(row[item])

                # if current rows trial type is equal to input, print that row
                if trial_type == row[self.trialspec_col]:
                    trial_spec = row
                    trial_mod = globals()[trial_type]
                    return trial_mod(trial_spec=trial_spec, lst_header=None)

                else:
                    pass


class trial_builder(object):
    '''
    build trials for each run
    need these -
        experiment_parameters: obj
            store experiment parameter

        trial_finder: obj
            it finds a trial generator for you

        stimulus_generator: obj
            it generate stimulus pair
    '''
    def __init__(self):
        self.trial_index = 0
        self.dict_trials = []
        self.last_trial = None
        self.init_trial_index = 0

    def initialise(self, task_t, go_n):
        '''
        clean the buffer and reset counter

        task_t: float
            the length of the block in second
        go_n: list, int
            a list of number of catch trials
        '''
        self.dict_trials = []
        self.task_t = task_t
        self.go_n = go_n
        self.last_trial = None
        self.trial_index = self.init_trial_index


    def block_trials(self, trial_finder, block, trial_headers):

        '''
        trial_finder: object
            it finds what type of trial you need based on a string

        block: str
            the name of the current block

        trial_headers: lst
            the trial headers

        return
            objects
        '''

        trial_NoGo = trial_finder.get(trial_type='NoGo')
        trial_NoGo.lst_header = trial_headers

        trial_Go1 = trial_finder.get(trial_type=block['GoTrial1'])
        trial_Go1.lst_header = trial_headers

        trial_Go2 = trial_finder.get(trial_type=block['GoTrial2'])
        trial_Go2.lst_header = trial_headers

        trial_Go = [trial_Go1, trial_Go2]

        return trial_NoGo, trial_Go

    def get_n_NoGo(self, trial_NoGo):
        '''
        generate a random number of no-go trials

        trial_NoGo: object
            the no-go trial object. only this object contains the information for this

        retrun
            int
        '''

        n_min = int(trial_NoGo.trial_spec['trial_n_min'])
        n_max = int(trial_NoGo.trial_spec['trial_n_max']) + 1

        return randrange(n_min, n_max, 1)

    def save_trial(self, cur_trial, block):
        '''
        save the trial to the temporary list

        cur_trial: dict
            a trial in dictionary form

        block: str
            the current block name

        '''
        cur_trial['Condition'] = block
        cur_trial['TrialIndex'] = self.trial_index
        self.trial_index += 1
        self.dict_trials.append(cur_trial)
        self.last_trial = cur_trial

    def build(self, experiment_parameters, trial_finder, \
              stimulus_generator, block):
        '''
        build the trial generator

        experiment_parameters: obj
            store experiment parameter

        trial_finder: obj
            it finds a trial generator for you

        stimulus_generator: obj
            it generate stimulus pair

        block: string or None
            indicate the task condiiton in the first block
            Options are '0', '1', or None (random start)

        '''
        for cur in range(experiment_parameters.runs):

            # load condtions
            blocks = experiment_parameters.conditions.copy()
            # initialize the output storage and the counter
            run  = []
            trial_idx_tmp = 0

            init_task_t, init_go_n = experiment_parameters.create_counter()

            for block in blocks:
                self.initialise(init_task_t, init_go_n)

                # get the specific go trials according to the block you are in
                trial_NoGo, trial_Go = self.block_trials(
                        trial_finder, block, experiment_parameters.headers)
                self.trial_index = trial_idx_tmp

                #while self.task_t >= 0: # start counting
                for i in range(experiment_parameters.block_go_n):
                    # get no-go trial number
                    n_NoGo = self.get_n_NoGo(trial_NoGo)

                    # genenrate the no-go trials before the go trial occur
                    for j in range(n_NoGo):
                        cur_trial, t = next(trial_NoGo.generate_trial(
                            stimulus_generator=stimulus_generator,
                            last_trial=self.last_trial))
                        self.task_t -= t
                        self.save_trial(cur_trial, block['Condition'])

                    # generate the go trial
                    # go trial: type 1 or type 2
                    # see which go trial type were all used
                    use_go = [i for i, e in enumerate(self.go_n) if e > 0]
                    if use_go:
                        # select a random one from the available ones
                        idx = choice(use_go)


                    if trial_Go[idx].__class__.__name__=='ExpSample':
                        pass
                        #self.task_t -= 3
                        # if it's experience sampling
                        #cur_trial, t = next(trial_Go[idx].generate_trial(
                        #stimulus_generator=expsampling_generator,
                        #last_trial=self.last_trial)) # n-back
                        #for trial in cur_trial:
                            #self.task_t -= t[0]
                            #self.save_trial(trial, block['Condition'])
                    else:
                        cur_trial, t = next(trial_Go[idx].generate_trial(
                        stimulus_generator=stimulus_generator,
                        last_trial=self.last_trial)) # n-back

                        self.task_t -= t
                        self.save_trial(cur_trial, block['Condition'])
                    
                        


                    # add 1~ 2 no-go trials and then a switch screen to end this block
                for k in range(randrange(1, 3, 1)):
                    cur_trial, t = next(trial_NoGo.generate_trial(
                                stimulus_generator=stimulus_generator,
                                last_trial=self.last_trial))
                    self.task_t -= t
                    self.save_trial(cur_trial, block['Condition'])

                cur_trial, t = next(trial_NoGo.generate_trial(
                    stimulus_generator=stimulus_generator,
                    last_trial=self.last_trial))
                cur_trial['TrialType'] = 'Switch'
                cur_trial['stimPicMid'] = 'SWITCH'
                cur_trial['stimPicLeft'] = None
                cur_trial['stimPicRight'] = None

                self.save_trial(cur_trial, 'Switch')
                #if self.task_t != 0:
                    # if this list of trials is not good for the block, restart
                    #init_task_t, init_go_n = experiment_parameters.create_counter()
                    #self.initialise(init_task_t, init_go_n)
                    #self.trial_index = trial_idx_tmp
                #else:
                    # if it's good save this block to the run
               
                run += self.dict_trials
                trial_idx_tmp = self.trial_index
            yield run



def str2float(string):
    '''
    detect if the string can be converted to float.
    if so, return the converted result
    else, return the input string
    '''
    try:
        return float(string)
    except ValueError:
        return string

# Base settings that apply to all environments.
# These settings can be overwritten by any of the
# environment settings.

BASE = {
    'test': False,
    'mouse_visible': False,
    'logging_level': logging.INFO
}


# Development environment settings. Used for testing,
# outside of the MR room.
DEV = {
    'env': 'dev',
    'test': True,
    'window_size': (800, 600),
    'logging_level': logging.DEBUG
}

# Production settings
PRODUCTION = {
    'test': False,
    'logging_level': logging.EXP
}

# Laboratory setting
# LAB = {
#     'env': 'lab',  # Enviroment name
#     'window_size': 'full_screen',
#     'input_method': 'keyboard'
#     }

LAB = {
    'env': 'lab',  # Enviroment name
    'window_size': (1280,800),
    'input_method': 'keyboard'
    }



# # Development environment settings. Used for testing,
# # outside of the MR room.
# DEV = {
#     'env': 'dev',  # Enviroment name
#     'window_size': (800, 600),
#     'button_box': None,  # No button box

#     # Number of runs
#     'n_runs': 1,

#     # Rating scale descriptions
#     'gaze_desc': "Left                   \
#                                         Right",
#     'self_desc': "Very Negative                   \
#                                         Very Positive",
#     'other_desc': "Very Negative                   \
#                                         Very Positive",
# }

MRI = {
    'env': 'mri',
    'window_size': 'full_screen',
    'input_method': 'serial',
}

# experiment specific version related setting
VER_A = {
        'rec_color': 'blue',
        'loc_color': 'red',
        'rec_keys': ['z', 'x'],
        'loc_keys': ['n', 'm'],
        'rec_keyans': ['yes', 'no'],
        'loc_keyans': ['left', 'right']
        }

VER_B = {
        'rec_color': 'red',
        'loc_color': 'blue',
        'rec_keys': ['n', 'm'],
        'loc_keys': ['z', 'x'],
        'rec_keyans': ['yes', 'no'],
        'loc_keyans': ['left', 'right']
        }

VER_A_MRI = {
            'rec_keys': ['left', 'right'],
            'loc_keys': ['left', 'right']
            }

VER_B_MRI = {
            'rec_keys': ['left', 'right'],
            'loc_keys': ['left', 'right']
            }

EXP_SAMPLING_A = {
        '0_back_color': 'blue',
        '1_back_color': 'red',
        'loc_keys': ['left', 'right'],
        'loc_keyans': ['left', 'right']
        }

EXP_SAMPLING_B = {
        '0_back_color': 'red',
        '1_back_color': 'blue',
        'loc_keys': ['left', 'right'],
        'loc_keyans': ['left', 'right']
        }

def get_trial_generator(block):
    '''
    return a trial generator and a list of data log headers
    '''
    # now define the generators
    # create experiment parameters
    if block == "0":
        condition_path = os.path.dirname(os.path.abspath(__file__)) + "//resources//ZeroBack_Task//ConditionsSpecifications_ES_zeroback.csv"
    elif block == "1":
        condition_path = os.path.dirname(os.path.abspath(__file__)) + "//resources//ZeroBack_Task//ConditionsSpecifications_ES_oneback.csv"

    parameters = experiment_parameters(
            block_length=BLOCK_TIME, block_go_n=BLOCK_GO_N, runs=1)
    parameters.load_conditions(condition_path)
    parameters.load_header(trialheader_path)
    #questions, _ = load_conditions_dict('./stimuli/ES_questions.csv')


    # create trial finder
    find_trial = trial_finder(trialspec_path=trialspec_path, trialspec_col=trialspec_col)

    # create stimulus generators
    # stimulus_generator = stimulus_twofeat(feature1=shape, feature2=texture)
    stimulus_generator = stimulus_onefeat(features=shape)
    #exp_sample_generator = stimulus_ExpSample(questions)
    # now build the trials
    builder = trial_builder()
    # build the trial generator
    trial_generator = builder.build(parameters, find_trial, stimulus_generator, block)

    return trial_generator, parameters.headers


def get_settings(env, ver, test=False):
    '''Return a dictionary of settings based on
    the specified environment, given by the parameter
    env. Can also specify whether or not to use testing settings.

    Include keypress counter balancing
    '''
    # Start with the base settings
    settings = BASE

    # display and key press counter balancing
    if ver == 'A':
        settings.update(EXP_SAMPLING_A)
    elif ver == 'B':
        settings.update(EXP_SAMPLING_B)
    else:
        raise ValueError('Version "{0}" not supported.'.format(ver))

    if env == 'lab':
        settings.update(LAB)
    # elif env == 'dev':
    #     settings.update(DEV)
    elif env == 'mri':
        settings.update(MRI)

    else:
        raise ValueError('Environment "{0}" not supported.'.format(env))

    # Update it with either the test or production settings

    if test:
        #settings.update(TEST)
        print('')
        
    else:
        settings.update(PRODUCTION)

    return settings

#from src.datastructure.stimulus import tup2str

def parse_stimulus_name(trial):
    '''
    parse tuples to proper file names
    '''
    for key in trial.keys():
        if type(trial[key]) is tuple:
            trial[key] = tup2str(stimulus_dir, trial[key], '.png')
        elif 'stimPic' in key and type(trial[key]) is str:
            if trial[key] in shape:
                trial[key] = stimulus_dir + trial[key] + '.png'
    return trial

def create_headers(list_headers):
    '''
    create ordered headers for the output data csv file
    '''

    headers = []

    for header in list_headers:
        headers.append((header, None))

    return OrderedDict(headers)

def write_csv(fileName, list_headers, thisTrial):
    '''
    append the data of the current trial to the data file
    if the data file has not been created, this function will create one


    attributes

    fileName: str
        the file name generated when capturing participant info

    list_headers: list
        the headers in a list, will pass on to function create_headers

    thisTrial: dict
        a dictionary storing the current trial
    '''

    # full_path = os.path.abspath(fileName)
    # directory = os.path.dirname(full_path)
    # create_dir(directory)
    # fieldnames = create_headers(list_headers)

    # if not os.path.isfile(full_path):
    #     # headers and the first entry
    #     with codecs.open(full_path, 'ab+', encoding='utf8') as f:
    #         dw = csv.DictWriter(f, fieldnames=fieldnames)
    #         dw.writeheader()
    #         dw.writerow(thisTrial)
    # else:
    #     with codecs.open(full_path, 'ab+', encoding='utf8') as f:
    #         dw = csv.DictWriter(f, fieldnames=fieldnames)
    #         dw.writerow(thisTrial)

def read_only(path):
    '''
    change the mode to read only
    '''
    #os.chmod(path, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)

class Paradigm(object):
    '''
    Study paradigm
    '''
    def __init__(self, win, escape_key='esc', color=0, *args, **kwargs):
        self.escape_key = escape_key
        self.trials = []
        self.stims = {}

        self.window = win

        # if window_size =='full_screen':
        #     self.window = visual.Window(fullscr=True, color=color, units='pix', *args, **kwargs)
        # else:
        #     self.window = visual.Window(size=window_size, color=color, allowGUI=True, units='pix', *args, **kwargs)


class fixation_cross(object):
    '''
    fixation cross for this task
    '''
    def __init__(self, window, color='black'):
        self.window = window

        # i dont know how to draw a fixation cross
        # self.line = visual.ShapeStim(self.window , name='verticle line',
        #     lineColor=None, fillColor=color,
        #     vertices=[(-2.5, 250), (-2.5,-250), (2.5,-250), (2.5, 250)])

        # self.dash = visual.ShapeStim(self.window , name='dash line',
        #     lineColor=None, fillColor=color,
        #     vertices=[(-10, 2.5), (-10, -2.5), (10,-2.5), (10, 2.5)])

        self.text = visual.TextStim(self.window, text="+", wrapWidth=1100, color=color, font=sans)

    def set_trial(self, trial):
        self.duration = trial['fix_duration']

    def show(self, clock):
        self.text.draw()
        self.window.flip()
        start_trial = clock.getTime()
        core.wait(self.duration)
        return start_trial


class Text(object):
    '''
    show text in the middle of the screen
    such as 'switch'
    '''
    def __init__(self, window, text, color):
        '''Initialize a text stimulus.
        Args:
        window - The window object
        text - text to display
        duration - the duration the text will appear
        keys - list of keys to press to continue to next stimulus. If None,
                will automatically go to the next stimulus.
        Additional args and kwargs are passed to the visual.TextStim
        constructor.
        '''
        self.window = window
        self.text = visual.TextStim(self.window, text=text, wrapWidth=1100, color=color, font=sans)
        self.duration = None

    def set_trial(self, trial):
        self.duration = trial['stim_duration']

    def show(self, clock):
        self.text.draw()
        self.window.flip()
        start_trial = clock.getTime()
        core.wait(self.duration)

        # set the following so it's competeble to responese screen
        Resp = None
        KeyResp = None
        KeyPressTime = None
        respRT = None
        correct = None

        return start_trial, KeyResp, Resp, KeyPressTime, respRT, correct


class responsescreen(object):
    '''
    the screen for the memory task
    '''
    def __init__(self, window, version):
        self.window = window
        self.line = visual.Line(self.window, start=(0,0.75), end=(0,-0.75),
            lineWidth=3, lineColor='black', fillColor='black', name = 'verticle line')
        # self.line = visual.ShapeStim(self.window , name='verticle line',
        #                 lineColor=None, fillColor='black',
        #                 vertices=[(-2.5, 250), (-2.5,-250), (2.5,-250), (2.5,250)])

        self.dash = visual.ShapeStim(self.window , name='dash line',
                lineColor=None, fillColor='black', pos=(0, 2.5))

        # self.dash = visual.ShapeStim(self.window , name='dash line',
        #                 lineColor=None, fillColor='black',
        #                 vertices=[(-10, 2.5), (-10, -2.5), (10,-2.5), (10, 2.5)])

        self.image_left = visual.ImageStim(self.window, name='stimPic-left',
                image=None, size=(0.5, 0.75), pos=(-0.5, 0))
        self.image_right = visual.ImageStim(self.window, name='stimPic-right',
                image=None, size=(0.5, 0.75), pos=(0.5, 0))
        self.image_mid = visual.ImageStim(self.window, name='stimPic-middle',
                image=None, size=(0.25, 0.4),pos=(0,0))

        self.quest_left = visual.TextStim(self.window, text='?',
                pos=(-0.5, 0), wrapWidth=500, color='black')
        self.quest_right = visual.TextStim(self.window, text='?',
                 pos=(0.5, 0), wrapWidth=500, color='black')
        self.quest_mid = visual.TextStim(self.window, text='?',
                pos=(0,0), wrapWidth=200, color='white')

        self.present_left = None
        self.present_right = None
        self.present_mid = None

        self.version = version
        self.keylist = []
        self.keyans = []

    def set_trial(self, trial):
        
        self.duration = trial['stim_duration']
        self.ans = trial['Ans']
        
        # change color of self.line and self.dash base on go trial task
        if 'NoGo'in trial['TrialType']:
            self.line.lineColor = 'black'
            self.dash.lineColor = 'black'

        elif 'Recog' in trial['TrialType']:
            self.line.lineColor = self.version['rec_color']
            self.dash.lineColor = self.version['rec_color']
            self.keylist = self.version['rec_keys']
            self.keyans = self.version['rec_keyans']

        elif 'Back' in trial['TrialType']:
            if 'Zero' in trial['TrialType']:
                self.line.lineColor = self.version['0_back_color']
                self.dash.lineColor = self.version['0_back_color']
            elif 'One' in trial['TrialType']:
                self.line.lineColor = self.version['1_back_color']
                self.dash.lineColor = self.version['1_back_color']
            else:
                self.line.lineColor = self.version['loc_color']
                self.dash.lineColor = self.version['loc_color']

            self.keylist = self.version['loc_keys']
            self.keyans = self.version['loc_keyans']

        if '?' == trial['stimPicLeft']:
            self.present_left = self.quest_left
            self.present_right = self.quest_right
        else:
            self.image_left.setImage(trial['stimPicLeft'])
            self.image_right.setImage(trial['stimPicRight'])
            self.present_left = self.image_left
            self.present_right = self.image_right

        if trial['stimPicMid'] is '?':
            self.present_mid = self.quest_mid

        elif trial['stimPicMid'] is None:
            self.present_mid = self.dash

        else:
            self.image_mid.setImage(trial['stimPicMid'])
            self.present_mid = self.image_mid

    def show(self, clock):
        event.clearEvents()

        correct = None
        respRT = np.nan
        KeyResp = None
        Resp = None
        KeyPressTime = np.nan

        self.line.draw()
        self.present_left.draw()
        self.present_right.draw()
        self.present_mid.draw()
        self.window.flip()

        start_trial = clock.getTime()
        trial_clock = core.Clock()
        while KeyResp is None and (trial_clock.getTime() <= self.duration) :
            # get key press and then disappear
            self.line.draw()
            self.present_left.draw()
            self.present_right.draw()
            self.present_mid.draw()
            self.window.flip()

            KeyResp, Resp, KeyPressTime = get_keyboard(
                    clock, self.keylist, self.keyans)

        # get reaction time and key press
        if not np.isnan(KeyPressTime):
            respRT = KeyPressTime - start_trial
        else:
            KeyResp, Resp = 'None', 'None'

        # get correct trials
        if self.ans == 'NA':
            correct = None
        elif self.ans == Resp:
            correct = 1
        else:
            correct = 0

        return start_trial, KeyResp, Resp, KeyPressTime, respRT, correct


class Question(object):
    '''
    collect mind wandering report
    '''
    def __init__(self, window, questions, color):
        '''Initialize a question stimulus.
        Args:
        window - The window object
        questions - a list of dictionaries
        keys - list of keys to press to continue to next stimulus. If None,
                will automatically go to the next stimulus.
        Additional args and kwargs are passed to the visual.TextStim
        constructor.
        '''
        self.window = window
        self.description = visual.TextStim(self.window, text=None, 
        wrapWidth=1100, color=color, font=sans)
        self.scale_l = visual.TextStim(self.window, text=None, 
        wrapWidth=1100, pos=[-300,-150],color=color, font=sans)
        self.scale_h = visual.TextStim(self.window, text=None, 
        wrapWidth=1100, pos=[300,-150],color=color, font=sans)
        self.questions = questions
        self.rating = visual.RatingScale(self.window, low=1, high=10, markerStart=5,
                precision=10, tickMarks=[1, 10], labels=[1, 10],
                leftKeys='left', rightKeys='right', acceptKeys='4')

    def set(self, trial):
        self.description.setText(trial['stimPicMid'])
        self.scale_l.setText(trial['stimPicLeft'])
        self.scale_h.setText(trial['stimPicRight'])
        if trial['stim_duration']:
            self.scale_max_time = trial['stim_duration']
        else:
            self.scale_max_time = 90
        self.rating.markerStart = trial['Ans']  # Ans column for ES marks the random starting point

    def show(self, clock):
        keyState=key.KeyStateHandler()
        self.window.winHandle.push_handlers(keyState)

        self.description.draw()
        self.scale_l.draw()
        self.scale_h.draw()
        self.rating.draw()
        self.window.flip()
        start_trial = clock.getTime()

        pos = self.rating.markerStart
        inc = 0.1

        while (self.rating.noResponse
               and clock.getTime() - start_trial < self.scale_max_time):
            if event.getKeys(keyList=['escape']):
                print('')
                #core.quit()

            if keyState[key._1] is True:
                pos -= inc
            elif keyState[key._2] is True:
                pos += inc

            if pos > 9:
                pos = 9
            elif pos < 0:
                pos = 0

            self.rating.setMarkerPos(pos)
            self.description.draw()
            self.scale_l.draw()
            self.scale_h.draw()
            self.rating.draw()
            self.window.flip()

        score = self.rating.getRating()
        rt = self.rating.getRT()
        self.rating.reset()
        return start_trial, score, rt


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


def quitEXP(endExpNow):
    if endExpNow:
        print('')
        #core.quit()


class instructions1(object):
    '''
    show instruction and wait for trigger
    '''
    def __init__(self, window, settings, instruction_txt, ready_txt):
        self.window = window
        self.settings = settings
        self.env = settings['env']
        self.instruction_txt = load_instruction(instruction_txt)
        self.ready_txt = load_instruction(ready_txt)[0]

        self.display = visual.TextStim(
                window, text='default text', font=sans, height=0.08,
                name='instruction',
                pos=[0,0], wrapWidth=1100,
                color='black',
                ) #object to display instructions

        self.display.size = 0.8
       

    def parse_inst(self):
        '''
        I hard coded the part with text needs changing.
        Will need to change this in the future
        '''
#        self.instruction_txt[2] = self.instruction_txt[2].replace(
#                '{COLOR_REC}', self.settings['rec_color'].upper())
#        self.instruction_txt[2] = self.instruction_txt[2].replace(
#                '{COLOR_LOC}', self.settings['loc_color'].upper())
#        self.instruction_txt[2] = self.instruction_txt[2].replace(
#                '{KEY_REC_0}', self.settings['rec_keys'][0].upper())
#        self.instruction_txt[2] = self.instruction_txt[2].replace(
#                '{KEY_REC_1}', self.settings['rec_keys'][1].upper())
#        self.instruction_txt[2] = self.instruction_txt[2].replace(
#                '{KEY_LOC_0}', self.settings['loc_keys'][0].upper())
#        self.instruction_txt[2] = self.instruction_txt[2].replace(
#                '{KEY_LOC_1}', self.settings['loc_keys'][1].upper())

        self.instruction_txt[2] = self.instruction_txt[2].replace(
                '{0_back_color}', self.settings['0_back_color'].upper())

        self.instruction_txt[2] = self.instruction_txt[2].replace(
                '{1_back_color}', self.settings['1_back_color'].upper())
        
        return self.instruction_txt[2]

    def show(self):
        # get instruction
        
        for i, cur in enumerate(self.instruction_txt):
            self.display.setText(cur)
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
        elif self.env == 'dev':
            event.waitKeys(keyList=[trigger_code])
        else: # not supported
            raise Exception('Unknown environment setting')


def subject_info(experiment_info):
    '''
    get subject information
    return a dictionary
    '''
    dlg_title = '{} subject details:'.format(experiment_info['Experiment'])
    #infoDlg = gui.DlgFromDict(experiment_info, title=dlg_title)

    experiment_info['Date'] = data.getDateStr()

    file_root = ('_').join([experiment_info['Subject'], experiment_info['Run'],
                            experiment_info['Experiment'], experiment_info['Date']])

    # experiment_info['DataFile'] = 'data' + os.path.sep + file_root + '.csv'
    # experiment_info['LogFile'] = 'data' + os.path.sep + file_root + '.log'

    if experiment_info['Environment'] is 'mri':
        experiment_info['MRIFile'] = 'data' + os.path.sep + file_root + '_voltime.csv'

    #if infoDlg.OK:
    return experiment_info
    #else:
        #core.quit()
        #print('User cancelled')


def event_logger(logging_level, LogFile):
    '''
    log events
    '''
    directory = os.path.dirname(LogFile)
    create_dir(directory)

    logging.console.setLevel(logging.WARNING)
    logging.LogFile(LogFile, level=logging_level)


def get_stim_screen(trial, switch_screen, stimulus_screen):
    '''
    trial: dict
        the current trial

    switch_screen: obj
        switch screen object

    stimulus_screen: obj
        stimulus screen object
    '''
    if trial['TrialType'] is 'Switch':
        switch_screen.set_trial(trial)
        return switch_screen
    else:
        stimulus_screen.set_trial(trial)
        return stimulus_screen


def runexp(logfile, expClock, win, writer, resultdict, runtime,dfile,seed):
    writer = writer[0]
    import random
    random.seed(a=seed)
    '''run.py
    build the main program here
    '''
    
    resultdict['Timepoint'], resultdict['Time'] = "0-Back Start", expClock.getTime()
    writer.writerow(resultdict)
    resultdict['Timepoint'], resultdict['Time'] = None,None
    INFO = {
        'Experiment': 'nback_expsampling',  # compulsory
        'Subject': '001',  # compulsory
        'Run': '1',  # compulsory
        'Version': 'A',  # counterbalance the fixation color
        'N-back': '1',  # start the task with 1-back or 0-back
        'Environment': 'lab'  # mri version can be tested on a normal stimuli delivery pc
        }

    # MRI related settings
    dummy_vol = 0
    tr = 2
    trigger_code = '5'

    def run_experiment():
        # collect participant info
        experiment_info = subject_info(INFO)

        # set up enviroment variables and generators
        # set test to False when collecting participant
        settings = get_settings(
                        env=experiment_info['Environment'],
                        ver=experiment_info['Version'], test=False)

        trial_generator, headers = get_trial_generator(experiment_info['N-back'])

        # skip instruction expect run 1
        if experiment_info['Run'] == '1':
            skip_instruction = False
        else:
            skip_instruction = True


        # set log file
        #event_logger(settings['logging_level'], experiment_info['LogFile'])

        # create experiment
        Experiment = Paradigm(win, escape_key='esc', color=0)

        # hide mouse
        event.Mouse(visible=False)

        # put instruction on screen and get trigger
    #    display_instructions(
    #            window=Experiment.window,
    #            settings=settings, skip=skip_instruction)

        instructions01 = instructions1(
            window=Experiment.window, settings=settings,
            instruction_txt=instr_txt1, ready_txt=ready_txt)
        instructions02 = instructions1(
            window=Experiment.window, settings=settings,
            instruction_txt=instr_txt2, ready_txt=ready_txt)
        instructions03 = instructions1(
            window=Experiment.window, settings=settings,
            instruction_txt=instr_txt3, ready_txt=ready_txt)
        instrimg = visual.ImageStim(win,image=(os.path.dirname(os.path.abspath(__file__)) + "//resources//OneBack_Task//1back.jpg"),size=[2,1])
        
        # skip instruction except run 1
        if experiment_info['Run'] == '1':
            instructions01.show()
            instructions02.show()
            instructions03.show()
            instrimg.draw()
            win.flip()
            event.waitKeys(keyList=['return'])
            
        else:
            pass

        # create display screens
        fixation = fixation_cross(window=Experiment.window, color='black')
        stimulus = responsescreen(window=Experiment.window, version=settings)
        
        # question = Question(window=Experiment.window, questions=None, color='white')
        switch = Text(window=Experiment.window, text='Switch', color='black')
        endtxt = open(os.path.dirname(os.path.abspath(__file__)) + '//resources//ZeroBack_Task//end_instr.txt', 'r').read().split('#\n')[0]
        end_msg = visual.TextStim(Experiment.window, text=endtxt, color='black',
                                wrapWidth=1100)
        

        # generate trials
        Experiment.trials = next(trial_generator)
        listof = []
        if not trial_generator.gi_frame.f_locals.get('run') == None:
            noGoCount = 0
            for test in trial_generator.gi_frame.f_locals.get('run'):
                if test['TrialType'] == 'ExpSample':
                    continue

                if test['TrialType'] == 'NoGo':
                    noGoCount += 1
                else:
                    noGoCount = 0
                
                if noGoCount > 8:
                    continue

                listof.append(test)
        import random
        block_a = random.sample(listof, int(len(listof)/2))
        for val in block_a:
                        listof[:] = [x for x in listof if x != val]
        block_b = listof
        if dfile == 'A':
            Experiment.trials = block_a
        if dfile == 'B':
            Experiment.trials = block_b
            #if test
        nogolis = []
        zbacklis = []
        finallist = []
        for trl in Experiment.trials:
            if trl['TrialType'] == 'NoGo':
                nogolis.append(trl)
            if trl['TrialType'] == 'OneBack':
                zbacklis.append(trl)
            c = 0
            cvt = 0
        zbacklis.extend(zbacklis)
        zbacklis.extend(zbacklis)
        zbacklis.extend(zbacklis)
        zbacklis.extend(zbacklis)
        zbacklis.extend(zbacklis)
        for enb, bm in enumerate(nogolis):
            if enb == 0:
                c = random.randint(3,6)
            if c != 0:
                c = c - 1
                finallist.append(bm)
            if c == 0:
                #old version
                #tmper = zbacklis[cvt]
                #NEW VERSION:
                tmper = zbacklis[cvt].copy()
                #del tmper['TrialIndex']
                if tmper["Ans"] == "right":
                    tmper['stimPicMid'] = finallist[-1]["stimPicRight"]
                if tmper["Ans"] == "left":
                    tmper['stimPicMid'] = finallist[-1]["stimPicLeft"]
                finallist.append(tmper)
                c = random.randint(3,6)
                cvt = cvt + 1
                # if cvt == 6:
                #     cvt = 0
        Experiment.trials = finallist  
        debugmode = False
        if debugmode == True:
            
            with open("C:/Users/Ian/Documents/GitHub/THINCLabTestRepo/Analysis/oneback.csv","a",newline="") as frdt:
                writerd = csv.writer(frdt)
                for row in finallist:
                    writerd.writerow(row.values())
                
        
        # get a global clock
        timer = expClock

        # dummy volumes
        if experiment_info['Environment'] is 'mri':
            fixation.set_trial({'fix_duration': tr * dummy_vol})
            t = fixation.show(timer)
            

        # get a global clock
        #timer = time
        trialclock = core.Clock()

        for enum, trial in enumerate(Experiment.trials):
            
            if trialclock.getTime() < runtime:
                # parse tuples to proper file names
                trial = parse_stimulus_name(trial)
                # prepare fixation cross and stimulus display
                fixation.set_trial(trial)
                fix_t = fixation.show(timer)
                

                if trial['TrialType'] == 'ExpSample':
                    pass
                        
                else:
                    # show stimulus screen and catch response
                    stim = get_stim_screen(trial, switch, stimulus)
                    resultdict['Timepoint'], resultdict['Time'], resultdict['Auxillary Data'] = trial['TrialType'] + "Stimulus Start", expClock.getTime(), trial['Condition']
                    writer.writerow(resultdict)
                    resultdict['Timepoint'], resultdict['Time'], resultdict['Auxillary Data'] = None,None, None
                    stim_t, KeyResp, Resp, KeyPressTime, respRT, correct = stim.show(timer)
                    iscorrect = []
                    #a = trial['Ans']
                    if trial['Ans'] == KeyResp:
                        iscorrect = True
                    elif trial['Ans'] == 'NA' and KeyResp == 'None':
                        iscorrect = True
                    else:
                        iscorrect = False
                    resultdict['Timepoint'], resultdict['Time'], resultdict['Response_Key'], resultdict['Auxillary Data'], resultdict['Is_correct'] = trial['TrialType'] + "Stimulus End", expClock.getTime(), KeyResp, trial['Condition'], iscorrect
                    writer.writerow(resultdict)
                    resultdict['Timepoint'], resultdict['Time'], resultdict['Response_Key'], resultdict['Auxillary Data'], resultdict['Is_correct'] = None,None,None,None,None
                    

                # post response fixation
                if respRT and trial['stim_duration'] - respRT > 0:
                    fixation.duration = trial['stim_duration'] - respRT
                    
                    _ = fixation.show(timer)
                    

                # dump information to trial
                trial['fixStart'] = fix_t
                trial['stimStart'] = stim_t
                trial['keyResp'] = KeyResp
                trial['resp'] = Resp
                trial['respCORR'] = correct
                trial['respRT'] = respRT
                trial['IDNO'] = experiment_info['Subject']
                trial['Run'] = experiment_info['Run']

                # write to csv
                #write_csv(experiment_info['DataFile'], headers, trial)

                # clear answers
                KeyResp = None
                correct = None
                respRT = None

        # ending message
        # end_msg.draw()
        Experiment.window.flip()
        # event.waitKeys(keyList=['return'])

        logging.flush()
        # change output files to read only
        #read_only(experiment_info['DataFile'])
        #read_only(experiment_info['LogFile'])
        # quit
        #Experiment.window.close()
        #core.quit()

    # now run this thing
    # if __name__ == "__main__":
    #     # set working directory as the location of this file
    #     _thisDir = os.path.dirname(os.path.abspath(__file__))
    #     os.chdir(_thisDir)

    run_experiment()

# logfile = "C://Users//Ian//Documents//GitHub//THINCLabTestRepo//TaskFiles//log_file//testfull2.csv"
# f = open(logfile, 'w')
# resultdict = {'Timepoint': None, 'Time': None, 'Is_correct': None, 'Experience Sampling Question': None, 'Experience Sampling Response':None, 'Task' : None, 'Task Iteration': None, 'Participant ID': None,'Response_Key':None, 'Auxillary Data': None}
# writer = csv.DictWriter(f, fieldnames=resultdict)
# numtrial = 10
# runtime = 100
# win = visual.Window(size=(1280, 800),color='white', winType='pyglet')
# expClock = core.Clock()
# runexp(logfile, expClock, win, writer, resultdict, numtrial, runtime)