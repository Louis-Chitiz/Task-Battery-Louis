import pandas as pd

file = pd.read_csv("Analysis/accuracy.csv").T
index = list(file.index)
index_acc = [x for x in index if "Accuracy" in x]
index_rp = [x for x in index if "Response Time" in x]
index_snt = [x for x in index if "Sentiment" in x]

index_min = [x.strip(" Accuracy") for x in index]
index_min = [x.split(" Response")[0] for x in index_min]
index_min = [x.split(" Sentiment")[0] for x in index_min]
index_min.remove('Subject')
index_unique = list(set(index_min))



def f(file_,index,name):
    file_temp = file_.loc[index].stack()
    file_temp = file_temp.reset_index()
    #file_temp = file_temp.drop(["level_1"],axis=1)
    file_temp['level_0'] = file_temp['level_0'].str.replace(name, '')


    file_temp["level_0"] = file_temp["level_0"] + file_temp["level_1"].astype(str)
    file_temp = file_temp.drop(["level_1"],axis=1)
    file_temp[0] = file_temp[0].astype(float)
    #file_temp["level_0"] = file_temp["level_0"].astype(int)

    return file_temp

file_acc = f(file,index_acc,"Accuracy")
file_rp = f(file,index_rp,"Response Time")
file_snt = f(file,index_snt,"Sentiment")

file_main = file_rp.merge(file_acc,on='level_0',how="outer").merge(file_snt,on='level_0',how="outer")
def func(x):
    x = x.rsplit(" ",1)[0]
    return x

file_main['level_0'] = file_main['level_0'].apply(func)

file_main = file_main.rename({"level_0":"Task","0_x":"Response Time","0_y":"Accuracy",0:"Sentiment"},axis=1)

file_main.to_csv("Analysis/outputforlewwy.csv")


print('e')