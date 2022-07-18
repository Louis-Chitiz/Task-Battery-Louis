import os
import random
import pandas as pd

PATH = "/Users/Louis/OneDrive/Smallwood/Scripts/2-back/WM Stimuli/"
STIMTYPES = ['FACES', 'SCENES2']

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

def imgdicter(img, imgfldr, trialtype, block_num):
    itemdict = {}
    itemdict['block'] = block_num
    itemdict['stimulus type'] = imgfldr
    itemdict['image'] = img
    itemdict['trial type'] = trialtype
    if trialtype == 'target':
        itemdict['correct_ans'] = 1
    elif trialtype == 'target-lure':
        itemdict['correct_ans'] = 2
    else:
        itemdict['correct_ans'] = 2
    
    return itemdict

def imgsampler(imgfldr, trial_num=35, target_num=5, tlure_num=5):
    path = os.path.join(PATH, imgfldr)

    # imgs = trial_num - (target_num + tlure_num)
    imglist = imglister(os.listdir(path), trial_num)

    # t_list = imglister(imglist, target_num)

    # tlsample = [x for x in imglist if x not in t_list]
    # tl_list = imglister(tlsample, tlure_num)

    # imgdictlist = []

    # imgdictlist = imgdicter(imglist, imgdictlist1, imgfldr, 'non-target')
    # imgdictlist3 = imgdicter(t_list, imgdictlist2, imgfldr, 'target')
    # imgdictlist = imgdicter(tl_list, imgdictlist3, imgfldr, 'target-lure')

    return imglist

def prep_blks(block_num=1):
    blklist = []
    count = 1
    while count <= block_num:
        stimtype = random.choice(STIMTYPES)
        blklist.append(stimtype)
        count += 1
    return blklist

def prep_targs(block_num, imgsample, imgfldr, n=2, t_num=5, tl_num=5):
    imglist = imgsample[0:8]
    tposlist = []
    plist = []
    for i in range(t_num):
        targ = random.choice(imglist)
        pos = imgsample.index(targ)
        imgsample[pos + n] = targ
        tposlist.append(pos + n)
        
        plist.append(pos)
        plist.append(pos+n)

        tos = imglist.index(targ)  
        if tos + n <= (len(imglist) - 1):
            imglist.remove(imglist[tos + n])
        imglist.remove(targ) 
    
    poslist = [x for x in range(0, len(imgsample))]
    nts = [x for x in poslist if x not in tposlist]

    for pos in nts:
        imgsample[pos] = imgdicter(imgsample[pos], imgfldr, 'non-target', block_num)
    
    for tpos in tposlist:
        imgsample[tpos] = imgdicter(imgsample[tpos], imgfldr, 'target', block_num)

    true_nts = [x for x in nts if x not in plist]
    llist = imglister(true_nts, tl_num)
    print(llist)

    return imgsample

def prep_lures(imgsample, n=2, lures=[1,3,4], tl_num=2):
    pass
# def prep_lures(imgsample, lures=[1,3,4], tl_num = 2):

# def prep_targs(imgsample, n=2):
#     targlist = [x for x in imgsample if x['trial type'] == 'target']
    
#     nposlist = []
#     for targ in targlist:
#         for trial in imgsample:
#             if trial['image'] == targ['image'] and trial['trial type'] == 'non-target':  
#                 trial['pair'] = targ['pair']
#                 npos = imgsample.index(trial)
#                 nposlist.append(npos)

#     for x in range(nposlist[0], len(imgsample)):
#         if imgsample[x]['pair'] != None and imgsample[x]['trial type'] == 'non-target':
#             npos = imgsample.index(imgsample[x])
#             for i in range(6, len(imgsample)):
#                 if imgsample[i]['pair'] == imgsample[npos]['pair'] and imgsample[i]['trial type'] == 'target':
#                     if imgsample[npos + n]['pair'] != None :
#                         imgsample = swapPos(imgsample, npos, i - n)
#                     else:
#                         imgsample = swapPos(imgsample, npos + n, i)
#                     break

#     return imgsample

# def prep_lures(imgsample, tlure_num=2, n=2):
#     lurelist = [x for x in imgsample if x['trial type'] == 'target-lure']
    
#     # print(imgsample)
#     # print('*' * 50)

#     # print(lurelist)
#     # print('*' * 50)

#     poslist = []
#     for i in range(len(imgsample)):
#         poslist.append(i)

#     print(poslist)

#     targlist = []
#     for trial in imgsample:
#         if trial['pair'] != None:
#             pos = imgsample.index(trial)
#             targlist.append(pos)

#     newposlist = [x for x in poslist if x not in targlist]

#     llist = []
#     plist = []
#     for lure in lurelist:
#         for trial in imgsample:
#             if trial['image'] == lure['image'] and trial['trial type'] == 'non-target':
#                 pos = imgsample.index(trial)
#                 print(newposlist)
#                 lposlist = [x for x in newposlist if pos - x != n and x - pos != n]
#                 llist.append(pos)
#                 print(lposlist)

#                 if len(poslist) > 1:
#                     lurepos = imglister(lposlist, 1)
#                     lurepos = lurepos[0]
#                 else:
#                     lurepos = lposlist[0]

#                 plist.append(lurepos)
#                 newposlist.remove(lurepos)
#                 print(lurepos)
#                 # print('*' * 50)

#                 count = 0
#                 for i in range(7, len(imgsample)):
#                     if imgsample[i]['trial type'] == 'target-lure' and imgsample[i]['trial type'] == lure['image']:
#                         imgsample = swapPos(imgsample, lurepos, i)
#                         newposlist.remove(i)
#                         count += 1

#             elif trial['trial type'] == 'target-lure':
#                 break

    
#     # print(imgsample)
#     # print('*' * 50)

#     for lpos in plist:
#         lure = imgsample[lpos]
#         for pos in llist:
#             img = imgsample[pos]
#             if lure['image'] == img['image']:
#                 if lpos < pos:
#                     imgsample = swapPos(imgsample, lpos, pos)
#                     break
    
#     # print(imgsample)

#     return imgsample

# def prep_lures_2(imgsample, lures=[1,3,4], trial_num=10):
#     lurelist = [x for x in imgsample if x['trial type'] == 'target-lure']
    
#     llist = []
#     for lure in lurelist:
#         for trial in imgsample:
#             if trial['image'] == lure['image'] and trial['trial type'] == 'non-target':  
#                 trial['lure'] = lure['lure']
#                 lpos = imgsample.index(trial)
#                 llist.append(lpos)
        
    
#     for x in range(llist[0], len(imgsample)):
#         if imgsample[x]['lure'] != None and imgsample[x]['trial type'] == 'non-target':
#             lpos = imgsample.index(imgsample[x])
#             for i in range(7, len(imgsample)):
#                 if imgsample[i]['lure'] == imgsample[lpos]['lure'] and imgsample[i]['trial type'] == 'target-lure':
#                     if imgsample[lpos + lures[0]]['lure'] == None and imgsample[lpos + lures[0]]['pair'] == None:
#                         imgsample = swapPos(imgsample, lpos + lures[0], i)
#                     elif lpos + lures[1] < trial_num and imgsample[lpos + lures[1]]['lure'] == None and imgsample[lpos + lures[1]]['pair'] == None:
#                         imgsample = swapPos(imgsample, lpos + lures[1], i)
#                     elif lpos + lures[2] < trial_num and imgsample[lpos + lures[2]]['lure'] == None and imgsample[lpos + lures[2]]['pair'] == None:
#                         imgsample = swapPos(imgsample, lpos + lures[2], i)
#                     else:
#                         print("not happening bub, keepin the lure where it is")
#                         break
#                     break
    
#     return imgsample

def prep_blk(block_num, imgsample, imgfldr, n=2, tlure_num=2):
    trials = prep_targs(block_num, imgsample=imgsample, imgfldr=imgfldr)
    return trials

def block_generator(block_order):
    blks = []
    for i in range(len(block_order)):
        print("BLOCK-" + str(i + 1) + " LURE POSITIONS:")
        imgs = imgsampler(block_order[i])
        block = prep_blk((i+1), imgs, block_order[i])
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

# imgs = imgsampler('TOOLS')
# print(imgs)
# imgs2 = prep_targs(imgs, 'TOOLS')
# print(imgs2)









    
