from __future__ import division
from psychopy import visual, gui, data, core, event, logging, info
from psychopy.constants import *  # things like STARTED, FINISHED
import numpy as np # whole numpy lib is available, prepend 'np.'
from numpy import sin, cos, tan, log, log10, pi, average, sqrt, std, deg2rad, rad2deg, linspace, asarray
from numpy.random import random, randint, normal, shuffle
import math
import random
import os
from copy import deepcopy as dcopy
from config import *

def initCasino(numSessions, blocksPerSession, expInfo):
    # initial global setup
    random_generator = np.random.RandomState(seed=None) # Create a random number stream from the clock
    ###### Setting up structures ######
    taskStruct = dict()
    dispStruct = dict()
    dispInfo = dict()
    ###### Global task properties ######
    # Specify testing monitor dimensions
    dispInfo['xRes'] = 1920
    dispInfo['yRes'] = 1200
    # Record dessiond ate
    taskStruct['Date'] = expInfo['date']
    # Record subject ID!
    taskStruct['subID'] = expInfo['SubNo']
    # Defining directories #
    homeDir = expInfo['homeDir']
    taskStruct['Dir'] = dict()
    taskStruct['Dir']['Images'] =  homeDir + os.sep + 'Images'
    taskStruct['Dir']['Output'] =  homeDir + os.sep + 'Output'
    taskStruct['Dir']['Payment'] = homeDir + os.sep + 'Payment'
    taskStruct['Dir']['CasinoCues'] =  taskStruct['Dir']['Images'] + os.sep + 'CasinoCues'
    taskStruct['Dir']['Flags'] = taskStruct['Dir']['CasinoCues'] + os.sep + 'World'
    taskStruct['Dir']['Global'] =  taskStruct['Dir']['Images'] + os.sep + 'Global'
    taskStruct['Dir']['Intro'] =  taskStruct['Dir']['Global'] + os.sep + 'Intro'
    taskStruct['Dir']['Roulette'] =  taskStruct['Dir']['Images'] + os.sep + 'Roulette'
    taskStruct['Dir']['StimCues'] =  taskStruct['Dir']['Images'] + os.sep + 'StimCues'
    # task properties
    taskStruct['numSessions'] = numSessions
    taskStruct['blocksPerSession'] = blocksPerSession
    # trial timing
    taskStruct['maxRT'] = 2
    taskStruct['fbTime'] = 1
    taskStruct['preFixTime'] = 1
    # Memory trial timing
    taskStruct['memMaxRT'] = 3
    # range of trial numbers (defined per block)
    taskStruct['minCasinoTrialNum'] = 23
    taskStruct['maxCasinoTrialNum'] = 23
    taskStruct['minCasinoFirstNum'] = 3
    taskStruct['maxCasinoFirstNum'] = 5
    taskStruct['minCasinoSecondNum'] = 8
    taskStruct['maxCasinoSecondNum'] = 19
    taskStruct['minRoulTrialNum'] = 3
    taskStruct['maxRoulTrialNum'] = 5
    taskStruct['numHabitTrials'] = 2
    # possible feedback jitter times
    if expInfo['Modality'] == 'behaviour':
        #fbJitter = np.linspace(0.2,0.5, taskStruct['numSessions'] * taskStruct['blocksPerSession'])
        #taskStruct['maxJitter'] = 0.5
        fbJitter = np.linspace(1, 3, taskStruct['numSessions'] * taskStruct['blocksPerSession'])
        taskStruct['maxJitter'] = 3
    elif expInfo['Modality'] == 'fMRI':
        fbJitter = np.linspace(1, 3, taskStruct['numSessions'] * taskStruct['blocksPerSession'])
        taskStruct['maxJitter'] = 3
    else:
        print "Error! Did not specify correct Modality type"
        core.wait(3)
        core.quit()
    # Max real money
    taskStruct['maxMoney'] = 20
    # Starting reward magnitude
    taskStruct['startAmount'] = '1200pt' # Options are $10; 1000pt
    taskStruct['startVal'] = 1200
    # Reward magnitude
    taskStruct['winAmount'] = '50pt' # Options are $1; 50pt; 25pt; 10pt
    taskStruct['winVal'] = 50 # options are 1, 50, 25, 10
    taskStruct['lossVal'] = taskStruct['winVal'] * -1
    # Context magnitudes:
    taskStruct['winContextAmount'] = '1000pt' # Options are $8; 800pt
    taskStruct['winContextVal'] = 1000 # options are 8 or 800
    taskStruct['lossContextVal'] = taskStruct['winContextVal'] * -1
    # Defining states
    taskStruct['practStateNames'] = np.array(['Canada','UK']) # Set Canada and UK to be the practice states (most familiar)
    taskStruct['stateNames'] = np.array(['Argentina','Barbados','Brazil','Chile','China','Columbia','Denmark','Egypt','France','Germany','Greece','India','Italy','Japan','Luxembourg','Madagascar','Malta','Morocco','Norway','Portugal','Russia','SouthKorea','Spain','Sweden','Taiwan','Thailand','Ukraine'])
    np.random.shuffle(taskStruct['stateNames'])
    # Counterbalancing
    if expInfo['sub_cb'] == 1:
        taskStruct['contextManip1'] = 'gain'
        taskStruct['contextManip2'] = 'loss'
        # Save counterbalance ID
        taskStruct['cbID'] = 1
    elif expInfo['sub_cb'] == 2:
        taskStruct['contextManip1'] = 'loss'
        taskStruct['contextManip2'] = 'gain'
        taskStruct['cbID'] = 2

    ## Initialize task variables
    taskStruct = initTaskVars(taskStruct,fbJitter)
    # Initialize practice variables
    taskStruct['numSessionsPract'] = 1
    taskStruct['blocksPerSessionPract'] = 2
    taskStruct = initPractVars(taskStruct,fbJitter)


    ###### Setting up the keyboard structure #######
    [keyStruct,taskStruct] = keyConfig(taskStruct)
    ###### Setting up the display structure #######
    # set up the screen
    if expInfo['Test Type'] == 'debug':
        dispInfo['screenScaling'] = 0.5
        screen = visual.Window(color='white', size=(dispInfo['xRes'] * dispInfo['screenScaling'] ,dispInfo['yRes'] * dispInfo['screenScaling']), pos=(0,0), fullscr=False, screen=0, allowGUI=True)
    elif expInfo['Test Type'] == 'test':
        dispInfo['screenScaling'] = 1
        screen = visual.Window(color='white', size=(dispInfo['xRes'],dispInfo['yRes']), fullscr=True, screen=0, allowGUI=False)
    else:
        print "Error! Did not specify correct Test type"
        core.wait(3)
        core.quit()
    dispStruct['screen'] = screen
    dispStruct['screen'].colorSpace='rgb'
    dispStruct['screen'].units="norm"
    dispStruct['screen'].blendMode='avg'
    dispStruct['screen'].useFBO=False
    dispStruct['screenScaling'] = dcopy(dispInfo['screenScaling'])
    # Get system information
    #dispStruct['sysInfo'] = info.RunTimeInfo(screen)
    #dispStruct['screen'].flip()
    # record screen dimensions
    #dispInfo['monitorRes'] = dispStruct['sysInfo']['experimentAuthor'].size
    dispInfo['monitorX'] = dispStruct['screen'].size[0]
    dispInfo['monitorY'] = dispStruct['screen'].size[1]
    dispStruct['monitorX'] = dcopy(dispInfo['monitorX'])
    dispStruct['monitorY'] = dcopy(dispInfo['monitorY'])
    dispInfo['fps'] = dispStruct['screen'].getActualFrameRate(nIdentical=10, nMaxFrames=100, nWarmUpFrames=10, threshold=1)
    dispStruct['fps'] = dcopy(dispInfo['fps'])
    # set screen text font and size
    dispInfo['textFont'] = 'Helvetica'
    dispStruct['textFont'] = dcopy(dispInfo['textFont'])
    ## Start loading images
    # Load intro screen
    dispStruct['intro'] = visual.ImageStim(dispStruct['screen'])
    dispStruct['intro'].size = 0.7
    introClock = core.Clock()
    while introClock.getTime() < 3:
        for frames in range(6):
            dispStruct['intro'].setImage(taskStruct['Dir']['Intro'] + os.sep + "c"+str(frames)+".tiff") # recode here to store all animation frames in mem, then draw from mem
            dispStruct['intro'].draw()
            dispStruct['screen'].flip()
            core.wait(7/dispStruct['fps'])
    # display 'loading' screen
    dispStruct['loadScreen'] = visual.TextStim(dispStruct['screen'])
    dispStruct['loadScreen'].ori = 0
    dispStruct['loadScreen'].name = 'Loading_screen'
    dispStruct['loadScreen'].text='Loading...'
    dispStruct['loadScreen'].font = dispInfo['textFont']
    dispStruct['loadScreen'].pos = screen.pos
    dispStruct['loadScreen'].height = 0.1
    dispStruct['loadScreen'].wrapWidth = None
    dispStruct['loadScreen'].alignHoriz = 'center'
    dispStruct['loadScreen'].color = 'black'
    dispStruct['loadScreen'].opacity = 1
    dispStruct['loadScreen'].setAutoDraw(True)
    dispStruct['screen'].flip()
    # display 'save' screen
    dispStruct['saveScreen'] = visual.TextStim(dispStruct['screen'])
    dispStruct['saveScreen'].ori = 0
    dispStruct['saveScreen'].name = 'Save_screen'
    dispStruct['saveScreen'].text='Saving...'
    dispStruct['saveScreen'].font = dispInfo['textFont']
    dispStruct['saveScreen'].pos = screen.pos
    dispStruct['saveScreen'].height = 0.1
    dispStruct['saveScreen'].wrapWidth = None
    dispStruct['saveScreen'].alignHoriz = 'center'
    dispStruct['saveScreen'].color = 'black'
    dispStruct['saveScreen'].opacity = 1
    ## Set up python objects for all generic task images
    # State flags - during break screen
    dispStruct['flagBreakPos']= [0,-0.2]
    dispStruct['flagBreakSize'] = 0.4
    # State flags - during the trial screens
    dispStruct['flagTrialPosL']= [-0.7,0]
    dispStruct['flagTrialPosR']= [0.7,0]
    dispStruct['flagTrialSize'] = 0.3
    # State names -- only during the trial screens
    dispStruct['stateNameTrialPosL']= [-0.7,0.25]
    dispStruct['stateNameTrialPosR']= [0.7,0.25]
    dispStruct['stateNameTrialHeight'] = 0.12
    # slot machines
    dispStruct['machineFile'] = taskStruct['Dir']['Global'] + os.sep  + "slotMachine.png"
    dispStruct['machineSize'] = 0.5
    dispStruct['machinePosL'] = [-0.25, 0]
    dispStruct['machinePosR'] = [0.25, 0]
    # (memory section) slot machines
    dispStruct['memMachineSize'] = dispStruct['machineSize'] * 1.3
    dispStruct['memMachinePos'] = [0,0]
    # pre-choice slots
    dispStruct['slotsFile'] = taskStruct['Dir']['Global'] + os.sep  + "slots.png"
    dispStruct['slotsSize'] = 0.25
    dispStruct['slotsPosL'] = [-0.25, 0.2]
    dispStruct['slotsPosR'] = [0.25, 0.2]
    # (memory section) slot machines
    dispStruct['memSlotsSize'] = dispStruct['slotsSize'] * 1.3
    dispStruct['memSlotsPos'] = [0, 0.3]
    # rotating slots
    dispStruct['rotatSlotsSize'] = [0.16, 0.22]
    # machine cues
    dispStruct['stimSize'] = 0.4
    dispStruct['stimPosL'] = [-0.25, -0.15]
    dispStruct['stimPosR'] = [0.25, -0.15]
    # Points bar properties
    dispStruct['pointsBarXLeft'] = -0.5
    dispStruct['pointsBarLength'] = dispStruct['pointsBarXLeft']+taskStruct['maxPointsScaled']
    dispStruct['pointsBarYTop'] = -0.5
    dispStruct['pointsBarHeight'] = -0.1
    dispStruct['pointsBarYBottom'] = dispStruct['pointsBarYTop']+dispStruct['pointsBarHeight']
    dispStruct['pointsBarVert']  = [(dispStruct['pointsBarXLeft'],dispStruct['pointsBarYTop']),(dispStruct['pointsBarLength'],dispStruct['pointsBarYTop']),(dispStruct['pointsBarLength'],dispStruct['pointsBarYBottom']),(dispStruct['pointsBarXLeft'],dispStruct['pointsBarYBottom'])]
    # (memory section) machine cues
    dispStruct['memStimSize'] = dispStruct['stimSize'] * 1.8
    dispStruct['memStimPos'] = [0,-0.15]
    # reward feedback
    dispStruct['habitFile'] = taskStruct['Dir']['Global'] + os.sep  + "practice.png"
    if taskStruct['winAmount'] == '$1':
        dispStruct['fbWinFile'] = taskStruct['Dir']['Global'] + os.sep  + "win_1.png"
        dispStruct['fbNoWinFile'] = taskStruct['Dir']['Global'] + os.sep  + "noWin_1.png"
    elif taskStruct['winAmount'] == '50pt':
        dispStruct['fbWinFile'] = taskStruct['Dir']['Global'] + os.sep  + "win_50.png"
        dispStruct['fbNoWinFile'] = taskStruct['Dir']['Global'] + os.sep  + "noWin_50.png"
    elif taskStruct['winAmount'] == '25pt':
        dispStruct['fbWinFile'] = taskStruct['Dir']['Global'] + os.sep  + "win_25.png"
        dispStruct['fbNoWinFile'] = taskStruct['Dir']['Global'] + os.sep  + "noWin_25.png"
    elif taskStruct['winAmount'] == '10pt':
        dispStruct['fbWinFile'] = taskStruct['Dir']['Global'] + os.sep  + "win_10.png"
        dispStruct['fbNoWinFile'] = taskStruct['Dir']['Global'] + os.sep  + "noWin_10.png"

    dispStruct['fbSize'] = 0.22
    dispStruct['fbPosL'] = [-0.25, 0.2]
    dispStruct['fbPosR'] = [0.25, 0.2]
    # static roulettes
    dispStruct['rouletteFile'] = taskStruct['Dir']['Roulette'] + os.sep + "roulette_static.png"
    dispStruct['rouletteSize'] = 0.4
    dispStruct['roulettePosL'] = [-0.25,0]
    dispStruct['roulettePosR'] = [0.25,0]
    # roulette feedback
    dispStruct['rouletteFbPosL'] = [-0.2, 0]
    dispStruct['rouletteFbPosR'] = [0.2, 0]
    ## Start drawing static images and save to memory
    # World Map
    dispStruct['Map'] = visual.ImageStim(dispStruct['screen'])
    dispStruct['Map'].image = taskStruct['Dir']['Global'] + os.sep + 'worldMap.png'
    dispStruct['Map'].rescaledSize = rescale(dispStruct['Map'], 0.6)
    dispStruct['Map'].setSize(dispStruct['Map'].rescaledSize)
    dispStruct['Map'].pos = [0,0.7]
    # Break flags
    dispStruct['flagBreakBlock'] = visual.ImageStim(dispStruct['screen'])
    dispStruct['flagBreakBlock'].rescaledSize = rescale(dispStruct['flagBreakBlock'],dispStruct['flagBreakSize'])
    dispStruct['flagBreakBlock'].setSize(dispStruct['flagBreakBlock'].rescaledSize)
    dispStruct['flagBreakBlock'].pos = dispStruct['flagBreakPos']
    # Set up draw objects
    dispStruct['flagTrialBlock'] = dict()
    dispStruct['stateNameBlock'] = dict()
    dispStruct['machine'] = dict()
    dispStruct['stimTrial'] = dict()
    dispStruct['fbTrial'] = dict()
    dispStruct['slotsTrial'] = dict()
    dispStruct['revolSlots'] = dict()
    dispStruct['rouletteTrial'] = dict()
    dispStruct['rotatRoulette'] = dict()
    dispStruct['rouletteFbTrial'] = dict()
    dispStruct['contextRouletteFbTrial'] = dict()
    dispStruct['airportFlag'] = dict()
    dispStruct['airportName'] = dict()
    dispStruct['instructFlag'] = dict()
    dispStruct['instructStateName'] = dict()
    dispStruct['practiceFlag'] = dict()
    dispStruct['practiceStateName'] = dict()
    dispStruct['practiceStims'] = dict()
    # displaying feedback (win)
    dispStruct['fbTrial']['Win'] = visual.ImageStim(dispStruct['screen'])
    dispStruct['fbTrial']['Win'].image = dispStruct['fbWinFile']
    dispStruct['fbTrial']['Win'].rescaledSize = rescale(dispStruct['fbTrial']['Win'],dispStruct['fbSize'])
    dispStruct['fbTrial']['Win'].setSize(dispStruct['fbTrial']['Win'].rescaledSize)
    # displaying feedback (noWin)
    dispStruct['fbTrial']['noWin'] = visual.ImageStim(dispStruct['screen'])
    dispStruct['fbTrial']['noWin'].image = dispStruct['fbNoWinFile']
    dispStruct['fbTrial']['noWin'].rescaledSize = rescale(dispStruct['fbTrial']['noWin'],dispStruct['fbSize'])
    dispStruct['fbTrial']['noWin'].setSize(dispStruct['fbTrial']['noWin'].rescaledSize)
    # displaying feedback (habituation practice)
    dispStruct['fbTrial']['Habit'] = visual.ImageStim(dispStruct['screen'])
    dispStruct['fbTrial']['Habit'].image = dispStruct['habitFile']
    dispStruct['fbTrial']['Habit'].rescaledSize = rescale(dispStruct['fbTrial']['Habit'],dispStruct['fbSize'])
    dispStruct['fbTrial']['Habit'].setSize(dispStruct['fbTrial']['Habit'].rescaledSize)
    # displaying left/right object
    for lr in range(2): ## For loop to create left and right displays in a clean way
        if lr == 0:
            flagPosition = dispStruct['flagTrialPosL'] # left is coded [0]
            stateNamePosition = dispStruct['stateNameTrialPosL']
            machinePosition = dispStruct['machinePosL']
            stimPosition = dispStruct['stimPosL']
            fbPosition =  dispStruct['fbPosL']
            slotsPosition = dispStruct['slotsPosL']
            roulettePosition = dispStruct['roulettePosL']
            rouletteFbPosition = dispStruct['rouletteFbPosL']
        elif lr ==1:
            flagPosition = dispStruct['flagTrialPosR'] # right is coded [1]
            stateNamePosition = dispStruct['stateNameTrialPosR']
            machinePosition = dispStruct['machinePosR']
            stimPosition = dispStruct['stimPosR']
            fbPosition = dispStruct['fbPosR']
            slotsPosition = dispStruct['slotsPosR']
            roulettePosition = dispStruct['roulettePosR']
            rouletteFbPosition = dispStruct['rouletteFbPosR']

        # displaying state flags
        dispStruct['flagTrialBlock'][lr] = visual.ImageStim(dispStruct['screen'])
        dispStruct['flagTrialBlock'][lr].pos = flagPosition
        # displaying state names
        dispStruct['stateNameBlock'][lr] = visual.TextStim(dispStruct['screen'], ori = 0, name = 'State_name', wrapWidth=None,color='black',opacity=1)
        dispStruct['stateNameBlock'][lr].font = dispInfo['textFont']
        dispStruct['stateNameBlock'][lr].pos = stateNamePosition
        dispStruct['stateNameBlock'][lr].height = dispStruct['stateNameTrialHeight']
        # displaying machines
        dispStruct['machine'][lr] = visual.ImageStim(dispStruct['screen'])
        dispStruct['machine'][lr].image = dispStruct['machineFile']
        dispStruct['machine'][lr].rescaledSize = rescale(dispStruct['machine'][lr],dispStruct['machineSize'])
        dispStruct['machine'][lr].setSize(dispStruct['machine'][lr].rescaledSize)
        dispStruct['machine'][lr].pos = machinePosition
        # displaying slots
        dispStruct['slotsTrial'][lr] = visual.ImageStim(dispStruct['screen'])
        dispStruct['slotsTrial'][lr].image = dispStruct['slotsFile']
        dispStruct['slotsTrial'][lr].rescaledSize = rescale(dispStruct['slotsTrial'][lr],dispStruct['slotsSize'])
        dispStruct['slotsTrial'][lr].setSize(dispStruct['slotsTrial'][lr].rescaledSize)
        dispStruct['slotsTrial'][lr].pos = slotsPosition
        # displaying rotating slots
        dispStruct['revolSlots'][lr] = visual.GratingStim(dispStruct['screen'])
        dispStruct['revolSlots'][lr].text = "sin"
        dispStruct['revolSlots'][lr].mask = "None"
        dispStruct['revolSlots'][lr].size = dispStruct['rotatSlotsSize']
        dispStruct['revolSlots'][lr].pos = slotsPosition
        dispStruct['revolSlots'][lr].sf = [2,0]
        dispStruct['revolSlots'][lr].ori = 90
        dispStruct['revolSlots'][lr].contrast= -1
        dispStruct['revolSlots'][lr].color = 'black'
        # displaying stimuli
        dispStruct['stimTrial'][lr] = visual.ImageStim(dispStruct['screen'])
        dispStruct['stimTrial'][lr].pos = stimPosition
        # displaying static roulette
        dispStruct['rouletteTrial'][lr] = visual.ImageStim(dispStruct['screen'])
        dispStruct['rouletteTrial'][lr].image = dispStruct['rouletteFile']
        dispStruct['rouletteTrial'][lr].rescaledSize = rescale(dispStruct['rouletteTrial'][lr],dispStruct['rouletteSize'])
        dispStruct['rouletteTrial'][lr].setSize(dispStruct['rouletteTrial'][lr].rescaledSize)
        dispStruct['rouletteTrial'][lr].pos = roulettePosition
        # displaying moving roulettes
        dispStruct['rotatRoulette'][lr] = visual.ImageStim(dispStruct['screen'])
        dispStruct['rotatRoulette'][lr].setSize(dispStruct['rouletteTrial'][lr].rescaledSize)
        dispStruct['rotatRoulette'][lr].pos = roulettePosition
        # displaying roulette feedback
        dispStruct['rouletteFbTrial'][lr] = visual.TextStim(dispStruct['screen'], ori = 0, name = 'Roulette_fb', wrapWidth=None,color='black',opacity=1)
        dispStruct['rouletteFbTrial'][lr].font = dispInfo['textFont']
        dispStruct['rouletteFbTrial'][lr].pos = rouletteFbPosition
        dispStruct['rouletteFbTrial'][lr].height = dispStruct['stateNameTrialHeight'] + 0.08
        # context manipulation large-outcome roulette feedback
        dispStruct['contextRouletteFbTrial'][lr] = visual.TextStim(dispStruct['screen'], ori = 0, name = 'Roulette_fb', wrapWidth=None,color='black',opacity=1)
        dispStruct['contextRouletteFbTrial'][lr].font = dispInfo['textFont']
        dispStruct['contextRouletteFbTrial'][lr].pos = rouletteFbPosition
        dispStruct['contextRouletteFbTrial'][lr].height = dispStruct['stateNameTrialHeight'] + 0.08
        # displaying airport flag (for roulette trials)
        dispStruct['airportFlag'][lr] = visual.ImageStim(dispStruct['screen'])
        dispStruct['airportFlag'][lr].setImage(taskStruct['Dir']['Global'] + os.sep + "airport.png")
        dispStruct['airportFlag'][lr].rescaledSize = rescale(dispStruct['airportFlag'][lr], dispStruct['flagTrialSize'])
        dispStruct['airportFlag'][lr].setSize(dispStruct['airportFlag'][lr].rescaledSize)
        dispStruct['airportFlag'][lr].pos = flagPosition
        # displaying airport name ('In Transit')
        dispStruct['airportName'][lr] = visual.TextStim(dispStruct['screen'],color='black',opacity=1)
        dispStruct['airportName'][lr].text = 'In Transit'
        dispStruct['airportName'][lr].font = dispInfo['textFont']
        dispStruct['airportName'][lr].pos = stateNamePosition
        dispStruct['airportName'][lr].height = dispStruct['stateNameTrialHeight']
        # displaying instruction states
        dispStruct['instructFlag'][lr] = visual.ImageStim(dispStruct['screen'])
        dispStruct['instructFlag'][lr].setImage(taskStruct['Dir']['Flags'] + os.sep + "flag_" + taskStruct['practStateNames'][0] + ".png")
        dispStruct['instructFlag'][lr].rescaledSize = rescale(dispStruct['instructFlag'][lr], dispStruct['flagTrialSize'])
        dispStruct['instructFlag'][lr].setSize(dispStruct['instructFlag'][lr].rescaledSize)
        dispStruct['instructFlag'][lr].pos = flagPosition
        # displaying instruction state names
        dispStruct['instructStateName'][lr] = visual.TextStim(dispStruct['screen'],color='black',opacity=1)
        dispStruct['instructStateName'][lr].text = taskStruct['practStateNames'][0]
        dispStruct['instructStateName'][lr].font = dispInfo['textFont']
        dispStruct['instructStateName'][lr].pos = stateNamePosition
        dispStruct['instructStateName'][lr].height = dispStruct['stateNameTrialHeight']
        # inital screen practice state flag
        dispStruct['practiceFlag'][lr] = visual.ImageStim(dispStruct['screen'])
        dispStruct['practiceFlag'][lr].pos = flagPosition
        #  practice state names
        dispStruct['practiceStateName'][lr] = visual.TextStim(dispStruct['screen'],color='black',opacity=1)
        dispStruct['practiceStateName'][lr].text = 'Practice'
        dispStruct['practiceStateName'][lr].font = dispInfo['textFont']
        dispStruct['practiceStateName'][lr].pos = stateNamePosition
        dispStruct['practiceStateName'][lr].height = dispStruct['stateNameTrialHeight']
        # practice stims
        dispStruct['practiceStims'][lr] = visual.ImageStim(dispStruct['screen'])
        dispStruct['practiceStims'][lr].pos = stimPosition
        dispStruct['practiceStims'][lr].setImage(taskStruct['Dir']['StimCues'] + os.sep + "i" + str(taskStruct['instructStim'][lr]) + ".bmp")
        dispStruct['practiceStims'][lr].rescaledSize = rescaleStim(dispStruct['practiceStims'][lr],dispStruct['stimSize'],dispStruct)
        dispStruct['practiceStims'][lr].setSize(dispStruct['practiceStims'][lr].rescaledSize)
    # Points bar properties
    dispStruct['pointsBar'] = visual.ShapeStim(dispStruct['screen'])
    dispStruct['pointsBar'].vertices = dispStruct['pointsBarVert']
    dispStruct['pointsBar'].lineColor = 'grey'
    dispStruct['pointsBar'].fillColor = 'grey'
    # Current amount bar
    dispStruct['currBar'] = visual.ShapeStim(dispStruct['screen'])
    dispStruct['currBar'].lineColor = 'royalblue'
    dispStruct['currBar'].fillColor = 'royalblue'
    # Gain bar
    dispStruct['winBar'] = visual.ShapeStim(dispStruct['screen'])
    dispStruct['winBar'].lineColor = 'chartreuse'
    dispStruct['winBar'].fillColor = 'chartreuse'
    # Loss bar
    dispStruct['lossBar'] = visual.ShapeStim(dispStruct['screen'])
    dispStruct['lossBar'].lineColor = 'royalblue'
    dispStruct['lossBar'].fillColor = 'royalblue'
    # Instructions starting amount example bar
    dispStruct['instructBarStartLength'] = dispStruct['pointsBarXLeft']+(taskStruct['maxPointsScaled']/3)
    dispStruct['instructBarStartVert'] = [(dispStruct['pointsBarXLeft'],dispStruct['pointsBarYTop']),(dispStruct['instructBarStartLength'],dispStruct['pointsBarYTop']),(dispStruct['instructBarStartLength'],dispStruct['pointsBarYBottom']),(dispStruct['pointsBarXLeft'],dispStruct['pointsBarYBottom'])]
    dispStruct['instructBar'] = visual.ShapeStim(dispStruct['screen'])
    dispStruct['instructBar'].vertices = dispStruct['instructBarStartVert']
    dispStruct['instructBar'].lineColor = 'royalblue'
    dispStruct['instructBar'].fillColor = 'royalblue'
    # Instructions win bar
    dispStruct['instructBarWinLength'] = dispStruct['pointsBarXLeft']+(taskStruct['maxPointsScaled']/3)+scalePoints(taskStruct,taskStruct['winVal'])
    dispStruct['instructBarWinVert'] = [(dispStruct['pointsBarXLeft'],dispStruct['pointsBarYTop']),(dispStruct['instructBarWinLength'],dispStruct['pointsBarYTop']),(dispStruct['instructBarWinLength'],dispStruct['pointsBarYBottom']),(dispStruct['pointsBarXLeft'],dispStruct['pointsBarYBottom'])]
    dispStruct['instructBarWin'] = visual.ShapeStim(dispStruct['screen'])
    dispStruct['instructBarWin'].vertices = dispStruct['instructBarWinVert']
    dispStruct['instructBarWin'].lineColor = 'chartreuse'
    dispStruct['instructBarWin'].fillColor = 'chartreuse'
    # Instructions loss bar
    dispStruct['instructBarLossLength'] = dispStruct['instructBarWinLength']-scalePoints(taskStruct,taskStruct['winVal'])
    dispStruct['instructBarLossVert'] = [(dispStruct['pointsBarXLeft'],dispStruct['pointsBarYTop']),(dispStruct['instructBarLossLength'],dispStruct['pointsBarYTop']),(dispStruct['instructBarLossLength'],dispStruct['pointsBarYBottom']),(dispStruct['pointsBarXLeft'],dispStruct['pointsBarYBottom'])]
    dispStruct['instructBarLoss'] = visual.ShapeStim(dispStruct['screen'])
    dispStruct['instructBarLoss'].vertices = dispStruct['instructBarLossVert']
    dispStruct['instructBarLoss'].lineColor = 'royalblue'
    dispStruct['instructBarLoss'].fillColor = 'royalblue'
    # Fixation object
    dispStruct['fixation'] = visual.TextStim(dispStruct['screen'], text='+', pos = [0,0], color = 'black', height =0.15, font = dispInfo['textFont'], wrapWidth = 1.8, alignHoriz='center')
    # Session-end Fixation object
    dispStruct['endFixation'] = visual.TextStim(dispStruct['screen'], text='+', pos = [0,0], color = 'red', height =0.15, font = dispInfo['textFont'], wrapWidth = 1.8, alignHoriz='center')
    # Subjective rating scale
    dispStruct['SubjRating'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['SubjRating'].text = 'How do you feel right now?'
    dispStruct['SubjRating'].pos = [0,0]
    dispStruct['SubjRatingQ'] = visual.RatingScale(dispStruct['screen'],choices=['very bad','bad','neutral','good','very good'],
        leftKeys=taskStruct['respKeyLeftName'],rightKeys=taskStruct['respKeyRightName'],marker='circle',markerStart=2,stretch=2,
        showAccept=True,acceptKeys=taskStruct['instrKeyNextName'],acceptSize=4,
        acceptPreText='Press ' + taskStruct['respKeyLeftName'] + ' to move left, or ' +  taskStruct['respKeyRightName'] + ' to move right',
        acceptText='Press ' + taskStruct['instrKeyNextName'] + ' to confirm your choice',
        noMouse=True,skipKeys=None,showValue=False,textColor='black',pos=[0,-0.4],
        maxTime = (taskStruct['maxRT'] + taskStruct['maxJitter']))
    # Subjective ratings scale confirm screen
    dispStruct['SubjRatingFB'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispInfo['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['SubjRatingFB'].text = 'Thanks for your response. We are saving it now.'
    dispStruct['SubjRatingFB'].pos = [0,0]
    # Memory probe machine template
    dispStruct['memMachine'] = visual.ImageStim(dispStruct['screen'])
    dispStruct['memMachine'].image = dispStruct['machineFile']
    dispStruct['memMachine'].rescaledSize = rescale(dispStruct['memMachine'],dispStruct['memMachineSize'])
    dispStruct['memMachine'].setSize(dispStruct['memMachine'].rescaledSize)
    dispStruct['memMachine'].pos = dispStruct['memMachinePos']
    # Memory probe machine slots tempalte
    dispStruct['memMachineSlots'] = visual.ImageStim(dispStruct['screen'])
    dispStruct['memMachineSlots'].image = dispStruct['slotsFile']
    dispStruct['memMachineSlots'].rescaledSize = rescale(dispStruct['memMachineSlots'],dispStruct['memSlotsSize'])
    dispStruct['memMachineSlots'].setSize(dispStruct['memMachineSlots'].rescaledSize)
    dispStruct['memMachineSlots'].pos = dispStruct['memSlotsPos']
    # Memory probe old-new scale
    if expInfo['sub_cb'] == 1:
        dispStruct['OldNewScaleQ'] = visual.RatingScale(dispStruct['screen'],choices=['New', 'Old'],respKeys=([taskStruct['respKeyLeftName'],taskStruct['respKeyRightName']]),marker='circle',markerColor='white',markerStart=0.5,stretch=2,showAccept=False,acceptKeys=([taskStruct['respKeyLeftName'],taskStruct['respKeyRightName']]),noMouse=True,skipKeys=None,showValue=False,textColor='black',pos=[0,-0.6],maxTime=taskStruct['memMaxRT'])
    elif expInfo['sub_cb'] == 2:
        dispStruct['OldNewScaleQ'] = visual.RatingScale(dispStruct['screen'],choices=['Old', 'New'],respKeys=([taskStruct['respKeyLeftName'],taskStruct['respKeyRightName']]),marker='circle',markerColor='white',markerStart=0.5,stretch=2,showAccept=False,acceptKeys=([taskStruct['respKeyLeftName'],taskStruct['respKeyRightName']]),noMouse=True,skipKeys=None,showValue=False,textColor='black',pos=[0,-0.6],maxTime=taskStruct['memMaxRT'])
    dispStruct['OldNewScaleKeys'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.06, font = dispInfo['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['OldNewScaleKeys'].text = 'Press ' + taskStruct['respKeyLeftName'] + ' for the left or ' + taskStruct['respKeyRightName'] + ' for the right.'
    dispStruct['OldNewScaleKeys'].pos = [0,-0.9]
    # Memory probe confidence scale
    dispStruct['ConfScale'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.075, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['ConfScale'].pos = [0,-0.6]
    if expInfo['sub_cb'] == 1:
        dispStruct['ConfScale'].text = "How sure are you that this machine is new or old?"
        dispStruct['ConfScaleQ'] = visual.RatingScale(dispStruct['screen'],choices=['Sure new', 'Not sure new', 'Not sure old', 'Sure old'],respKeys=([taskStruct['respKeyLeftName'],taskStruct['instrKeyPrevName'],taskStruct['instrKeyNextName'],taskStruct['respKeyRightName']]),marker='circle',markerColor='white',markerStart=1.5,stretch=2,showAccept=False,acceptKeys=([taskStruct['respKeyLeftName'],taskStruct['instrKeyPrevName'],taskStruct['instrKeyNextName'],taskStruct['respKeyRightName']]),noMouse=True,skipKeys=None,showValue=False,textColor='black',pos=[0,-0.63],maxTime=taskStruct['memMaxRT'])
    elif expInfo['sub_cb'] == 2:
        dispStruct['ConfScale'].text = "How sure are you that this machine is old or new?"
        dispStruct['ConfScaleQ'] = visual.RatingScale(dispStruct['screen'],choices=['Sure old','Not sure old','Not sure new','Sure new'],respKeys=([taskStruct['respKeyLeftName'],taskStruct['instrKeyPrevName'],taskStruct['instrKeyNextName'],taskStruct['respKeyRightName']]),marker='circle',markerColor='white',markerStart=1.5,stretch=2,showAccept=False,acceptKeys=([taskStruct['respKeyLeftName'],taskStruct['instrKeyPrevName'],taskStruct['instrKeyNextName'],taskStruct['respKeyRightName']]),noMouse=True,skipKeys=None,showValue=False,textColor='black',pos=[0,-0.63],maxTime=taskStruct['memMaxRT'])
    dispStruct['ConfScaleKeys'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.06, font = dispInfo['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['ConfScaleKeys'].text = 'Press ' + taskStruct['respKeyLeftName'] + ' or ' + taskStruct['instrKeyPrevName'] + ' or ' + taskStruct['instrKeyNextName'] + ' or ' + taskStruct['respKeyRightName'] + '.'
    dispStruct['ConfScaleKeys'].pos = [0,-0.9]
    # Memory response box
    dispStruct['memFB'] = visual.Rect(dispStruct['screen'])
    dispStruct['memFB'].size = [dispStruct['memMachine'].size[0] * 2, dispStruct['memMachine'].size[1] * 2]
    dispStruct['memFB'].pos = dispStruct['memMachinePos']
    dispStruct['memFB'].lineColor = 'green'
    # Initialize special messages
    # Screen footer
    dispStruct['footer'] = visual.TextStim(dispStruct['screen'], color = 'black', font = dispStruct['textFont'], wrapWidth = 1.8)
    dispStruct['footer'].text = 'Your travels will continue in:'
    dispStruct['footer'].pos = [-0.15,-0.8]
    # Screen counters
    # Counter 2
    dispStruct['counter2'] = visual.TextStim(dispStruct['screen'], color = 'black', font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['counter2'].text = '2 seconds'
    dispStruct['counter2'].pos = [dispStruct['footer'].pos[0]+0.6,dispStruct['footer'].pos[1]]
    # Counter 1
    dispStruct['counter1'] = visual.TextStim(dispStruct['screen'], color = 'black', font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['counter1'].text = '1 second'
    dispStruct['counter1'].pos = [dispStruct['footer'].pos[0]+0.6,dispStruct['footer'].pos[1]]
    # Wait for experimenter
    dispStruct['experimenter'] = visual.TextStim(dispStruct['screen'], text='Please get ready. Waiting for experimenter.', pos = [0,0], color = 'black', height =0.15, font = dispInfo['textFont'], wrapWidth = 1.8, alignHoriz='center')
    # Wait for scanner pulse
    dispStruct['pulse'] = visual.TextStim(dispStruct['screen'], text='Waiting for the scanner...', pos = [0,0], color = 'black', height =0.15, font = dispInfo['textFont'], wrapWidth = 1.8, alignHoriz='center')
    # No response error
    dispStruct['noRespErr'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispInfo['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['noRespErr'].text = 'Please respond faster. This trial has been cancelled.'
    dispStruct['noRespErr'].pos = [0,0]

    # Set up ITI (static wait) object
    dispStruct['ITI'] = core.StaticPeriod(screenHz=dispStruct['fps'],win=screen,name='ITI')
    # Between casino screen time
    dispStruct['wTime'] = 2
    # Close loading screen
    dispStruct['loadScreen'].setAutoDraw(False)
    return(taskStruct,dispStruct,dispInfo,keyStruct)



######
def initTaskVars(taskStruct,fbJitter):
    ## Set up points bar
    taskStruct['maxPoints'] =12500
    taskStruct['minPoints'] = 0
    taskStruct['maxPointsScaled'] = scalePoints(taskStruct, taskStruct['maxPoints'])
    # Initialize total points tracker
    taskStruct['totalPointsScaled'] = np.zeros((((np.mean((taskStruct['minCasinoTrialNum'], taskStruct['maxCasinoTrialNum']),dtype=int) + np.mean((taskStruct['minRoulTrialNum'],taskStruct['maxRoulTrialNum']),dtype=int) + taskStruct['numHabitTrials']) * (taskStruct['numSessions'] * taskStruct['blocksPerSession'])) +  taskStruct['numSessions'],2),dtype=float)
    # stimulus IDs (randomized, preceeded by 's')
    taskStruct['c1ID'] = np.arange(84)+1 # for context 1
    taskStruct['c2ID'] = np.arange(84,168)+1 # for context 2
    taskStruct['c3ID'] = np.arange(168,251)+1 # for context 2
    taskStruct['stimID'] = np.concatenate((np.random.permutation(taskStruct['c1ID']),np.random.permutation(taskStruct['c2ID']),np.random.permutation(taskStruct['c3ID'])),axis=0)
    # total stimulus exposure across the experiment
    taskStruct['familiarity'] = np.zeros(taskStruct['stimID'].shape,dtype='int')
    # which stimuli are in the pool currently
    taskStruct['stimPool'] = np.zeros(taskStruct['stimID'].shape, dtype='bool')
    # flags which stimuli can no longer be used
    taskStruct['isBurned'] = np.zeros(taskStruct['stimID'].shape, dtype='bool')

    ###### Set up bandit pair orderings ######
    # when is the first novel/familiar trial shown? Trial 1 or 2?
    firstNovelSet = np.arange(taskStruct['minCasinoFirstNum'],taskStruct['maxCasinoFirstNum']+1)
    firstNovelTrial = np.concatenate((np.random.permutation(firstNovelSet),np.random.permutation(firstNovelSet),np.random.permutation(firstNovelSet),np.random.permutation(firstNovelSet),np.random.permutation(firstNovelSet),np.random.permutation(firstNovelSet)),axis=0)
    firstNovelTrial = firstNovelTrial - 1 # indexing variable - start at 0
    # possible second novel/familiar display
    secondStimTrialSpan = np.round(np.linspace(taskStruct['minCasinoSecondNum'], taskStruct['maxCasinoSecondNum'], taskStruct['numSessions'] * taskStruct['blocksPerSession'])).astype(int)
    secondNovelTrial = np.random.permutation(secondStimTrialSpan)
    secondNovelTrial = secondNovelTrial - 1 # indexing variable - start at 0
    secondFamiliarTrial = np.flipud(secondNovelTrial)
    # Carry over variables
    stateNames = dcopy(taskStruct['stateNames'])
    # record absolute trial number (across entire task)
    taskStruct['taskEventNoAbs']  = np.arange(((taskStruct['numSessions'] * taskStruct['blocksPerSession'] * (np.mean([taskStruct['minRoulTrialNum'],taskStruct['maxRoulTrialNum']],dtype='int') + taskStruct['numHabitTrials']+ np.mean([taskStruct['minCasinoTrialNum'],taskStruct['maxCasinoTrialNum']],dtype='int'))) + taskStruct['numSessions']))[:, np.newaxis] + 1
    taskStruct['taskEventNoAbsType'] = np.chararray(taskStruct['taskEventNoAbs'].shape,4)
    # record within-session trial number
    taskStruct['taskEventNoSession'] = dict()
    taskStruct['taskEventNoSessionType'] = dict()
    # Set up collector bins for mood ratings (one per session)
    taskStruct['sessionInfo'] = dict()
    taskStruct['sessionInfo']['sessionNum'] = np.arange(taskStruct['numSessions']).astype('int')[:, np.newaxis] + 1
    taskStruct['sessionInfo']['moodRating'] = np.empty((taskStruct['numSessions'],1))
    taskStruct['sessionInfo']['moodRating'][:] = np.NAN
    taskStruct['sessionInfo']['moodRT'] = np.empty((taskStruct['numSessions'],1))
    taskStruct['sessionInfo']['moodRT'][:] = np.NAN
    # Set up on which block per session the mood rating screen will be presented
    subjRatingSet = np.arange(taskStruct['blocksPerSession'])
    subjRatingBlockNum = np.random.choice(subjRatingSet,taskStruct['numSessions'],replace=True)
    taskStruct['sessionInfo']['moodRatingBlockNum'] = np.empty((taskStruct['numSessions'],1))
    taskStruct['sessionInfo']['moodRatingBlockNum'][:,0] = subjRatingBlockNum    
    # Set up the session
    taskStruct['sessions'] = dict()
    for sI in range(taskStruct['numSessions']):
        # record within-session number
        taskStruct['taskEventNoSession'][sI]  = np.arange(((taskStruct['blocksPerSession'] * (np.mean([taskStruct['minRoulTrialNum'],taskStruct['maxRoulTrialNum']],dtype='int') + taskStruct['numHabitTrials']+ np.mean([taskStruct['minCasinoTrialNum'],taskStruct['maxCasinoTrialNum']],dtype='int'))) + 1))[:, np.newaxis] + 1
        taskStruct['taskEventNoSessionType'][sI] = np.chararray(taskStruct['taskEventNoSession'][sI].shape,4)
        # Initialize session structure
        sessionStruct = dict()
        # number of roulettes per blockStruct
        sessionRouletteSpan = np.round(np.linspace(taskStruct['minRoulTrialNum'],taskStruct['maxRoulTrialNum'],taskStruct['blocksPerSession'])).astype(int)
        sessionRouletteSpan = np.flipud(sessionRouletteSpan) # inverts the vectors so high roulette span  paired with low bandit span in block
        # number of trials per block
        sessionTrialSpan = np.round(np.linspace(taskStruct['minCasinoTrialNum'],taskStruct['maxCasinoTrialNum'],taskStruct['blocksPerSession'])).astype(int)
        # pull out a balanced sampling of feedback jitter times
        if (taskStruct['blocksPerSession'] % 2) == 0:
            # even number of blocks
            sessionFBI = np.hstack((np.arange(0,int(math.ceil(taskStruct['blocksPerSession']/2))),np.arange(int(len(fbJitter)-math.floor(taskStruct['blocksPerSession']/2)+1)-1,len(fbJitter))))
        else:
            sessionFBI = np.hstack((np.arange(0,int(math.floor(taskStruct['blocksPerSession']/2))),np.round(len(fbJitter)/2),np.arange(int(len(fbJitter)-math.floor(taskStruct['blocksPerSession']/2)+1)-1,len(fbJitter)))).astype(int)
            # end
        # pair longest jitter time with fewest trial blocks
        #the result is that across a session, you always get the mean jitter time (i.e. 2 seconds jitter)
        sessionFBJitter = np.flipud(fbJitter[sessionFBI])
        fbJitter = np.delete(fbJitter,sessionFBI)
        # pair long & short ITIs within a session to balance overall duration
        # i.e. by randomizing sessionTrialSpan and session by the same pairingOrder, the longest # of trial blocks is always paired with the shortest feedback time
        # So that block time length is defined by mean feedback jitter time and mean trialspan
        pairingOrder = np.random.permutation(len(sessionTrialSpan))
        sessionTrialSpan = sessionTrialSpan[pairingOrder]
        sessionFBJitter = sessionFBJitter[pairingOrder]
        sessionRouletteSpan = sessionRouletteSpan[pairingOrder]
        sessionRouletteJitter = np.flipud(sessionFBJitter)
        # first novel/familiar pairing
        sessionFirstNovelTrial = firstNovelTrial[np.arange(0,taskStruct['blocksPerSession'])]
        firstNovelTrial = np.delete(firstNovelTrial,np.arange(0,taskStruct['blocksPerSession']))
        # second novel stimulus for this session
        sessionSecondNovelTrial = secondNovelTrial[np.arange(0,taskStruct['blocksPerSession'])]
        secondNovelTrial = np.delete(secondNovelTrial,np.arange(0,taskStruct['blocksPerSession']))
        # second familar stimulus for this session (the fam stim paired with the second novel stim)
        sessionSecondFamiliarTrial = secondFamiliarTrial[np.arange(0,taskStruct['blocksPerSession'])]
        secondFamiliarTrial = np.delete(secondFamiliarTrial,np.arange(0,taskStruct['blocksPerSession']))
        # get the states out
        stateNameIDs =  np.random.choice(range(len(stateNames)),taskStruct['blocksPerSession'], replace=False)
        sessionStateNames = stateNames[stateNameIDs]
        stateNames = np.delete(stateNames,stateNameIDs)
        # Intialize blockStruct
        sessionStruct['blocks'] = dict()
        for bI in range(taskStruct['blocksPerSession']):
            # define number of stims possible, and number of trials in this block
            numStims = len(taskStruct['stimID'])
            numTrials = sessionTrialSpan[bI]
            numHabitTrials = taskStruct['numHabitTrials']
            # define number of roulette trials that preceed this block
            numRoulettes = sessionRouletteSpan[bI]
            # hold all block information
            blockStruct = dict()
            blockStruct['numStims'] = numStims
            blockStruct['numHabitTrials'] = numHabitTrials
            blockStruct['habitTrialType'] = np.repeat(np.array('habit'),numHabitTrials)
            blockStruct['numTrials'] = numTrials
            blockStruct['trialType'] = np.repeat(np.array('bandit'),numTrials)
            # roulette trial length (before block)
            blockStruct['numRoulettes'] = numRoulettes
            blockStruct['roulTrialType'] = np.repeat(np.array('roulette'),numRoulettes)
            # on which roulette trial is the context manipulation shown?
            if numRoulettes == taskStruct['minRoulTrialNum']:
                blockStruct['rouletteContext'] = 1
            else: 
                blockStruct['rouletteContext'] = np.random.randint(1,numRoulettes-1) # indexing variable - start at 0
            # record the current state
            blockStruct['stateName'] = sessionStateNames[bI]
            # sessions number (within which block is embedded)
            blockStruct['sessionNum'] = (np.zeros((numTrials,1)) + (sI+1)).astype(int) # indicator - start at 1
            # current block number
            blockStruct['blockNum'] = (np.zeros((numTrials,1)) + (bI+1)).astype(int) # indicator - start at 1
            # trial number (within block)
            blockStruct['trialNum'] = np.arange(numTrials).astype(int) + 1 # indicator - start at 1
            # roulette block number
            blockStruct['roulBlockNum'] = (np.zeros((numTrials,1)) + (bI+1)).astype(int) # indicator - start at 1
            # roulette trial number list
            blockStruct['roulTrialNum'] = np.arange(numRoulettes).astype(int) + 1 # indicator - start at 1
            # when is the first novel/familiar pair shown?
            # indexing variable - start at 0
            blockStruct['firstNovelTrial'] = sessionFirstNovelTrial[bI] # indexing variable - start at 0
            blockStruct['firstFamiliarTrial'] = 0
            # on which trial are the second novel/familiar simuli shown
            blockStruct['secondNovelTrial'] = sessionSecondNovelTrial[bI] # indexing variable - start at 0
            blockStruct['secondFamiliarTrial'] = sessionSecondFamiliarTrial[bI] # indexing variable - start at 0
            # which stimuli are visible on each trial
            blockStruct['isTrialStim'] = np.zeros((numTrials,numStims),dtype=bool)
            # which stimuli are presented left/right
            blockStruct['trialStimID'] = np.empty((numTrials,2))
            blockStruct['trialStimID'][:] = np.NAN
            # Index of current trial stimuli (left and right) from the whole stim pool
            blockStruct['presentedStimIndices'] = np.empty((numTrials,2),dtype='int')
            blockStruct['presentedStimIndices'][:] = np.NAN
            # which stimulus (left/right) was the one selected?
            blockStruct['trialStimSelect'] = np.zeros((numTrials,2), dtype=bool)
            # did the selected stimulus (left/right) win?
            blockStruct['trialStimSelectWin'] = np.zeros((numTrials,2), dtype=bool)
            # was the stimulus selected?
            blockStruct['isSelected'] = np.zeros((numTrials,numStims),dtype=bool)
            # did the selected stimulus win?
            blockStruct['isWin'] = np.zeros((numTrials,numStims),dtype=bool)
            # did they win on the bandit?
            blockStruct['trialOutcome'] = np.zeros((numTrials,1),dtype = bool)
            blockStruct['trialOutcomeVal'] = np.zeros((numTrials,1))
            # did the roulette win?
            blockStruct['roulTrialWin'] = np.zeros((numRoulettes,1),dtype=bool)
            blockStruct['roulTrialOutcomeVal'] = np.zeros((numRoulettes,1))
            blockStruct['roulTrialOutcomeVal'][:] = np.NAN
            # the response actions (left/right key press)
            blockStruct['respKey'] = np.chararray((numTrials,1),1)
            # the habituation response actions (left/right key press)
            blockStruct['habitRespKey'] = np.chararray((numHabitTrials,1),1)
            # the roulette response actions (left/right key press)
            blockStruct['roulRespKey'] = np.chararray((numRoulettes,1),1)
            # response time for each trial
            blockStruct['RT'] = np.empty((numTrials,1))
            blockStruct['RT'][:] = np.NAN
            # response time for habituation trial
            blockStruct['habitRT'] = np.empty((numHabitTrials,1))
            blockStruct['habitRT'][:] = np.NAN
            # roulette response time for each trial
            blockStruct['roulRT'] = np.empty((numRoulettes,1))
            blockStruct['roulRT'][:] = np.NAN
            # reset the sampling and win counts
            blockStruct['numSamples'] = np.zeros((1,numStims)).astype(int)
            blockStruct['numWins'] = np.zeros((1,numStims)).astype(int)
            # roulette event timing info
            blockStruct['rPreFix'] = np.empty((numRoulettes,1))
            blockStruct['rPreFix'][:] = np.NAN
            blockStruct['rStim'] = np.empty((numRoulettes,1))
            blockStruct['rStim'][:] = np.NAN
            blockStruct['rResp'] = np.empty((numRoulettes,1))
            blockStruct['rResp'][:] = np.NAN
            blockStruct['rFB'] = np.empty((numRoulettes,1))
            blockStruct['rFB'][:] = np.NAN
            blockStruct['rITIFix'] = np.empty((numRoulettes,1))
            blockStruct['rITIFix'][:] = np.NAN
            # habituation timing info
            blockStruct['hPreFix'] = np.empty((numHabitTrials,1))
            blockStruct['hPreFix'][:] = np.NAN
            blockStruct['hStim'] = np.empty((numHabitTrials,1))
            blockStruct['hStim'][:] = np.NAN
            blockStruct['hResp'] = np.empty((numHabitTrials,1))
            blockStruct['hResp'][:] = np.NAN
            blockStruct['hFB'] = np.empty((numHabitTrials,1))
            blockStruct['hFB'][:] = np.NAN
            blockStruct['hITIFix'] = np.empty((numHabitTrials,1))
            blockStruct['hITIFix'][:] = np.NAN
            # event timing info
            blockStruct['tPreFix'] = np.empty((numTrials,1))
            blockStruct['tPreFix'][:] = np.NAN
            blockStruct['tStim'] = np.empty((numTrials,1))
            blockStruct['tStim'][:] = np.NAN
            blockStruct['tResp'] = np.empty((numTrials,1))
            blockStruct['tResp'][:] = np.NAN
            blockStruct['tFB'] = np.empty((numTrials,1))
            blockStruct['tFB'][:] = np.NAN
            blockStruct['tITIFix'] = np.empty((numTrials,1))
            blockStruct['tITIFix'][:] = np.NAN
            # subjective rating timing info
            blockStruct['sPreFix'] = np.empty((1,1))
            blockStruct['sPreFix'] = np.NAN
            blockStruct['sStim'] = np.empty((1,1))
            blockStruct['sStim'] = np.NAN
            blockStruct['sResp'] = np.empty((1,1))
            blockStruct['sResp'] = np.NAN
            blockStruct['sFB'] = np.empty((1,1))
            blockStruct['sFB'] = np.NAN
            # habitutation trial timing info
            blockStruct['habitTrialRunTime'] = np.empty((numHabitTrials,1))
            blockStruct['habitTrialRunTime'][:] = np.NAN
            # trial timing info
            blockStruct['trialRunTime'] = np.empty((numTrials,1))
            blockStruct['trialRunTime'][:] = np.NAN
            # trial timing info
            blockStruct['roulTrialRunTime'] = np.empty((numRoulettes,1))
            blockStruct['roulTrialRunTime'][:] = np.NAN
            # the feedback and iti jitter for this block
            blockStruct['fbJitter'] = sessionFBJitter[bI]
            blockStruct['roulFbJitter'] = sessionRouletteJitter[bI]
            # Save current block initializations
            sessionStruct['blocks'][bI] = dcopy(blockStruct)
             # end
        # store the session structure
        taskStruct['sessions'][sI] = dcopy(sessionStruct)
        ## reminder: to go into these data after storing it, the syntax looks like: ## taskStruct['sessions'][sI].blocks[bI].__dict__
        # end
    # randomise session order
    taskStruct['sessions'] = dict(zip(taskStruct['sessions'].keys(), random.sample(taskStruct['sessions'].values(), len(taskStruct['sessions']))))
    # Fix first block of the first session, for each of the sessions, to have 0-lag
    taskStruct['sessions'][0]['blocks'][0]['firstNovelTrial'] = 0
    taskStruct['sessions'][0]['blocks'][0]['secondNovelTrial'] = 0
    taskStruct['sessions'][0]['blocks'][0]['secondFamiliarTrial'] = 0
    # Fix the occurence of the first novel trial in context sessions
    fixedFirstNovelSet = np.concatenate(([3],np.random.permutation([4,5])),axis=0)
    for bI in range(taskStruct['blocksPerSession']):
        taskStruct['sessions'][2]['blocks'][bI]['firstNovelTrial'] = fixedFirstNovelSet[bI]
        taskStruct['sessions'][4]['blocks'][bI]['firstNovelTrial'] = fixedFirstNovelSet[bI]    
    return(taskStruct)

def initPractVars(taskStruct,fbJitter):
    # define ID of instruction stimuli (preceeded by 'p')
    taskStruct['instructStim'] = np.arange(3)+1 # file name, so start with 1
    # define ID of practice stimuli (preceeded by 'i')
    taskStruct['practStimID'] = np.arange(9)+1 # file name, so start with 1
    np.random.shuffle(taskStruct['practStimID'])
    # total stimulus exposure across the practice section
    taskStruct['practFamiliarity'] = np.zeros(taskStruct['practStimID'].shape,dtype='int')
    # which stimuli are in the pool currently
    taskStruct['practStimPool'] = np.zeros(taskStruct['practStimID'].shape, dtype='bool')
    # flags which stimuli can no longer be used
    taskStruct['practIsBurned'] = np.zeros(taskStruct['practStimID'].shape, dtype='bool')

    ###### Set up bandit pair orderings ######
    # when is the first novel/familiar trial shown? Trial 1 or 2?
    firstNovelTrial = np.arange(taskStruct['minCasinoFirstNum'],taskStruct['maxCasinoFirstNum']+1)
    firstNovelTrial = firstNovelTrial - 1 # indexing variable - start at 0
    # possible second novel/familiar display
    secondStimTrialSpan = np.round(np.linspace(taskStruct['minCasinoSecondNum'],taskStruct['maxCasinoSecondNum'],taskStruct['blocksPerSessionPract'])).astype(int)
    secondNovelTrial = np.random.permutation(secondStimTrialSpan)
    secondNovelTrial = secondNovelTrial - 1 # indexing variable - start at 0
    secondFamiliarTrial = np.flipud(secondNovelTrial)
    # Carry over variables
    stateNames = dcopy(taskStruct['practStateNames'])
    # record absolute trial number (across entire task)
    taskStruct['practEventNoAbs']  = np.arange(((taskStruct['numSessionsPract'] * taskStruct['blocksPerSessionPract'] * (np.mean(taskStruct['maxRoulTrialNum'],dtype='int') + taskStruct['numHabitTrials']+ np.mean([taskStruct['minCasinoTrialNum'],taskStruct['maxCasinoTrialNum']],dtype='int'))) + taskStruct['numSessionsPract']))[:, np.newaxis] + 1
    taskStruct['practEventNoAbsType'] = np.chararray(taskStruct['practEventNoAbs'].shape,4)
    # record within-session trial number
    taskStruct['practEventNoSession'] = dict()
    taskStruct['practEventNoSessionType'] = dict()
    # Set up collector bins for mood ratings (one per session)
    taskStruct['practSessionInfo'] = dict()
    taskStruct['practSessionInfo']['sessionNum'] = np.arange(taskStruct['numSessionsPract']).astype('int')[:, np.newaxis] + 1
    taskStruct['practSessionInfo']['moodRating'] = np.empty((taskStruct['blocksPerSessionPract'],1))
    taskStruct['practSessionInfo']['moodRating'][:] = np.NAN
    taskStruct['practSessionInfo']['moodRT'] = np.empty((taskStruct['blocksPerSessionPract'],1))
    taskStruct['practSessionInfo']['moodRT'][:] = np.NAN
    ## Set up the sessions
    taskStruct['practSession'] = dict()
    for sI in range(taskStruct['numSessionsPract']):
        # record within-session number
        taskStruct['practEventNoSession'][sI]  = np.arange(((taskStruct['blocksPerSessionPract'] * (np.mean(taskStruct['maxRoulTrialNum'],dtype='int') + taskStruct['numHabitTrials']+ np.mean([taskStruct['minCasinoTrialNum'],taskStruct['maxCasinoTrialNum']],dtype='int'))) + 1))[:, np.newaxis] + 1
        taskStruct['practEventNoSessionType'][sI] = np.chararray(taskStruct['practEventNoSession'][sI].shape,4)
        # Intialize session structure
        sessionStruct = dict()
        # number of roulettes per blockStruct
        sessionRouletteSpan = np.round(np.linspace(taskStruct['minRoulTrialNum'],taskStruct['maxRoulTrialNum'],taskStruct['blocksPerSessionPract'])).astype(int)
        sessionRouletteSpan = np.flipud(sessionRouletteSpan) # inverts the vectors so high roulette span  paired with low bandit span in block
        # number of trials per block
        sessionTrialSpan = np.round(np.linspace(taskStruct['minCasinoTrialNum'],taskStruct['maxCasinoTrialNum'],taskStruct['blocksPerSessionPract'])).astype(int)
        # pull out a balanced sampling of feedback jitter times
        if (taskStruct['blocksPerSessionPract'] % 2) == 0:
            # even number of blocks
            sessionFBI = np.hstack((np.arange(0,int(math.ceil(taskStruct['blocksPerSessionPract']/2))),np.arange(int(len(fbJitter)-math.floor(taskStruct['blocksPerSessionPract']/2)+1)-1,len(fbJitter))))
        else:
            sessionFBI = np.hstack((np.arange(0,int(math.floor(taskStruct['blocksPerSessionPract']/2))),np.round(len(fbJitter)/2),np.arange(int(len(fbJitter)-math.floor(taskStruct['blocksPerSessionPract']/2)+1)-1,len(fbJitter)))).astype(int)
            # end
        # pair longest jitter time with fewest trial blocks
        #the result is that across a session, you always get the mean jitter time (i.e. 2 seconds jitter)
        sessionFBJitter = np.flipud(fbJitter[sessionFBI])
        fbJitter = np.delete(fbJitter,sessionFBI)
        # pair long & short ITIs within a session to balance overall duration
        # i.e. by randomizing sessionTrialSpan and session by the same pairingOrder, the longest # of trial blocks is always paired with the shortest feedback time
        # So that block time length is defined by mean feedback jitter time and mean trialspan
        pairingOrder = np.random.permutation(len(sessionTrialSpan))
        sessionTrialSpan = sessionTrialSpan[pairingOrder]
        sessionFBJitter = sessionFBJitter[pairingOrder]
        sessionRouletteSpan = sessionRouletteSpan[pairingOrder]
        sessionRouletteJitter = np.flipud(sessionFBJitter)
        # first novel/familiar pairing
        sessionFirstNovelTrial = firstNovelTrial[np.arange(0,taskStruct['blocksPerSessionPract'])]
        firstNovelTrial = np.delete(firstNovelTrial,np.arange(0,taskStruct['blocksPerSessionPract']))
        # second novel stimulus for this session
        sessionSecondNovelTrial = secondNovelTrial[np.arange(0,taskStruct['blocksPerSessionPract'])]
        secondNovelTrial = np.delete(secondNovelTrial,np.arange(0,taskStruct['blocksPerSessionPract']))
        # second familar stimulus for this session (the fam stim paired with the second novel stim)
        sessionSecondFamiliarTrial = secondFamiliarTrial[np.arange(0,taskStruct['blocksPerSessionPract'])]
        secondFamiliarTrial = np.delete(secondFamiliarTrial,np.arange(0,taskStruct['blocksPerSessionPract']))
        # get the states out
        stateNameIDs = np.random.choice(range(len(stateNames)),taskStruct['blocksPerSessionPract'], replace=False)
        sessionStateNames = stateNames[stateNameIDs]
        stateNames = np.delete(stateNames,stateNameIDs)
        # Set up the blocks
        sessionStruct['practBlocks'] = dict()
        for bI in range(taskStruct['blocksPerSessionPract']):
            # define number of stims possible, and number of trials in this block
            numStims = len(taskStruct['practStimID'])
            numTrials = sessionTrialSpan[bI]
            numHabitTrials = taskStruct['numHabitTrials']
            # define number of roulette trials that preceed this block
            numRoulettes = sessionRouletteSpan[bI]
            # hold all block information
            blockStruct = dict()
            blockStruct['numStims'] = numStims
            blockStruct['numHabitTrials'] = numHabitTrials
            blockStruct['habitTrialType'] = np.repeat(np.array('habit'),numHabitTrials)
            blockStruct['numTrials'] = numTrials
            blockStruct['trialType'] = np.repeat(np.array('bandit'),numTrials)
            # roulette trial length (before block)
            blockStruct['numRoulettes'] = numRoulettes
            blockStruct['roulTrialType'] = np.repeat(np.array('roulette'),numRoulettes)
            # on which roulette trial is the context manipulation shown?
            if numRoulettes == taskStruct['minRoulTrialNum']:
                blockStruct['rouletteContext'] = 1
            else: 
                blockStruct['rouletteContext'] = np.random.randint(1,numRoulettes-1) # indexing variable - start at 0
            # record the current state
            blockStruct['stateName'] = sessionStateNames[bI]
            # sessions number (within which block is embedded)
            blockStruct['sessionNum'] = (np.zeros((numTrials,1)) + (sI+1)).astype(int) # indicator - start at 1
            # current block number
            blockStruct['blockNum'] = (np.zeros((numTrials,1)) + (bI+1)).astype(int) # indicator - start at 1
            # trial number (within block)
            blockStruct['trialNum'] = np.arange(numTrials).astype(int) + 1 # indicator - start at 1
            # roulette block number
            blockStruct['roulBlockNum'] = (np.zeros((numTrials,1)) + (bI+1)).astype(int) # indicator - start at 1
            # roulette trial number list
            blockStruct['roulTrialNum'] = np.arange(numRoulettes).astype(int) + 1 # indicator - start at 1
            # when is the first novel/familiar pair shown?
            # indexing variable - start at 0
            blockStruct['firstNovelTrial'] = sessionFirstNovelTrial[bI] # indexing variable - start at 0
            blockStruct['firstFamiliarTrial'] = 0
            # on which trial are the second novel/familiar simuli shown
            blockStruct['secondNovelTrial'] = sessionSecondNovelTrial[bI] # indexing variable - start at 0
            blockStruct['secondFamiliarTrial'] = sessionSecondFamiliarTrial[bI] # indexing variable - start at 0
            # which stimuli are visible on each trial
            blockStruct['isTrialStim'] = np.zeros((numTrials,numStims),dtype=bool)
            # which stimuli are presented on a trial
            blockStruct['trialStimID'] = np.empty((numTrials,2))
            blockStruct['trialStimID'][:] = np.NAN
            # Index of current trial stimuli (left and right) from the whole stim pool
            blockStruct['presentedStimIndices'] = np.empty((numTrials,2),dtype='int')
            blockStruct['presentedStimIndices'][:] = np.NAN
            # which stimulus (left/right) was the one selected?
            blockStruct['trialStimSelect'] = np.zeros((numTrials,2), dtype=bool)
            # did the selected stimulus (left/right) win?
            blockStruct['trialStimSelectWin'] = np.zeros((numTrials,2), dtype=bool)
            # was the stimulus selected?
            blockStruct['isSelected'] = np.zeros((numTrials,numStims),dtype=bool)
            # did the selected stimulus win?
            blockStruct['isWin'] = np.zeros((numTrials,numStims),dtype=bool)
            # did they win on the bandit?
            blockStruct['trialOutcome'] = np.zeros((numTrials,1),dtype = bool)
            blockStruct['trialOutcomeVal'] = np.zeros((numTrials,1))
            # did the roulette win?
            blockStruct['roulTrialWin'] = np.zeros((numRoulettes,1),dtype=bool)
            blockStruct['roulTrialOutcomeVal'] = np.zeros((numRoulettes,1),dtype='int')
            blockStruct['roulTrialOutcomeVal'][:] = np.NAN
            # the response actions (left/right key press)
            blockStruct['respKey'] = np.chararray((numTrials,1),1)
            # the habituation response actions (left/right key press)
            blockStruct['habitRespKey'] = np.chararray((numHabitTrials,1),1)
            # the roulette response actions (left/right key press)
            blockStruct['roulRespKey'] = np.chararray((numRoulettes,1),1)
            # response time for each trial
            blockStruct['RT'] = np.empty((numTrials,1))
            blockStruct['RT'][:] = np.NAN
            # response time for habituation trial
            blockStruct['habitRT'] = np.empty((numHabitTrials,1))
            blockStruct['habitRT'][:] = np.NAN
            # roulette response time for each trial
            blockStruct['roulRT'] = np.empty((numRoulettes,1))
            blockStruct['roulRT'][:] = np.NAN
            # initialize the sampling and win counts
            blockStruct['numSamples'] = np.zeros((1,numStims)).astype(int)
            blockStruct['numWins'] = np.zeros((1,numStims)).astype(int)
            # roulette event timing info
            blockStruct['rPreFix'] = np.empty((numRoulettes,1))
            blockStruct['rPreFix'][:] = np.NAN
            blockStruct['rStim'] = np.empty((numRoulettes,1))
            blockStruct['rStim'][:] = np.NAN
            blockStruct['rResp'] = np.empty((numRoulettes,1))
            blockStruct['rResp'][:] = np.NAN
            blockStruct['rFB'] = np.empty((numRoulettes,1))
            blockStruct['rFB'][:] = np.NAN
            blockStruct['rITIFix'] = np.empty((numRoulettes,1))
            blockStruct['rITIFix'][:] = np.NAN
            # habituation timing info
            blockStruct['hPreFix'] = np.empty((numHabitTrials,1))
            blockStruct['hPreFix'][:] = np.NAN
            blockStruct['hStim'] = np.empty((numHabitTrials,1))
            blockStruct['hStim'][:] = np.NAN
            blockStruct['hResp'] = np.empty((numHabitTrials,1))
            blockStruct['hResp'][:] = np.NAN
            blockStruct['hFB'] = np.empty((numHabitTrials,1))
            blockStruct['hFB'][:] = np.NAN
            blockStruct['hITIFix'] = np.empty((numHabitTrials,1))
            blockStruct['hITIFix'][:] = np.NAN
            # event timing info
            blockStruct['tPreFix'] = np.empty((numTrials,1))
            blockStruct['tPreFix'][:] = np.NAN
            blockStruct['tStim'] = np.empty((numTrials,1))
            blockStruct['tStim'][:] = np.NAN
            blockStruct['tResp'] = np.empty((numTrials,1))
            blockStruct['tResp'][:] = np.NAN
            blockStruct['tFB'] = np.empty((numTrials,1))
            blockStruct['tFB'][:] = np.NAN
            blockStruct['tITIFix'] = np.empty((numTrials,1))
            blockStruct['tITIFix'][:] = np.NAN
            # subjective rating timing info
            blockStruct['sPreFix'] = np.empty((1,1))
            blockStruct['sPreFix'] = np.NAN
            blockStruct['sStim'] = np.empty((1,1))
            blockStruct['sStim'] = np.NAN
            blockStruct['sResp'] = np.empty((1,1))
            blockStruct['sResp'] = np.NAN
            blockStruct['sFB'] = np.empty((1,1))
            blockStruct['sFB'] = np.NAN
            # habitutation trial timing info
            blockStruct['habitTrialRunTime'] = np.empty((numHabitTrials,1))
            blockStruct['habitTrialRunTime'][:] = np.NAN
            # trial timing info
            blockStruct['trialRunTime'] = np.empty((numTrials,1))
            blockStruct['trialRunTime'][:] = np.NAN
            # roulette trial timing info
            blockStruct['roulTrialRunTime'] = np.empty((numRoulettes,1))
            blockStruct['roulTrialRunTime'][:] = np.NAN
            # subjective rating trial info
            blockStruct['ratingTrialRunTime'] = np.empty((1,1))
            blockStruct['ratingTrialRunTime'] = np.NAN
            # the feedback and iti jitter for this block
            blockStruct['fbJitter'] = sessionFBJitter[bI]
            blockStruct['roulFbJitter'] = sessionRouletteJitter[bI]
            # Save current block initializations
            sessionStruct['practBlocks'][bI] = dcopy(blockStruct)
             # end
        # store the session structure
        taskStruct['practSession'][sI] = dcopy(sessionStruct)
        ## reminder: to go into these data after storing it, the syntax looks like: ## taskStruct['sessions'][sI].blocks[bI].__dict__
        # end
    # set first block of the first session
    taskStruct['practSession'][0]['practBlocks'][0]['firstNovelTrial'] = 0
    taskStruct['practSession'][0]['practBlocks'][0]['secondNovelTrial'] = 0
    taskStruct['practSession'][0]['practBlocks'][0]['secondFamiliarTrial'] = 0
    return(taskStruct)

