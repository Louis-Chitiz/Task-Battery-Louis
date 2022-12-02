
import os
import csv
import numpy as np
os.chdir(".")
graddict = {}
global sentimentdict
sentimentdict = {}

if os.path.exists("Analysis/accuracy.csv"):
    os.remove("Analysis/accuracy.csv")
with open("Analysis/accuracy.csv","a") as f:
    newdict = {"Subject":None,"Experience Sampling Questions Response Time":None,
        "GoNoGo Task Response Time":None, "Go Task Accuracy":None,"NoGo Task Accuracy":None,
        "Finger Tapping Task Response Time":None, "Finger Tapping Task Accuracy":None,
        "Two-Back Task-faces Response Time":None, "Two-Back Task-faces Accuracy":None,
        "Two-Back Task-scenes Response Time":None, "Two-Back Task-scenes Accuracy":None,
        "One-Back Task Response Time":None, "One-Back Task Accuracy":None,
        "Zero-Back Task Response Time":None, "Zero-Back Task Accuracy":None,
        "Hard Math Task Response Time":None, "Hard Math Task Accuracy":None,
        "Easy Math Task Response Time":None, "Easy Math Task Accuracy":None,
        "Friend Task Response Time":None, "Friend Task Sentiment":None,
        "You Task Response Time":None, "You Task Sentiment":None
        }
    writer = csv.writer(f)
    writer.writerow(newdict)


with open("Tasks/taskScripts/resources/Self_Task/Self_Stimuli.csv",'r') as f:
    reader = csv.reader(f)
    for e,row in enumerate(reader):
        if e == 0:
            continue
        sentimentdict.update({row[6]:row[8]})
        print(row)

with open("Tasks/taskScripts/resources/Other_Task/Other_Stimuli.csv",'r') as f:
    reader = csv.reader(f)
    for e,row in enumerate(reader):
        if e == 0:
            continue
        sentimentdict.update({row[6]:row[8]})
        print(row)

with open('Analysis/coords.csv','r') as ft:
    rd = csv.reader(ft)
    for e,row in enumerate(rd):
        if e == 0:
            continue
        graddict.update({row[0]:[float(row[1]),float(row[2]),float(row[3])]})
        print(row)


line_dict= {"Task_name":None,
        "Participant #":None,
        "Runtime_mod":None,
        "Absorption_response":None,
        "Other_response":None,
        "Problem_response":None,
        "Words_response":None,
        "Sounds_response":None,
        "Images_response":None,
        "Past_response":None,
        "Distracting_response":None,
        "Focus_response":None,
        "Intrusive_response":None,
        "Deliberate_response":None,
        "Detailed_response":None,
        "Future_response":None,
        "Emotion_response":None,
        "Self_response":None,
        "Knowledge_response":None,
        "Gradient 1":None,
        "Gradient 2":None,
        "Gradient 3":None
        }

if os.path.exists(os.path.join(os.getcwd(),"Analysis/output.csv")):
        os.remove(os.path.join(os.getcwd(),"Analysis/output.csv"))


with open(os.path.join(os.getcwd(),"Analysis/output.csv"), 'a', newline="") as outf:
    wr = csv.writer(outf)
    wr.writerow(list(line_dict.keys()))



def sortingfunction(exp,row,resps):
    global prevtime
    global en
    if exp == "Reading Task":
        # Collect no data
        pass
    if exp == "Experience Sampling Questions":
        # Collect response time
        
        print(row)
        if row[3].split("_")[1] == "start":
            prevtime = float(row[1])
        elif row[3].split("_")[1] == "response":
            resptime = float(row[1]) - prevtime  
            resps[exp]["Response Time"].append(resptime)
        pass
    if exp == "Memory Task":
        # Collect no data
        pass
    if exp == "GoNoGo Task":
        # Collect response time, % correct
        try:
            # Resp time
            if row[0].split(" ")[1] == "start":
                prevtime = float(row[1])
            elif row[0].split(" ")[1] == "end":
                resptime = float(row[1]) - prevtime  
                resps[exp]["Response Time"].append(resptime)
            # Accuracy
            if row[2] != '':
                if row[2] == 'noResponse':
                    if row[9] == 'Type: Go':
                        resps[exp]["Accuracy - Go"].append(False)
                if row[2].upper() == 'FALSE':
                    if row[9] == 'Type: Go':
                        resps[exp]["Accuracy - Go"].append(True)
                if row[2].upper() == 'FALSE':
                    if row[9] == 'Type: NoGo':
                        resps[exp]["Accuracy - NoGo"].append(False)
                if row[2].upper() == 'TRUE':
                    if row[9] == 'Type: NoGo':
                        resps[exp]["Accuracy - NoGo"].append(True)
        except Exception as e:
            print(e)
            pass
        pass
    if exp == "Finger Tapping Task": #### NO RESPONSE TIME
        print(row)
        if row[1] != "":    
            try:
                if row[0].split(" ",2)[2] == "Trial Start":
                    prevtime = float(row[1])
                elif row[0].split(" ",2)[2] == "Trial End":
                    resptime = float(row[1]) - prevtime  
                    resps[exp]["Response Time"].append(resptime)
            except:
                pass
        if row[0] == 'Finger Tapping Trial End':
            if row[2].upper() == "TRUE":
                resps[exp]["Accuracy"].append(True)
            elif row[2].upper() == "FALSE":
                resps[exp]["Accuracy"].append(False)
            else:
                return 1/0
        # Collect response time, % correct
        pass
    if exp == "Two-Back Task-faces": #DONT HAVE THE CORRECT TRUE/FALSE ON TRIALS
        print(row)
        if row[0] == "Choice presented":
            prevtime = float(row[1])
        elif row[0] == "2-back Trial End":
            resptime = float(row[1]) - prevtime  
            resps[exp]["Response Time"].append(resptime)
        # Collect response time, % correct
        if row[0] == "2-back Trial End":
            if row[2].upper() == "TRUE":
                resps[exp]["Accuracy"].append(True)
            elif row[2].upper() == "FALSE":
                resps[exp]["Accuracy"].append(False)
            else:
                return 1/0
        pass
    if exp == "Two-Back Task-scenes": #DONT HAVE THE CORRECT TRUE/FALSE ON TRIALS
        print(row)
        if row[0] == "Choice presented":
            prevtime = float(row[1])
        elif row[0] == "2-back Trial End":
            resptime = float(row[1]) - prevtime  
            resps[exp]["Response Time"].append(resptime)
        # Collect response time, % correct
        if row[0] == "2-back Trial End":
            if row[2].upper() == "TRUE":
                resps[exp]["Accuracy"].append(True)
            elif row[2].upper() == "FALSE":
                resps[exp]["Accuracy"].append(False)
            else:
                return 1/0
        pass
    if exp == "One-Back Task": #DONT HAVE THE CORRECT TRUE/FALSE ON TRIALS
        print(row)
        if row[0] == "OneBackStimulus Start":
            prevtime = float(row[1])
        elif row[0] == "OneBackStimulus End":
            resptime = float(row[1]) - prevtime  
            resps[exp]["Response Time"].append(resptime)
        # Collect response time, % correct
        if row[0] == "OneBackStimulus End":
            if row[2].upper() == "TRUE":
                resps[exp]["Accuracy"].append(True)
            elif row[2].upper() == "FALSE":
                resps[exp]["Accuracy"].append(False)
            else:
                return 1/0
        pass
    if exp == "Zero-Back Task":
        if row[0] == "ZeroBackStimulus Start":
            prevtime = float(row[1])
        elif row[0] == "ZeroBackStimulus End":
            resptime = float(row[1]) - prevtime  
            resps[exp]["Response Time"].append(resptime)
        # Collect response time, % correct
        if row[0] == "ZeroBackStimulus End":
            if row[2].upper() == "TRUE":
                resps[exp]["Accuracy"].append(True)
            elif row[2].upper() == "FALSE":
                resps[exp]["Accuracy"].append(False)
            else:
                return 1/0
        pass
        # Collect response time, % correct
        pass
    if exp == "Hard Math Task":
        print(row)
        if row[0] == 'Choice presented':
            prevtime = float(row[1])
        elif row[0] == 'Choice made':
            resptime = float(row[1]) - prevtime  
            resps[exp]["Response Time"].append(resptime)
        # Collect response time, % correct
        if row[0] == 'Math Trial End':
            if not "en" in globals():
                
                en = 0
            if en == 0:
                en = 1
                if row[2].upper() == "TRUE":
                    resps[exp]["Accuracy"].append(True)
                elif row[2].upper() == "FALSE":
                    resps[exp]["Accuracy"].append(False)
                else:
                    return 1/0
            elif en == 1:
                en = 0
            
        pass
    if exp == "Easy Math Task":
        if row[0] == 'Choice presented':
            prevtime = float(row[1])
        elif row[0] == 'Choice made':
            resptime = float(row[1]) - prevtime  
            resps[exp]["Response Time"].append(resptime)
        # Collect response time, % correct
        if row[0] == 'Math Trial End':
            if not "en" in globals():
                # global en
                en = 0
            if en == 0:
                en = 1
                if row[2].upper() == "TRUE":
                    resps[exp]["Accuracy"].append(True)
                elif row[2].upper() == "FALSE":
                    resps[exp]["Accuracy"].append(False)
                else:
                    return 1/0
            elif en == 1:
                en = 0
        # Collect response time, % correct
        pass
    if exp == "Friend Task": #NO RESPONSE TIMES
        print(row)
        if row[0].split('_')[0] == 'Start':
            prevtime = float(row[1])
        elif row[0].split('_')[0] == 'End':
            resptime = float(row[1]) - prevtime  
            resps[exp]["Response Time"].append(resptime)
        # Collect response time, sentiment
        if row[0].split('_')[0] == 'End':
            sentdirection = sentimentdict[row[0].split('_')[2]]
            
            if row[8] == 'right':
                applies = True
            if row[8] == 'left':
                applies = False
            if row[8] == "None":
                #resps[exp]["Sentiment"].append("noresponse")
                return  
            if sentdirection == 'Negative':
                if applies == True:
                    resps[exp]["Sentiment"].append(False)      
                elif applies == False:
                    resps[exp]["Sentiment"].append(True)  
                
            if sentdirection == 'Positive':
                if applies == True:
                    resps[exp]["Sentiment"].append(True)      
                elif applies == False:
                    resps[exp]["Sentiment"].append(False)  
                        
            
            
        pass
    if exp == "You Task":
        if row[0].split('_')[0] == 'Start':
            prevtime = float(row[1])
        elif row[0].split('_')[0] == 'End':
            resptime = float(row[1]) - prevtime  
            resps[exp]["Response Time"].append(resptime)
        # Collect response time, sentiment
        if row[0].split('_')[0] == 'End':
            sentdirection = sentimentdict[row[0].split('_')[2]]
            
            if row[8] == 'right':
                applies = True
            if row[8] == 'left':
                applies = False
            if row[8] == "None":
                #resps[exp]["Sentiment"].append("noresponse")
                return  
            if sentdirection == 'Negative':
                if applies == True:
                    resps[exp]["Sentiment"].append(False)      
                elif applies == False:
                    resps[exp]["Sentiment"].append(True)  
                
            if sentdirection == 'Positive':
                if applies == True:
                    resps[exp]["Sentiment"].append(True)      
                elif applies == False:
                    resps[exp]["Sentiment"].append(False)  
        # Collect response time, sentiment
        pass
    
        #print("e")    
    pass



for file in os.listdir("Tasks/log_file"):
    
    ftemp = file.split('.')[0]
    resps = {"Experience Sampling Questions":{"Response Time":[]},
             "GoNoGo Task":{"Response Time":[], "Accuracy - Go":[],"Accuracy - NoGo":[]},
             "Finger Tapping Task":{"Response Time":[], "Accuracy":[]},
             "Two-Back Task-faces":{"Response Time":[], "Accuracy":[]},
             "Two-Back Task-scenes":{"Response Time":[], "Accuracy":[]},
             "One-Back Task":{"Response Time":[], "Accuracy":[]},
             "Zero-Back Task":{"Response Time":[], "Accuracy":[]},
             "Hard Math Task":{"Response Time":[], "Accuracy":[]},
             "Easy Math Task":{"Response Time":[], "Accuracy":[]},
             "Friend Task":{"Response Time":[], "Sentiment":[]},
             "You Task":{"Response Time":[], "Sentiment":[]}
             }

    if not 'full' in ftemp.split('_'):
        line_dict= {"Task_name":None,
        "Participant #":None,
        "Runtime_mod":None,
        "Absorption_response":None,
        "Other_response":None,
        "Problem_response":None,
        "Words_response":None,
        "Sounds_response":None,
        "Images_response":None,
        "Past_response":None,
        "Distracting_response":None,
        "Focus_response":None,
        "Intrusive_response":None,
        "Deliberate_response":None,
        "Detailed_response":None,
        "Future_response":None,
        "Emotion_response":None,
        "Self_response":None,
        "Knowledge_response":None,
        "Gradient 1":None,
        "Gradient 2":None,
        "Gradient 3":None
        }

        _,_,subject,seed = ftemp.split("_")
        line_dict["Participant #"] = subject
        
        with open(os.path.join("Tasks/log_file",file)) as f:
            reader = csv.reader(f)
            
            for row in reader:
                
                if row[0] == 'Runtime Mod':
                    line_dict["Runtime_mod"] = row[1]
                
                if row[0] == 'ESQ':
                    enum +=1
                    if ect == 0:
                        task_name = row[10]
                        # if task_name == "Movie Task-Movie Task-bridge":
                        #     task_name = "Movie Task-bridge"
                        #     row[10] = "Movie Task-bridge"
                        # if task_name == "Movie Task-Movie Task-incept":
                        #     task_name = "Movie Task-incept"
                        #     row[10] = "Movie Task-incept"
                        line_dict["Task_name"] = task_name
                        ect = 1
                    if task_name == row[10]:
                        line_dict[row[3]]=row[4]
                    if enum == 16:
                        if task_name == "Movie Task-Movie Task-bridge":
                            line_dict["Task_name"] = "Movie Task-bridge"
                            #row[10] = "Movie Task-bridge"
                        if task_name == "Movie Task-Movie Task-incept":
                            line_dict["Task_name"] = "Movie Task-incept"
                            #row[10] = "Movie Task-incept"
                        grads = graddict[line_dict["Task_name"]]
                        line_dict["Gradient 1"],line_dict["Gradient 2"],line_dict["Gradient 3"] = grads
                        with open("Analysis/output.csv", 'a', newline="") as outf:
                            wr = csv.writer(outf)
                            wr.writerow(list(line_dict.values()))
                        task_name = row[10]
                        line_dict[row[3]]=row[4]
                        line_dict["Task_name"] = task_name
                    #print(row)
                else:
                    ect = 0
                    enum =0
                
        print(file)
    else:
        stats = {}
        expdict = {}
        captsubj = False
        ready = False
        resps.update({"Subject":subject})
        with open(os.path.join("Tasks/log_file",file)) as f:
            reader = csv.reader(f)
            
            for row in reader:
                
                # Subject name
                if captsubj == True:
                    stats.update({"Subject":row[2]})
                    captsubj = False
                if row[0] == "Block Runtime":
                    if row[2] == "Subject":
                        captsubj = True
                        
                # Experiment name
                elif row[0] == "EXPERIMENT DATA:":
                    expdict = {}
                    expdict.update({"Experiment":row[1]})
                    ready = False
                
                # Trigger start on next line
                elif row[0] == "Start Time":
                    ready = True
                elif ready == True:
                    if expdict["Experiment"] == 'Two-Back Task':
                        sortingfunction(expdict["Experiment"] + "-" + row[9],row,resps)  
                    else:
                        sortingfunction(expdict["Experiment"],row,resps)  
                    
                print(row)
        with open("Analysis/accuracy.csv","a",newline="") as f:
            newdict = {"Subject":resps['Subject'],
             "Experience Sampling Questions Response Time":np.mean(resps['Experience Sampling Questions']['Response Time']),
             "GoNoGo Task Response Time":np.mean(resps['GoNoGo Task']['Response Time']), "NoGo Task Accuracy":(resps['GoNoGo Task']['Accuracy - NoGo'].count(True)/len(resps['GoNoGo Task']['Accuracy - NoGo'])), "Go Task Accuracy":(resps['GoNoGo Task']['Accuracy - Go'].count(True)/len(resps['GoNoGo Task']['Accuracy - Go'])),
             "Finger Tapping Task Response Time":np.mean(resps['Finger Tapping Task']['Response Time']), "Finger Tapping Task Accuracy":(resps['Finger Tapping Task']['Accuracy'].count(True)/len(resps['Finger Tapping Task']['Accuracy'])),
             "Two-Back Task-faces Response Time":np.mean(resps['Two-Back Task-faces']['Response Time']), "Two-Back Task-faces Accuracy":(resps['Two-Back Task-faces']['Accuracy'].count(True)/len(resps['Two-Back Task-faces']['Accuracy'])),
             "Two-Back Task-scenes Response Time":np.mean(resps['Two-Back Task-scenes']['Response Time']), "Two-Back Task-scenes Accuracy":(resps['Two-Back Task-scenes']['Accuracy'].count(True)/len(resps['Two-Back Task-scenes']['Accuracy'])),
             "One-Back Task Response Time":np.mean(resps['One-Back Task']['Response Time']), "One-Back Task Accuracy":(resps['One-Back Task']['Accuracy'].count(True)/len(resps['One-Back Task']['Accuracy'])),
             "Zero-Back Task Response Time":np.mean(resps['Zero-Back Task']['Response Time']), "Zero-Back Task Accuracy":(resps['Zero-Back Task']['Accuracy'].count(True)/len(resps['Zero-Back Task']['Accuracy'])),
             "Hard Math Task Response Time":np.mean(resps['Hard Math Task']['Response Time']), "Hard Math Task Accuracy":(resps['Hard Math Task']['Accuracy'].count(True)/len(resps['Hard Math Task']['Accuracy'])),
             "Easy Math Task Response Time":np.mean(resps['Easy Math Task']['Response Time']), "Easy Math Task Accuracy":(resps['Easy Math Task']['Accuracy'].count(True)/len(resps['Easy Math Task']['Accuracy'])),
             "Friend Task Response Time":np.mean(resps['Friend Task']['Response Time']), "Friend Task Sentiment":(resps['Friend Task']['Sentiment'].count(True)/len(resps['Friend Task']['Sentiment'])),
             "You Task Response Time":np.mean(resps['You Task']['Response Time']), "You Task Sentiment":(resps['You Task']['Sentiment'].count(True)/len(resps['You Task']['Sentiment']))
             }
            writer = csv.writer(f)
            writer.writerow(newdict.values())
