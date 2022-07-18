import os
import random
import pandas as pd

PATH = "/Users/Louis/OneDrive/Smallwood/Scripts/2-back/WM Stimuli/"
# STIMTYPES = ['BODY', 'BP1', 'BP2', 'BP3', 'FACES', 'SCENES1', 'SCENES2', 'TOOLS']
STIMTYPES = 'FACES'

def swapPos(itms, pos1, pos2):
    itms[pos1], itms[pos2] = itms[pos2], itms[pos1]
    return itms

def imglister(sample, ct):
    itemlist = []

    count = 0
    while count < ct:
        item = random.choice(sample)
        if item not in itemlist:
            itemlist.append(item)
            count += 1
        else: 
            continue

    return itemlist

def imgdicter(itemlist, dictlist, imgfldr, trialtype):
    count = 1
    l_count = 1
    for item in itemlist:
        itemdict = {}
        itemdict['stimulus type'] = imgfldr
        itemdict['image'] = item
        itemdict['trial type'] = trialtype
        if trialtype == 'target':
            itemdict['pair'] = count
            itemdict['lure'] = None
            count += 1
            itemdict['correct_ans'] = 1
        elif trialtype == 'target-lure':
            itemdict['pair'] = None
            itemdict['lure'] = l_count
            l_count += 1
            itemdict['correct_ans'] = 2
        else:
            itemdict['pair'] = None
            itemdict['lure'] = None
            itemdict['correct_ans'] = 2
        dictlist.append(itemdict)
    
    return dictlist

def imgsampler(imgfldr, trial_num=10, target_num=2, tlure_num=2):
    path = os.path.join(PATH, imgfldr)

    imgs = trial_num - (target_num + tlure_num)
    imglist = imglister(os.listdir(path), imgs)

    t_list = imglister(imglist, target_num)

    tlsample = [x for x in imglist if x not in t_list]
    tl_list = imglister(tlsample, tlure_num)

    imgdictlist1 = []

    imgdictlist2 = imgdicter(imglist, imgdictlist1, imgfldr, 'non-target')
    imgdictlist3 = imgdicter(t_list, imgdictlist2, imgfldr, 'target')
    imgdictlist = imgdicter(tl_list, imgdictlist3, imgfldr, 'target-lure')

    return imgdictlist

def prep_blks(block_num=1):
    blklist = imglister(STIMTYPES, block_num)
    return blklist

def prep_targs(imgsample, n=2):
    targlist = [x for x in imgsample if x['trial type'] == 'target']
    
    nposlist = []
    for targ in targlist:
        for trial in imgsample:
            if trial['image'] == targ['image'] and trial['trial type'] == 'non-target':  
                trial['pair'] = targ['pair']
                npos = imgsample.index(trial)
                nposlist.append(npos)

    for npos in nposlist:
        for i in range(6, len(imgsample)):
            if imgsample[i]['pair'] == imgsample[npos]['pair'] and imgsample[i]['trial type'] == 'target':
                imgsample = swapPos(imgsample, npos + n, i)
                break

    return imgsample

def prep_lures(imgsample, tlure_num=2, n=2):
    lurelist = [x for x in imgsample if x['trial type'] == 'target-lure']
    
    # print(imgsample)
    # print('*' * 50)

    # print(lurelist)
    # print('*' * 50)

    poslist = []
    for i in range(len(imgsample)):
        poslist.append(i)

    print(poslist)

    targlist = []
    for trial in imgsample:
        if trial['pair'] != None:
            pos = imgsample.index(trial)
            targlist.append(pos)

    newposlist = [x for x in poslist if x not in targlist]

    llist = []
    plist = []
    for lure in lurelist:
        for trial in imgsample:
            if trial['image'] == lure['image'] and trial['trial type'] == 'non-target':
                pos = imgsample.index(trial)
                print(newposlist)
                lposlist = [x for x in newposlist if pos - x != n and x - pos != n]
                llist.append(pos)
                print(lposlist)

                if len(poslist) > 1:
                    lurepos = imglister(lposlist, 1)
                    lurepos = lurepos[0]
                else:
                    lurepos = lposlist[0]

                plist.append(lurepos)
                newposlist.remove(lurepos)
                print(lurepos)
                # print('*' * 50)

                count = 0
                for i in range(7, len(imgsample)):
                    if imgsample[i]['trial type'] == 'target-lure' and imgsample[i]['trial type'] == lure['image']:
                        imgsample = swapPos(imgsample, lurepos, i)
                        newposlist.remove(i)
                        count += 1

            elif trial['trial type'] == 'target-lure':
                break

    
    # print(imgsample)
    # print('*' * 50)

    for lpos in plist:
        lure = imgsample[lpos]
        for pos in llist:
            img = imgsample[pos]
            if lure['image'] == img['image']:
                if lpos < pos:
                    imgsample = swapPos(imgsample, lpos, pos)
                    break
    
    # print(imgsample)

    return imgsample

def prep_lures_2(imgsample, lures=[1,3,4], trial_num=10):
    lurelist = [x for x in imgsample if x['trial type'] == 'target-lure']
    
    llist = []
    for lure in lurelist:
        for trial in imgsample:
            if trial['image'] == lure['image'] and trial['trial type'] == 'non-target':  
                trial['lure'] = lure['lure']
                lpos = imgsample.index(trial)
                llist.append(lpos)
        
    
    for lpos in llist:
        for i in range(7, len(imgsample)):
            if imgsample[i]['lure'] == imgsample[lpos]['lure'] and imgsample[i]['trial type'] == 'target-lure':
                if imgsample[lpos + lures[0]]['lure'] == None and imgsample[lpos + lures[0]]['pair'] == None:
                    imgsample = swapPos(imgsample, lpos + lures[0], i)
                elif lpos + lures[2] < trial_num and imgsample[lpos + lures[1]]['lure'] == None and imgsample[lpos + lures[1]]['pair'] == None:
                    imgsample = swapPos(imgsample, lpos + lures[1], i)
                elif lpos + lures[2] < trial_num and imgsample[lpos + lures[2]]['lure'] == None and imgsample[lpos + lures[2]]['pair'] == None:
                    imgsample = swapPos(imgsample, lpos + lures[2], i)
                else:
                    print("not happening bub, keepin the lure where it is")
                    break
    
    return imgsample

def prep_blk(imgsample, n=2, tlure_num=2):
    semitrials = prep_targs(imgsample=imgsample, n=n)
    trials = prep_lures_2(semitrials)
    return trials

def block_generator(block_order):
    blks = []
    for stimtype in block_order:
        imgs = imgsampler(stimtype)
        block = prep_blk(imgs)
        blks.append(block)

    return blks

def block_remover(blockSet):
    result = []

    i = 0

    for block in blockSet:
        for trial in block:
            trial['expr_onset'] = i * 2.5
            i += 1

            result.append(trial)

    return result

def new_csv_creator(dictList, csv_path=PATH):
    newData = {}
    
    for d in dictList:
        
        keys = list(d.keys())

        for key in keys:
            value = d[key]

            if key in newData:
                newData[key].append(value)
            else:
                newData[key] = [value]

    df = pd.DataFrame(newData)
    csv_path = "/Users/Louis/OneDrive/Smallwood/Scripts/2-back"
    filename = "taskblocks.csv"
    df.to_csv(os.path.join(csv_path, filename), index=False)
    print('blocks saved.')
    return csv_path

random.seed()
blk_order = prep_blks()
data = block_generator(blk_order)
random.shuffle(data)
data = block_remover(data)
data = new_csv_creator(data)









    
