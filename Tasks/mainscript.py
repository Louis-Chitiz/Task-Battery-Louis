
# Main script written by Ian Goodall-Halliwell. Subscripts are individually credited. Many have been extensively modified, for better or for worse (probably for worse o__o ).



from psychopy import core, visual, gui, event

import time
import csv

import yaml
#from Tasks.taskScripts import memoryTask
import taskScripts
import os
import random
os.chdir(os.path.dirname(os.path.realpath(__file__)))
if not os.path.exists(os.path.join(os.getcwd(),"log_file")):
        os.mkdir(os.path.join(os.getcwd(),"log_file"))
# This class is responsible for creating and holding the information about how each task should run.
# It contains the number of repetitions and a global runtime variable.
# It also contains the subject ID, and will eventually use the experiment seed to randomize trial order.
class metadatacollection():
        def __init__(self,INFO):#, main_log_location):
                self.INFO = INFO
                #self.main_log_location = main_log_location

                # Don't really know what this is, best to leave it be probably
                self.sbINFO = "Test"


        # This opens the GUI        
        def rungui(self):
                self.sbINFO = gui.DlgFromDict(self.INFO)

        # This writes info collected from the GUI into the logfile
        def collect_metadata(self):  
                print(self.sbINFO.data)
                if os.path.exists(os.path.join(os.getcwd()+self.sbINFO.data[1])): 
                        os.remove(os.path.join(os.getcwd()+self.sbINFO.data[1]))
                if not os.path.exists(os.path.join(os.getcwd(),'log_file')):
                        os.mkdir(os.path.join(os.getcwd(),'log_file'))
                f = open(os.path.join(os.getcwd() + '/log_file/output_log_{}_{}_full.csv'.format(self.sbINFO.data[1],self.INFO['Experiment Seed'])), 'w', newline='')
                fq = open(os.path.join(os.getcwd() + '/log_file/output_log_{}_{}.csv'.format(self.sbINFO.data[1],self.INFO['Experiment Seed'])), 'w', newline='')
                metawriter = csv.writer(f)
                metawriter2 = csv.writer(fq)
                metawriter.writerow(["METADATA:"])
                metawriter.writerow(self.sbINFO.inputFieldNames)
                metawriter.writerow(self.sbINFO.data)
                metawriter2.writerow(["METADATA:"])
                metawriter2.writerow(self.sbINFO.inputFieldNames)
                metawriter2.writerow(self.sbINFO.data)
                random.seed(a=int(metacoll.INFO['Experiment Seed']))
                metawriter.writerow(["Time after setup", taskbattery.time.getTime()])
                metawriter2.writerow(["Time after setup",taskbattery.time.getTime()])
                writer = csv.DictWriter(f, fieldnames=taskbattery.resultdict)
                writer.writeheader()
                writer2 = csv.DictWriter(fq, fieldnames=taskbattery.resultdict)
                writer2.writeheader()
                f.close()
                fq.close()
        
        
# Creates a list of all the tasks, and allows you to iterate through them without closing the window
class taskbattery(metadatacollection):
        time = core.Clock()
        resultdict = {'Timepoint': None, 'Time': None, 'Is_correct': None, 'Experience Sampling Question': None, 'Experience Sampling Response':None, 'Task' : None, 'Task Iteration': None, 'Participant ID': None, 'Response_Key':None, 'Auxillary Data': None, 'Assoc Task':None}
        #self.win = visual.Window(size=(1280, 800),color='white', winType='pyglet',fullscr=True)
        def __init__(self, tasklist, ESQtask, INFO):
                self.tasklist = tasklist
                taskbattery.ESQtask = ESQtask
                self.INFO = INFO
                self.taskexeclist = []
                self.win = visual.Window(size=(1440, 960),color='white', winType='pyglet',fullscr=True)
                self.text = text_2 = visual.TextStim(win=self.win, name='text_2',
                        text='Welcome to our experiment. \n Please follow the instructions on-screen and notify the attending researcher if anything is unclear \n We are thankful for your participation. \n Press <return/enter> to continue.',
                        font='Arial',
                        anchorHoriz='center', anchorVert='center', wrapWidth=None, ori=0, 
                        color='black', colorSpace='rgb', opacity=1, 
                        languageStyle='LTR',
                        depth=0.0)
                taskbattery.win = self.win
        
        
        #def initializeBattery(self):
                #for i in self.tasklist:

        def run_battery(self):
                self.text.draw(self.win)
                self.win.flip()
                time.sleep(1)
                event.waitKeys(keyList=['return'])
                self.win.flip()
                
                
                for en,i in enumerate(self.tasklist):
                        os.chdir(os.getcwd())
                        i.show()
                        i.run()
                        pp = len(self.tasklist)
                        if en < len(self.tasklist):
                                i.end()
                        
                        
#OPEN THE TRIAL FILES AND CUT THEM INTO BLOCKS

# This creates a class which feeds all the necessary information into the task functions imported from each task file
# Allows you to create different task instances, which will be useful for creating blocks (my current project)
# Saves the log file after each task. It takes some extra time, but it prevents a crash from corrupting the file
class task(taskbattery,metadatacollection):
        def __init__(self, task_module, main_log_location, backup_log_location,  name, trialclass, runtime, dfile, ver, esq=False):#, trialfile, ver):
                self.main_log_location = main_log_location
                self.backup_log_location = backup_log_location # Not yet implemented
                self.task_module = task_module # The imported task function
                self.name = name # A name for each task to be written in the logfile
                
                self.trialclass = trialclass # Has something to do with writing task name into the logfile I think? Probably don't touch this.
                self.runtime = runtime # A "universal" "maximum" time each task can take. Will not stop mid trial, but will prevent trial repetions after the set time in seconds
                self.esq = esq
                self.ver = ver
                self.dfile = dfile
                #super.__init__()
        
        def initvers(self):
                os.chdir(os.getcwd())
                try:
                        f = open(os.path.join(os.getcwd(), self.dfile), 'r', newline="")
                except:
                        try:
                                f = open(os.path.join(os.path.join(os.getcwd(),'taskScripts'), self.dfile), 'r', newline="")
                        except:
                                f = open(os.path.join(os.getcwd(), self.dfile), 'r', newline="")
                d_reader = csv.DictReader(f)

                #get fieldnames from DictReader object and store in list
                self.headers = d_reader.fieldnames
                r = csv.reader(f)
                l = []
                for row in r:
                        l.append(row)
                        
                self.l = l
                
                incrordecr = random.choice([-1,1])
                amnt = random.randint(5,15)
                self.runtime = self.runtime + amnt*incrordecr
                with open(self.main_log_location, 'a', newline="") as o:
                        metawrite = csv.writer(o)
                        metawrite.writerow(" ")
                        metawrite.writerow(["Runtime Mod",(amnt*incrordecr)])
        def setver(self):
                ###
                ###   ###   NEED TO LOAD THE FILES FROM CSV AND PRESERVE THE HEADERS, THEN PUT THE OLD HEADERS INTO THE NEW BLOCK CSVs
                ###
                self.ver_a = random.sample(self.l, round(len(self.l)/2) )
                b = self.l
                for val in self.ver_a:
                        b[:] = [x for x in b if x != val]
                random.shuffle(b)
                b.insert(0,*[self.headers])
                self.ver_b = b
                random.shuffle(self.ver_a)
                
                self.ver_a.insert(0, self.headers)
                
                lis = [self.ver_a,self.ver_b]
                for enum, thing in enumerate(lis):
                        
                        if not os.path.exists(os.getcwd()+ '//tmp'):
                                os.mkdir(os.getcwd()+ '//tmp')
                        if not os.path.exists(os.getcwd()+ '//tmp//%s' %(self.name)):
                                os.mkdir(os.getcwd() + '//tmp//%s' %(self.name))
                        if os.path.exists(os.getcwd() + '//tmp//%s' %(self.name + "//" + self.name + "_version_"+ str(enum) + ".csv")):
                                os.remove(os.getcwd() + '//tmp//%s' %(self.name + "//" + self.name + "_version_"+ str(enum) + ".csv"))
                        with open(os.getcwd() + '//tmp//%s' %(self.name + "//" + self.name + "_version_"+ str(enum) + ".csv"), mode='w', newline="") as file:
                                
                                file_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                                for subthing in thing:
                                        file_writer.writerow(subthing)
                self._ver_a_name = os.getcwd() + '//tmp//%s' %(self.name + "//" + self.name + "_version_"+ str(0) + ".csv")
                self._ver_b_name = os.getcwd() + '//tmp//%s' %(self.name + "//" + self.name + "_version_"+ str(1) + ".csv")
        def setver3(self):
                ###
                ###   ###   NEED TO LOAD THE FILES FROM CSV AND PRESERVE THE HEADERS, THEN PUT THE OLD HEADERS INTO THE NEW BLOCK CSVs
                ###
                self.ver_a = random.sample(self.l, round(len(self.l)/3) )
                b = self.l
                for val in self.ver_a:
                        b[:] = [x for x in b if x != val]
                random.shuffle(b)
                
                self.ver_b = random.sample(b, round(len(b)/2) )
                c = b
                for val in self.ver_a:
                        c[:] = [x for x in c if x != val]
                random.shuffle(c)
                
                
                c.insert(0,*[self.headers])
                self.ver_c = c
                
                random.shuffle(self.ver_a)
                random.shuffle(self.ver_b)
                
                self.ver_a.insert(0, self.headers)
                self.ver_b.insert(0, self.headers)
                
                lis = [self.ver_a,self.ver_b,self.ver_c]
                for enum, thing in enumerate(lis):
                        
                        if not os.path.exists(os.getcwd()+ '//tmp'):
                                os.mkdir(os.getcwd()+ '//tmp')
                        if not os.path.exists(os.getcwd()+ '//tmp//%s' %(self.name)):
                                os.mkdir(os.getcwd() + '//tmp//%s' %(self.name))
                        if os.path.exists(os.getcwd() + '//tmp//%s' %(self.name + "//" + self.name + "_version_"+ str(enum) + ".csv")):
                                os.remove(os.getcwd() + '//tmp//%s' %(self.name + "//" + self.name + "_version_"+ str(enum) + ".csv"))
                        with open(os.getcwd() + '//tmp//%s' %(self.name + "//" + self.name + "_version_"+ str(enum) + ".csv"), mode='w', newline="") as file:
                                
                                file_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                                for subthing in thing:
                                        file_writer.writerow(subthing)
                self._ver_a_name = os.getcwd() + '//tmp//%s' %(self.name + "//" + self.name + "_version_"+ str(0) + ".csv")
                self._ver_b_name = os.getcwd() + '//tmp//%s' %(self.name + "//" + self.name + "_version_"+ str(1) + ".csv")   
                self._ver_c_name = os.getcwd() + '//tmp//%s' %(self.name + "//" + self.name + "_version_"+ str(2) + ".csv")        
                self._ver_d_name = None         
                                
        def run(self):
                global prevname
                if not os.path.exists(self.main_log_location):
                        if self.main_log_location.split(".")[1] == None:
                                os.mkdir(self.main_log_location.split("/")[0])      
                fr = open(self.main_log_location, 'a', newline="")
                f = open((self.main_log_location.split(".")[0] + "_full.csv"), 'a', newline="")
                fre = csv.writer(fr)
                r = csv.writer(f)
                
                writer = csv.DictWriter(f, fieldnames=taskbattery.resultdict)
                r.writerow(["EXPERIMENT DATA:",self.name])
                r.writerow(["Start Time", taskbattery.time.getTime()])
                writer2 = csv.DictWriter(fr, fieldnames=taskbattery.resultdict)
                fre.writerow(["EXPERIMENT DATA:",self.name])
                fre.writerow(["Start Time", taskbattery.time.getTime()])
                taskbattery.resultdict = {'Timepoint': None, 'Time': None, 'Is_correct': None, 'Experience Sampling Question': None, 'Experience Sampling Response':None, 'Task' : self.name, 'Task Iteration': '1', 'Participant ID': self.trialclass[1], 'Response_Key' : None, 'Auxillary Data': None, 'Assoc Task':None}
                if self.esq == False:
                        if self.ver == 1:
                                dataver = self.task_module.runexp(self.backup_log_location, taskbattery.time, taskbattery.win, [writer,writer2], taskbattery.resultdict, self.runtime, self._ver_a_name, int(metacoll.INFO['Experiment Seed']))
                        if self.ver == 2:
                                dataver = self.task_module.runexp(self.backup_log_location, taskbattery.time, taskbattery.win, [writer,writer2], taskbattery.resultdict, self.runtime, self._ver_b_name, int(metacoll.INFO['Experiment Seed']))
                        if self.ver == 3:
                                dataver = self.task_module.runexp(self.backup_log_location, taskbattery.time, taskbattery.win, [writer,writer2], taskbattery.resultdict, self.runtime, self._ver_c_name, int(metacoll.INFO['Experiment Seed']))
                        if self.ver == 4:
                                dataver = self.task_module.runexp(self.backup_log_location, taskbattery.time, taskbattery.win, [writer,writer2], taskbattery.resultdict, self.runtime, self._ver_d_name, int(metacoll.INFO['Experiment Seed']))
                
                if self.esq == True:
                        
                        taskbattery.resultdict = {'Timepoint': None, 'Time': None, 'Is_correct': None, 'Experience Sampling Question': None, 'Experience Sampling Response':None, 'Task' : self.name, 'Task Iteration': '1', 'Participant ID': self.trialclass[1], 'Response_Key' : None, 'Auxillary Data': None, 'Assoc Task':taskbattery.prevname}
                        self.task_module.runexp(self.backup_log_location, taskbattery.time, taskbattery.win, [writer,writer2], taskbattery.resultdict, self.runtime, None, int(metacoll.INFO['Experiment Seed']))
                        dataver = None
                f.close()
                fr.close()
                taskbattery.resultdict = {'Timepoint': None, 'Time': None, 'Is_correct': None, 'Experience Sampling Question': None, 'Experience Sampling Response':None, 'Task' : None, 'Task Iteration': None, 'Participant ID': None,'Response_Key':None, 'Auxillary Data': None, 'Assoc Task':None}
                if dataver != None:
                        self.name = self.name + "-" + dataver
                taskbattery.prevname = self.name



class taskgroup(taskbattery,metadatacollection):
        def __init__(self,tasks,instrpath):
                self.tasks = tasks
                self.instrpath = instrpath
                
                
                
        def show(self):
                text_inst = visual.TextStim(win=taskbattery.win, name='text_4',
                        text='',
                        font='Open Sans',
                        pos=(0, 0), height=0.1, wrapWidth=None, ori=0.0, 
                        color='black', colorSpace='rgb', opacity=None, 
                        languageStyle='LTR',
                        depth=0.0)
                try:
                        with open(os.path.join(os.path.join(os.getcwd(),"taskScripts"),self.instrpath), newline="") as f:
                                lines1 = f.read()
                except:
                        with open(os.path.join(os.getcwd(),self.instrpath), newline="") as f:
                                lines1 = f.read()
                text_inst.setText(lines1)
                text_inst.draw()
                taskbattery.win.flip()
                time.sleep(1)
                event.waitKeys(keyList=['return'])
                
        def run(self):
                for taskgrp in self.tasks:
                        if taskgrp == None:
                                continue
                        for task in taskgrp:
                                print("Now initializing {}".format(task.name))
                                task.initvers()
                                print("Now setting up {}".format(task.name))
                                task.setver3()
                                print("Now running {}".format(task.name))
                                task.run()
                                print("Now starting ESQ for {}".format(task.name))
                                taskbattery.ESQtask.run()
                        
        def end(self):
                text_inst = visual.TextStim(win=taskbattery.win, name='text_1',
                        text='This is the end of this phase of the experiment. \n Please take a break if you need to before continuing with the study',
                        font='Open Sans',
                        pos=(0, 0), height=0.1, wrapWidth=None, ori=0.0, 
                        color='black', colorSpace='rgb', opacity=None, 
                        languageStyle='LTR',
                        depth=0.0)
                text_inst.draw()
                taskbattery.win.flip()
                time.sleep(1)
                event.waitKeys(keyList=['return'])
                taskbattery.win.flip()
                
        def shuffle(self):
                a = self.tasks
                for a in self.tasks:
                        random.shuffle(a)
                random.shuffle(self.tasks)
                print('')
                        
        
        

### HAVE TO EXPOSE ESQ TASK TO MOVIE SCRIPT

if __name__ == "__main__":
        
        with open(os.path.join(os.pardir, 'config.yaml'),'r') as f:
                config = yaml.safe_load(f)
        # Info Dict
        INFO = {
                        'Experiment Seed': random.randint(1, 9999999),  
                        'Subject': 'Enter Name Here', 
                        
                        }



        # Main and backup data file


        # Run the GUI and save output to logfile
        metacoll = metadatacollection(INFO)
        metacoll.rungui()
        metacoll.collect_metadata()
        metacoll.INFO['Block Runtime'] = 75
        
        # Defining output datafile
        datafile = str(os.getcwd() + '/log_file/output_log_{}_{}.csv'.format(metacoll.INFO['Subject'],metacoll.INFO['Experiment Seed']))
        datafileBackup = 'log_file/testfullbackup.csv'
        if not os.path.exists("tmp"):
                os.mkdir("tmp")
        # with open("tmp/esqtmp.pkl",'wb') as frrr:
        #         pkl.dump([datafile,datafileBackup,metacoll.sbINFO.data,int(metacoll.INFO['Block Runtime'])],frrr)
        ESQTask = task(taskScripts.ESQ, datafile, datafileBackup, "Experience Sampling Questions", metacoll.sbINFO.data, int(metacoll.INFO['Block Runtime']),'resources/GoNoGo_Task/gonogo_stimuli.csv',1, esq=True)
        
        # Defining each task as a task object
        
        
        friendTask = task(taskScripts.otherTask, datafile, datafileBackup, "Friend Task", metacoll.sbINFO.data, int(metacoll.INFO['Block Runtime']),'resources/Other_Task/Other_Stimuli.csv', 1)
        youTask = task(taskScripts.selfTask, datafile, datafileBackup, "You Task", metacoll.sbINFO.data, int(metacoll.INFO['Block Runtime']),'resources/Self_Task/Self_Stimuli.csv', 1)
        gonogoTask = task(taskScripts.gonogoTask, datafile, datafileBackup, "GoNoGo Task", metacoll.sbINFO.data, int(metacoll.INFO['Block Runtime']),'resources/GoNoGo_Task/gonogo_stimuli.csv', 1)
        fingertapTask = task(taskScripts.fingertappingTask, datafile, datafileBackup, "Finger Tapping Task",  metacoll.sbINFO.data, int(metacoll.INFO['Block Runtime']),'resources/GoNoGo_Task/gonogo_stimuli.csv', 1)
        readingTask = task(taskScripts.readingTask, datafile, datafileBackup, "Reading Task",  metacoll.sbINFO.data, int(metacoll.INFO['Block Runtime']),"resources/Reading_Task/sem_stim_run.csv", 1)
        memTask = task(taskScripts.memoryTask, datafile, datafileBackup,"Memory Task",  metacoll.sbINFO.data, int(metacoll.INFO['Block Runtime']),'resources/Memory_Task/Memory_prompts.csv', 1)
        zerobackTask = task(taskScripts.zerobackTask, datafile, datafileBackup,"Zero-Back Task",  metacoll.sbINFO.data, int(metacoll.INFO['Block Runtime']),'resources//ZeroBack_Task//ConditionsSpecifications_ES_zeroback.csv', 1)
        onebackTask = task(taskScripts.onebackTask, datafile, datafileBackup,"One-Back Task",  metacoll.sbINFO.data, int(metacoll.INFO['Block Runtime']),'resources//ZeroBack_Task//ConditionsSpecifications_ES_oneback.csv', 1)
        easymathTask1 = task(taskScripts.easymathTask, datafile, datafileBackup,"Easy Math Task",  metacoll.sbINFO.data, int(metacoll.INFO['Block Runtime']),"resources/Maths_Task/new_math_stimuli1.csv", 1)
        hardmathTask1 = task(taskScripts.hardmathTask, datafile, datafileBackup,"Hard Math Task",  metacoll.sbINFO.data, int(metacoll.INFO['Block Runtime']),"resources/Maths_Task/new_math_stimuli2.csv", 1)
        twobackTaskfaces1 = task(taskScripts.twobacktaskfaces, datafile, datafileBackup,"Two-Back Task",  metacoll.sbINFO.data, int(metacoll.INFO['Block Runtime']),'resources/GoNoGo_Task/gonogo_stimuli.csv', 1)
        twobackTaskscenes1 = task(taskScripts.twobacktaskscenes, datafile, datafileBackup,"Two-Back Task",  metacoll.sbINFO.data, int(metacoll.INFO['Block Runtime']),'resources/GoNoGo_Task/gonogo_stimuli.csv', 1)
        
        #Block 2

        friendTask2 = task(taskScripts.otherTask, datafile, datafileBackup, "Friend Task",  metacoll.sbINFO.data, int(metacoll.INFO['Block Runtime']),'resources/Other_Task/Other_Stimuli.csv', 2)
        youTask2 = task(taskScripts.selfTask, datafile, datafileBackup, "You Task",  metacoll.sbINFO.data, int(metacoll.INFO['Block Runtime']),'resources/Self_Task/Self_Stimuli.csv', 2)
        gonogoTask2 = task(taskScripts.gonogoTask, datafile, datafileBackup, "GoNoGo Task",  metacoll.sbINFO.data, int(metacoll.INFO['Block Runtime']),'resources/GoNoGo_Task/gonogo_stimuli.csv', 2)
        fingertapTask2 = task(taskScripts.fingertappingTask, datafile, datafileBackup, "Finger Tapping Task",  metacoll.sbINFO.data, int(metacoll.INFO['Block Runtime']),'resources/GoNoGo_Task/gonogo_stimuli.csv', 2)
        readingTask2 = task(taskScripts.readingTask, datafile, datafileBackup, "Reading Task",  metacoll.sbINFO.data, int(metacoll.INFO['Block Runtime']),"resources/Reading_Task/sem_stim_run.csv", 2)
        memTask2 = task(taskScripts.memoryTask, datafile, datafileBackup,"Memory Task",  metacoll.sbINFO.data, int(metacoll.INFO['Block Runtime']),'resources/Memory_Task/Memory_prompts.csv', 2)
        zerobackTask2 = task(taskScripts.zerobackTask, datafile, datafileBackup,"Zero-Back Task",  metacoll.sbINFO.data, int(metacoll.INFO['Block Runtime']),'resources//ZeroBack_Task//ConditionsSpecifications_ES_zeroback.csv', 2)
        onebackTask2 = task(taskScripts.onebackTask, datafile, datafileBackup,"One-Back Task",  metacoll.sbINFO.data, int(metacoll.INFO['Block Runtime']),'resources//ZeroBack_Task//ConditionsSpecifications_ES_oneback.csv', 2)
        easymathTask2 = task(taskScripts.easymathTask, datafile, datafileBackup,"Easy Math Task",  metacoll.sbINFO.data, int(metacoll.INFO['Block Runtime']),"resources/Maths_Task/new_math_stimuli1.csv", 2)
        hardmathTask2 = task(taskScripts.hardmathTask, datafile, datafileBackup,"Hard Math Task",  metacoll.sbINFO.data, int(metacoll.INFO['Block Runtime']),"resources/Maths_Task/new_math_stimuli2.csv", 2)
        twobackTaskfaces2 = task(taskScripts.twobacktaskfaces, datafile, datafileBackup,"Two-Back Task",  metacoll.sbINFO.data, int(metacoll.INFO['Block Runtime']),'resources/GoNoGo_Task/gonogo_stimuli.csv', 2)
        twobackTaskscenes2 = task(taskScripts.twobacktaskscenes, datafile, datafileBackup,"Two-Back Task",  metacoll.sbINFO.data, int(metacoll.INFO['Block Runtime']),'resources/GoNoGo_Task/gonogo_stimuli.csv', 2)
        

        #Block 3 
        friendTask3 = task(taskScripts.otherTask, datafile, datafileBackup, "Friend Task",  metacoll.sbINFO.data, int(metacoll.INFO['Block Runtime']),'resources/Other_Task/Other_Stimuli.csv', 3)
        youTask3 = task(taskScripts.selfTask, datafile, datafileBackup, "You Task",  metacoll.sbINFO.data, int(metacoll.INFO['Block Runtime']),'resources/Self_Task/Self_Stimuli.csv', 3)
        gonogoTask3 = task(taskScripts.gonogoTask, datafile, datafileBackup, "GoNoGo Task",  metacoll.sbINFO.data, int(metacoll.INFO['Block Runtime']),'resources/GoNoGo_Task/gonogo_stimuli.csv', 3)
        fingertapTask3 = task(taskScripts.fingertappingTask, datafile, datafileBackup, "Finger Tapping Task",  metacoll.sbINFO.data, int(metacoll.INFO['Block Runtime']),'resources/GoNoGo_Task/gonogo_stimuli.csv', 3)
        readingTask3 = task(taskScripts.readingTask, datafile, datafileBackup, "Reading Task",  metacoll.sbINFO.data, int(metacoll.INFO['Block Runtime']),"resources/Reading_Task/sem_stim_run.csv", 3)
        memTask3 = task(taskScripts.memoryTask, datafile, datafileBackup,"Memory Task",  metacoll.sbINFO.data, int(metacoll.INFO['Block Runtime']),'resources/Memory_Task/Memory_prompts.csv', 3)
        zerobackTask3 = task(taskScripts.zerobackTask, datafile, datafileBackup,"Zero-Back Task",  metacoll.sbINFO.data, int(metacoll.INFO['Block Runtime']),'resources//ZeroBack_Task//ConditionsSpecifications_ES_zeroback.csv', 3)
        onebackTask3 = task(taskScripts.onebackTask, datafile, datafileBackup,"One-Back Task",  metacoll.sbINFO.data, int(metacoll.INFO['Block Runtime']),'resources//ZeroBack_Task//ConditionsSpecifications_ES_oneback.csv', 3)
        easymathTask3 = task(taskScripts.easymathTask, datafile, datafileBackup,"Easy Math Task",  metacoll.sbINFO.data, int(metacoll.INFO['Block Runtime']),"resources/Maths_Task/new_math_stimuli1.csv", 3)
        hardmathTask3 = task(taskScripts.hardmathTask, datafile, datafileBackup,"Hard Math Task",  metacoll.sbINFO.data, int(metacoll.INFO['Block Runtime']),"resources/Maths_Task/new_math_stimuli2.csv", 3)
        #twobackTask3 = task(taskScripts.twobacktask, datafile, datafileBackup,"Two-Back Task",  metacoll.sbINFO.data, int(metacoll.INFO['Block Runtime']),'resources/GoNoGo_Task/gonogo_stimuli.csv', 3)
        


        movieTask1 = task(taskScripts.movieTask, datafile, 1,"Movie Task",  metacoll.sbINFO.data, int(metacoll.INFO['Block Runtime']),'resources//Movie_Task//csv//sorted_filmList.csv', 1)
        movieTask2 = task(taskScripts.movieTask, datafile, 2,"Movie Task",  metacoll.sbINFO.data, int(metacoll.INFO['Block Runtime']),'resources//Movie_Task//csv//sorted_filmList.csv', 2)
        movieTask3 = task(taskScripts.movieTask, datafile, 3,"Movie Task",  metacoll.sbINFO.data, int(metacoll.INFO['Block Runtime']),'resources//Movie_Task//csv//sorted_filmList.csv', 3)
        movieTask4 = task(taskScripts.movieTask, datafile, 4,"Movie Task",  metacoll.sbINFO.data, int(metacoll.INFO['Block Runtime']),'resources//Movie_Task//csv//sorted_filmList.csv', 4)
        # Defining task GROUPS (groups will always be shown together, preceded by an instruction screen)
        
<<<<<<< Updated upstream
        friendgroup = [friendTask,friendTask2,friendTask3]
        yougroup = [youTask,youTask2,youTask3]
        gonogogroup = [gonogoTask,gonogoTask2,gonogoTask3]
        fingertapgroup = [fingertapTask,fingertapTask2,fingertapTask3]
        readinggroup = [readingTask,readingTask2,readingTask3]
        memorygroup = [memTask,memTask2,memTask3]
        onebackgroup = [onebackTask,onebackTask2,onebackTask3]
        zerobackgroup = [zerobackTask,zerobackTask2,zerobackTask3]
        ezmathgroup = [easymathTask1,easymathTask2,easymathTask3]
        hardmathgroup = [hardmathTask1,hardmathTask2,hardmathTask3]
        twobackfacegroup = [twobackTaskfaces1,twobackTaskfaces2]
        twobackscenegroup = [twobackTaskscenes1,twobackTaskscenes2]
        moviegroup = [movieTask1,movieTask2]
=======
        self_other = taskgroup([[friendTask,friendTask2,friendTask3],[youTask,youTask2,youTask3]],"resources/group_inst/self_other.txt" )
        gonogo_fingtap = taskgroup([[gonogoTask,gonogoTask2,gonogoTask3],[fingertapTask,fingertapTask2,fingertapTask3]],"resources/group_inst/gonogo_fingtap.txt")
        reading_memory = taskgroup([[readingTask,readingTask2,readingTask3],[memTask,memTask2,memTask3]],"resources/group_inst/reading_memory.txt")
        oneback_zeroback = taskgroup([[zerobackTask,zerobackTask2,zerobackTask3],[onebackTask,onebackTask2,onebackTask3]],"resources/group_inst/oneback_zeroback.txt")
        ezmath_hrdmath = taskgroup([[easymathTask1,easymathTask2,easymathTask3],[hardmathTask1,hardmathTask2,hardmathTask3]],"resources/group_inst/ezmath_hrdmath.txt")
        twobackTask_grp = taskgroup([[twobackTaskfaces1,twobackTaskfaces2],[twobackTaskscenes1,twobackTaskscenes2]],"resources/group_inst/ezmath_hrdmath.txt")
        movie_main = taskgroup([[movieTask1,movieTask2]],"resources/group_inst/movie_main.txt")
        gonogo = taskgroup([[gonogoTask,gonogoTask2,gonogoTask3]],"resources/group_inst/gonogo_fingtap.txt")
        
        
>>>>>>> Stashed changes

        #if config['randomize_task']:
        #        fulltaskgroups = random.sample(list(allgroups),config['num_task_in_subset'])

<<<<<<< Updated upstream
        #fulltaskgroups_ = {x:allgroups[x] if x in fulltaskgroups else None for x in list(allgroups.keys())}


        
        self_other = taskgroup([friendgroup,yougroup],"resources/group_inst/self_other.txt" )
        gonogo_fingtap = taskgroup([gonogogroup,fingertapgroup],"resources/group_inst/gonogo_fingtap.txt")
        reading_memory = taskgroup([readinggroup,memorygroup],"resources/group_inst/reading_memory.txt")
        oneback_zeroback = taskgroup([zerobackgroup,onebackgroup],"resources/group_inst/oneback_zeroback.txt")
        ezmath_hrdmath = taskgroup([ezmathgroup,hardmathgroup],"resources/group_inst/ezmath_hrdmath.txt")
        twobackTask_grp = taskgroup([twobackfacegroup,twobackscenegroup],"resources/group_inst/ezmath_hrdmath.txt")
        movie_main = taskgroup([moviegroup],"resources/group_inst/movie_main.txt")
=======
        fulltasklist = [self_other,gonogo_fingtap,reading_memory,oneback_zeroback,ezmath_hrdmath,movie_main,twobackTask_grp]
        fulltasklist = [gonogo]
     
>>>>>>> Stashed changes

 
        fulltasklist = [self_other,gonogo_fingtap,reading_memory,oneback_zeroback,ezmath_hrdmath,movie_main,twobackTask_grp]
        
        if config['randomize_task']:
                fulltasklist = random.sample(list(fulltasklist),config['num_task_in_subset'])
        
        
        # Shuffles the order of the tasks in taskgroups
        for enum, blk in enumerate(fulltasklist):
                blk.shuffle()
        
        # Shuffle the order of the taskgroups
        random.shuffle(fulltasklist)
        tasks = fulltasklist

        tbt = taskbattery(tasks, ESQTask, INFO)
        
        tbt.run_battery()
        print("Success")