import pandas as pd

stimuli1 = pd.read_csv('math_stimuli1.csv')
stimuli2 = pd.read_csv('math_stimuli2.csv')


colNames = stimuli1.columns

stim1_rows = stimuli1.shape[0]
stim2_rows = stimuli2.shape[0]

df1 = pd.DataFrame(columns=colNames)
df2 = pd.DataFrame(columns=colNames)

def fileSorter(stimuli, rows):
    
    rowList=[]

    for row in range(rows):
        choice = stimuli.iat[row, 1]
        splitChoice = choice.split()
        num1 = int(splitChoice[0])
        num2 = int(splitChoice[2])
        if num1 < 10 and num2 < 10:
            rowList.append(row)
    
    return rowList

firstList = fileSorter(stimuli1, stim1_rows)
secondList = fileSorter(stimuli2, stim2_rows)

rows = stimuli1.loc[firstList]
print(rows)
df1 = df1.append(rows, ignore_index=True)
rows2 = stimuli2.loc[secondList]
df1 = df1.append(rows2, ignore_index=True)

df1.to_csv("easy_math.csv")
# df2.to_csv("hard_math.csv")
        