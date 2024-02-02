from psychopy import visual, gui, data, core, event, logging, info
from psychopy.constants import * 
import numpy as np # whole numpy lib is available, prepend 'np.'
import os
from scipy.io import savemat
from copy import deepcopy as dcopy
from config import *
from packager import *

def runMemory(expInfo,taskStruct,dispStruct,keyStruct):
    memStruct = initMemory(taskStruct, dispStruct)
    rangeMemTrials = range(len(np.where(memStruct['memPool'])[0]))
    # Start memory section clock
    memStruct['memClock'] = core.Clock()
    memStruct['memSessionInfo']['startTime'] = memStruct['memClock'].getTime()
    # Starting fixation period  
    dispStruct['fixation'].setAutoDraw(True)
    dispStruct['screen'].flip()   
    dispStruct['fixation'].setAutoDraw(False)
    core.wait(memStruct['memSessionInfo']['memFixTime'])
    # Run through trials
    for mI in rangeMemTrials:       
        memStruct['mPreFix'][mI] = memStruct['memClock'].getTime()
        # Run the trial 
        memStruct = runMemoryTrial(expInfo,memStruct,dispStruct,keyStruct,mI)
    # Memory task is done - show end fixation
    dispStruct['endFixation'].setAutoDraw(True)
    dispStruct['screen'].flip()
    memStruct['memSessionInfo']['endTime'] = memStruct['memClock'].getTime()
    memStruct['memSessionInfo']['duration'] = memStruct['memSessionInfo']['startTime'] - memStruct['memSessionInfo']['endTime']
    dispStruct['endFixation'].setAutoDraw(False)
    core.wait(1)
    # Save and compute data
    dispStruct['saveScreen'].setAutoDraw(True)
    dispStruct['screen'].flip() 
    dispStruct['ITI'].start(dispStruct['wTime']) 
    memStruct = computeMemory(memStruct)	
    # Clean and save memory session
    memPack = cleanDataMemory(memStruct)
    save_obj(memPack['MemoryTask'], taskStruct['Dir']['Output']  + os.sep + 'Task' + os.sep + 'MemoryProbe' + os.sep + str(expInfo['SubNo']) + '_Data_Memory')
    savemat(taskStruct['Dir']['Output'] + os.sep + 'Task' + os.sep + 'MemoryProbe' + os.sep + 'MAT' + os.sep + str(expInfo['SubNo']) + '_Data_Memory.mat', memPack['MemoryTask'], oned_as='row')
    dispStruct['saveScreen'].setAutoDraw(False)
    dispStruct['ITI'].complete()
    # Show end-memory section screen 
    dispStruct['memEnd'] = dict()
    while True:
        dispStruct = EndPageMemory(dispStruct)
        # Wait for starting confirmation response
        response = event.waitKeys(keyList=keyStruct['instrKeyDone'])
        if keyStruct['instrKeyDone'] in response:
            break
    return()

def initMemory(taskStruct, dispStruct):
    # Initialize inputs
    memStruct = dict()
    familiarity = taskStruct['familiarity']
    stimIDs = taskStruct['stimID']
    # Initialize familiar and novel vectors
    familiarStims = np.zeros(len(stimIDs),dtype='bool')
    novelStims = np.zeros(len(stimIDs),dtype='bool')
    # Pull out list of familiar stimuli
    familiarStims[np.where(familiarity > 0)[0]] = True
    # Pull out list of novel stimuli
    novelSet = np.where(familiarity == 0)[0] #indices for stimID
    novelStims[np.random.choice(novelSet,len(np.where(familiarStims)[0]),replace=False)] = True
    # Combine familiar and novel to create a stimulus pool for the memory section
    memStruct['memPool'] = familiarStims + novelStims
    # Create a randomized vector of which element to pull from the large list of all stims in experiment
    memStruct['memStimIndex'] = np.where(memStruct['memPool'])[0] # index of trial tI within the larger vector of all stims
    np.random.shuffle(memStruct['memStimIndex']) # This object is the index of what was presented on trial tI   
    # Get the stim IDs for this index
    memStruct['memIDs'] = stimIDs[memStruct['memStimIndex']]
    # Store all memID images into an imageCache
    if 'memImageCache' in memStruct:
        del memStruct['memImageCache']
    memImageCache = dict()
    for i in memStruct['memIDs']:
        stimNo = i
        #imageCache[i] = visual.TextStim(screen, text=str(stimNo), color = 'black', height =0.15, font = dispStruct['textFont'], wrapWidth = 1.8)
        memImageCache[i] = visual.ImageStim(win=dispStruct['screen'], image=taskStruct['Dir']['StimCues']+os.sep+'s'+str(stimNo)+'.bmp')
        memImageCache[i].rescaledSize = rescaleStim(memImageCache[i],dispStruct['memStimSize'],dispStruct)
        memImageCache[i].setSize(memImageCache[i].rescaledSize)
        memImageCache[i].pos = dispStruct['memStimPos']
        # to index the cached visual.ImageStim objects, use imageCache[index]
    memStruct['memImageCache'] = memImageCache
    
    # Data tracking - determined
    memStruct['isNovel'] = novelStims[memStruct['memStimIndex']]
    memStruct['isFamiliar'] = familiarStims[memStruct['memStimIndex']]
    memStruct['familiarity'] = familiarity[memStruct['memStimIndex']]
    # Data tracking - awaiting response
    memStruct['OldNewRating'] = np.empty(len(memStruct['memStimIndex'])) # Code so '1' is old and '2' is new regardless of counterbalance
    memStruct['OldNewRT'] = np.empty(len(memStruct['memStimIndex']))
    memStruct['ConfRating'] = np.empty(len(memStruct['memStimIndex'])) # Code up confidence so '1' is sure old and '4' is sure new, regardless of counterbalance
    memStruct['ConfRT'] = np.empty(len(memStruct['memStimIndex']))
    # Data tracking - need to be computed
    memStruct['ACC'] = np.empty(len(memStruct['memStimIndex']))
    memStruct['isFalseHit'] = np.empty(len(memStruct['memStimIndex']))
    memStruct['isFalseMiss'] = np.empty(len(memStruct['memStimIndex']))
    # Create a dictionary for memory task info
    memStruct['memSessionInfo'] = dict()
    memStruct['memSessionInfo']['numFamiliarStims'] = len(np.where((familiarStims))[0])
    memStruct['memSessionInfo']['numNovelStims'] = len(np.where((novelStims))[0])
    memStruct['memSessionInfo']['numStimsTotal'] = len(np.where((memStruct['memPool']))[0])
    memStruct['memSessionInfo']['OldNewFbTime'] = 0.5
    memStruct['memSessionInfo']['ConfFbTime'] = 0.5
    memStruct['memSessionInfo']['memFixTime'] = 0.5
    # Record memory task onsets
    memStruct['mPreFix'] = np.empty((len(memStruct['memPool']),1))
    memStruct['mONStim'] = np.empty((len(memStruct['memPool']),1))
    memStruct['mONFB'] = np.empty((len(memStruct['memPool']),1))
    memStruct['mConfStim'] = np.empty((len(memStruct['memPool']),1))
    memStruct['mConfFB'] = np.empty((len(memStruct['memPool']),1))
    return(memStruct)

def runMemoryTrial(expInfo,memStruct,dispStruct,keyStruct,mI):
    # Pull out the stimulus for this trial, from the imageCache
    trialStimID = memStruct['memIDs'][mI]
    trialStimObj = memStruct['memImageCache'][trialStimID]
    ## Old New Section
    # Clear rating scale from previous trials
    dispStruct['OldNewScaleQ'].reset() # reset the rating scale
    OldNewRT = 0 # reset the rating RT
    # Show stim
    dispStruct['screen'].flip()
    OldNewStimOnset = memStruct['memClock'].getTime()
    # Draw rating scale
    dispStruct['memMachine'].setAutoDraw(True)
    dispStruct['memMachineSlots'].setAutoDraw(True)
    trialStimObj.setAutoDraw(True)
    event.clearEvents()
    while dispStruct['OldNewScaleQ'].noResponse:
        dispStruct['OldNewScaleQ'].draw()
        dispStruct['OldNewScaleKeys'].draw()
        dispStruct['screen'].flip()
    # Query to see if response was given
    OldNewResp = dispStruct['OldNewScaleQ'].getRating()
    OldNewRT = dispStruct['OldNewScaleQ'].getRT()
    # If response given in time: 
    if OldNewRT < dispStruct['OldNewScaleQ'].maxTime:
        # Keep response
        OldNewOutOnset = memStruct['memClock'].getTime()
        # show green box - feedback 
        dispStruct['memFB'].setAutoDraw(True)    
        dispStruct['screen'].flip()
        core.wait(memStruct['memSessionInfo']['OldNewFbTime'])
        dispStruct['ITI'].start(memStruct['memSessionInfo']['memFixTime'] + (dispStruct['OldNewScaleQ'].maxTime - OldNewRT))
    else:
        # Response too slow
        OldNewOutOnset = np.nan
        OldNewResp = 'NA'
        OldNewRT = np.nan        
        # show no-response error feedback
        dispStruct['noRespErr'].setAutoDraw(True)
        dispStruct['memMachine'].setAutoDraw(False)
        dispStruct['memMachineSlots'].setAutoDraw(False)
        trialStimObj.setAutoDraw(False)
        dispStruct['screen'].flip()
        core.wait(memStruct['memSessionInfo']['OldNewFbTime'])
        dispStruct['ITI'].start(memStruct['memSessionInfo']['memFixTime'])
    # Log and pack up responses
    if OldNewResp == 'Old':
        OldNewKey = 1
    elif OldNewResp == 'New':
        OldNewKey = 2
    elif OldNewResp == 'NA':
        OldNewKey = np.nan
    else: 
        OldNewKey = np.nan
    # Save trial data
    memStruct['OldNewRating'][mI] = OldNewKey
    memStruct['OldNewRT'][mI] = OldNewRT
    # Log onsets
    memStruct['mONStim'][mI] = OldNewStimOnset
    memStruct['mONFB'][mI] = OldNewOutOnset
    # Close fixation
    dispStruct['memMachine'].setAutoDraw(False)
    dispStruct['memMachineSlots'].setAutoDraw(False)
    trialStimObj.setAutoDraw(False)
    dispStruct['noRespErr'].setAutoDraw(False) 
    dispStruct['memFB'].setAutoDraw(False)    
    dispStruct['ITI'].complete()
    
    ## Confidence rating section 
    # Clear rating scale from previous trials
    dispStruct['ConfScaleQ'].reset() # reset the rating scale
    ConfRT = 0 # reset the rating RT
    # Show stim
    ConfStimOnset = memStruct['memClock'].getTime()
    # Draw rating scale
    dispStruct['memMachine'].setAutoDraw(True)
    dispStruct['memMachineSlots'].setAutoDraw(True)
    trialStimObj.setAutoDraw(True)
    event.clearEvents()
    while dispStruct['ConfScaleQ'].noResponse:
        dispStruct['ConfScaleQ'].draw()
        dispStruct['ConfScale'].draw()
        dispStruct['ConfScaleKeys'].draw()
        dispStruct['screen'].flip()	 	
    # Query to see if response was given
    ConfResp = dispStruct['ConfScaleQ'].getRating()
    ConfRT = dispStruct['ConfScaleQ'].getRT()
    # If response given in time: 
    if ConfRT < dispStruct['ConfScaleQ'].maxTime:
        # Keep response
        ConfOutOnset = memStruct['memClock'].getTime()    
        # show green box - feedback 
        dispStruct['memFB'].setAutoDraw(True) 
        dispStruct['screen'].flip()   
        core.wait(memStruct['memSessionInfo']['ConfFbTime'])
        # Clear screen before fixation
        dispStruct['memMachine'].setAutoDraw(False)
        dispStruct['memMachineSlots'].setAutoDraw(False)
        trialStimObj.setAutoDraw(False)
        dispStruct['screen'].flip()
        dispStruct['memFB'].setAutoDraw(False)
        # Show interim fixation
        dispStruct['fixation'].setAutoDraw(True)
        dispStruct['screen'].flip()
        dispStruct['ITI'].start(memStruct['memSessionInfo']['memFixTime'] + (dispStruct['ConfScaleQ'].maxTime - ConfRT))
    else:
        # Response too slow
        ConfOutOnset = np.nan
        ConfResp = 'NA'
        ConfRT = np.nan        
        # show no-response error feedback
        dispStruct['noRespErr'].setAutoDraw(True)
        dispStruct['memMachine'].setAutoDraw(False)
        dispStruct['memMachineSlots'].setAutoDraw(False)
        trialStimObj.setAutoDraw(False)
        dispStruct['screen'].flip()
        dispStruct['noRespErr'].setAutoDraw(False)
        core.wait(memStruct['memSessionInfo']['ConfFbTime'])
        # Show interim fixation
        dispStruct['fixation'].setAutoDraw(True)
        dispStruct['screen'].flip()
        dispStruct['ITI'].start(memStruct['memSessionInfo']['memFixTime'])
    # Log and pack up responses
    if ConfResp == 'Sure old':
        ConfKey = 1
    elif ConfResp == 'Not sure old':
        ConfKey = 2
    elif ConfResp == 'Not sure new':
        ConfKey = 3
    elif ConfResp == 'Sure new':
        ConfKey = 4
    elif ConfResp == 'NA':
        ConfKey = np.nan
    else:
        ConfKey = np.nan
    # Save trial data
    memStruct['ConfRating'][mI] = ConfKey
    memStruct['ConfRT'][mI] = ConfRT
    # Log onsets
    memStruct['mConfStim'][mI] = ConfStimOnset
    memStruct['mConfFB'][mI] = ConfOutOnset
    dispStruct['fixation'].setAutoDraw(False)
    dispStruct['ITI'].complete()
    return(memStruct)


def computeMemory(memStruct):
    # Compute memory accuracy
    for i in range(len(memStruct['memStimIndex'])):
        if (memStruct['isFamiliar'][i] == True and memStruct['OldNewRating'][i] == 1) or (memStruct['isNovel'][i] == True and memStruct['OldNewRating'][i] == 2):
            memStruct['ACC'][i] = 1
        elif np.isnan(memStruct['OldNewRating'][i]):
            memStruct['ACC'][i] = np.nan
        else: 
            memStruct['ACC'][i] = 0
    #Compute false hits on old (is actually new, rated as old)
    for i in range(len(memStruct['memStimIndex'])):
        if (memStruct['isNovel'][i] == True and memStruct['OldNewRating'][i] == 1):
            memStruct['isFalseHit'][i] = 1
        elif np.isnan(memStruct['OldNewRating'][i]):
            memStruct['isFalseHit'][i] = np.nan
        else: 
            memStruct['isFalseHit'][i] = 0
    # Compute false misses on old (is actually old, rated as new)
    for i in range(len(memStruct['memStimIndex'])):
        if (memStruct['isFamiliar'][i] == True and memStruct['OldNewRating'][i] == 2):
            memStruct['isFalseMiss'][i] = 1
        elif np.isnan(memStruct['OldNewRating'][i]):
            memStruct['isFalseMiss'][i] = np.nan
        else: 
            memStruct['isFalseMiss'][i] = 0
    # Computer overall percent accurate
    accuracyVec = dcopy(memStruct['ACC'])
    accuracyVec = accuracyVec[~np.isnan(accuracyVec)]
    memStruct['memPercent'] = np.sum(accuracyVec)/len(accuracyVec)
    return(memStruct)


def EndPageMemory(dispStruct):
    # Session end page
    dispStruct['memEnd']['page1_head'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.09, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['memEnd']['page1_head'].text = '--Session End--'
    dispStruct['memEnd']['page1_head'].pos = [0,0.8]
    # Session text 1
    dispStruct['memEnd']['page1_text1'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['memEnd']['page1_text1'].text = 'This marks the end of the experiment.'
    dispStruct['memEnd']['page1_text1'].pos = [0,0.2]
    # Session text 2
    dispStruct['memEnd']['page1_text2'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['memEnd']['page1_text2'].text = 'Please tell the experimenter you are done. Thanks!'
    dispStruct['memEnd']['page1_text2'].pos = [0,-0.2]
    # Draw page
    dispStruct['memEnd']['page1_head'].draw()
    dispStruct['memEnd']['page1_text1'].draw()
    dispStruct['memEnd']['page1_text2'].draw()
    dispStruct['screen'].flip()
    return(dispStruct)
