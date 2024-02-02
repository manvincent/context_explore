# Load Libraries
import os
from psychopy import visual, gui, data, core, event, logging, info
from psychopy.constants import *  
# Ensure that relative paths start from the same directory as this script
homeDir = '/Users/vincentman/Dropbox/Graduate_School/Caltech/Context_Casino/Experiment/Context_Casino'
os.chdir(homeDir)

# Add dependencies
from Dependencies import *

## Experiment start ##
# Store info about the experiment session
# Reference: allowable inputs
# SubNo. - has to be digits
# Version - full or part
# Modality - behaviour or fMRI
# Mode - new or exist
check = 0
while check == 0:
    expName = 'Casino Royale'  # from the Builder filename that created this script
    expInfo = {'SubNo':999,'Version':'full','Modality':'behaviour','Mode':'new'}
    dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
    if dlg.OK == False:
        print('User Cancelled')  # user pressed cancel
        core.wait(3)
        core.quit()
    # Check to see there's no existing subject ID - if there is, repeat this dialogue box
    if (expInfo['Mode'] == 'new') and (os.path.isfile(homeDir + os.sep + 'Output' + os.sep + 'Supplementary' + os.sep + 'Inits' + os.sep + str(expInfo['SubNo']) + '_Init.pkl')):
        check = 0
        print 'That file already exists, try another subject number!'
    else:
        check = 1

if expInfo['Version'] == 'part':
    # Instructions/Practice/Task/ProbeInstruct/ProbeTask - yes or no
    # Starting Run - has to be a digit (not python ordering, starts at 1)
    # Test Type - test or debug
    expPart = {'Instructions':'yes','Practice':'yes','Task':'yes','ProbeInstruct':'yes','ProbeTask':'yes','Starting Run':'1','Test Type':'test'}
    dlg = gui.DlgFromDict(dictionary=expPart, title='Partial Version')
    if dlg.OK == False:
        print('User Cancelled')  # user pressed cancel
        core.wait(3)
        core.quit()
    expInfo['Instructions'] = expPart['Instructions']
    expInfo['Practice'] = expPart['Practice']
    expInfo['Task'] = expPart['Task']
    expInfo['ProbeInstruct'] = expPart['ProbeInstruct']
    expInfo['ProbeTask'] = expPart['ProbeTask']
    expInfo['Starting Run'] = expPart['Starting Run']
    expInfo['Test Type'] = expPart['Test Type']
elif expInfo['Version'] == 'full':
    expInfo['Test Type'] = 'test'
else:
    print "Error! Did not specify correct Version type"
    core.wait(3)
    core.quit()
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName
expInfo['homeDir'] = homeDir

# initialize the task structure parameters
numSessions = 6
blocksPerSession = 3
# Set up between-subject counterbalance
expInfo = counterbalance(expInfo) # output is given by expInfo['sub_cb']

#####  Casino Task Section  #####
sessionClock = core.Clock()
print sessionClock.getTime()
# Initialize general casino parameters
if expInfo['Mode'] == 'new':
    [taskStruct,dispStruct,dispInfo,keyStruct] = initCasino(numSessions, blocksPerSession, expInfo)
    save_obj(taskStruct, homeDir + os.sep + 'Output' + os.sep + 'Supplementary' + os.sep + 'Inits' + os.sep + str(expInfo['SubNo']) + '_Init')
elif expInfo['Mode'] == 'exist':
    print 'Loading pre-existing subject initializations'
    [taskStruct,dispStruct,dispInfo,keyStruct] = initCasino(numSessions, blocksPerSession, expInfo)
    taskStruct = reloadInit(taskStruct,homeDir,expInfo)

# Run Casino game
if expInfo['Version'] == 'part':
    if (not int(expInfo['Starting Run']) == 1):
        print 'Loading pre-existing session information'
        taskStruct = reloadPrevSess(taskStruct,homeDir,expInfo)
    if expInfo['Instructions'] == 'yes':
        dispStruct = runCasinoInstruct(dispStruct,keyStruct,taskStruct,expInfo)
    if expInfo['Practice'] == 'yes':
        [taskStruct,dispStruct,keyStruct] = runCasinoPract(expInfo,taskStruct,dispStruct,dispInfo,keyStruct)
    if expInfo['Task'] == 'yes':
        [taskStruct,dispStruct,keyStruct] = runCasino(expInfo,taskStruct,dispStruct,dispInfo,keyStruct)
    if expInfo['ProbeInstruct'] == 'yes':
        print 'Loading pre-existing subject parameters'
        taskStruct = reloadMemInstruct(taskStruct,homeDir,expInfo)
        dispStruct = runMemInstruct(dispStruct,keyStruct,taskStruct,expInfo)
    if expInfo['ProbeTask'] == 'yes':
        print 'Loading pre-existing subject parameters'
        taskStruct = reloadMemTask(taskStruct,homeDir,expInfo)
        runMemory(expInfo,taskStruct,dispStruct,keyStruct)
elif expInfo['Version'] == 'full':
    dispStruct = runCasinoInstruct(dispStruct,keyStruct,taskStruct,expInfo)
    [taskStruct,dispStruct,keyStruct] = runCasinoPract(expInfo,taskStruct,dispStruct,dispInfo,keyStruct)
    [taskStruct,dispStruct,keyStruct] = runCasino(expInfo,taskStruct,dispStruct,dispInfo,keyStruct)
    dispStruct = runMemInstruct(dispStruct,keyStruct,taskStruct,expInfo)
    runMemory(expInfo,taskStruct,dispStruct,keyStruct)




