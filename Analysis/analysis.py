import os
import csv
os.chdir(".")
graddict = {}
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
        "Modality_response":None,
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
for file in os.listdir("Tasks/log_file"):
    
    ftemp = file.split('.')[0]
    
    if not 'full' in ftemp.split('_'):
        line_dict= {"Task_name":None,
        "Participant #":None,
        "Runtime_mod":None,
        "Absorption_response":None,
        "Other_response":None,
        "Problem_response":None,
        "Modality_response":None,
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
                        line_dict["Task_name"] = task_name
                        ect = 1
                    if task_name == row[10]:
                        line_dict[row[3]]=row[4]
                    if enum == 14:
                        grads = graddict[line_dict["Task_name"]]
                        line_dict["Gradient 1"],line_dict["Gradient 2"],line_dict["Gradient 3"] = grads
                        with open("Analysis/output.csv", 'a', newline="") as outf:
                            wr = csv.writer(outf)
                            #wr.writerow(list(line_dict.keys()))
                            wr.writerow(list(line_dict.values()))
                        task_name = row[10]
                        line_dict[row[3]]=row[4]
                        line_dict["Task_name"] = task_name
                    print(row)
                else:
                    ect = 0
                    enum =0
                
        print(file)