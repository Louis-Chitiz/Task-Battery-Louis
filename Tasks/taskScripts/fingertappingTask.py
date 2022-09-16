#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2021.2.3),
    on September 20, 2021, at 20:59
If you publish work using this script the most relevant publication is:

    Peirce J, Gray JR, Simpson S, MacAskill M, Höchenberger R, Sogo H, Kastman E, Lindeløv JK. (2019) 
        PsychoPy2: Experiments in behavior made easy Behav Res 51: 195. 
        https://doi.org/10.3758/s13428-018-01193-y

"""

from __future__ import absolute_import, division

from psychopy import locale_setup
from psychopy import prefs
from psychopy import sound, gui, visual, core, data, event, logging, clock, colors
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)

import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle, choice 
import os  # handy system and path functions
import sys  # to get file system encoding
import csv

from psychopy.hardware import keyboard



# Ensure that relative paths start from the same directory as this script

def runexp(filename, timer, win, writer, resultdict, runtime,dfile,seed):
    writer = writer[0]
    import random
    random.seed(a=seed)
    win.flip()
    # Ensure that relative paths start from the same directory as this script
    

    # Store info about the experiment session
    psychopyVersion = '2021.2.3'
    expName = 'FingTap'  # from the Builder filename that created this script
    expInfo = {'session': '001', 'participant': ''}
    dlg = expInfo
    # dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expName)
    # if dlg.OK == False:
    #     core.quit()  # user pressed cancel
    expInfo['date'] = data.getDateStr()  # add a simple timestamp
    expInfo['expName'] = expName
    expInfo['psychopyVersion'] = psychopyVersion

    # Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc


    # An ExperimentHandler isn't essential but helps with data saving
    thisExp = data.ExperimentHandler(name=expName, version='',
        extraInfo=expInfo, runtimeInfo=None,
        originPath='C:\\Users\\Ian\\Documents\\TaskRepo\\Basic_fMRI_Test_programs\\FingTap.py',
        savePickle=False, saveWideText=False,
     autoLog=False)
    # save a log file for detail verbose info
    #logFile = logging.LogFile(filename+'.log', level=logging.EXP)
    logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file
    endExpNow = False  # flag for 'escape' or other condition => quit the exp
    frameTolerance = 0.001  # how close to onset before 'same' frame

    # Start Code - component code to be run after the window creation

    # Setup the Window
    #win = visual.Window(
    #    size=[1200, 720], fullscr=False, screen=0, 
    #    winType='pyglet', allowGUI=False, allowStencil=False,
    #    monitor='testMonitor', color=[-1,-1,-1], colorSpace='rgb',
    #    blendMode='avg', useFBO=True, 
    #    units='deg')
    # store frame rate of monitor if we can measure it
    expInfo['frameRate'] = win.getActualFrameRate()
    if expInfo['frameRate'] != None:
        frameDur = 1.0 / round(expInfo['frameRate'])
    else:
        frameDur = 1.0 / 60.0  # could not measure, so guess

    # Setup eyetracking
    ioDevice = ioConfig = ioSession = ioServer = eyetracker = None

    # create a default keyboard (e.g. to check for escape)
    defaultKeyboard = keyboard.Keyboard(bufferSize=1000000)

    # Initialize components for Routine "Trigger"
    TriggerClock = core.Clock()
    with open(os.path.dirname(os.path.abspath(__file__)) + "//resources//Fingertapping_Task//Fingertapping_instr1.txt") as f:
        lines1 = f.read()
    text1 = visual.TextStim(win=win, name='text',
        text=lines1,
        font='Arial',
        units='norm', anchorHoriz='center', anchorVert='center', wrapWidth=2, ori=0, 
        color='black', colorSpace='rgb', opacity=1, 
        languageStyle='LTR',
        depth=0.0)
    with open(os.path.dirname(os.path.abspath(__file__)) + "//resources//Fingertapping_Task//Fingertapping_instr2.txt") as f:
        lines2 = f.read()
    text2 = visual.TextStim(win=win, name='text',
        text=lines2,
        font='Arial',
        units='norm', anchorHoriz='center', anchorVert='center', wrapWidth=2, ori=0, 
        color='black', colorSpace='rgb', opacity=1, 
        languageStyle='LTR',
        depth=0.0)
    with open(os.path.dirname(os.path.abspath(__file__)) + "//resources//Fingertapping_Task//Fingertapping_instr3.txt") as f:
        lines3 = f.read()
    text3 = visual.TextStim(win=win, name='text',
        text=lines3,
        font='Arial',
        units='norm', anchorHoriz='center', anchorVert='center', wrapWidth=2, ori=0, 
        color='black', colorSpace='rgb', opacity=1, 
        languageStyle='LTR',
        depth=0.0)
    key_resp_2 = keyboard.Keyboard(bufferSize=1000000)
    mouse = event.Mouse(win=win)
    x, y = [None, None]
    mouse.mouseClock = core.Clock()

    # Initialize components for Routine "Finger_tap"
    Finger_tapClock = core.Clock()
    text_2 = visual.TextStim(win=win, name='text_2',
        text='Tap the fingers of your right hand',
        font='Arial',
        anchorHoriz='center', anchorVert='center', wrapWidth=None, ori=0, 
        color='black', colorSpace='rgb', opacity=1, 
        languageStyle='LTR',
        depth=0.0);

    # Initialize components for Routine "Tap"
    TapClock = core.Clock()
    polygon = visual.Rect(
        win=win, name='polygon',
        size=400, units='pix',
        ori=0.0, pos=(0, 0),
        lineWidth=1.0,     colorSpace='rgb',  lineColor='black', fillColor='black',
        opacity=None, depth=0.0, interpolate=True)
    key_resp = keyboard.Keyboard(bufferSize=1000000)

    # Initialize components for Routine "Blank"
    BlankClock = core.Clock()
    text_4 = visual.TextStim(win=win, name='text_4',
        text='+',
        font='Arial',
        pos=[0, 0], anchorHoriz='center', anchorVert='center', wrapWidth=None, ori=0, 
        color='black', colorSpace='rgb', opacity=1, 
        languageStyle='LTR',
        depth=0.0);

    # Initialize components for Routine "Blank"
    BlankClock = core.Clock()
    text_4 = visual.TextStim(win=win, name='text_4',
        text='+',
        font='Arial',
        pos=[0, 0], anchorHoriz='center', anchorVert='center', wrapWidth=None, ori=0, 
        color='black', colorSpace='rgb', opacity=1, 
        languageStyle='LTR',
        depth=0.0);

    # Create some handy timers
    globalClock = timer  # to track the time since experiment started
    routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 

    # ------Prepare to start Routine "Trigger"-------
    continueRoutine = True
    # update component parameters for each repeat
    key_resp_2.keys = []
    key_resp_2.rt = []
    _key_resp_2_allKeys = []
    # setup some python lists for storing info about the mouse
    gotValidClick = False  # until a click is received
    mouse.mouseClock.reset()
    # keep track of which components have finished
    TriggerComponents = [text1, key_resp_2, mouse]
    for thisComponent in TriggerComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    TriggerClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1
    import time
    #win.flip()
    win.flip()
    text1.draw(win)
    win.flip()
    time.sleep(1)
    event.waitKeys(keyList=['return'])
    win.flip()
    text2.draw(win)
    win.flip()
    time.sleep(1)
    event.waitKeys(keyList=['return'])
    win.flip()
    text3.draw(win)
    win.flip()
    time.sleep(1)
    event.waitKeys(keyList=['return'])
    
    # -------Run Routine "Trigger"-------
    # while continueRoutine:
    #     # get current time
    #     t = TriggerClock.getTime()
    #     tThisFlip = win.getFutureFlipTime(clock=TriggerClock)
    #     tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    #     frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    #     # update/draw components on each frame

    #     # *text* updates
    #     # if text1.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
    #     #     # keep track of start time/frame for later
    #     #     text1.frameNStart = frameN  # exact frame index
    #     #     text1.tStart = t  # local t and not account for scr refresh
    #     #     text1.tStartRefresh = tThisFlipGlobal  # on global time
    #     #     win.timeOnFlip(text1, 'tStartRefresh')  # time at next scr refresh
    #     #     text1.setAutoDraw(True)

    #     # *key_resp_2* updates
    #     waitOnFlip = False
        
    #     if key_resp_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
    #         # keep track of start time/frame for later
    #         key_resp_2.frameNStart = frameN  # exact frame index
    #         key_resp_2.tStart = t  # local t and not account for scr refresh
    #         key_resp_2.tStartRefresh = tThisFlipGlobal  # on global time
    #         win.timeOnFlip(key_resp_2, 'tStartRefresh')  # time at next scr refresh
    #         key_resp_2.status = STARTED
    #         # keyboard checking is just starting
    #         waitOnFlip = True
    #         win.callOnFlip(key_resp_2.clock.reset)  # t=0 on next screen flip
    #         win.callOnFlip(key_resp_2.clearEvents, eventType='keyboard')  # clear events on next screen flip
    #     if key_resp_2.status == STARTED and not waitOnFlip:
    #         theseKeys = key_resp_2.getKeys(keyList=['return'], waitRelease=False)
    #         _key_resp_2_allKeys.extend(theseKeys)
    #         if len(_key_resp_2_allKeys):
    #             key_resp_2.keys = _key_resp_2_allKeys[-1].name  # just the last key pressed
    #             key_resp_2.rt = _key_resp_2_allKeys[-1].rt
    #             # a response ends the routine
    #             continueRoutine = False
    #     # *mouse* updates
    #     if mouse.status == NOT_STARTED and t >= 0.0-frameTolerance:
    #         # keep track of start time/frame for later
    #         mouse.frameNStart = frameN  # exact frame index
    #         mouse.tStart = t  # local t and not account for scr refresh
    #         mouse.tStartRefresh = tThisFlipGlobal  # on global time
    #         win.timeOnFlip(mouse, 'tStartRefresh')  # time at next scr refresh
    #         mouse.status = STARTED
    #         prevButtonState = mouse.getPressed()  # if button is down already this ISN'T a new click
    #     if mouse.status == STARTED:  # only update if started and not finished!
    #         buttons = mouse.getPressed()
    #         if buttons != prevButtonState:  # button state changed?
    #             prevButtonState = buttons
    #             if sum(buttons) > 0:  # state changed to a new click
    #                 # abort routine on response
    #                 continueRoutine = False
        
    #     # check for quit (typically the Esc key)
    #     #if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
    #         #core.quit()

    #     # check if all components have finished
    #     if not continueRoutine:  # a component has requested a forced-end of Routine
    #         break
    #     continueRoutine = False  # will revert to True if at least one component still running
    #     for thisComponent in TriggerComponents:
    #         if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
    #             continueRoutine = True
    #             break  # at least one component has not yet finished

    #     # refresh the screen
    #     if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
    #         win.flip()
    #         event.waitKeys(keyList=['return'])

    # # -------Ending Routine "Trigger"-------
    # for thisComponent in TriggerComponents:
    #     if hasattr(thisComponent, "setAutoDraw"):
    #         thisComponent.setAutoDraw(False)
    resultdict['Timepoint'], resultdict['Time'] = 'Finger Tapping Start', timer.getTime()
    writer.writerow(resultdict)
    resultdict['Timepoint'], resultdict['Time'] = None,None
    thisExp.addData('text.started', text1.tStartRefresh)
    thisExp.addData('text.stopped', text1.tStopRefresh)
    # check responses
    if key_resp_2.keys in ['', [], None]:  # No response was made
        key_resp_2.keys = None
    thisExp.addData('key_resp_2.keys',key_resp_2.keys)
    if key_resp_2.keys != None:  # we had a response
        thisExp.addData('key_resp_2.rt', key_resp_2.rt)
    thisExp.addData('key_resp_2.started', key_resp_2.tStartRefresh)
    thisExp.addData('key_resp_2.stopped', key_resp_2.tStopRefresh)
    thisExp.nextEntry()
    # store data for thisExp (ExperimentHandler)
    x, y = mouse.getPos()
    buttons = mouse.getPressed()
    thisExp.addData('mouse.x', x)
    thisExp.addData('mouse.y', y)
    thisExp.addData('mouse.leftButton', buttons[0])
    thisExp.addData('mouse.midButton', buttons[1])
    thisExp.addData('mouse.rightButton', buttons[2])
    thisExp.addData('mouse.started', mouse.tStart)
    thisExp.addData('mouse.stopped', mouse.tStop)
    thisExp.nextEntry()
    # the Routine "Trigger" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()

    # set up handler to look after randomisation of conditions etc
    trials = data.TrialHandler(nReps=100, method='random', 
        extraInfo=expInfo, originPath=-1,
        trialList=[None],
        seed=None, name='trials')
    thisExp.addLoop(trials)  # add the loop to the experiment
    thisTrial = trials.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
    if thisTrial != None:
        for paramName in thisTrial:
            exec('{} = thisTrial[paramName]'.format(paramName))
    trialtimer = core.MonotonicClock()
    for thisTrial in trials:
        if trialtimer.getTime() <= runtime:
            resultdict['Timepoint'], resultdict['Time'] = 'Finger Tapping Block Start', timer.getTime()
            writer.writerow(resultdict)
            resultdict['Timepoint'], resultdict['Time'] = None,None
            currentLoop = trials
            # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
            if thisTrial != None:
                for paramName in thisTrial:
                    exec('{} = thisTrial[paramName]'.format(paramName))

            # ------Prepare to start Routine "Finger_tap"-------
            continueRoutine = True
            routineTimer.add(5.000000)
            # update component parameters for each repeat
            # keep track of which components have finished
            text_2.setText(np.random.choice(["Now tap in time with the black square using you left hand","Now tap in time with the black square using you right hand"])) 
            Finger_tapComponents = [text_2]
            for thisComponent in Finger_tapComponents:
                thisComponent.tStart = None
                thisComponent.tStop = None
                thisComponent.tStartRefresh = None
                thisComponent.tStopRefresh = None
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            # reset timers
            t = 0
            _timeToFirstFrame = win.getFutureFlipTime(clock="now")
            Finger_tapClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
            frameN = -1

            # -------Run Routine "Finger_tap"-------
            while continueRoutine and routineTimer.getTime() > 0:
                # get current time
                
                t = Finger_tapClock.getTime()
                tThisFlip = win.getFutureFlipTime(clock=Finger_tapClock)
                tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame

                # *text_2* updates
                if text_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                    # keep track of start time/frame for later
                    text_2.frameNStart = frameN  # exact frame index
                    text_2.tStart = t  # local t and not account for scr refresh
                    text_2.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(text_2, 'tStartRefresh')  # time at next scr refresh
                    text_2.setAutoDraw(True)
                if text_2.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > text_2.tStartRefresh + 3-frameTolerance:
                        # keep track of stop time/frame for later
                        text_2.tStop = t  # not accounting for scr refresh
                        text_2.frameNStop = frameN  # exact frame index
                        win.timeOnFlip(text_2, 'tStopRefresh')  # time at next scr refresh
                        text_2.setAutoDraw(False)

                # check for quit (typically the Esc key)
                #if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                    #core.quit()

                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in Finger_tapComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished

                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()

            # -------Ending Routine "Finger_tap"-------
            for thisComponent in Finger_tapComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            trials.addData('text_2.started', text_2.tStartRefresh)
            trials.addData('text_2.stopped', text_2.tStopRefresh)

            # set up handler to look after randomisation of conditions etc
            trials_2 = data.TrialHandler(nReps=5.0, method='random', 
                extraInfo=expInfo, originPath=-1,
                trialList=[None],
                seed=None, name='trials_2')
            thisExp.addLoop(trials_2)  # add the loop to the experiment
            thisTrial_2 = trials_2.trialList[0]  # so we can initialise stimuli with some values
            # abbreviate parameter names if possible (e.g. rgb = thisTrial_2.rgb)
            if thisTrial_2 != None:
                for paramName in thisTrial_2:
                    exec('{} = thisTrial_2[paramName]'.format(paramName))

            for thisTrial_2 in trials_2:
                currentLoop = trials_2
                # abbreviate parameter names if possible (e.g. rgb = thisTrial_2.rgb)
                if thisTrial_2 != None:
                    for paramName in thisTrial_2:
                        exec('{} = thisTrial_2[paramName]'.format(paramName))

                # ------Prepare to start Routine "Tap"-------
                continueRoutine = True
                routineTimer.add(5.000000)
                # update component parameters for each repeat
                key_resp.keys = []
                key_resp.rt = []
                _key_resp_allKeys = []
                # keep track of which components have finished
                TapComponents = [polygon, key_resp]
                for thisComponent in TapComponents:
                    thisComponent.tStart = None
                    thisComponent.tStop = None
                    thisComponent.tStartRefresh = None
                    thisComponent.tStopRefresh = None
                    if hasattr(thisComponent, 'status'):
                        thisComponent.status = NOT_STARTED
                # reset timers
                t = 0
                _timeToFirstFrame = win.getFutureFlipTime(clock="now")
                TapClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
                frameN = -1

                # -------Run Routine "Tap"-------
                while continueRoutine and routineTimer.getTime() > 0:
                    # get current time
                    t = TapClock.getTime()
                    tThisFlip = win.getFutureFlipTime(clock=TapClock)
                    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                    # update/draw components on each frame

                    # *polygon* updates
                    if polygon.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                        # keep track of start time/frame for later
                        polygon.frameNStart = frameN  # exact frame index
                        polygon.tStart = t  # local t and not account for scr refresh
                        polygon.tStartRefresh = tThisFlipGlobal  # on global time
                        win.timeOnFlip(polygon, 'tStartRefresh')  # time at next scr refresh
                        polygon.setAutoDraw(True)
                    if polygon.status == STARTED:
                        # is it time to stop? (based on global clock, using actual start)
                        if tThisFlipGlobal > polygon.tStartRefresh + 5-frameTolerance:
                            # keep track of stop time/frame for later
                            polygon.tStop = t  # not accounting for scr refresh
                            polygon.frameNStop = frameN  # exact frame index
                            win.timeOnFlip(polygon, 'tStopRefresh')  # time at next scr refresh
                            polygon.setAutoDraw(False)

                    # *key_resp* updates
                    waitOnFlip = False
                    if key_resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                        # keep track of start time/frame for later
                        key_resp.frameNStart = frameN  # exact frame index
                        key_resp.tStart = t  # local t and not account for scr refresh
                        key_resp.tStartRefresh = tThisFlipGlobal  # on global time
                        win.timeOnFlip(key_resp, 'tStartRefresh')  # time at next scr refresh
                        key_resp.status = STARTED
                        # keyboard checking is just starting
                        waitOnFlip = True
                        win.callOnFlip(key_resp.clock.reset)  # t=0 on next screen flip
                        win.callOnFlip(key_resp.clearEvents, eventType='keyboard')
                        resultdict['Timepoint'], resultdict['Time'] = 'Finger Tapping Trial Start', timer.getTime()
                        writer.writerow(resultdict)
                        resultdict['Timepoint'], resultdict['Time'] = None,None  # clear events on next screen flip
                    if key_resp.status == STARTED:
                        # is it time to stop? (based on global clock, using actual start)
                        if tThisFlipGlobal > key_resp.tStartRefresh + 5-frameTolerance:
                            # keep track of stop time/frame for later
                            key_resp.tStop = t  # not accounting for scr refresh
                            key_resp.frameNStop = frameN  # exact frame index
                            win.timeOnFlip(key_resp, 'tStopRefresh')  # time at next scr refresh
                            key_resp.status = FINISHED
                    if key_resp.status == STARTED and not waitOnFlip:
                        theseKeys = key_resp.getKeys(keyList=['space'], waitRelease=False)
                        _key_resp_allKeys.extend(theseKeys)
                        if len(_key_resp_allKeys):
                            key_resp.keys = _key_resp_allKeys[-1].name  # just the last key pressed
                            key_resp.rt = _key_resp_allKeys[-1].rt
                            # a response ends the routine
                            continueRoutine = False

                    # check for quit (typically the Esc key)
                    #if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                        #core.quit()

                    # check if all components have finished
                    if not continueRoutine:  # a component has requested a forced-end of Routine
                        break
                    continueRoutine = False  # will revert to True if at least one component still running
                    for thisComponent in TapComponents:
                        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                            continueRoutine = True
                            break  # at least one component has not yet finished

                    # refresh the screen
                    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                        win.flip()

                # -------Ending Routine "Tap"-------
                for thisComponent in TapComponents:
                    if hasattr(thisComponent, "setAutoDraw"):
                        thisComponent.setAutoDraw(False)
                trials_2.addData('polygon.started', polygon.tStartRefresh)
                trials_2.addData('polygon.stopped', polygon.tStopRefresh)
                # check responses
                if key_resp.keys in ['', [], None]:  # No response was made
                    key_resp.keys = None
                    iscorrect = False
                trials_2.addData('key_resp.keys',key_resp.keys)
                if key_resp.keys != None:  # we had a response
                    trials_2.addData('key_resp.rt', key_resp.rt)
                    iscorrect = True
                
                trials_2.addData('key_resp.started', key_resp.tStartRefresh)
                trials_2.addData('key_resp.stopped', key_resp.tStopRefresh)
                
                resultdict['Timepoint'], resultdict['Time'], resultdict['Is_correct'] = 'Finger Tapping Trial End', timer.getTime(), iscorrect
                writer.writerow(resultdict)
                resultdict['Timepoint'], resultdict['Time'], resultdict['Is_correct'] = None,None,None
                

                # ------Prepare to start Routine "Blank"-------
                continueRoutine = True
                # update component parameters for each repeat
                stimulus_interval = randint(low = 1, high = 5)
                thisExp.addData('stimulus_interval', stimulus_interval)
                # keep track of which components have finished
                BlankComponents = [text_4]
                for thisComponent in BlankComponents:
                    thisComponent.tStart = None
                    thisComponent.tStop = None
                    thisComponent.tStartRefresh = None
                    thisComponent.tStopRefresh = None
                    if hasattr(thisComponent, 'status'):
                        thisComponent.status = NOT_STARTED
                # reset timers
                t = 0
                _timeToFirstFrame = win.getFutureFlipTime(clock="now")
                BlankClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
                frameN = -1

                # -------Run Routine "Blank"-------
                while continueRoutine:
                    # get current time
                    t = BlankClock.getTime()
                    tThisFlip = win.getFutureFlipTime(clock=BlankClock)
                    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                    # update/draw components on each frame

                    # *text_4* updates
                    if text_4.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                        # keep track of start time/frame for later
                        text_4.frameNStart = frameN  # exact frame index
                        text_4.tStart = t  # local t and not account for scr refresh
                        text_4.tStartRefresh = tThisFlipGlobal  # on global time
                        win.timeOnFlip(text_4, 'tStartRefresh')  # time at next scr refresh
                        text_4.setAutoDraw(True)
                    if text_4.status == STARTED:
                        # is it time to stop? (based on global clock, using actual start)
                        if tThisFlipGlobal > text_4.tStartRefresh + stimulus_interval-frameTolerance:
                            # keep track of stop time/frame for later
                            text_4.tStop = t  # not accounting for scr refresh
                            text_4.frameNStop = frameN  # exact frame index
                            win.timeOnFlip(text_4, 'tStopRefresh')  # time at next scr refresh
                            text_4.setAutoDraw(False)

                    # check for quit (typically the Esc key)
                    #if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                        #core.quit()

                    # check if all components have finished
                    if not continueRoutine:  # a component has requested a forced-end of Routine
                        break
                    continueRoutine = False  # will revert to True if at least one component still running
                    for thisComponent in BlankComponents:
                        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                            continueRoutine = True
                            break  # at least one component has not yet finished

                    # refresh the screen
                    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                        win.flip()

                # -------Ending Routine "Blank"-------
                for thisComponent in BlankComponents:
                    if hasattr(thisComponent, "setAutoDraw"):
                        thisComponent.setAutoDraw(False)
                trials_2.addData('text_4.started', text_4.tStartRefresh)
                trials_2.addData('text_4.stopped', text_4.tStopRefresh)
                #resultdict['Timepoint'], resultdict['Time'] = 'square stimulus ended', text_4.tStartRefresh
                #writer.writerow(resultdict) 
                
                #f.writerow()
                stimulus_interval = randint(low = 1, high = 5)
                thisExp.addData('stimulus_interval', stimulus_interval)
                # the Routine "Blank" was not non-slip safe, so reset the non-slip timer
                routineTimer.reset()
                thisExp.nextEntry()

            # completed 5.0 repeats of 'trials_2'


            # ------Prepare to start Routine "Blank"-------
            continueRoutine = True
            # update component parameters for each repeat
            stimulus_interval = randint(low = 1, high = 5)
            thisExp.addData('stimulus_interval', stimulus_interval)
            # keep track of which components have finished
            BlankComponents = [text_4]
            for thisComponent in BlankComponents:
                thisComponent.tStart = None
                thisComponent.tStop = None
                thisComponent.tStartRefresh = None
                thisComponent.tStopRefresh = None
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            # reset timers
            t = 0
            _timeToFirstFrame = win.getFutureFlipTime(clock="now")
            BlankClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
            frameN = -1

            # -------Run Routine "Blank"-------
            while continueRoutine:
                # get current time
                t = BlankClock.getTime()
                tThisFlip = win.getFutureFlipTime(clock=BlankClock)
                tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame

                # *text_4* updates
                if text_4.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                    # keep track of start time/frame for later
                    text_4.frameNStart = frameN  # exact frame index
                    text_4.tStart = t  # local t and not account for scr refresh
                    text_4.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(text_4, 'tStartRefresh')  # time at next scr refresh
                    text_4.setAutoDraw(True)
                if text_4.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > text_4.tStartRefresh + stimulus_interval-frameTolerance:
                        # keep track of stop time/frame for later
                        text_4.tStop = t  # not accounting for scr refresh
                        text_4.frameNStop = frameN  # exact frame index
                        win.timeOnFlip(text_4, 'tStopRefresh')  # time at next scr refresh
                        text_4.setAutoDraw(False)

                # check for quit (typically the Esc key)
                #if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                    #core.quit()

                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in BlankComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished

                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()

            # -------Ending Routine "Blank"-------
            for thisComponent in BlankComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            trials.addData('text_4.started', text_4.tStartRefresh)
            trials.addData('text_4.stopped', text_4.tStopRefresh)
            stimulus_interval = randint(low = 1, high = 5)
            thisExp.addData('stimulus_interval', stimulus_interval)
            # the Routine "Blank" was not non-slip safe, so reset the non-slip timer
            routineTimer.reset()
            thisExp.nextEntry()

    # completed 10 repeats of 'trials'


    # Flip one final time so any remaining win.callOnFlip() 
    # and win.timeOnFlip() tasks get executed before quitting
    win.flip()

    # these shouldn't be strictly necessary (should auto-save)
    #thisExp.saveAsWideText(filename+'.csv', delim='auto')
    #thisExp.saveAsPickle(filename)
    logging.flush()
    # make sure everything is closed down
    thisExp.abort()  # or data files will save again on exit
    #win.close()
    #core.quit()

