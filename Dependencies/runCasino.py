from psychopy import visual, gui, data, core, event, logging, info
from psychopy.constants import *
import numpy as np # whole numpy lib is available, prepend 'np.'
import os
from scipy.io import savemat
from config import *
from packager import *

def runCasino(expInfo,taskStruct,dispStruct,dispInfo,keyStruct):
    dispStruct['Start'] = dict()
    dispStruct['End'] = dict()
    ## Initialize session parameters
    taskStruct['sessionInfo']['numBlockStims'] = np.zeros(taskStruct['blocksPerSession'],dtype='int')+6
    taskStruct['sessionInfo']['numBlockNovels'] = np.zeros(taskStruct['blocksPerSession'],dtype='int')+2
    taskStruct['sessionInfo']['startTime'] = dict()
    taskStruct['sessionInfo']['endTime'] = dict()
    # Run start page depending on whether it's a fresh run
    if expInfo['Version'] == 'full' or (expInfo['Version'] == 'part' and int(expInfo['Starting Run']) == 1):
        startSession = range(taskStruct['numSessions']) # start from first session
        # Display endowment/starting page
        currPage = 1
        while True:
            dispStruct = feval('StartPage_' + str(currPage),expInfo,dispStruct,taskStruct)
            # Wait for starting confirmation response
            response = event.waitKeys(keyList=[keyStruct['instrKeyNext'],'escape'])
            if keyStruct['instrKeyNext'] in response:
                break
            elif 'escape' in response:
                print "Aborting program..."
                core.wait(2)
                core.quit()
    # If starting mid-way through task, don't show endowment page
    elif expInfo['Version'] == 'part' and (not int(expInfo['Starting Run']) == '1'):
        startSession = range((int(expInfo['Starting Run']) - 1),taskStruct['numSessions']) # stat from specified session (note that initCasino will be turned off if this is the case)
    # Initialize session event counter
    TaskEventAbs = -1
    # Loop through sessions
    for sI in startSession:
        # clear session-specific variables if not first session
        if sI > 0 and (expInfo['Version'] == 'full' or (expInfo['Version'] == 'part' and int(expInfo['Starting Run']) == '1')):
            del taskStruct['sessionClock']
            del outPack
            del matOut
        # Intialize within-session counter
        TaskEventSess = -1
        sessionStruct = taskStruct['sessions'][sI]
        # Wait for scanner pulse if fMRI
        if expInfo['Modality'] == 'fMRI':
            while True:
                # Draw pulse-wait screen
                dispStruct['experimenter'].draw()
                dispStruct['screen'].flip()
                # Wait for starting confirmation response
                response = event.waitKeys(keyList=[keyStruct['instrKeyDone'],'escape'])
                if keyStruct['instrKeyDone'] in response:
                    break
                elif 'escape' in response:
                    print "Aborting program..."
                    core.wait(2)
                    core.quit()
            while True:
                # Draw pulse-wait screen
                dispStruct['pulse'].draw()
                dispStruct['screen'].flip()
                # Wait for starting confirmation response
                response = event.waitKeys(keyList=[keyStruct['pulseKeyCode'],'escape'])
                if keyStruct['pulseKeyCode'] in response:
                    break
                elif 'escape' in response:
                    print "Aborting program..."
                    core.wait(2)
                    core.quit()
        # Get session start time
        taskStruct['sessionClock'] = core.Clock()
        taskStruct['sessionInfo']['startTime'][sI] = taskStruct['sessionClock'].getTime()
        for bI in range(taskStruct['blocksPerSession']):
            print 'Session # ' + str(sI+1) + ': Block # ' + str(bI+1)
            # end temp print
            blockStruct = sessionStruct['blocks'][bI]
            # Load transit (airport) screen
            dispStruct = blockRouletteStartScreen(dispStruct,taskStruct)
            # Initialize roulette trial section
            dispStruct['ITI'].start(1)
            # Create numpy array of roulette trial outcomes
            blockStruct['roulWin'] = np.ones(blockStruct['numRoulettes'],dtype='int')
            blockStruct['roulWin'][0:int(np.rint(len(blockStruct['roulWin'])/2))] = -1
            np.random.shuffle(blockStruct['roulWin'])
            dispStruct['ITI'].complete() # Close static period
            # Run through roulette trials
            for rI in range(blockStruct['numRoulettes']):
                # Show fixation before trial
                dispStruct['fixation'].setAutoDraw(True)
                dispStruct['screen'].flip()
                blockStruct['rPreFix'][rI] = taskStruct['sessionClock'].getTime()
                # Set up roulette trial
                dispStruct['ITI'].start(taskStruct['preFixTime'])
                [blockStruct,dispStruct,winTrial,winVal] = initRoulTrial(taskStruct, dispStruct, blockStruct, sI, bI, rI)
                # Update counters
                TaskEventAbs = TaskEventAbs + 1
                TaskEventSess = TaskEventSess + 1
                # Record trial type for this event
                taskStruct['taskEventNoAbsType'][TaskEventAbs]='Roul'
                taskStruct['taskEventNoSessionType'][sI][TaskEventSess] = 'Roul'
                # Record total points at start of trial
                currTotal = dispStruct['currBarLength'] - dispStruct['pointsBarXLeft']
                taskStruct['totalPointsScaled'][TaskEventAbs,0] = currTotal
                dispStruct['ITI'].complete()
                # Run roulette trial!
                [dispStruct,blockStruct] = runRouletteTrial(taskStruct, dispStruct, keyStruct, blockStruct, winTrial, winVal, rI)
                # If no response on context roulette trial, then push context roulette to the next trial: 
                if blockStruct['roulRespKey'][rI] == 'N':
                    blockStruct['rouletteContext'] += 1                 
                # Reset currBar color
                dispStruct['currBar'].lineColor = 'royalblue'
                dispStruct['currBar'].fillColor = 'royalblue'
                # Record total points at end of trial
                currTotal = dispStruct['currBarLength'] - dispStruct['pointsBarXLeft']
                taskStruct['totalPointsScaled'][TaskEventAbs,1] = currTotal
            # Get timing for this block
            blockClock = core.Clock()
            blockStruct['blockStartTime'] = blockClock.getTime()
            # Specify state names (and flags), and load state-start screen
            dispStruct = blockStartScreen(dispStruct,taskStruct,blockStruct)
            # Intitialize block information
            dispStruct['ITI'].start(1)
            # Initialize block
            # Update the stimulus pool
            [taskStruct['stimPool'], taskStruct['isBurned']] = updateStimPool(taskStruct,sI,bI)
            # Initialize the block
            [blockStruct,dispStruct] = initBlock(taskStruct,dispStruct,blockStruct,bI)
            dispStruct['ITI'].complete() # Close static period
            # Timing habituation trials
            for htI in range(taskStruct['numHabitTrials']):
                dispStruct['fixation'].setAutoDraw(True)
                dispStruct['screen'].flip()
                blockStruct['hPreFix'][htI] = taskStruct['sessionClock'].getTime()
                dispStruct['ITI'].start(taskStruct['preFixTime'])
                # Update counters
                TaskEventAbs = TaskEventAbs + 1
                TaskEventSess = TaskEventSess + 1
                # Record trial type for this event
                taskStruct['taskEventNoAbsType'][TaskEventAbs]='Prac'
                taskStruct['taskEventNoSessionType'][sI][TaskEventSess] = 'Prac'
                # Record total points at start/end of trial
                currTotal = dispStruct['currBarLength'] - dispStruct['pointsBarXLeft']
                taskStruct['totalPointsScaled'][TaskEventAbs,0] = currTotal
                taskStruct['totalPointsScaled'][TaskEventAbs,1] = currTotal
                dispStruct['ITI'].complete()
                # Run timing-habituation trials
                [taskStruct,blockStruct] = runHabitTrial(taskStruct, dispStruct, keyStruct, blockStruct, htI)
            # End habituation trials
            dispStruct = habitEndScreen(dispStruct)
            # print diagnostics
            #print 'familarStims ' + str(np.where(taskStruct['familiarity'] > 0)[0])
            #print 'updated stimPool ' + str(np.where(taskStruct['stimPool'])[0])
            # Proceed to trials
            for tI in range(blockStruct['numTrials']):
                # show fixation while loading
                dispStruct['fixation'].setAutoDraw(True)
                dispStruct['screen'].flip()
                blockStruct['tPreFix'][tI] = taskStruct['sessionClock'].getTime()
                # Set up trial structure
                dispStruct['ITI'].start(taskStruct['preFixTime'])
                blockStruct = initTrial(taskStruct,dispStruct,blockStruct,tI)
                # Update counters
                TaskEventAbs = TaskEventAbs + 1
                TaskEventSess = TaskEventSess + 1
                # Record trial type for this event
                taskStruct['taskEventNoAbsType'][TaskEventAbs]='Band'
                taskStruct['taskEventNoSessionType'][sI][TaskEventSess] = 'Band'
                # Record total points at start of trial
                currTotal = dispStruct['currBarLength'] - dispStruct['pointsBarXLeft']
                taskStruct['totalPointsScaled'][TaskEventAbs,0] = currTotal
                dispStruct['ITI'].complete()
                # Run the trial
                [taskStruct,dispStruct,blockStruct] = runCasinoTrial(taskStruct, dispStruct, keyStruct, blockStruct, tI)
                # update the exposure count
                taskStruct['familiarity'][blockStruct['isTrialStim'][tI]] = taskStruct['familiarity'][blockStruct['isTrialStim'][tI]] + 1
                # Record total points at end of trial
                currTotal = dispStruct['currBarLength'] - dispStruct['pointsBarXLeft']
                taskStruct['totalPointsScaled'][TaskEventAbs,1] = currTotal
                # Subjective rating section
                if tI == 20 and taskStruct['sessionInfo']['moodRatingBlockNum'][sI,0] == bI:
                    # show fixation while loading
                    dispStruct['fixation'].setAutoDraw(True)
                    dispStruct['screen'].flip()
                    blockStruct['sPreFix'] = taskStruct['sessionClock'].getTime()
                    # Set up trial structure
                    dispStruct['ITI'].start(taskStruct['preFixTime'])
                    # Update counters
                    TaskEventAbs = TaskEventAbs + 1
                    TaskEventSess = TaskEventSess + 1
                    # Record trial type for this event
                    taskStruct['taskEventNoAbsType'][TaskEventAbs]='Subj'
                    taskStruct['taskEventNoSessionType'][sI][TaskEventSess] = 'Subj'
                    # Record total points at start/end of trial
                    currTotal = dispStruct['currBarLength'] - dispStruct['pointsBarXLeft']
                    taskStruct['totalPointsScaled'][TaskEventAbs,0] = currTotal
                    taskStruct['totalPointsScaled'][TaskEventAbs,1] = currTotal
                    dispStruct['fixation'].setAutoDraw(False)
                    dispStruct['ITI'].complete()
                    # Present subjective rating screen
                    [taskStruct,blockStruct] = runSubjRatingTrial(taskStruct, dispStruct, blockStruct, sI)
            # Block is done - show post block reset screen
            dispStruct = blockEndScreen(dispStruct)
            dispStruct['screen'].flip()
            # end block loop
        dispStruct['endFixation'].setAutoDraw(True)
        dispStruct['screen'].flip()
        taskStruct['sessionInfo']['endTime'][sI] = taskStruct['sessionClock'].getTime()
        dispStruct['endFixation'].setAutoDraw(False)
        core.wait(1)
        #  Save procedure
        dispStruct['saveScreen'].setAutoDraw(True)
        dispStruct['screen'].flip()
        dispStruct['ITI'].start(dispStruct['wTime'])
        # Clean and pack up data
        outPack = cleanDataSession(taskStruct,dispInfo,keyStruct,sI)
        # Save data (for current session)
        save_obj(outPack['Task'], taskStruct['Dir']['Output']  + os.sep + 'Task' + os.sep + 'Sessions' + os.sep + str(expInfo['SubNo']) + '_Data_sess' + str(sI+1))
        save_obj(outPack['Display'], taskStruct['Dir']['Output'] + os.sep + 'Task' + os.sep + 'Sessions' + os.sep  + str(expInfo['SubNo']) + '_Display_sess' + str(sI+1))
        save_obj(outPack['Keys'], taskStruct['Dir']['Output'] + os.sep + 'Task' + os.sep + 'Sessions' + os.sep  + str(expInfo['SubNo']) + '_Keys_sess' + str(sI+1))
        # Save as .mat files (for current session)
        matOut = convertMatSession(outPack,sI)
        savemat(taskStruct['Dir']['Output'] + os.sep + 'Task' + os.sep + 'Sessions' + os.sep + 'MAT' + os.sep + str(expInfo['SubNo']) + '_Data_sess' + str(sI+1) + '.mat', matOut, oned_as='row')
        dispStruct['saveScreen'].setAutoDraw(False)
        dispStruct['ITI'].complete()
        # Show end-session screen
        if not sI == taskStruct['numSessions'] - 1:
            while True:
                dispStruct = EndPage(expInfo,dispStruct,taskStruct)
                # Wait for starting confirmation response
                response = event.waitKeys(keyList=keyStruct['instrKeyNext'])
                if keyStruct['instrKeyNext'] in response:
                    break
    #  Save procedure
    dispStruct['saveScreen'].setAutoDraw(True)
    dispStruct['screen'].flip()
    dispStruct['ITI'].start(dispStruct['wTime'])
    # Clean and pack up data
    outPack = cleanData(taskStruct,dispInfo,keyStruct,startSession,'Task')
    # Save data (for current session)
    save_obj(outPack['Task'], taskStruct['Dir']['Output']  + os.sep + 'Task' + os.sep + str(expInfo['SubNo']) + '_Data_All')
    save_obj(outPack['Display'], taskStruct['Dir']['Output'] + os.sep + 'Task' + os.sep  + str(expInfo['SubNo']) + '_Display_All')
    save_obj(outPack['Keys'], taskStruct['Dir']['Output'] + os.sep + 'Task' + os.sep  + str(expInfo['SubNo']) + '_Keys_All')
    # Save as .mat files (for current session)
    matOut = convertMat(outPack,startSession,'Task')
    savemat(taskStruct['Dir']['Output'] + os.sep + 'Task' + os.sep + 'MAT' + os.sep + str(expInfo['SubNo']) + '_Data_All.mat', matOut, oned_as='row')
    dispStruct['saveScreen'].setAutoDraw(False)
    dispStruct['ITI'].complete()
    # Calculate and output payment
    currTotal = dispStruct['currBarLength'] - dispStruct['pointsBarXLeft']
    payOut = payment(taskStruct['maxMoney'],currTotal)
    np.savetxt(taskStruct['Dir']['Payment'] + os.sep + 'sub' + str(expInfo['SubNo']) + '_Payment.txt', ["Payment Amount: $%s" % payOut], fmt='%s')
    # Show end-task screen
    while True:
        dispStruct = EndTask(dispStruct,taskStruct)
        # Wait for starting confirmation response
        response = event.waitKeys(keyList=keyStruct['instrKeyDone'])
        if keyStruct['instrKeyDone'] in response:
            break
    return(taskStruct,dispStruct,keyStruct)

def StartPage_1(expInfo,dispStruct,taskStruct):
    # Session starting page
    dispStruct['Start']['page1_head'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.09, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Start']['page1_head'].text = '--Game Start--'
    dispStruct['Start']['page1_head'].pos = [0,0.8]
    # Session text 1
    dispStruct['Start']['page1_text1'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Start']['page1_text1'].text = 'We are now giving your starting amount of:'
    dispStruct['Start']['page1_text1'].pos = [0,0.2]
    # Session text 2
    dispStruct['Start']['page1_text2'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.14, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Start']['page1_text2'].text = taskStruct['startAmount']
    dispStruct['Start']['page1_text2'].pos = [0,0]
    # Session text 3
    dispStruct['Start']['page1_text3'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Start']['page1_text3'].text = 'You are now playing for real amounts.'
    dispStruct['Start']['page1_text3'].pos = [0,-0.2]
    # Session text 4
    dispStruct['Start']['page1_text4'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Start']['page1_text4'].text = 'The outcomes you get will determine how much money you leave with.'
    dispStruct['Start']['page1_text4'].pos = [0,-0.4]
    # Session text 5
    dispStruct['Start']['page1_text5'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispStruct['textFont'], wrapWidth = 1.8)
    dispStruct['Start']['page1_text5'].pos = [0,-0.8]
    if expInfo['Modality'] == 'behaviour':
        dispStruct['Start']['page1_text5'].text = 'Please get ready, and press ' + taskStruct['instrKeyNextName'] + ' to begin.'
    elif expInfo['Modality'] == 'fMRI':
        dispStruct['Start']['page1_text5'].text = 'Please keep still, and press ' + taskStruct['instrKeyNextName'] + ' to begin.'
    # Set up win bar for initial starting amount
    dispStruct['winBarLength'] = dispStruct['pointsBarXLeft']+scalePoints(taskStruct,taskStruct['startVal'])
    dispStruct['winBarVert'] = [(dispStruct['pointsBarXLeft'],dispStruct['pointsBarYTop']),(dispStruct['winBarLength'],dispStruct['pointsBarYTop']),(dispStruct['winBarLength'],dispStruct['pointsBarYBottom']),(dispStruct['pointsBarXLeft'],dispStruct['pointsBarYBottom'])]
    dispStruct['winBar'].vertices = dispStruct['winBarVert']
    # Intialize currBar length
    dispStruct['currBarLength'] = dispStruct['pointsBarXLeft']+scalePoints(taskStruct,taskStruct['startVal'])
    dispStruct['currBarVert'] = [(dispStruct['pointsBarXLeft'],dispStruct['pointsBarYTop']),(dispStruct['currBarLength'],dispStruct['pointsBarYTop']),(dispStruct['currBarLength'],dispStruct['pointsBarYBottom']),(dispStruct['pointsBarXLeft'],dispStruct['pointsBarYBottom'])]
    dispStruct['currBar'].vertices = dispStruct['currBarVert']
    # Draw page
    dispStruct['Start']['page1_head'].draw()
    dispStruct['Start']['page1_text1'].draw()
    dispStruct['Start']['page1_text2'].draw()
    dispStruct['Start']['page1_text3'].draw()
    dispStruct['Start']['page1_text4'].draw()
    dispStruct['pointsBar'].draw()
    dispStruct['winBar'].draw()
    dispStruct['Start']['page1_text5'].draw()
    dispStruct['screen'].flip()
    return(dispStruct)


def EndPage(expInfo, dispStruct,taskStruct):
    # Session end page
    dispStruct['End']['page1_head'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.09, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['End']['page1_head'].text = '--Session End--'
    dispStruct['End']['page1_head'].pos = [0,0.8]
    # Session text 1
    dispStruct['End']['page1_text1'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['End']['page1_text1'].text = 'This session has now ended.'
    dispStruct['End']['page1_text1'].pos = [0,0.2]
    # Session text 2
    dispStruct['End']['page1_text2'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['End']['page1_text2'].text = 'Take a short break, and get ready for the next session.'
    dispStruct['End']['page1_text2'].pos = [0,-0.2]
    # Session text 3
    dispStruct['End']['page1_text3'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispStruct['textFont'], wrapWidth = 1.8)
    dispStruct['End']['page1_text3'].pos = [0,-0.8]
    if expInfo['Modality'] == 'behaviour':
        dispStruct['End']['page1_text3'].text = 'Please get ready, and press ' + taskStruct['instrKeyNextName'] + '.'
    elif expInfo['Modality'] == 'fMRI':
        dispStruct['End']['page1_text3'].text = 'Please keep still, and press ' + taskStruct['instrKeyNextName'] + '.'
    # Draw page
    dispStruct['End']['page1_head'].draw()
    dispStruct['End']['page1_text1'].draw()
    dispStruct['End']['page1_text2'].draw()
    dispStruct['End']['page1_text3'].draw()
    dispStruct['screen'].flip()
    return(dispStruct)



def blockRouletteStartScreen(dispStruct,taskStruct):
    # Define block intro screen text
    dispStruct['roulIntroText'] = visual.TextStim(dispStruct['screen'], color = 'black', font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['roulIntroText'].text = 'You are in transit to a new country.'
    dispStruct['roulIntroText'].pos = [0,0.5]
    dispStruct['roulIntroText'].height = dispStruct['stateNameTrialHeight']
    # Define block intro screen flag
    dispStruct['roulIntroFlag'] = visual.ImageStim(dispStruct['screen'])
    dispStruct['roulIntroFlag'].setImage(taskStruct['Dir']['Global'] + os.sep + "airport.png")
    dispStruct['roulIntroFlag'].rescaledSize = rescale(dispStruct['roulIntroFlag'], 0.9)
    dispStruct['roulIntroFlag'].setSize(dispStruct['roulIntroFlag'].rescaledSize)
    dispStruct['roulIntroFlag'].pos = [0,0]
    # Draw
    dispStruct['roulIntroText'].setAutoDraw(True)
    dispStruct['roulIntroFlag'].setAutoDraw(True)
    dispStruct['footer'].setAutoDraw(True)
    # Count Down
    dispStruct['counter2'].draw()
    dispStruct['screen'].flip()
    core.wait(1)
    dispStruct['counter1'].draw()
    dispStruct['screen'].flip()
    # Clear screen
    dispStruct['roulIntroText'].setAutoDraw(False)
    dispStruct['roulIntroFlag'].setAutoDraw(False)
    dispStruct['footer'].setAutoDraw(False)
    return(dispStruct)

def blockStartScreen(dispStruct,taskStruct,blockStruct):
    # Define block intro screen text
    dispStruct['stateIntroText'] = visual.TextStim(dispStruct['screen'], color = 'black', font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['stateIntroText'].text = 'Today you will be playing in ' + blockStruct['stateName']  + '!'
    dispStruct['stateIntroText'].pos = [0,0.35]
    dispStruct['stateIntroText'].height = dispStruct['stateNameTrialHeight']
    # Define block intro screen flag
    dispStruct['stateIntroFlag'] = visual.ImageStim(dispStruct['screen'])
    dispStruct['stateIntroFlag'].setImage(taskStruct['Dir']['Flags'] + os.sep + "flag_" + blockStruct['stateName']  + ".png")
    dispStruct['stateIntroFlag'].rescaledSize = rescale(dispStruct['stateIntroFlag'], dispStruct['flagBreakSize']*1.5)
    dispStruct['stateIntroFlag'].setSize(dispStruct['stateIntroFlag'].rescaledSize)
    dispStruct['stateIntroFlag'].pos = dispStruct['flagBreakPos']
    # Draw
    dispStruct['Map'].setAutoDraw(True)
    dispStruct['stateIntroText'].setAutoDraw(True)
    dispStruct['stateIntroFlag'].setAutoDraw(True)
    dispStruct['footer'].setAutoDraw(True)
    # Count down
    dispStruct['counter2'].draw()
    dispStruct['screen'].flip()
    core.wait(1)
    dispStruct['counter1'].draw()
    dispStruct['screen'].flip()
    # Clear screen
    dispStruct['Map'].setAutoDraw(False)
    dispStruct['stateIntroText'].setAutoDraw(False)
    dispStruct['stateIntroFlag'].setAutoDraw(False)
    dispStruct['footer'].setAutoDraw(False)
    return(dispStruct)

def habitEndScreen(dispStruct):
    # Text
    dispStruct['habitEndText1'] = visual.TextStim(dispStruct['screen'], color = 'black', font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['habitEndText1'].text = "Done practice. Let's get started."
    dispStruct['habitEndText1'].pos = [0,0.35]
    dispStruct['habitEndText1'].height = 0.1
    # Draw
    dispStruct['habitEndText1'].setAutoDraw(True)
    dispStruct['footer'].setAutoDraw(True)
    # Count down
    dispStruct['counter2'].draw()
    dispStruct['screen'].flip()
    core.wait(1)
    dispStruct['counter1'].draw()
    dispStruct['screen'].flip()
    core.wait(1)
    # Clear screen
    dispStruct['habitEndText1'].setAutoDraw(False)
    dispStruct['footer'].setAutoDraw(False)
    return(dispStruct)


def blockEndScreen(dispStruct):
    # Text
    dispStruct['blockEndText1'] = visual.TextStim(dispStruct['screen'], color = 'black', font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['blockEndText1'].text = 'Your time at this casino has come to an end.'
    dispStruct['blockEndText1'].pos = [0,0.35]
    dispStruct['blockEndText1'].height = 0.1
    # Draw
    dispStruct['blockEndText1'].setAutoDraw(True)
    dispStruct['footer'].setAutoDraw(True)
    # Count down
    dispStruct['counter2'].draw()
    dispStruct['screen'].flip()
    core.wait(1)
    dispStruct['counter1'].draw()
    dispStruct['screen'].flip()
    core.wait(1)
    # Clear screen
    dispStruct['blockEndText1'].setAutoDraw(False)
    dispStruct['footer'].setAutoDraw(False)
    return(dispStruct)


def initRoulTrial(taskStruct, dispStruct, blockStruct, sI, bI, rI):
    # Determine whether the roulette will win or lose this trial
    outcome = blockStruct['roulWin'][rI]
    if outcome == 1:
        winTrial = True
        winVal = taskStruct['winVal']
        for lr in range(2):
            dispStruct['rouletteFbTrial'][lr].text = taskStruct['winAmount']
    elif outcome == -1:
        winTrial = False
        winVal = taskStruct['lossVal']
        for lr in range(2):
            dispStruct['rouletteFbTrial'][lr].text = '-' + taskStruct['winAmount']
    # Context manipulation
    if (sI == 2) and (bI == 0) and (rI == blockStruct['rouletteContext']):
        # Parameters for first context manipulation
        if taskStruct['contextManip1'] == 'gain':
            winTrial = True
            winVal = taskStruct['winContextVal']
            for lr in range(2):
                dispStruct['rouletteFbTrial'][lr].text = taskStruct['winContextAmount']
        elif taskStruct['contextManip1'] == 'loss':
            winTrial = False
            winVal = taskStruct['lossContextVal']
            for lr in range(2):
                dispStruct['rouletteFbTrial'][lr].text = '-' + taskStruct['winContextAmount']
    elif (sI == 4) and (bI == 0) and (rI == blockStruct['rouletteContext']):
        # Parameters for second context manipulation
        if taskStruct['contextManip2'] == 'gain':
            winTrial = True
            winVal = taskStruct['winContextVal']
            for lr in range(2):
                dispStruct['rouletteFbTrial'][lr].text = taskStruct['winContextAmount']
        elif taskStruct['contextManip2'] == 'loss':
            winTrial = False
            winVal = taskStruct['lossContextVal']
            for lr in range(2):
                dispStruct['rouletteFbTrial'][lr].text = '-' + taskStruct['winContextAmount']
    # Pack up trial properties
    blockStruct['roulTrialWin'][rI] = winTrial
    blockStruct['roulTrialOutcomeVal'][rI] = winVal
    # End pre-trial fixation
    dispStruct['fixation'].setAutoDraw(False)
    # Show template images (bandits, slots, etc)
    for lr in range(2):
        dispStruct['rouletteTrial'][lr].setAutoDraw(True)
        dispStruct['airportName'][lr].setAutoDraw(True)
        dispStruct['airportFlag'][lr].setAutoDraw(True)
    # Show curr points bar
    dispStruct['pointsBar'].setAutoDraw(True)
    dispStruct['currBar'].setAutoDraw(True)
    return(blockStruct,dispStruct,winTrial,winVal)


def runRouletteTrial(taskStruct, dispStruct, keyStruct, blockStruct, winTrial, winVal, rI):
    # Flip screen and wait for response
    dispStruct['screen'].flip()
    stimOnset = taskStruct['sessionClock'].getTime() # get stim onset time (since start of session)
    response = event.clearEvents()
    while (taskStruct['sessionClock'].getTime()  - stimOnset) <= taskStruct['maxRT']:
        # wait for response
        response = event.getKeys(keyList=[keyStruct['respKeyLeft'],keyStruct['respKeyRight']])
        # Which option was selected
        if not response:
            respOnset = np.nan
            respKey = 'N'
            isWin = False
            outcomeOnset = np.nan
        elif response:
            isWin = winTrial
            # Get response time to calculate RT below
            respOnset = taskStruct['sessionClock'].getTime()
            # which response was made
            if keyStruct['respKeyRight'] in response:
                # right key was pressed
                respKey = 'R'
                respStimIndex = 1
            elif keyStruct['respKeyLeft'] in response:
                # left key was pressed
                respKey = 'L'
                respStimIndex = 0
            # Feedback Jitter (rotating reels)
            dispStruct['rouletteTrial'][respStimIndex].setAutoDraw(False)
            revolClock = core.Clock()
            while revolClock.getTime() < blockStruct['roulFbJitter']:
                for frames in range(11):
                    dispStruct['rotatRoulette'][respStimIndex].setImage(taskStruct['Dir']['Roulette'] + os.sep + "roulette"+str(frames)+".tiff") # recode here to store all animation frames in mem, then draw from mem
                    dispStruct['rotatRoulette'][respStimIndex].draw()
                    dispStruct['screen'].flip()
            # once the reels stop spinning, show the reward
            dispStruct['rouletteFbTrial'][respStimIndex].setAutoDraw(True)
            # Show win or loss points bar
            if isWin:
                # Show win bar
                dispStruct['currBar'].setAutoDraw(False)
                dispStruct['winBarLength'] = dispStruct['currBarLength'] + scalePoints(taskStruct,winVal)
                dispStruct['winBarVert'] = [(dispStruct['pointsBarXLeft'],dispStruct['pointsBarYTop']),(dispStruct['winBarLength'],dispStruct['pointsBarYTop']),(dispStruct['winBarLength'],dispStruct['pointsBarYBottom']),(dispStruct['pointsBarXLeft'],dispStruct['pointsBarYBottom'])]
                dispStruct['winBar'].vertices = dispStruct['winBarVert']
                dispStruct['winBar'].setAutoDraw(True)
                dispStruct['currBar'].setAutoDraw(True)           
            else:
                # Show loss bar
                dispStruct['currBar'].setAutoDraw(False)
                dispStruct['currBar'].lineColor = 'red'
                dispStruct['currBar'].fillColor = 'red'
                dispStruct['currBar'].setAutoDraw(True)
                dispStruct['lossBarLength'] = dispStruct['currBarLength'] - scalePoints(taskStruct,np.absolute(winVal))
                dispStruct['lossBarVert'] = [(dispStruct['pointsBarXLeft'],dispStruct['pointsBarYTop']),(dispStruct['lossBarLength'],dispStruct['pointsBarYTop']),(dispStruct['lossBarLength'],dispStruct['pointsBarYBottom']),(dispStruct['pointsBarXLeft'],dispStruct['pointsBarYBottom'])]
                dispStruct['lossBar'].vertices = dispStruct['lossBarVert']
                dispStruct['lossBar'].setAutoDraw(True)            
            dispStruct['screen'].flip()
            outcomeOnset = taskStruct['sessionClock'].getTime() # get outcome onset time (since start of session)
            dispStruct['rouletteFbTrial'][respStimIndex].setAutoDraw(False)
            core.wait(taskStruct['fbTime'])
            break
    # clear screen and show fixation
    for lr in range(2):
        dispStruct['rouletteTrial'][lr].setAutoDraw(False)
        dispStruct['airportName'][lr].setAutoDraw(False)
        dispStruct['airportFlag'][lr].setAutoDraw(False)
    dispStruct['pointsBar'].setAutoDraw(False)
    dispStruct['currBar'].setAutoDraw(False)
    dispStruct['winBar'].setAutoDraw(False)
    dispStruct['lossBar'].setAutoDraw(False)
    if not response:
        rt = taskStruct['maxRT']
        # show no-response error feedback
        dispStruct['noRespErr'].setAutoDraw(True)
        dispStruct['screen'].flip()
        dispStruct['noRespErr'].setAutoDraw(False)
        core.wait(blockStruct['fbJitter'] + taskStruct['fbTime'])
    elif response:
        rt = respOnset - stimOnset
    dispStruct['screen'].flip()
    dispStruct['fixation'].setAutoDraw(True)
    dispStruct['screen'].flip()
    itiFixOnset = taskStruct['sessionClock'].getTime()
    # Record variables into structure during ITI fixation period
    dispStruct['ITI'].start((taskStruct['maxRT']-rt)+(taskStruct['maxJitter'] - blockStruct['roulFbJitter']))
    # Clear images and reset trial positions
    dispStruct['fixation'].setAutoDraw(False)
    # Package all trial properties
    blockStruct['roulRespKey'][rI] = respKey
    blockStruct['rStim'][rI] = stimOnset
    blockStruct['rResp'][rI] = respOnset
    blockStruct['roulRT'][rI] = rt
    blockStruct['rFB'][rI] = outcomeOnset
    blockStruct['rITIFix'][rI] = itiFixOnset
    # Update currBar
    if response:
        if isWin:
            dispStruct['currBarLength'] = dispStruct['winBarLength']
            dispStruct['currBarVert'] = [(dispStruct['pointsBarXLeft'],dispStruct['pointsBarYTop']),(dispStruct['currBarLength'],dispStruct['pointsBarYTop']),(dispStruct['currBarLength'],dispStruct['pointsBarYBottom']),(dispStruct['pointsBarXLeft'],dispStruct['pointsBarYBottom'])]
            dispStruct['currBar'].vertices = dispStruct['currBarVert']    
        else:
            dispStruct['currBarLength'] = dispStruct['lossBarLength']
            dispStruct['currBarVert'] = [(dispStruct['pointsBarXLeft'],dispStruct['pointsBarYTop']),(dispStruct['currBarLength'],dispStruct['pointsBarYTop']),(dispStruct['currBarLength'],dispStruct['pointsBarYBottom']),(dispStruct['pointsBarXLeft'],dispStruct['pointsBarYBottom'])]
            dispStruct['currBar'].vertices = dispStruct['currBarVert']    
    dispStruct['ITI'].complete()
    blockStruct['roulTrialRunTime'][rI] = taskStruct['sessionClock'].getTime()-blockStruct['rPreFix'][rI]
    return(dispStruct,blockStruct)


def updateStimPool(taskStruct, sI, bI):
    stimPool = np.copy(taskStruct['stimPool']) # length of all stims in whole task set
    isBurned = np.copy(taskStruct['isBurned'])
    if sI == 0 and bI == 0: # if first block of entire task (first session), # novels = # stims (all novel)
        numBlockStims = taskStruct['sessionInfo']['numBlockStims'][bI]
        numBlockNovels = taskStruct['sessionInfo']['numBlockStims'][bI]
    else:
        numBlockStims = taskStruct['sessionInfo']['numBlockStims'][bI]
        numBlockNovels = taskStruct['sessionInfo']['numBlockNovels'][bI]
    # add in the block's novel stimuli
    novelStims = np.where((stimPool==False) & (isBurned==False))[0]
    stimPool[np.random.choice(novelStims,numBlockNovels,replace=False)] = True # boolean indicating which stims in the whole set are active

    # remove a random sample of old stimuli if we need to
    numToRemove = np.sum(stimPool) - numBlockStims
    if numToRemove > 0:
        canRemove = np.copy(stimPool)
        canRemove[novelStims] = False
        # sample from available stimuli to remove some
        removeStimsIndex = np.where(canRemove)[0]
        removeStims = np.random.choice(removeStimsIndex, numToRemove, replace=False)
        stimPool[removeStims] = False
        isBurned[removeStims] = True
    return(stimPool, isBurned)


def initBlock(taskStruct,dispStruct,blockStruct,bI):
    screen = dispStruct['screen']
    stimPool = taskStruct['stimPool'] # Boolean of length = len(all stims in set) indicating which are active now
    stimIDs = taskStruct['stimID'] # the filename IDs of the all the stims in the set
    familiarity = taskStruct['familiarity']
    # copy - variable indicating active pool of stimuli for this block
    blockStruct['isPoolStim'] = np.array(stimPool) # record a boolean of length = len(all stims) indicating stims that are active for this block
    blockStruct['isPoolStimID'] = np.array(taskStruct['stimID'][stimPool]) # record the filname IDs of all stims that are active for this block
    # re-sample the win probabilities
    blockStruct['pWin'] = np.zeros(len(stimPool))
    if np.random.uniform() > 0.5:
        newVals = np.linspace(0.2, 0.8, np.sum(stimPool))
    else:
        newVals = np.linspace(0.4, 0.6, np.sum(stimPool))
        newVals[0] = 0.2

    blockStruct['pWin'][stimPool] = np.random.permutation(newVals) # length = len(all stims) indicating P(win) values for only the active stims

    # If not the first block, clear the image cache
    if 'imageCache' in blockStruct:
        del blockStruct['imageCache']
    # Load the block stimuli for all active stims within the stim set. Indexed by ordering
    imageCache = dict()
    for i in np.where(stimPool)[0]:
        stimNo = stimIDs[i]
        #imageCache[i] = visual.TextStim(screen, text=str(stimNo), color = 'black', height =0.15, font = dispStruct['textFont'], wrapWidth = 1.8)
        imageCache[i] = visual.ImageStim(win=screen, image=taskStruct['Dir']['StimCues']+os.sep+'s'+str(stimNo)+'.bmp')
        imageCache[i].rescaledSize = rescaleStim(imageCache[i],dispStruct['stimSize'],dispStruct)
        imageCache[i].setSize(imageCache[i].rescaledSize)
        # to index the cached visual.ImageStim objects, use imageCache[index]
    blockStruct['imageCache'] = imageCache # imageCache is a dict where objects are keyed by their index in the overall stim pool (not by stimID)
    # To refer to the index of the stimulus in the overall stim pool array : imageCache[i]
    # To refer to the actual filename IDs of the sitmulus: stimIDs[i]

    # pull out familiar/novel stimuli
    familiarStims = np.where((stimPool) & (familiarity > 0))[0] # indexes where in stimPool (of length = len(all stims)) there are some familiar stims
    novelStims = np.where((stimPool) & (familiarity == 0))[0] # indexes where in stimPool (of length = len(all stims)) there are some novel stims

    # initialize familiar/novel second pair flags
    blockStruct['isSecondFamiliarStim'] = np.zeros(len(stimPool),dtype='bool') # boolean of length = len(all stims)
    blockStruct['isSecondNovelStim'] = np.zeros(len(stimPool),dtype='bool') # boolean of length = len(all stims)
    blockStruct['isPairedFirstFamiliarStim'] = np.zeros(len(stimPool),dtype='bool')

    if len(familiarStims) > 0: # i.e. if not the first block of task
        # sample a familiar pair for the second pairing
        secondFamiliarIndex = np.random.randint(len(familiarStims))
        blockStruct['isSecondFamiliarStim'][familiarStims[secondFamiliarIndex]] = True # booliean of length = len(all stims), indicates whether a given stimulis is the second familiar one
        # sample a familiar stimulus for the first novel pairing
        familiarStims = np.delete(familiarStims,secondFamiliarIndex)
        blockStruct['isPairedFirstFamiliarStim'][familiarStims[np.random.randint(len(familiarStims))]] = True # booliean of length = len(all stims), indicates whether a given stimulis is the second familiar one

    # sample a novel stimulus
    if len(novelStims) > 0:
        blockStruct['isSecondNovelStim'][novelStims[np.random.randint(len(novelStims))]] = True # booliean of length = len(all stims), indicates whether a given stimulis is the second novel one

    # Set up current state info
    dispStruct['blockStateName'] = dict()
    dispStruct['blockFlag'] = dict()
    for lr in range(2):
        if lr == 0:
            flagPosition = dispStruct['flagTrialPosL'] # left is coded [0]
            stateNamePosition = dispStruct['stateNameTrialPosL']
        elif lr ==1:
            flagPosition = dispStruct['flagTrialPosR'] # right is coded [1]
            stateNamePosition = dispStruct['stateNameTrialPosR']

        # Define block state
        dispStruct['blockStateName'][lr] = visual.TextStim(dispStruct['screen'],color='black',opacity=1)
        dispStruct['blockStateName'][lr].text = blockStruct['stateName']
        dispStruct['blockStateName'][lr].font = dispStruct['textFont']
        dispStruct['blockStateName'][lr].pos = stateNamePosition
        dispStruct['blockStateName'][lr].height = dispStruct['stateNameTrialHeight']
        # Define block flag
        dispStruct['blockFlag'][lr] = visual.ImageStim(dispStruct['screen'])
        dispStruct['blockFlag'][lr].setImage(taskStruct['Dir']['Flags'] + os.sep + "flag_" + blockStruct['stateName']  + ".png")
        dispStruct['blockFlag'][lr].rescaledSize = rescale(dispStruct['blockFlag'][lr], dispStruct['flagTrialSize'])
        dispStruct['blockFlag'][lr].setSize(dispStruct['blockFlag'][lr].rescaledSize)
        dispStruct['blockFlag'][lr].pos = flagPosition
    return(blockStruct,dispStruct)


def initTrial(taskStruct, dispStruct, blockStruct, tI):
    familiarity = taskStruct['familiarity']
    # Initialize which stims are actually shown on this trial - what are the TRIAL 2 stimuli?
    isTrialStim = np.zeros(len(taskStruct['stimPool']),dtype='bool') # boolean of length = len(all stims)
    # Initialize which stims can be shown on this trial - what are the available block set from the overall pool?
    stimPool = dcopy(taskStruct['stimPool']) # boolean - indicates whether stim is active from overall pool

    # Is the familiar stimulus paired with the first novel stimulus available
    if tI < blockStruct['firstNovelTrial']:
        stimPool[np.where(blockStruct['isPairedFirstFamiliarStim'])[0]] = False

    # Is the second familiar stimulus available
    if tI < blockStruct['secondFamiliarTrial']:
        stimPool[np.where(blockStruct['isSecondFamiliarStim'])[0]] = False

    # Is the second novel stimulus available
    if tI < blockStruct['secondNovelTrial']:
        stimPool[np.where(blockStruct['isSecondNovelStim'])[0]] = False

   # set up the special trials
    if tI == blockStruct['firstFamiliarTrial']:
        familiarStims = np.where((familiarity > 0) & (blockStruct['numSamples'][0] == 0) & (stimPool))[0]
        if len(familiarStims) < 2:
            # cannot form familiar/familiar pair
            availableStims = np.where(stimPool)[0] # the indices of the available stimuli in the active block set (array of indices (indexes stimPool of length = len(all stims)) of mutable length)
        else:
            # draw a familiar and a familiar stimulus to pair
            availableStims = np.copy(familiarStims)
    elif tI < blockStruct['firstNovelTrial']: # unsampled familiar pair (1st or 2nd pairing)
        familiarStims = np.where((familiarity > 0) & (stimPool))[0]
        if len(familiarStims) < 2:
            # cannot form familiar/familiar pair
            availableStims = np.where(stimPool)[0] # the indices of the available stimuli in the active block set (array of indices (indexes stimPool of length = len(all stims)) of mutable length)
        else:
            # draw a familiar and a familiar stimulus to pair
            availableStims = np.copy(familiarStims)
    elif tI == blockStruct['firstNovelTrial']: # UNSAMPLED novel/familiar pair (1st or 2nd pairing)
        familiarStims = np.where(blockStruct['isPairedFirstFamiliarStim'])[0]
        novelStims = np.where((familiarity == 0) & (stimPool))[0] #these return stim indices from the stimPool, not stimIDs
        if len(familiarStims) == 0:
            # cannot form novel/familiar pair
            availableStims = np.where(stimPool)[0]
        else:
            # pair them
            availableStims = np.concatenate((novelStims,familiarStims),axis=0)
    elif tI == blockStruct['secondFamiliarTrial'] or tI == blockStruct['secondNovelTrial']:
        availableFamiliarStims = np.array([]).astype('int')
        availableNovelStims = np.array([]).astype('int')
        # check to see if the second familiar stim should be paired
        if tI == blockStruct['secondFamiliarTrial']:
            availableFamiliarStims = np.where(blockStruct['isSecondFamiliarStim'])[0]
        # check to see if the second novel stim should be paired
        if tI == blockStruct['secondNovelTrial']:
            availableNovelStims = np.where(blockStruct['isSecondNovelStim'])[0]
        # combine available familiar and novel stimuli
        availableSecondStims = np.concatenate((availableFamiliarStims,availableNovelStims),axis=0)
        # random selection (uncertainty)
        numToAdd = 2-len(availableSecondStims)
        if numToAdd > 0:
            addStimPool = dcopy(stimPool)
            addStimPool[availableSecondStims] = False
            stimsToAddIndex = np.where(addStimPool)[0]
            stimsToAdd = stimsToAddIndex[np.random.permutation(len(stimsToAddIndex))]
            availableStims = np.concatenate((availableSecondStims, stimsToAdd[range(numToAdd)]),axis=0)
        else:
            availableStims = availableSecondStims
    else:
        # sample available stimuli at random
        availableStims = np.where(stimPool)[0]
    # random sample from available set
    availableStims = availableStims.astype('int') # gives the indices of the available, active stims in the entire stim pool set
    isTrialStim[np.random.choice(availableStims,size=2,replace=False)] = True # boolean of length = len(all stims), indicates which two stimuli (of the entire pool) are the ones for this trial
    blockStruct['isTrialStim'][tI] = isTrialStim
    # Pull out indexes of current trial stimuli from the whole stim pool
    stimIndices = np.where(isTrialStim)[0] # these gives the indices in the entire stimulus pool for this trial's two stimuli
    np.random.shuffle(stimIndices) # Randomise which stimulus is left vs right
    blockStruct['presentedStimIndices'][tI] = np.copy(stimIndices)
    # record the actual active stim filenames (stimIDs) of the current trial
    blockStruct['trialStimID'][tI] = taskStruct['stimID'][stimIndices]

    # Initialize trial display drawings
    # End pre-trial fixation
    dispStruct['fixation'].setAutoDraw(False)
    # Show template images (bandits, slots, etc)
    for lr in range(2):
        dispStruct['machine'][lr].setAutoDraw(True)
        dispStruct['slotsTrial'][lr].setAutoDraw(True)

    # Show state info
    for lr in range(2):
        dispStruct['blockFlag'][lr].setAutoDraw(True)
        dispStruct['blockStateName'][lr].setAutoDraw(True)

    # Show stimulus cues
    for lr in range(len(stimIndices)):
        if lr == 0:
            stimPosition = dispStruct['stimPosL']
        elif lr ==1:
            stimPosition = dispStruct['stimPosR']
        dispStruct['stimTrial'][lr] = blockStruct['imageCache'][stimIndices[lr]]
        dispStruct['stimTrial'][lr].pos = stimPosition
        dispStruct['stimTrial'][lr].setAutoDraw(True)

    # Show curr points bar
    dispStruct['pointsBar'].setAutoDraw(True)
    dispStruct['currBar'].setAutoDraw(True)
    return(blockStruct)


def runCasinoTrial(taskStruct, dispStruct, keyStruct, blockStruct, tI):
    # Flip screen and wait for response
    dispStruct['screen'].flip()
    stimOnset = taskStruct['sessionClock'].getTime() # get stim onset time
    response = event.clearEvents()
    while (taskStruct['sessionClock'].getTime()  - stimOnset) <= taskStruct['maxRT']:
        # wait for response
        response = event.getKeys(keyList=[keyStruct['respKeyLeft'],keyStruct['respKeyRight']])
        # Which option was selected
        if not response:
            respOnset = np.nan
            respKey = 'N'
            selectedStimIndex = 'NA'
            isWin = False
            winVal = np.nan
            winTrial = False
            outcomeOnset = np.nan
            blockStruct['trialStimSelect'][tI,:] = 0
            blockStruct['trialStimSelectWin'][tI,:] = 0
        elif response:
            # Get response time to calculate RT below
            respOnset = taskStruct['sessionClock'].getTime()
            # which response was made
            if keyStruct['respKeyRight'] in response:
                # right key was pressed
                respKey = 'R'
                respStimIndex = 1
                dispStruct['fbTrial']['Win'].pos = dispStruct['slotsPosR']
                dispStruct['fbTrial']['noWin'].pos = dispStruct['slotsPosR']
            elif keyStruct['respKeyLeft'] in response:
                # left key was pressed
                respKey = 'L'
                respStimIndex = 0
                dispStruct['fbTrial']['Win'].pos = dispStruct['slotsPosL']
                dispStruct['fbTrial']['noWin'].pos = dispStruct['slotsPosL']
            selectedStimIndex = blockStruct['presentedStimIndices'][tI,respStimIndex]
            # Feedback Jitter (rotating reels)
            dispStruct['revolSlots'][respStimIndex].setAutoDraw(True)
            reelClock = core.Clock()
            while reelClock.getTime() < blockStruct['fbJitter']:
                dispStruct['revolSlots'][respStimIndex].phase += 0.3
                dispStruct['screen'].flip()
            dispStruct['revolSlots'][respStimIndex].setAutoDraw(False)
            # Determine its outcome and display reward
            isWin = (blockStruct['pWin'][selectedStimIndex] > np.random.uniform(0,1))
            if isWin:
                dispStruct['fbTrial']['Win'].setAutoDraw(True)
                # Show win bar
                dispStruct['currBar'].setAutoDraw(False)
                dispStruct['winBarLength'] = dispStruct['currBarLength'] + scalePoints(taskStruct,taskStruct['winVal'])
                dispStruct['winBarVert'] = [(dispStruct['pointsBarXLeft'],dispStruct['pointsBarYTop']),(dispStruct['winBarLength'],dispStruct['pointsBarYTop']),(dispStruct['winBarLength'],dispStruct['pointsBarYBottom']),(dispStruct['pointsBarXLeft'],dispStruct['pointsBarYBottom'])]
                dispStruct['winBar'].vertices = dispStruct['winBarVert']
                dispStruct['winBar'].setAutoDraw(True)
                dispStruct['currBar'].setAutoDraw(True)
            else:
                dispStruct['fbTrial']['noWin'].setAutoDraw(True)
            dispStruct['screen'].flip()
            outcomeOnset = taskStruct['sessionClock'].getTime() # get outcome onset time
             # present the feed back for designed amount of time and record some data
            dispStruct['ITI'].start(taskStruct['fbTime'])
            # Note the selected stimulus
            blockStruct['trialStimSelect'][tI,respStimIndex] = True
            # track selection and win if there was a response
            blockStruct['isSelected'][tI, selectedStimIndex] = True
            blockStruct['isWin'][tI, selectedStimIndex] = isWin
            # Update sampling count
            blockStruct['numSamples'][0,selectedStimIndex] = blockStruct['numSamples'][0,selectedStimIndex] + 1
            if isWin:
                # Track if selected stim won
                blockStruct['numWins'][0,selectedStimIndex] = blockStruct['numWins'][0,selectedStimIndex] + 1
                # record whether the selected side (left/right) actually won
                blockStruct['trialStimSelectWin'][tI,respStimIndex] = True
                winVal = taskStruct['winVal']
                winTrial = True
            else:
                winVal = 0
                winTrial = False
            dispStruct['ITI'].complete()
            break
    # clear screen and show fixation
    for lr in range(2):
        dispStruct['machine'][lr].setAutoDraw(False)
        dispStruct['slotsTrial'][lr].setAutoDraw(False)
        dispStruct['blockStateName'][lr].setAutoDraw(False)
        dispStruct['blockFlag'][lr].setAutoDraw(False)
        dispStruct['stimTrial'][lr].setAutoDraw(False)
    dispStruct['fbTrial']['Win'].setAutoDraw(False)
    dispStruct['fbTrial']['noWin'].setAutoDraw(False)
    dispStruct['pointsBar'].setAutoDraw(False)
    dispStruct['currBar'].setAutoDraw(False)
    dispStruct['winBar'].setAutoDraw(False)
    if not response:
        rt = np.nan
        waitRT = taskStruct['maxRT']
        # show no-response error feedback
        dispStruct['noRespErr'].setAutoDraw(True)
        dispStruct['screen'].flip()
        dispStruct['noRespErr'].setAutoDraw(False)
        core.wait(blockStruct['fbJitter'] + taskStruct['fbTime'])
    elif response:
        rt = respOnset - stimOnset
        waitRT = rt
    dispStruct['screen'].flip()
    dispStruct['fixation'].setAutoDraw(True)
    dispStruct['screen'].flip()
    itiFixOnset = taskStruct['sessionClock'].getTime()
    # Record variables into structure during ITI fixation period
    dispStruct['ITI'].start((taskStruct['maxRT']-waitRT)+(taskStruct['maxJitter'] - blockStruct['fbJitter']))
    # Clear images and reset trial positions
    dispStruct['fixation'].setAutoDraw(False)
    dispStruct['fbTrial']['Win'].pos = [0,0] # reset win image position for next trial
    # Record all data
    blockStruct['trialOutcome'][tI] = winTrial
    blockStruct['trialOutcomeVal'][tI] = winVal
    blockStruct['respKey'][tI] = respKey
    # Record onset times
    blockStruct['tStim'][tI] = stimOnset
    blockStruct['tResp'][tI] = respOnset
    blockStruct['RT'][tI] = rt
    blockStruct['tFB'][tI] = outcomeOnset
    blockStruct['tITIFix'][tI] = itiFixOnset
    # Update currBar    
    if isWin:
        dispStruct['currBarLength'] = dispStruct['winBarLength']
        dispStruct['currBarVert'] = [(dispStruct['pointsBarXLeft'],dispStruct['pointsBarYTop']),(dispStruct['currBarLength'],dispStruct['pointsBarYTop']),(dispStruct['currBarLength'],dispStruct['pointsBarYBottom']),(dispStruct['pointsBarXLeft'],dispStruct['pointsBarYBottom'])]
        dispStruct['currBar'].vertices = dispStruct['currBarVert']    
    dispStruct['ITI'].complete()
    blockStruct['trialRunTime'][tI] = taskStruct['sessionClock'].getTime()-blockStruct['tPreFix'][tI]
    return(taskStruct,dispStruct,blockStruct)

def runSubjRatingTrial(taskStruct, dispStruct, blockStruct, sI):
    dispStruct['SubjRatingQ'].reset() # reset the rating scale
    ratingRT = 0 # reset the starting RT
    # Time allowed for ratings scale response = stimTime + fbJitter + fbTime
    dispStruct['screen'].flip()
    ratingOnset = taskStruct['sessionClock'].getTime()
    event.clearEvents()
    # Keep drawing and wait for response
    while dispStruct['SubjRatingQ'].noResponse:
        dispStruct['SubjRating'].draw()
        dispStruct['SubjRatingQ'].draw()
        dispStruct['screen'].flip()
    ratingChoice = dispStruct['SubjRatingQ'].getRating()
    ratingRT = dispStruct['SubjRatingQ'].getRT()
    if ratingRT < dispStruct['SubjRatingQ'].maxTime:
        # Keep response
        dispStruct['SubjRatingFB'].setAutoDraw(True)
        dispStruct['screen'].flip()
        outcomeOnset = taskStruct['sessionClock'].getTime()
        dispStruct['SubjRatingFB'].setAutoDraw(False)
        dispStruct['ITI'].start((dispStruct['SubjRatingQ'].maxTime - ratingRT) + taskStruct['fbTime'])
    else:
        # Response too slow
        ratingRT = np.nan
        ratingChoice = 'NA'
        # show no-response error feedback
        dispStruct['noRespErr'].setAutoDraw(True)
        dispStruct['screen'].flip()
        outcomeOnset = np.nan
        dispStruct['noRespErr'].setAutoDraw(False)
        dispStruct['ITI'].start(taskStruct['fbTime']) # give 0.5 seconds to pack up data
    # No ITI fixations for these trials (given max fbJitter time to make ratings)
    # Convert response strings to code:
    if ratingChoice == 'very bad':
        respKey = 1
    elif ratingChoice == 'bad':
        respKey = 2
    elif ratingChoice == 'neutral':
        respKey = 3
    elif ratingChoice == 'good':
        respKey = 4
    elif ratingChoice == 'very good':
        respKey = 5
    elif ratingChoice == 'NA':
        respKey = np.nan
    else:
        respKey = np.nan
    # Package all trial properties
    taskStruct['sessionInfo']['moodRating'][sI] = respKey
    blockStruct['sStim'] = ratingOnset
    blockStruct['sResp'] = ratingOnset + ratingRT
    taskStruct['sessionInfo']['moodRT'][sI] = ratingRT
    blockStruct['sFB'] = outcomeOnset
    dispStruct['ITI'].complete()
    blockStruct['ratingTrialRunTime'] = taskStruct['sessionClock'].getTime()-blockStruct['sPreFix']
    return(taskStruct,blockStruct)

def runHabitTrial(taskStruct, dispStruct, keyStruct, blockStruct, htI):
    # end pre-stim fixation
    dispStruct['fixation'].setAutoDraw(False)
    # Flip screen and wait for response
    for lr in range(2):
        dispStruct['blockFlag'][lr].setAutoDraw(True)
        dispStruct['practiceStateName'][lr].setAutoDraw(True)
        dispStruct['machine'][lr].setAutoDraw(True)
        dispStruct['practiceStims'][lr].setAutoDraw(True)
        dispStruct['slotsTrial'][lr].setAutoDraw(True)
    dispStruct['screen'].flip()
    stimOnset = taskStruct['sessionClock'].getTime() # get stim onset time
    response = event.clearEvents()
    while (taskStruct['sessionClock'].getTime()  - stimOnset) <= taskStruct['maxRT']:
        # wait for response
        response = event.getKeys(keyList=[keyStruct['respKeyLeft'],keyStruct['respKeyRight']])
        # Which option was selected
        if not response:
            respOnset = np.nan
            respKey = 'N'
            selectedStimIndex = 'NA'
            outcomeOnset = np.nan
        elif response:
            # Get response time to calculate RT below
            respOnset = taskStruct['sessionClock'].getTime()
            # which response was made
            if keyStruct['respKeyRight'] in response:
                # right key was pressed
                respKey = 'R'
                respStimIndex = 1
                dispStruct['fbTrial']['Habit'].pos = dispStruct['slotsPosR']
            elif keyStruct['respKeyLeft'] in response:
                # left key was pressed
                respKey = 'L'
                respStimIndex = 0
                dispStruct['fbTrial']['Habit'].pos = dispStruct['slotsPosL']
            # Feedback Jitter (rotating reels)
            dispStruct['revolSlots'][respStimIndex].setAutoDraw(True)
            reelClock = core.Clock()
            while reelClock.getTime() < blockStruct['fbJitter']:
                dispStruct['revolSlots'][respStimIndex].phase += 0.3
                dispStruct['screen'].flip()
            dispStruct['revolSlots'][respStimIndex].setAutoDraw(False)
            # Display 'practice' outcome
            dispStruct['fbTrial']['Habit'].setAutoDraw(True)
            dispStruct['screen'].flip()
            outcomeOnset = taskStruct['sessionClock'].getTime() # get outcome onset time
             # present the feed back for designed amount of time and record some data
            dispStruct['ITI'].start(taskStruct['fbTime'])
            dispStruct['ITI'].complete()
            break
    # clear screen and show fixation
    for lr in range(2):
        dispStruct['blockFlag'][lr].setAutoDraw(False)
        dispStruct['practiceStateName'][lr].setAutoDraw(False)
        dispStruct['machine'][lr].setAutoDraw(False)
        dispStruct['practiceStims'][lr].setAutoDraw(False)
        dispStruct['slotsTrial'][lr].setAutoDraw(False)
    dispStruct['fbTrial']['Habit'].setAutoDraw(False)
    if not response:
        rt = np.nan
        waitRT = taskStruct['maxRT']
        # show no-response error feedback
        dispStruct['noRespErr'].setAutoDraw(True)
        dispStruct['screen'].flip()
        dispStruct['noRespErr'].setAutoDraw(False)
        core.wait(blockStruct['fbJitter'] + taskStruct['fbTime'])
    elif response:
        rt = respOnset - stimOnset
        waitRT = rt
    dispStruct['screen'].flip()
    dispStruct['fixation'].setAutoDraw(True)
    dispStruct['screen'].flip()
    itiFixOnset = taskStruct['sessionClock'].getTime()
    # Record variables into structure during Iti fixation period
    dispStruct['ITI'].start((taskStruct['maxRT']-waitRT)+(taskStruct['maxJitter'] - blockStruct['fbJitter']))
    # Clear images and reset trial positions
    dispStruct['fixation'].setAutoDraw(False)
    dispStruct['fbTrial']['Habit'].pos = [0,0] # reset win image position for next trial
    # Record all data
    blockStruct['habitRespKey'][htI] = respKey
    # Record onset times
    blockStruct['hStim'][htI] = stimOnset
    blockStruct['hResp'][htI] = respOnset
    blockStruct['habitRT'][htI] = rt
    blockStruct['hFB'][htI] = outcomeOnset
    blockStruct['hITIFix'][htI] = itiFixOnset
    dispStruct['ITI'].complete()
    blockStruct['habitTrialRunTime'][htI] = taskStruct['sessionClock'].getTime()-blockStruct['hPreFix'][htI]
    return(taskStruct,blockStruct)

# End of task screen:
def EndTask(dispStruct,taskStruct):
    # Session end page
    dispStruct['End']['page2_head'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.09, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['End']['page2_head'].text = '--Task End--'
    dispStruct['End']['page2_head'].pos = [0,0.8]
    # Session text 1
    dispStruct['End']['page2_text1'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['End']['page2_text1'].text = 'This part of the experiment has now ended.'
    dispStruct['End']['page2_text1'].pos = [0,0.2]
    # Session text 3
    dispStruct['End']['page2_text2'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispStruct['textFont'], wrapWidth = 1.8)
    dispStruct['End']['page2_text2'].pos = [0,-0.8]
    dispStruct['End']['page2_text2'].text = 'Please alert the experimenter.'
    # Draw page
    dispStruct['End']['page2_head'].draw()
    dispStruct['End']['page2_text1'].draw()
    dispStruct['End']['page2_text2'].draw()
    dispStruct['screen'].flip()
    return(dispStruct)

# Extra functions required locally
def feval(defName, *args):
    return eval(defName)(*args)