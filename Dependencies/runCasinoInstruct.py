from psychopy import visual, gui, data, core, event, logging, info
from psychopy.constants import *
import numpy as np # whole numpy lib is available, prepend 'np.'
import os
from config import *

def runCasinoInstruct(dispStruct,keyStruct,taskStruct,expInfo):
    pages = range(47)
    # Set up instruction display dictionary
    dispStruct['Instruct'] = dict()
    # Initialize instruction keys and display
    dispStruct = initInstDisplay(dispStruct,keyStruct,taskStruct)
    currPage = 1
    while True:
        # Run instruction function
        dispStruct = feval('Instructions_Casino_' + str(currPage),dispStruct,taskStruct)
        # wait for response
        if currPage == 7:
            response = event.waitKeys(keyList=[keyStruct['respKeyLeft'],keyStruct['instrKeyPrev'],'escape'])
            if keyStruct['instrKeyPrev'] in response:
                # Move back a screen
                currPage = max(1,currPage-1)
                print "Page " + str(currPage)
            elif keyStruct['respKeyLeft'] in response:
                # Move forward a screen
                currPage = min(len(pages), currPage+1)
                print "Page " + str(currPage)
        elif currPage == 10:
            response = event.waitKeys(keyList=[keyStruct['respKeyRight'],keyStruct['instrKeyPrev'],'escape'])
            if keyStruct['instrKeyPrev'] in response:
                # Move back a screen
                currPage = max(1,currPage-1)
                print "Page " + str(currPage)
            elif keyStruct['respKeyRight'] in response:
                # Move forward a screen
                currPage = min(len(pages), currPage+1)
                print "Page " + str(currPage)
        elif currPage == 13:
            response = event.waitKeys(keyList=[keyStruct['respKeyLeft'],keyStruct['instrKeyPrev'],'escape'])
            if keyStruct['instrKeyPrev'] in response:
                # Move back a screen
                currPage = max(1,currPage-1)
                print "Page " + str(currPage)
            elif keyStruct['respKeyLeft'] in response:
                # Move forward a screen
                currPage = min(len(pages), currPage+1)
                print "Page " + str(currPage)
        elif currPage == 14:
            response = event.waitKeys(keyList=[keyStruct['respKeyRight'],keyStruct['instrKeyPrev'],'escape'])
            if keyStruct['instrKeyPrev'] in response:
                # Move back a screen
                currPage = max(1,currPage-1)
                print "Page " + str(currPage)
            elif keyStruct['respKeyRight'] in response:
                # Move forward a screen
                currPage = min(len(pages), currPage+1)
                print "Page " + str(currPage)
        elif currPage == 25:
            if dispStruct['Instruct']['page25_scale'].getRating() == 'no idea(4)':
                # Move forward a screen
                currPage = min(len(pages), currPage+1)
                print "Page " + str(currPage)
            else:
                dispStruct = errRestart(dispStruct)
                currPage = 15
                print "Page " + str(currPage)
        elif currPage == 26:
            if dispStruct['Instruct']['page26_scale'].getRating() == 'the same(2)':
                # Move forward a screen
                currPage = min(len(pages), currPage+1)
                print "Page " + str(currPage)
            else:
                currPage = 15
                dispStruct = errRestart(dispStruct)
        elif currPage == 28:
            response = event.waitKeys(keyList=[keyStruct['respKeyLeft'],'escape'])
            if keyStruct['respKeyLeft'] in response:
                # Move forward a screen
                currPage = min(len(pages), currPage+1)
                print "Page " + str(currPage)
        elif currPage == 30:
            response = event.waitKeys(keyList=[keyStruct['respKeyRight'],'escape'])
            if keyStruct['respKeyRight'] in response:
                # Move forward a screen
                currPage = min(len(pages), currPage+1)
                print "Page " + str(currPage)
        elif currPage == 32:
            response = event.waitKeys(keyList=[keyStruct['respKeyLeft'],'escape'])
            if keyStruct['respKeyLeft'] in response:
                # Move forward a screen
                currPage = min(len(pages), currPage+1)
                print "Page " + str(currPage)
        elif currPage == 34:
            response = event.waitKeys(keyList=[keyStruct['respKeyRight'],'escape'])
            if keyStruct['respKeyRight'] in response:
                # Move forward a screen
                currPage = min(len(pages), currPage+1)
                print "Page " + str(currPage)
        elif currPage == 36:
            if dispStruct['Instruct']['page36_scale'].getRating() == 'good':
                currPage = min(len(pages), currPage+1)
                print "Page " + str(currPage)
            else:
                dispStruct = errWarning(dispStruct)
        elif currPage == 37:
            if dispStruct['Instruct']['page37_scale'].getRating() == 'bad':
                currPage = min(len(pages), currPage+1)
                print "Page " + str(currPage)
            else:
                dispStruct = errWarning(dispStruct)
        elif currPage == 39:
            response = event.waitKeys(keyList=keyStruct['instrAllowable'])
            if expInfo['Modality'] == 'behaviour':
                if keyStruct['instrKeyPrev'] in response:
                    # Move back a screen
                    currPage = max(1,currPage-1)
                    print "Page " + str(currPage)
                elif keyStruct['instrKeyNext'] in response:
                    # Move forward two screens
                    currPage = min(len(pages), currPage+2)
                    print "Page " + str(currPage)
            elif expInfo['Modality'] == 'fMRI':
                if keyStruct['instrKeyPrev'] in response:
                    # Move back a screen
                    currPage = max(1,currPage-1)
                    print "Page " + str(currPage)
                elif keyStruct['instrKeyNext'] in response:
                    # Move forward two screens
                    currPage = min(len(pages), currPage+1)
                    print "Page " + str(currPage)
        elif currPage == 41:
            response = event.waitKeys(keyList=[keyStruct['respKeyLeft'],keyStruct['instrKeyPrev'],'escape'])
            if keyStruct['instrKeyPrev'] in response:
                # Move back a screen
                currPage = max(1,currPage-1)
                print "Page " + str(currPage)
            elif keyStruct['respKeyLeft'] in response:
                # Move forward a screen
                currPage = min(len(pages), currPage+1)
                print "Page " + str(currPage)
        elif currPage == 43:
            response = event.waitKeys(keyList=[keyStruct['respKeyRight'],'escape'])
            if keyStruct['respKeyRight'] in response:
                # Move forward a screen
                currPage = min(len(pages), currPage+1)
                print "Page " + str(currPage)
        elif currPage == len(pages):
            response = event.waitKeys(keyList=keyStruct['instrAllowable'].append(keyStruct['instrKeyDone']))
            if keyStruct['instrKeyPrev'] in response:
                # Move back a screen
                if expInfo['Modality'] == 'behaviour':
                    currPage = max(1,currPage-2)
                    print "Page " + str(currPage)
                elif expInfo['Modality'] == 'fMRI':
                    currPage = max(1,currPage-1)
                    print "Page " + str(currPage)
            elif keyStruct['instrKeyDone'] in response:
                break
        else:
            response = event.waitKeys(keyList=keyStruct['instrAllowable'])
            if keyStruct['instrKeyPrev'] in response:
                # Move back a screen
                currPage = max(1,currPage-1)
                print "Page " + str(currPage)
            elif keyStruct['instrKeyNext'] in response:
                # Move forward a screen
                currPage = min(len(pages), currPage+1)
                print "Page " + str(currPage)
        if 'escape' in response:
            print "Aborting program..."
            core.wait(2)
            core.quit()
    return(dispStruct)

# Sub-functions under runCasinoInstruct.py
def initInstDisplay(dispStruct,keyStruct,taskStruct):
    # Instruction text nav
    dispStruct['Instruct']['textNav'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.05, font = dispStruct['textFont'], wrapWidth = 1.8)
    dispStruct['Instruct']['textNav'].text = 'Navigate through the instructions with the "' + taskStruct['instrKeyPrevName'] + '" (previous) and "' + taskStruct['instrKeyNextName'] + '" (next) keys'
    dispStruct['Instruct']['textNav'].pos = [0,-0.8]
    # Initialize what the practice stims ares
    for lr in range(2):
        dispStruct['stimTrial'][lr].setImage(taskStruct['Dir']['StimCues'] + os.sep + "i" + str(taskStruct['instructStim'][lr]) + ".bmp")
        dispStruct['stimTrial'][lr].rescaledSize = rescaleStim(dispStruct['stimTrial'][lr],dispStruct['stimSize'],dispStruct)
        dispStruct['stimTrial'][lr].setSize(dispStruct['stimTrial'][lr].rescaledSize)
    # Specify where win and non-win are positioned for the instructions
    dispStruct['fbTrial']['noWin'].pos = dispStruct['slotsPosR']
    dispStruct['fbTrial']['Win'].pos = dispStruct['slotsPosL']
    # Specify which side is win/loss for the roulette feedback (instructions only)
    dispStruct['rouletteFbTrial'][1].text = taskStruct['winAmount'] # gain roulette
    dispStruct['rouletteFbTrial'][0].text = '-' + taskStruct['winAmount'] # loss roulette
    # Specify which side is the win/loss for the context manipulation roulette feedbacks (instructions only)
    dispStruct['contextRouletteFbTrial'][0].text = taskStruct['winContextAmount']
    dispStruct['contextRouletteFbTrial'][1].text = '-' + taskStruct['winContextAmount']
    # Additional instructions-only images
    dispStruct['Instruct']['Casino_Depiction'] = visual.ImageStim(dispStruct['screen'])
    dispStruct['Instruct']['Casino_Depiction'].setImage(taskStruct['Dir']['Global'] + os.sep + "RewardDepiction.png")
    dispStruct['Instruct']['Casino_Depiction'].pos = [0,0]
    dispStruct['Instruct']['Casino_Depiction'].rescaledSize = rescale(dispStruct['Instruct']['Casino_Depiction'],1.2)
    dispStruct['Instruct']['Casino_Depiction'].setSize(dispStruct['Instruct']['Casino_Depiction'].rescaledSize)
    return(dispStruct)

def Instructions_Casino_1(dispStruct,taskStruct):
    # Instruction header
    dispStruct['Instruct']['page1_head'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.09, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page1_head'].text = '--Instructions 1--'
    dispStruct['Instruct']['page1_head'].pos = [0,0.8]
    # Instruction text 1
    dispStruct['Instruct']['page1_text1'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page1_text1'].text = 'You are going on a gambling trip around the world.'
    dispStruct['Instruct']['page1_text1'].pos = [0,0.2]
    # Instruction text 2
    dispStruct['Instruct']['page1_text2'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page1_text2'].text = 'Each day you will visit one casino in a different country and be given free games on the slot machines, and a starting amount of ' + taskStruct['startAmount'] + '.'
    dispStruct['Instruct']['page1_text2'].pos = [0,-0.2]
    # Draw page
    dispStruct['Instruct']['page1_head'].draw()
    dispStruct['Instruct']['page1_text1'].draw()
    dispStruct['Instruct']['page1_text2'].draw()
    dispStruct['Instruct']['textNav'].draw()
    dispStruct['screen'].flip()
    return(dispStruct)


def Instructions_Casino_2(dispStruct,taskStruct):
    # Instruction header
    dispStruct['Instruct']['page2_head'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.09, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page2_head'].text = '--Instructions 2--'
    dispStruct['Instruct']['page2_head'].pos = [0,0.8]
    # Instruction text 1
    dispStruct['Instruct']['page2_text1'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page2_text1'].text = 'This is what you will see each turn:'
    dispStruct['Instruct']['page2_text1'].pos = [0,0.6]
    # Draw page
    dispStruct['Instruct']['page2_head'].draw()
    dispStruct['Instruct']['page2_text1'].draw()
    dispStruct['Instruct']['textNav'].draw()
    for lr in range(2):
        dispStruct['instructFlag'][lr].draw()
        dispStruct['instructStateName'][lr].draw()
        dispStruct['machine'][lr].draw()
        dispStruct['stimTrial'][lr].draw()
        dispStruct['slotsTrial'][lr].draw()
    dispStruct['screen'].flip()
    return(dispStruct)

def Instructions_Casino_3(dispStruct,taskStruct):
    # Instruction header
    dispStruct['Instruct']['page3_head'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.09, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page3_head'].text = '--Instructions 3--'
    dispStruct['Instruct']['page3_head'].pos = [0,0.8]
    # Instruction text 1
    dispStruct['Instruct']['page3_text1'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page3_text1'].text = 'The flags are there to remind of the country you are visiting.'
    dispStruct['Instruct']['page3_text1'].pos = [0,0.6]
    # Draw page
    dispStruct['Instruct']['page3_head'].draw()
    dispStruct['Instruct']['page3_text1'].draw()
    dispStruct['Instruct']['textNav'].draw()
    for lr in range(2):
        dispStruct['instructFlag'][lr].draw()
        dispStruct['instructStateName'][lr].draw()
        dispStruct['machine'][lr].draw()
        dispStruct['stimTrial'][lr].draw()
        dispStruct['slotsTrial'][lr].draw()

    dispStruct['screen'].flip()
    return(dispStruct)

def Instructions_Casino_4(dispStruct,taskStruct):
    # Instruction header
    dispStruct['Instruct']['page4_head'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.09, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page4_head'].text = '--Instructions 4--'
    dispStruct['Instruct']['page4_head'].pos = [0,0.8]
    # Instruction text 1
    dispStruct['Instruct']['page4_text1'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page4_text1'].text = 'You will get to play several different slot machines in each casino.'
    dispStruct['Instruct']['page4_text1'].pos = [0,0.6]
    # Instruction text 2
    dispStruct['Instruct']['page4_text2'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page4_text2'].text = 'Each machine has a unique image to help you tell them apart.'
    dispStruct['Instruct']['page4_text2'].pos = [0,0.5]
    # Draw page
    dispStruct['Instruct']['page4_head'].draw()
    dispStruct['Instruct']['page4_text1'].draw()
    dispStruct['Instruct']['page4_text2'].draw()
    dispStruct['Instruct']['textNav'].draw()
    for lr in range(2):
        dispStruct['instructFlag'][lr].draw()
        dispStruct['instructStateName'][lr].draw()
        dispStruct['machine'][lr].draw()
        dispStruct['stimTrial'][lr].draw()
        dispStruct['slotsTrial'][lr].draw()

    dispStruct['screen'].flip()
    return(dispStruct)

def Instructions_Casino_5(dispStruct,taskStruct):
    # Instruction header
    dispStruct['Instruct']['page5_head'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.09, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page5_head'].text = '--Instructions 5--'
    dispStruct['Instruct']['page5_head'].pos = [0,0.8]
    # Instruction text 1
    dispStruct['Instruct']['page5_text1'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page5_text1'].text = 'On each turn you will see two different machines, one on the left and one on the right.'
    dispStruct['Instruct']['page5_text1'].pos = [0,0.6]
    # Instruction text 2
    dispStruct['Instruct']['page5_text2'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page5_text2'].text = 'You will have ' + str(taskStruct['maxRT']) + ' seconds to select one.'
    dispStruct['Instruct']['page5_text2'].pos = [0,0.5]
    # Draw page
    dispStruct['Instruct']['page5_head'].draw()
    dispStruct['Instruct']['page5_text1'].draw()
    dispStruct['Instruct']['page5_text2'].draw()
    dispStruct['Instruct']['textNav'].draw()
    for lr in range(2):
        dispStruct['instructFlag'][lr].draw()
        dispStruct['instructStateName'][lr].draw()
        dispStruct['machine'][lr].draw()
        dispStruct['stimTrial'][lr].draw()
        dispStruct['slotsTrial'][lr].draw()

    dispStruct['screen'].flip()
    return(dispStruct)

def Instructions_Casino_6(dispStruct,taskStruct):
    # Instruction header
    dispStruct['Instruct']['page6_head'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.09, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page6_head'].text = '--Instructions 6--'
    dispStruct['Instruct']['page6_head'].pos = [0,0.8]
    # Instruction text 1
    dispStruct['Instruct']['page6_text1'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page6_text1'].text = 'Machines appear on the left and right totally at random.'
    dispStruct['Instruct']['page6_text1'].pos = [0,0.6]
    # Instruction text 2
    dispStruct['Instruct']['page6_text2'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page6_text2'].text = 'This is ensure right or left handed people do not have any advantages.'
    dispStruct['Instruct']['page6_text2'].pos = [0,0.5]
    # Draw page
    dispStruct['Instruct']['page6_head'].draw()
    dispStruct['Instruct']['page6_text1'].draw()
    dispStruct['Instruct']['page6_text2'].draw()
    dispStruct['Instruct']['textNav'].draw()
    for lr in range(2):
        dispStruct['instructFlag'][lr].draw()
        dispStruct['instructStateName'][lr].draw()
        dispStruct['machine'][lr].draw()
        dispStruct['stimTrial'][lr].draw()
        dispStruct['slotsTrial'][lr].draw()

    dispStruct['screen'].flip()
    return(dispStruct)

def Instructions_Casino_7(dispStruct,taskStruct):
    # Instruction header
    dispStruct['Instruct']['page7_head'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.09, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page7_head'].text = '--Instructions 7--'
    dispStruct['Instruct']['page7_head'].pos = [0,0.8]
    # Instruction text 1
    dispStruct['Instruct']['page7_text1'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page7_text1'].text = 'Please select the machine presented on the left using the ' + taskStruct['respKeyLeftName']+ ' key now.'
    dispStruct['Instruct']['page7_text1'].pos = [0,0.6]
    # Draw page
    dispStruct['Instruct']['page7_head'].draw()
    dispStruct['Instruct']['page7_text1'].draw()
    dispStruct['Instruct']['textNav'].draw()
    for lr in range(2):
        dispStruct['instructFlag'][lr].draw()
        dispStruct['instructStateName'][lr].draw()
        dispStruct['machine'][lr].draw()
        dispStruct['stimTrial'][lr].draw()
        dispStruct['slotsTrial'][lr].draw()

    dispStruct['screen'].flip()
    return(dispStruct)

def Instructions_Casino_8(dispStruct,taskStruct):
    # Instruction header
    dispStruct['Instruct']['page8_head'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.09, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page8_head'].text = '--Instructions 8--'
    dispStruct['Instruct']['page8_head'].pos = [0,0.8]
    # Instruction text 1
    dispStruct['Instruct']['page8_text1'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page8_text1'].text = 'When you select a machine, the slots will spin:'
    dispStruct['Instruct']['page8_text1'].pos = [0,0.6]
    # Draw page
    dispStruct['Instruct']['page8_head'].setAutoDraw(True)
    dispStruct['Instruct']['page8_text1'].setAutoDraw(True)
    dispStruct['Instruct']['textNav'].setAutoDraw(True)
    for lr in range(2):
        dispStruct['instructFlag'][lr].setAutoDraw(True)
        dispStruct['instructStateName'][lr].setAutoDraw(True)
        dispStruct['machine'][lr].setAutoDraw(True)
        dispStruct['stimTrial'][lr].setAutoDraw(True)
        dispStruct['slotsTrial'][lr].setAutoDraw(True)
    dispStruct['revolSlots'][0].setAutoDraw(True)
    instructClock = core.Clock()
    while instructClock.getTime() < 1.5:
        dispStruct['revolSlots'][0].phase += 0.3
        dispStruct['screen'].flip()
    dispStruct['revolSlots'][0].setAutoDraw(False)
    # once the reels stop spinning, show the reward
    dispStruct['fbTrial']['Win'].setAutoDraw(True)
    dispStruct['screen'].flip()
    # Clear screen for next instructions
    dispStruct['Instruct']['page8_head'].setAutoDraw(False)
    dispStruct['Instruct']['page8_text1'].setAutoDraw(False)
    dispStruct['Instruct']['textNav'].setAutoDraw(False)
    for lr in range(2):
        dispStruct['instructFlag'][lr].setAutoDraw(False)
        dispStruct['instructStateName'][lr].setAutoDraw(False)
        dispStruct['machine'][lr].setAutoDraw(False)
        dispStruct['stimTrial'][lr].setAutoDraw(False)
        dispStruct['slotsTrial'][lr].setAutoDraw(False)
    dispStruct['fbTrial']['Win'].setAutoDraw(False)
    return(dispStruct)

def Instructions_Casino_9(dispStruct,taskStruct):
    # Instruction header
    dispStruct['Instruct']['page9_head'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.09, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page9_head'].text = '--Instructions 9--'
    dispStruct['Instruct']['page9_head'].pos = [0,0.8]
    # Instruction text 1
    dispStruct['Instruct']['page9_text1'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page9_text1'].text = 'After you select a machine you will see if it won or not.'
    dispStruct['Instruct']['page9_text1'].pos = [0,0.6]
    # Instruction text 2
    dispStruct['Instruct']['page9_text2'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page9_text2'].text = 'If the machine wins, you earn ' + taskStruct['winAmount'] + '.'
    dispStruct['Instruct']['page9_text2'].pos = [0,0.5]
    # Draw page
    dispStruct['Instruct']['page9_head'].draw()
    dispStruct['Instruct']['page9_text1'].draw()
    dispStruct['Instruct']['page9_text2'].draw()
    dispStruct['Instruct']['textNav'].draw()
    for lr in range(2):
        dispStruct['instructFlag'][lr].draw()
        dispStruct['instructStateName'][lr].draw()
        dispStruct['machine'][lr].draw()
        dispStruct['stimTrial'][lr].draw()
        dispStruct['slotsTrial'][lr].draw()

    dispStruct['fbTrial']['Win'].draw()
    dispStruct['screen'].flip()
    return(dispStruct)

def Instructions_Casino_10(dispStruct,taskStruct):
    # Instruction header
    dispStruct['Instruct']['page10_head'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.09, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page10_head'].text = '--Instructions 10--'
    dispStruct['Instruct']['page10_head'].pos = [0,0.8]
    # Instruction text 1
    dispStruct['Instruct']['page10_text1'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page10_text1'].text = 'Please select the machine presented on the right using the ' + taskStruct['respKeyRightName']+ ' key now.'
    dispStruct['Instruct']['page10_text1'].pos = [0,0.6]
    # Draw page
    dispStruct['Instruct']['page10_head'].draw()
    dispStruct['Instruct']['page10_text1'].draw()
    dispStruct['Instruct']['textNav'].draw()
    for lr in range(2):
        dispStruct['instructFlag'][lr].draw()
        dispStruct['instructStateName'][lr].draw()
        dispStruct['machine'][lr].draw()
        dispStruct['stimTrial'][lr].draw()
        dispStruct['slotsTrial'][lr].draw()

    dispStruct['screen'].flip()
    return(dispStruct)

def Instructions_Casino_11(dispStruct,taskStruct):
    # Instruction header
    dispStruct['Instruct']['page11_head'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.09, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page11_head'].text = '--Instructions 11--'
    dispStruct['Instruct']['page11_head'].pos = [0,0.8]
    # Draw page
    dispStruct['Instruct']['page11_head'].setAutoDraw(True)
    dispStruct['Instruct']['textNav'].setAutoDraw(True)
    for lr in range(2):
        dispStruct['instructFlag'][lr].setAutoDraw(True)
        dispStruct['instructStateName'][lr].setAutoDraw(True)
        dispStruct['machine'][lr].setAutoDraw(True)
        dispStruct['stimTrial'][lr].setAutoDraw(True)
        dispStruct['slotsTrial'][lr].setAutoDraw(True)
    dispStruct['revolSlots'][1].setAutoDraw(True)
    instructClock = core.Clock()
    while instructClock.getTime() < 1.5:
        dispStruct['revolSlots'][1].phase += 0.3
        dispStruct['screen'].flip()
    dispStruct['revolSlots'][1].setAutoDraw(False)
    # once the reels stop spinning, show the reward
    dispStruct['fbTrial']['noWin'].setAutoDraw(True)
    dispStruct['screen'].flip()
    # Clear screen for next instructions
    dispStruct['Instruct']['page11_head'].setAutoDraw(False)
    dispStruct['Instruct']['textNav'].setAutoDraw(False)
    for lr in range(2):
        dispStruct['instructFlag'][lr].setAutoDraw(False)
        dispStruct['instructStateName'][lr].setAutoDraw(False)
        dispStruct['machine'][lr].setAutoDraw(False)
        dispStruct['stimTrial'][lr].setAutoDraw(False)
        dispStruct['slotsTrial'][lr].setAutoDraw(False)
    dispStruct['fbTrial']['noWin'].setAutoDraw(False)
    return(dispStruct)

def Instructions_Casino_12(dispStruct,taskStruct):
    # Instruction header
    dispStruct['Instruct']['page12_head'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.09, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page12_head'].text = '--Instructions 12--'
    dispStruct['Instruct']['page12_head'].pos = [0,0.8]
    # Instruction text 2
    dispStruct['Instruct']['page12_text2'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page12_text2'].text = 'If the machine does NOT win, you earn nothing.'
    dispStruct['Instruct']['page12_text2'].pos = [0,0.6]
    # Draw page
    dispStruct['Instruct']['page12_head'].draw()
    dispStruct['Instruct']['page12_text2'].draw()
    dispStruct['Instruct']['textNav'].draw()
    for lr in range(2):
        dispStruct['instructFlag'][lr].draw()
        dispStruct['instructStateName'][lr].draw()
        dispStruct['machine'][lr].draw()
        dispStruct['stimTrial'][lr].draw()
        dispStruct['slotsTrial'][lr].draw()

    dispStruct['fbTrial']['noWin'].draw()
    dispStruct['screen'].flip()
    return(dispStruct)

def Instructions_Casino_13(dispStruct,taskStruct):
    # Instruction header
    dispStruct['Instruct']['page13_head'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.09, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page13_head'].text = '--Instructions 13--'
    dispStruct['Instruct']['page13_head'].pos = [0,0.8]
    # Instruction text 2
    dispStruct['Instruct']['page13_text1'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page13_text1'].text = 'Please indicate which machine won now, using the ' + taskStruct['respKeyLeftName']+ ' and ' + taskStruct['respKeyRightName']+ ' keys.'
    dispStruct['Instruct']['page13_text1'].pos = [0,0.6]
    # Draw page
    dispStruct['Instruct']['page13_head'].draw()
    dispStruct['Instruct']['page13_text1'].draw()
    dispStruct['Instruct']['textNav'].draw()
    # Draw reward
    for lr in range(2):
        dispStruct['instructFlag'][lr].draw()
        dispStruct['instructStateName'][lr].draw()
        dispStruct['machine'][lr].draw()
        dispStruct['stimTrial'][lr].draw()
        dispStruct['slotsTrial'][lr].draw()

    dispStruct['fbTrial']['noWin'].draw()
    dispStruct['fbTrial']['Win'].draw()
    dispStruct['screen'].flip()
    return(dispStruct)

def Instructions_Casino_14(dispStruct,taskStruct):
    # Instruction header
    dispStruct['Instruct']['page14_head'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.09, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page14_head'].text = '--Instructions 14--'
    dispStruct['Instruct']['page14_head'].pos = [0,0.8]
    # Instruction text 2
    dispStruct['Instruct']['page14_text1'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page14_text1'].text = 'Please indicate which machine did NOT win now, using the ' + taskStruct['respKeyLeftName']+ ' and ' + taskStruct['respKeyRightName']+ ' keys.'
    dispStruct['Instruct']['page14_text1'].pos = [0,0.6]
    # Draw page
    dispStruct['Instruct']['page14_head'].draw()
    dispStruct['Instruct']['page14_text1'].draw()
    dispStruct['Instruct']['textNav'].draw()
    # Draw reward
    for lr in range(2):
        dispStruct['instructFlag'][lr].draw()
        dispStruct['instructStateName'][lr].draw()
        dispStruct['machine'][lr].draw()
        dispStruct['stimTrial'][lr].draw()
        dispStruct['slotsTrial'][lr].draw()

    dispStruct['fbTrial']['noWin'].draw()
    dispStruct['fbTrial']['Win'].draw()
    dispStruct['screen'].flip()
    return(dispStruct)

def Instructions_Casino_15(dispStruct,taskStruct):
    # Instruction header
    dispStruct['Instruct']['page15_head'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.09, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page15_head'].text = '--Instructions 15--'
    dispStruct['Instruct']['page15_head'].pos = [0,0.8]
    # Instruction text 1
    dispStruct['Instruct']['page15_text1'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page15_text1'].text = 'In each country you visit, you will go to one casino and gamble.'
    dispStruct['Instruct']['page15_text1'].pos = [0,0.6]
    # Draw page
    dispStruct['Instruct']['page15_head'].draw()
    dispStruct['Instruct']['page15_text1'].draw()
    dispStruct['Instruct']['textNav'].draw()
    for lr in range(2):
        dispStruct['stimTrial'][lr].setImage(taskStruct['Dir']['StimCues'] + os.sep + "i" + str(taskStruct['instructStim'][lr]) + ".bmp")
        dispStruct['stimTrial'][lr].rescaledSize = rescaleStim(dispStruct['stimTrial'][lr],dispStruct['stimSize'],dispStruct)
        dispStruct['stimTrial'][lr].setSize(dispStruct['stimTrial'][lr].rescaledSize)
        dispStruct['instructStateName'][lr].text = taskStruct['practStateNames'][0]
        dispStruct['instructFlag'][lr].setImage(taskStruct['Dir']['Flags'] + os.sep + "flag_" + taskStruct['practStateNames'][0] + ".png")
        dispStruct['instructFlag'][lr].draw()
        dispStruct['instructStateName'][lr].draw()
        dispStruct['machine'][lr].draw()
        dispStruct['stimTrial'][lr].draw()
        dispStruct['slotsTrial'][lr].draw()

    dispStruct['screen'].flip()
    return(dispStruct)

def Instructions_Casino_16(dispStruct,taskStruct):
    # Instruction header
    dispStruct['Instruct']['page16_head'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.09, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page16_head'].text = '--Instructions 16--'
    dispStruct['Instruct']['page16_head'].pos = [0,0.8]
    # Instruction text 1
    dispStruct['Instruct']['page16_text1'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page16_text1'].text = 'Each casino has programmed its own machines according to national gambling laws. No casino will be better or worse than any other.'
    dispStruct['Instruct']['page16_text1'].pos = [0,0.6]
    # Draw page
    dispStruct['Instruct']['page16_head'].draw()
    dispStruct['Instruct']['page16_text1'].draw()
    dispStruct['Instruct']['textNav'].draw()
    for lr in range(2):
        dispStruct['instructFlag'][lr].draw()
        dispStruct['instructStateName'][lr].draw()
        dispStruct['machine'][lr].draw()
        dispStruct['stimTrial'][lr].draw()
        dispStruct['slotsTrial'][lr].draw()

    dispStruct['screen'].flip()
    return(dispStruct)

def Instructions_Casino_17(dispStruct,taskStruct):
    # Instruction header
    dispStruct['Instruct']['page17_head'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.09, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page17_head'].text = '--Instructions 17--'
    dispStruct['Instruct']['page17_head'].pos = [0,0.8]
    # Instruction text 1
    dispStruct['Instruct']['page17_text1'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page17_text1'].text = 'Each machine is programmed to have some chance of winning. Some machines win frequently, others win rarely, and the rest are somewhere in between.'
    dispStruct['Instruct']['page17_text1'].pos = [0,0.6]
    # Draw page
    dispStruct['Instruct']['page17_head'].draw()
    dispStruct['Instruct']['page17_text1'].draw()
    dispStruct['Instruct']['textNav'].draw()
    for lr in range(2):
        dispStruct['instructFlag'][lr].draw()
        dispStruct['instructStateName'][lr].draw()
        dispStruct['machine'][lr].draw()
        dispStruct['stimTrial'][lr].draw()
        dispStruct['slotsTrial'][lr].draw()

    dispStruct['screen'].flip()
    return(dispStruct)

def Instructions_Casino_18(dispStruct,taskStruct):
    # Instruction header
    dispStruct['Instruct']['page18_head'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.09, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page18_head'].text = '--Instructions 18--'
    dispStruct['Instruct']['page18_head'].pos = [0,0.8]
    # Instruction text 1
    dispStruct['Instruct']['page18_text1'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page18_text1'].text = 'Because machines are separately programmed by each casino, even if you see a machine from another country, they are different machines. You will not know which machines are the best when you arrive at a new casino.'
    dispStruct['Instruct']['page18_text1'].pos = [0,0.6]
    # Draw page
    dispStruct['Instruct']['page18_head'].draw()
    dispStruct['Instruct']['page18_text1'].draw()
    dispStruct['Instruct']['textNav'].draw()
    for lr in range(2):
        dispStruct['instructFlag'][lr].draw()
        dispStruct['instructStateName'][lr].draw()
        dispStruct['machine'][lr].draw()
        dispStruct['stimTrial'][lr].draw()
        dispStruct['slotsTrial'][lr].draw()

    dispStruct['screen'].flip()
    return(dispStruct)

def Instructions_Casino_19(dispStruct,taskStruct):
    # Instruction header
    dispStruct['Instruct']['page19_head'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.09, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page19_head'].text = '--Instructions 19--'
    dispStruct['Instruct']['page19_head'].pos = [0,0.8]
    # Instruction text 1
    dispStruct['Instruct']['page19_text1'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page19_text1'].text = 'You will have to learn this on your own.'
    dispStruct['Instruct']['page19_text1'].pos = [0,0.6]
    # Draw page
    dispStruct['Instruct']['page19_head'].draw()
    dispStruct['Instruct']['page19_text1'].draw()
    dispStruct['Instruct']['textNav'].draw()
    for lr in range(2):
        dispStruct['instructFlag'][lr].draw()
        dispStruct['instructStateName'][lr].draw()
        dispStruct['machine'][lr].draw()
        dispStruct['stimTrial'][lr].draw()
        dispStruct['slotsTrial'][lr].draw()

    dispStruct['screen'].flip()
    return(dispStruct)

def Instructions_Casino_20(dispStruct,taskStruct):
    # Instruction header
    dispStruct['Instruct']['page20_head'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.09, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page20_head'].text = '--Instructions 20--'
    dispStruct['Instruct']['page20_head'].pos = [0,0.8]
    # Instruction text 1
    dispStruct['Instruct']['page20_text1'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page20_text1'].text = 'For example, if the machine on the right was programmed to win 75% of the time in ' + taskStruct['practStateNames'][0] + '...'
    dispStruct['Instruct']['page20_text1'].pos = [0,0.6]
    # Draw page
    dispStruct['Instruct']['page20_head'].draw()
    dispStruct['Instruct']['page20_text1'].draw()
    dispStruct['Instruct']['textNav'].draw()
    for lr in range(2):
        dispStruct['stimTrial'][lr].setImage(taskStruct['Dir']['StimCues'] + os.sep + "i" + str(taskStruct['instructStim'][lr]) + ".bmp")
        dispStruct['stimTrial'][lr].rescaledSize = rescaleStim(dispStruct['stimTrial'][lr],dispStruct['stimSize'],dispStruct)
        dispStruct['stimTrial'][lr].setSize(dispStruct['stimTrial'][lr].rescaledSize)
        dispStruct['instructStateName'][lr].text = taskStruct['practStateNames'][0]
        dispStruct['instructFlag'][lr].setImage(taskStruct['Dir']['Flags'] + os.sep + "flag_" + taskStruct['practStateNames'][0] + ".png")
        dispStruct['instructFlag'][lr].draw()
        dispStruct['instructStateName'][lr].draw()
        dispStruct['machine'][lr].draw()
        dispStruct['stimTrial'][lr].draw()
        dispStruct['slotsTrial'][lr].draw()

    dispStruct['screen'].flip()
    return(dispStruct)

def Instructions_Casino_21(dispStruct,taskStruct):
    # Instruction header
    dispStruct['Instruct']['page21_head'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.09, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page21_head'].text = '--Instructions 21--'
    dispStruct['Instruct']['page21_head'].pos = [0,0.8]
    # Instruction text 1
    dispStruct['Instruct']['page21_text1'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page21_text1'].text = 'A machine that looks the same in ' + taskStruct['practStateNames'][1] + ' might be programmed to win 16% or 82% of the time.'
    dispStruct['Instruct']['page21_text1'].pos = [0,0.6]
    # Instruction text 2
    dispStruct['Instruct']['page21_text2'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page21_text2'].text = 'It could be anything.'
    dispStruct['Instruct']['page21_text2'].pos = [0,0.5]
    # Draw page
    dispStruct['Instruct']['page21_head'].draw()
    dispStruct['Instruct']['page21_text1'].draw()
    dispStruct['Instruct']['page21_text2'].draw()
    dispStruct['Instruct']['textNav'].draw()
    for lr in range(2):
        dispStruct['stimTrial'][lr].setImage(taskStruct['Dir']['StimCues'] + os.sep + "i" + str(taskStruct['instructStim'][lr]+1) + ".bmp")
        dispStruct['stimTrial'][lr].rescaledSize = rescaleStim(dispStruct['stimTrial'][lr],dispStruct['stimSize'],dispStruct)
        dispStruct['stimTrial'][lr].setSize(dispStruct['stimTrial'][lr].rescaledSize)
        dispStruct['instructStateName'][lr].text = taskStruct['practStateNames'][1]
        dispStruct['instructFlag'][lr].setImage(taskStruct['Dir']['Flags'] + os.sep + "flag_" + taskStruct['practStateNames'][1] + ".png")
        dispStruct['instructFlag'][lr].rescaledSize = rescale(dispStruct['instructFlag'][lr], dispStruct['flagTrialSize'])
        dispStruct['instructFlag'][lr].setSize(dispStruct['instructFlag'][lr].rescaledSize)
        dispStruct['instructFlag'][lr].draw()
        dispStruct['instructStateName'][lr].draw()
        dispStruct['machine'][lr].draw()
        dispStruct['stimTrial'][lr].draw()
        dispStruct['slotsTrial'][lr].draw()

    dispStruct['screen'].flip()
    return(dispStruct)


def Instructions_Casino_22(dispStruct,taskStruct):
    # Instruction header
    dispStruct['Instruct']['page22_head'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.09, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page22_head'].text = '--Instructions 22--'
    dispStruct['Instruct']['page22_head'].pos = [0,0.8]
    # Instruction text 1
    dispStruct['Instruct']['page22_text1'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page22_text1'].text = "However, each machine's chance of winning will stay the same while you are in the same casino."
    dispStruct['Instruct']['page22_text1'].pos = [0,0.6]
    # Instruction text 1
    dispStruct['Instruct']['page22_text2'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page22_text2'].text = 'Because within a casino, it will be the same machine!'
    dispStruct['Instruct']['page22_text2'].pos = [0,0.5]
    # Draw page
    dispStruct['Instruct']['page22_head'].draw()
    dispStruct['Instruct']['page22_text1'].draw()
    dispStruct['Instruct']['page22_text2'].draw()
    dispStruct['Instruct']['textNav'].draw()
    for lr in range(2):
        dispStruct['instructFlag'][lr].draw()
        dispStruct['instructStateName'][lr].draw()
        dispStruct['machine'][lr].draw()
        dispStruct['stimTrial'][lr].draw()
        dispStruct['slotsTrial'][lr].draw()
    dispStruct['screen'].flip()
    return(dispStruct)


def Instructions_Casino_23(dispStruct,taskStruct):
    # Instruction header
    dispStruct['Instruct']['page23_head'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.09, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page23_head'].text = '--Instructions 23--'
    dispStruct['Instruct']['page23_head'].pos = [0,0.8]
    # Instruction text 1
    dispStruct['Instruct']['page23_text1'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page23_text1'].text = 'Here is what you may expect from playing the same machine 5 times in 2 different casinos:'
    dispStruct['Instruct']['page23_text1'].pos = [0,0.6]
    # Draw page
    dispStruct['Instruct']['page23_head'].draw()
    dispStruct['Instruct']['page23_text1'].draw()
    dispStruct['Instruct']['textNav'].draw()
    dispStruct['Instruct']['Casino_Depiction'].draw()
    dispStruct['screen'].flip()
    return(dispStruct)

def Instructions_Casino_24(dispStruct,taskStruct):
    # Instruction header
    dispStruct['Instruct']['page24_head'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.09, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page24_head'].text = '--Instructions 24--'
    dispStruct['Instruct']['page24_head'].pos = [0,0.8]
    # Instruction text 1
    dispStruct['Instruct']['page24_text1'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page24_text1'].text = 'In ' +  taskStruct['practStateNames'][0] + ' , this machine was programmed to win 60% of the time...'
    dispStruct['Instruct']['page24_text1'].pos = [0,0.6]
    # Instruction text 1
    dispStruct['Instruct']['page24_text2'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page24_text2'].text = 'But in ' + taskStruct['practStateNames'][1] + ' , this machine was programmed to win 20% of the time.'
    dispStruct['Instruct']['page24_text2'].pos = [0,0.5]
    # Draw page
    dispStruct['Instruct']['page24_head'].draw()
    dispStruct['Instruct']['page24_text1'].draw()
    dispStruct['Instruct']['page24_text2'].draw()
    dispStruct['Instruct']['textNav'].draw()
    dispStruct['Instruct']['Casino_Depiction'].draw()
    dispStruct['screen'].flip()
    return(dispStruct)


def Instructions_Casino_25(dispStruct,taskStruct):
    # Instruction header
    dispStruct['Instruct']['page25_head'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.09, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page25_head'].text = '--Instructions 25--'
    dispStruct['Instruct']['page25_head'].pos = [0,0.8]
    # Instruction text 1
    dispStruct['Instruct']['page25_scaleQ'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page25_scaleQ'].text = 'Using the keys below, tell me how good this machine will be in France?'
    dispStruct['Instruct']['page25_scaleQ'].pos = [0,-0.2]
    dispStruct['Instruct']['page25_scale'] = visual.RatingScale(dispStruct['screen'],choices=['bad(1)','average(2)','good(3)','no idea(4)'],respKeys=([taskStruct['respKeyLeftName'],taskStruct['instrKeyPrevName'],taskStruct['instrKeyNextName'],taskStruct['respKeyRightName']]),marker='circle',markerColor='white',markerStart=1.5,stretch=2,showAccept=False,acceptKeys=([taskStruct['respKeyLeftName'],taskStruct['instrKeyPrevName'],taskStruct['instrKeyNextName'],taskStruct['respKeyRightName']]),noMouse=True,skipKeys=None,showValue=False,textColor='black',pos=[0,-0.6])
    # Draw page
    dispStruct['stimTrial']['question'] = visual.ImageStim(dispStruct['screen'])
    dispStruct['stimTrial']['question'].setImage(taskStruct['Dir']['StimCues'] + os.sep + "i" + str(taskStruct['instructStim'][1]) + ".bmp")
    dispStruct['stimTrial']['question'].rescaledSize = rescaleStim(dispStruct['stimTrial']['question'],0.6,dispStruct)
    dispStruct['stimTrial']['question'].setSize(dispStruct['stimTrial']['question'].rescaledSize)
    dispStruct['stimTrial']['question'].pos = [0,0.2]
    event.clearEvents()
    while dispStruct['Instruct']['page25_scale'].noResponse:
        dispStruct['Instruct']['page25_head'].draw()
        dispStruct['Instruct']['page25_scaleQ'].draw()
        dispStruct['Instruct']['page25_scale'].draw()
        dispStruct['stimTrial']['question'].draw()
        dispStruct['screen'].flip()
    return(dispStruct)



def Instructions_Casino_26(dispStruct,taskStruct):
    # Instruction header
    dispStruct['Instruct']['page26_head'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.09, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page26_head'].text = '--Instructions 26--'
    dispStruct['Instruct']['page26_head'].pos = [0,0.8]
    # Instruction text 1
    dispStruct['Instruct']['page26_scaleQ'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page26_scaleQ'].text = 'If this machine was programmed to win 80% of the time in France at the start of the day, by the end of the day, how frequently will it win?'
    dispStruct['Instruct']['page26_scaleQ'].pos = [0,-0.2]
    dispStruct['Instruct']['page26_scale'] = visual.RatingScale(dispStruct['screen'],choices = ['less often(1)','the same(2)','more often(3)','no idea(4)'],respKeys=([taskStruct['respKeyLeftName'],taskStruct['instrKeyPrevName'],taskStruct['instrKeyNextName'],taskStruct['respKeyRightName']]),marker='circle',markerColor='white',markerStart=1.5,stretch=2,showAccept=False,acceptKeys=([taskStruct['respKeyLeftName'],taskStruct['instrKeyPrevName'],taskStruct['instrKeyNextName'],taskStruct['respKeyRightName']]),noMouse=True,skipKeys=None,showValue=False,textColor='black',pos=[0,-0.6])
    # Draw page
    event.clearEvents()
    while dispStruct['Instruct']['page26_scale'].noResponse:
        dispStruct['Instruct']['page26_head'].draw()
        dispStruct['Instruct']['page26_scaleQ'].draw()
        dispStruct['Instruct']['page26_scale'].draw()
        dispStruct['stimTrial']['question'].draw()
        dispStruct['screen'].flip()
    return(dispStruct)

def Instructions_Casino_27(dispStruct,taskStruct):
    # Instruction header
    dispStruct['Instruct']['page27_head'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.09, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page27_head'].text = '--Instructions 27--'
    dispStruct['Instruct']['page27_head'].pos = [0,0.8]
    # Instruction text 1
    dispStruct['Instruct']['page27_text1'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page27_text1'].text = 'When you are in transit between casinos, you will play roulette games that look like this:'
    dispStruct['Instruct']['page27_text1'].pos = [0,0.6]
    # Draw page
    dispStruct['Instruct']['page27_head'].draw()
    dispStruct['Instruct']['page27_text1'].draw()
    dispStruct['Instruct']['textNav'].draw()
    for lr in range(2):
        dispStruct['airportName'][lr].draw()
        dispStruct['airportFlag'][lr].draw()
        dispStruct['rouletteTrial'][lr].draw()

    dispStruct['screen'].flip()
    return(dispStruct)

def Instructions_Casino_28(dispStruct,taskStruct):
    # Instruction header
    dispStruct['Instruct']['page28_head'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.09, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page28_head'].text = '--Instructions 28--'
    dispStruct['Instruct']['page28_head'].pos = [0,0.8]
    # Instruction text 1
    dispStruct['Instruct']['page28_text1'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page28_text1'].text = 'Like the slots games, you choose between one of the roulettes.'
    dispStruct['Instruct']['page28_text1'].pos = [0,0.6]
    # Instruction text 2
    dispStruct['Instruct']['page28_text2'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page28_text2'].text = 'Select the one on the left now.'
    dispStruct['Instruct']['page28_text2'].pos = [0,0.5]
    # Draw page
    dispStruct['Instruct']['page28_head'].draw()
    dispStruct['Instruct']['page28_text1'].draw()
    dispStruct['Instruct']['page28_text2'].draw()
    for lr in range(2):
        dispStruct['airportName'][lr].draw()
        dispStruct['airportFlag'][lr].draw()
        dispStruct['rouletteTrial'][lr].draw()
    dispStruct['screen'].flip()
    return(dispStruct)

def Instructions_Casino_29(dispStruct,taskStruct):
    # Instruction header
    dispStruct['Instruct']['page29_head'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.09, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page29_head'].text = '--Instructions 29--'
    dispStruct['Instruct']['page29_head'].pos = [0,0.8]
    # Instruction text 1
    dispStruct['Instruct']['page29_text1'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page29_text1'].text = 'When you select a roulette, it will spin:'
    dispStruct['Instruct']['page29_text1'].pos = [0,0.6]
    # Instruction text 2
    dispStruct['Instruct']['page29_text2'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page29_text2'].text = 'If the roulette does not win, you lose ' + taskStruct['winAmount'] + '.'
    dispStruct['Instruct']['page29_text2'].pos = [0,0.5]
    # Draw page
    dispStruct['Instruct']['page29_head'].setAutoDraw(True)
    dispStruct['Instruct']['page29_text1'].setAutoDraw(True)
    for lr in range(2):
        dispStruct['airportName'][lr].setAutoDraw(True)
        dispStruct['airportFlag'][lr].setAutoDraw(True)
        dispStruct['rouletteTrial'][lr].setAutoDraw(True)
    dispStruct['rouletteTrial'][0].setAutoDraw(False)
    instructClock = core.Clock()
    while instructClock.getTime() < 1.5:
        for frames in range(11):
            dispStruct['rotatRoulette'][0].setImage(taskStruct['Dir']['Roulette'] + os.sep + "roulette"+str(frames)+".tiff") # recode here to store all animation frames in mem, then draw from mem
            dispStruct['rotatRoulette'][0].draw()
            dispStruct['screen'].flip()
    # once the reels stop spinning, show the reward
    dispStruct['rouletteFbTrial'][0].setAutoDraw(True)
    dispStruct['Instruct']['page29_text2'].setAutoDraw(True)
    dispStruct['Instruct']['textNav'].setAutoDraw(True)
    dispStruct['screen'].flip()
    # Clear screen for next instructions
    dispStruct['Instruct']['page29_head'].setAutoDraw(False)
    dispStruct['Instruct']['page29_text1'].setAutoDraw(False)
    dispStruct['Instruct']['page29_text2'].setAutoDraw(False)
    dispStruct['Instruct']['textNav'].setAutoDraw(False)
    for lr in range(2):
        dispStruct['airportName'][lr].setAutoDraw(False)
        dispStruct['airportFlag'][lr].setAutoDraw(False)
        dispStruct['rouletteTrial'][lr].setAutoDraw(False)
    dispStruct['rouletteFbTrial'][0].setAutoDraw(False)
    return(dispStruct)


def Instructions_Casino_30(dispStruct,taskStruct):
    # Instruction header
    dispStruct['Instruct']['page30_head'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.09, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page30_head'].text = '--Instructions 30--'
    dispStruct['Instruct']['page30_head'].pos = [0,0.8]
    # Instruction text 1
    dispStruct['Instruct']['page30_text1'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page30_text1'].text = 'Select the one on the right now.'
    dispStruct['Instruct']['page30_text1'].pos = [0,0.6]
    # Draw page
    dispStruct['Instruct']['page30_head'].draw()
    dispStruct['Instruct']['page30_text1'].draw()
    for lr in range(2):
        dispStruct['airportName'][lr].draw()
        dispStruct['airportFlag'][lr].draw()
        dispStruct['rouletteTrial'][lr].draw()

    dispStruct['screen'].flip()
    return(dispStruct)

def Instructions_Casino_31(dispStruct,taskStruct):
    # Instruction header
    dispStruct['Instruct']['page31_head'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.09, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page31_head'].text = '--Instructions 31--'
    dispStruct['Instruct']['page31_head'].pos = [0,0.8]
    # Instruction text 2
    dispStruct['Instruct']['page31_text2'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page31_text2'].text = 'If the roulette wins, you earn ' + taskStruct['winAmount'] + '.'
    dispStruct['Instruct']['page31_text2'].pos = [0,0.6]
    # Draw page
    dispStruct['Instruct']['page31_head'].setAutoDraw(True)
    for lr in range(2):
        dispStruct['airportName'][lr].setAutoDraw(True)
        dispStruct['airportFlag'][lr].setAutoDraw(True)
        dispStruct['rouletteTrial'][lr].setAutoDraw(True)
    dispStruct['rouletteTrial'][1].setAutoDraw(False)
    instructClock = core.Clock()
    while instructClock.getTime() < 1.5:
        for frames in range(11):
            dispStruct['rotatRoulette'][1].setImage(taskStruct['Dir']['Roulette'] + os.sep + "roulette"+str(frames)+".tiff") # recode here to store all animation frames in mem, then draw from mem
            dispStruct['rotatRoulette'][1].draw()
            dispStruct['screen'].flip()
    # once the reels stop spinning, show the reward
    dispStruct['rouletteFbTrial'][1].setAutoDraw(True)
    dispStruct['Instruct']['page31_text2'].setAutoDraw(True)
    dispStruct['Instruct']['textNav'].setAutoDraw(True)
    dispStruct['screen'].flip()
    # Clear screen for next instructions
    dispStruct['Instruct']['page31_head'].setAutoDraw(False)
    dispStruct['Instruct']['page31_text2'].setAutoDraw(False)
    dispStruct['Instruct']['textNav'].setAutoDraw(False)
    for lr in range(2):
        dispStruct['airportName'][lr].setAutoDraw(False)
        dispStruct['airportFlag'][lr].setAutoDraw(False)
        dispStruct['rouletteTrial'][lr].setAutoDraw(False)
    dispStruct['rouletteFbTrial'][1].setAutoDraw(False)
    dispStruct['Instruct']['page31_text2'].setAutoDraw(False)
    return(dispStruct)

def Instructions_Casino_32(dispStruct,taskStruct):
    # Instruction header
    dispStruct['Instruct']['page32_head'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.09, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page32_head'].text = '--Instructions 32--'
    dispStruct['Instruct']['page32_head'].pos = [0,0.8]
    # Instruction text 1
    dispStruct['Instruct']['page32_text1'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page32_text1'].text = 'Select the one on the left now.'
    dispStruct['Instruct']['page32_text1'].pos = [0,0.6]
    # Draw page
    dispStruct['Instruct']['page32_head'].draw()
    dispStruct['Instruct']['page32_text1'].draw()
    for lr in range(2):
        dispStruct['airportName'][lr].draw()
        dispStruct['airportFlag'][lr].draw()
        dispStruct['rouletteTrial'][lr].draw()
    dispStruct['screen'].flip()
    return(dispStruct)


def Instructions_Casino_33(dispStruct,taskStruct):
    # Instruction header
    dispStruct['Instruct']['page33_head'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.09, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page33_head'].text = '--Instructions 33--'
    dispStruct['Instruct']['page33_head'].pos = [0,0.8]
    # Instruction text 2
    dispStruct['Instruct']['page33_text1'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page33_text1'].text = 'Sometimes, the roulettes will lead to a large win of ' + taskStruct['winContextAmount'] + '!!!'
    dispStruct['Instruct']['page33_text1'].pos = [0,0.5]
    # Draw page
    dispStruct['Instruct']['page33_head'].setAutoDraw(True)
    for lr in range(2):
        dispStruct['airportName'][lr].setAutoDraw(True)
        dispStruct['airportFlag'][lr].setAutoDraw(True)
        dispStruct['rouletteTrial'][lr].setAutoDraw(True)
    dispStruct['rouletteTrial'][0].setAutoDraw(False)
    instructClock = core.Clock()
    while instructClock.getTime() < 1.5:
        for frames in range(11):
            dispStruct['rotatRoulette'][0].setImage(taskStruct['Dir']['Roulette'] + os.sep + "roulette"+str(frames)+".tiff") # recode here to store all animation frames in mem, then draw from mem
            dispStruct['rotatRoulette'][0].draw()
            dispStruct['screen'].flip()
    # once the reels stop spinning, show the reward
    dispStruct['contextRouletteFbTrial'][0].setAutoDraw(True)
    dispStruct['Instruct']['page33_text1'].setAutoDraw(True)
    dispStruct['Instruct']['textNav'].setAutoDraw(True)
    dispStruct['screen'].flip()
    # Clear screen for next instructions
    dispStruct['Instruct']['page33_head'].setAutoDraw(False)
    dispStruct['Instruct']['page33_text1'].setAutoDraw(False)
    dispStruct['Instruct']['textNav'].setAutoDraw(False)
    for lr in range(2):
        dispStruct['airportName'][lr].setAutoDraw(False)
        dispStruct['airportFlag'][lr].setAutoDraw(False)
        dispStruct['rouletteTrial'][lr].setAutoDraw(False)
    dispStruct['contextRouletteFbTrial'][0].setAutoDraw(False)
    return(dispStruct)

def Instructions_Casino_34(dispStruct,taskStruct):
    # Instruction header
    dispStruct['Instruct']['page34_head'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.09, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page34_head'].text = '--Instructions 34--'
    dispStruct['Instruct']['page34_head'].pos = [0,0.8]
    # Instruction text 1
    dispStruct['Instruct']['page34_text1'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page34_text1'].text = 'Select the one on the right now.'
    dispStruct['Instruct']['page34_text1'].pos = [0,0.6]
    # Draw page
    dispStruct['Instruct']['page34_head'].draw()
    dispStruct['Instruct']['page34_text1'].draw()
    for lr in range(2):
        dispStruct['airportName'][lr].draw()
        dispStruct['airportFlag'][lr].draw()
        dispStruct['rouletteTrial'][lr].draw()

    dispStruct['screen'].flip()
    return(dispStruct)

def Instructions_Casino_35(dispStruct,taskStruct):
    # Instruction header
    dispStruct['Instruct']['page35_head'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.09, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page35_head'].text = '--Instructions 35--'
    dispStruct['Instruct']['page35_head'].pos = [0,0.8]
    # Instruction text 2
    dispStruct['Instruct']['page35_text1'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page35_text1'].text = 'Other times, the roulettes will lead to a large LOSS of ' + taskStruct['winContextAmount'] + '!!!'
    dispStruct['Instruct']['page35_text1'].pos = [0,0.5]
    # Draw page
    dispStruct['Instruct']['page35_head'].setAutoDraw(True)
    for lr in range(2):
        dispStruct['airportName'][lr].setAutoDraw(True)
        dispStruct['airportFlag'][lr].setAutoDraw(True)
        dispStruct['rouletteTrial'][lr].setAutoDraw(True)
    dispStruct['rouletteTrial'][1].setAutoDraw(False)
    instructClock = core.Clock()
    while instructClock.getTime() < 1.5:
        for frames in range(11):
            dispStruct['rotatRoulette'][1].setImage(taskStruct['Dir']['Roulette'] + os.sep + "roulette"+str(frames)+".tiff") # recode here to store all animation frames in mem, then draw from mem
            dispStruct['rotatRoulette'][1].draw()
            dispStruct['screen'].flip()
    # once the reels stop spinning, show the reward
    dispStruct['contextRouletteFbTrial'][1].setAutoDraw(True)
    dispStruct['Instruct']['page35_text1'].setAutoDraw(True)
    dispStruct['Instruct']['textNav'].setAutoDraw(True)
    dispStruct['screen'].flip()
    # Clear screen for next instructions
    dispStruct['Instruct']['page35_head'].setAutoDraw(False)
    dispStruct['Instruct']['page35_text1'].setAutoDraw(False)
    dispStruct['Instruct']['textNav'].setAutoDraw(False)
    for lr in range(2):
        dispStruct['airportName'][lr].setAutoDraw(False)
        dispStruct['airportFlag'][lr].setAutoDraw(False)
        dispStruct['rouletteTrial'][lr].setAutoDraw(False)
    dispStruct['contextRouletteFbTrial'][1].setAutoDraw(False)
    return(dispStruct)

def Instructions_Casino_36(dispStruct,taskStruct):
    # Instruction header
    dispStruct['Instruct']['page36_head'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.09, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page36_head'].text = '--Instructions 36--'
    dispStruct['Instruct']['page36_head'].pos = [0,0.8]
    # Instruction text 1
    dispStruct['Instruct']['page36_text1'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page36_text1'].text = 'Occasionally you will be asked how you feel at the current moment.'
    dispStruct['Instruct']['page36_text1'].pos = [0,0.6]
    # Instruction text 2
    dispStruct['Instruct']['page36_text2'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page36_text2'].text = '(Please indicate that you are feeling "good" now.)'
    dispStruct['Instruct']['page36_text2'].pos = [0,0.5]
    # create a RatingScale object:
    dispStruct['Instruct']['page36_scaleQ'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page36_scaleQ'].text = 'How do you feel right now?'
    dispStruct['Instruct']['page36_scaleQ'].pos = [0,0]
    dispStruct['Instruct']['page36_scale'] = visual.RatingScale(dispStruct['screen'],choices=['very bad','bad','neutral','good','very good'],
        leftKeys=taskStruct['respKeyLeftName'],rightKeys=taskStruct['respKeyRightName'],marker='circle',markerStart=2,stretch=2,
        showAccept=True,acceptKeys=taskStruct['instrKeyNextName'],acceptSize=4,
        acceptPreText='Press ' + taskStruct['respKeyLeftName'] + ' to move left, or ' +  taskStruct['respKeyRightName'] + ' to move right',
        acceptText='Press ' + taskStruct['instrKeyNextName'] + ' to confirm your choice',
        noMouse=True,skipKeys=None,showValue=False,textColor='black',pos=[0,-0.6])
    # Draw page
    event.clearEvents()
    while dispStruct['Instruct']['page36_scale'].noResponse:
        dispStruct['Instruct']['page36_head'].draw()
        dispStruct['Instruct']['page36_text1'].draw()
        dispStruct['Instruct']['page36_text2'].draw()
        dispStruct['Instruct']['page36_scaleQ'].draw()
        dispStruct['Instruct']['page36_scale'].draw()
        dispStruct['screen'].flip()
    return(dispStruct)

def Instructions_Casino_37(dispStruct,taskStruct):
    # Instruction header
    dispStruct['Instruct']['page37_head'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.09, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page37_head'].text = '--Instructions 37--'
    dispStruct['Instruct']['page37_head'].pos = [0,0.8]
    # Instruction text 1
    dispStruct['Instruct']['page37_text1'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page37_text1'].text = 'As a reminder, you press ' + taskStruct['respKeyLeftName'] + ' to move left, or ' +  taskStruct['respKeyRightName'] + ' to move right.'
    dispStruct['Instruct']['page37_text1'].pos = [0,0.6]
    # Instruction text 2
    dispStruct['Instruct']['page37_text2'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page37_text2'].text = 'And then press ' + taskStruct['instrKeyNextName'] + ' to confirm your choice.'
    dispStruct['Instruct']['page37_text2'].pos = [0,0.5]
    # Instruction text 2
    dispStruct['Instruct']['page37_text3'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page37_text3'].text = '(Please indicate that you are feeling "bad" now.)'
    dispStruct['Instruct']['page37_text3'].pos = [0,0.3]
    # create a RatingScale object:
    dispStruct['Instruct']['page37_scaleQ'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page37_scaleQ'].text = 'How do you feel right now?'
    dispStruct['Instruct']['page37_scaleQ'].pos = [0,0]
    dispStruct['Instruct']['page37_scale'] = visual.RatingScale(dispStruct['screen'],choices=['very bad','bad','neutral','good','very good'],
        leftKeys=taskStruct['respKeyLeftName'],rightKeys=taskStruct['respKeyRightName'],marker='circle',markerStart=2,stretch=2,
        showAccept=True,acceptKeys=taskStruct['instrKeyNextName'],acceptSize=4,
        acceptPreText='Press ' + taskStruct['respKeyLeftName'] + ' to move left, or ' +  taskStruct['respKeyRightName'] + ' to move right',
        acceptText='Press ' + taskStruct['instrKeyNextName'] + ' to confirm your choice',
        noMouse=True,skipKeys=None,showValue=False,textColor='black',pos=[0,-0.6])
    # Draw page
    event.clearEvents()
    while dispStruct['Instruct']['page37_scale'].noResponse:
        dispStruct['Instruct']['page37_head'].draw()
        dispStruct['Instruct']['page37_text1'].draw()
        dispStruct['Instruct']['page37_text2'].draw()
        dispStruct['Instruct']['page37_text3'].draw()
        dispStruct['Instruct']['page37_scaleQ'].draw()
        dispStruct['Instruct']['page37_scale'].draw()
        dispStruct['screen'].flip()
    return(dispStruct)


def Instructions_Casino_38(dispStruct,taskStruct):
    # Instruction header
    dispStruct['Instruct']['page38_head'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.09, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page38_head'].text = '--Instructions 38--'
    dispStruct['Instruct']['page38_head'].pos = [0,0.8]
    # Instruction text 1
    dispStruct['Instruct']['page38_text1'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page38_text1'].text = 'At the end of the trip, you will be awarded actual money based upon the amount you earned throughout the trip.'
    dispStruct['Instruct']['page38_text1'].pos = [0,0.2]
    # Instruction text 2
    dispStruct['Instruct']['page38_text2'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page38_text3'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    if taskStruct['winAmount'] == '$1':
        dispStruct['Instruct']['page38_text2'].text = 'A random sampling of trials will be selected from throughout the experiment - you will get the actual outcomes of these trials.'
        dispStruct['Instruct']['page38_text3'].text = 'Thus, it is advantageous to treat all trials as if they could be selected to contribute to your final awarded amount!'
    else:
        dispStruct['Instruct']['page38_text2'].text = 'The points you get on every trial will be aggregated, converted to cash, and the final awarded amount will be based on that.'
        dispStruct['Instruct']['page38_text3'].text = 'All trials (except practice) will contribute to your final awarded amount!'
    dispStruct['Instruct']['page38_text2'].pos = [0,-0.2]
    dispStruct['Instruct']['page38_text3'].pos = [0,-0.6]
    # Draw page
    dispStruct['Instruct']['page38_head'].draw()
    dispStruct['Instruct']['page38_text1'].draw()
    dispStruct['Instruct']['page38_text2'].draw()
    dispStruct['Instruct']['page38_text3'].draw()
    dispStruct['Instruct']['textNav'].draw()
    dispStruct['screen'].flip()
    return(dispStruct)


def Instructions_Casino_39(dispStruct,taskStruct):
    # Instruction header
    dispStruct['Instruct']['page39_head'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.09, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page39_head'].text = '--Instructions 39--'
    dispStruct['Instruct']['page39_head'].pos = [0,0.8]
    # Instruction text 1
    dispStruct['Instruct']['page39_text1'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page39_text1'].text = 'On all trials where your points contribute to real money, you will see a status bar at the bottom of the screen:'
    dispStruct['Instruct']['page39_text1'].pos = [0,0.6]
    # Draw page
    dispStruct['Instruct']['page39_head'].draw()
    dispStruct['Instruct']['page39_text1'].draw()
    dispStruct['Instruct']['textNav'].draw()
    for lr in range(2):
        dispStruct['instructFlag'][lr].draw()
        dispStruct['instructStateName'][lr].draw()
        dispStruct['machine'][lr].draw()
        dispStruct['stimTrial'][lr].draw()
        dispStruct['slotsTrial'][lr].draw()
    dispStruct['pointsBar'].draw()
    dispStruct['instructBar'].draw()
    dispStruct['screen'].flip()
    return(dispStruct)

def Instructions_Casino_40(dispStruct,taskStruct):
    # Instruction header
    dispStruct['Instruct']['page40_head'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.09, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page40_head'].text = '--Instructions 40--'
    dispStruct['Instruct']['page40_head'].pos = [0,0.8]
    # Instruction text 1
    dispStruct['Instruct']['page40_text1'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page40_text1'].text = 'The grey bar indicates the amount of possible points in the game. Its length represents the maximum real money you can earn.'
    dispStruct['Instruct']['page40_text1'].pos = [0,0.6]
    # Draw page
    dispStruct['Instruct']['page40_head'].draw()
    dispStruct['Instruct']['page40_text1'].draw()
    dispStruct['Instruct']['textNav'].draw()
    for lr in range(2):
        dispStruct['instructFlag'][lr].draw()
        dispStruct['instructStateName'][lr].draw()
        dispStruct['machine'][lr].draw()
        dispStruct['stimTrial'][lr].draw()
        dispStruct['slotsTrial'][lr].draw()
    dispStruct['pointsBar'].draw()
    dispStruct['instructBar'].draw()
    dispStruct['screen'].flip()
    return(dispStruct)

def Instructions_Casino_41(dispStruct,taskStruct):
    # Instruction header
    dispStruct['Instruct']['page41_head'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.09, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page41_head'].text = '--Instructions 41--'
    dispStruct['Instruct']['page41_head'].pos = [0,0.8]
    # Instruction text 1
    dispStruct['Instruct']['page41_text1'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page41_text1'].text = 'The blue bar indicates the current amount of points you have.\nChoose the left machine now.'
    dispStruct['Instruct']['page41_text1'].pos = [0,0.6]
    # Draw page
    dispStruct['Instruct']['page41_head'].draw()
    dispStruct['Instruct']['page41_text1'].draw()
    dispStruct['Instruct']['textNav'].draw()
    for lr in range(2):
        dispStruct['instructFlag'][lr].draw()
        dispStruct['instructStateName'][lr].draw()
        dispStruct['machine'][lr].draw()
        dispStruct['stimTrial'][lr].draw()
        dispStruct['slotsTrial'][lr].draw()
    dispStruct['pointsBar'].draw()
    dispStruct['instructBar'].draw()
    dispStruct['screen'].flip()
    return(dispStruct)

def Instructions_Casino_42(dispStruct,taskStruct):
    # Instruction header
    dispStruct['Instruct']['page42_head'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.09, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page42_head'].text = '--Instructions 42--'
    dispStruct['Instruct']['page42_head'].pos = [0,0.8]
    # Instruction text 1
    dispStruct['Instruct']['page42_text1'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page42_text1'].text = 'The bar will update with a green amount if you win, indicating how many points you won.'
    dispStruct['Instruct']['page42_text1'].pos = [0,0.6]
    # Draw page
    dispStruct['Instruct']['page42_head'].setAutoDraw(True)
    dispStruct['Instruct']['page42_text1'].setAutoDraw(True)
    dispStruct['Instruct']['textNav'].setAutoDraw(True)
    for lr in range(2):
        dispStruct['instructFlag'][lr].setAutoDraw(True)
        dispStruct['instructStateName'][lr].setAutoDraw(True)
        dispStruct['machine'][lr].setAutoDraw(True)
        dispStruct['stimTrial'][lr].setAutoDraw(True)
        dispStruct['slotsTrial'][lr].setAutoDraw(True)
    dispStruct['pointsBar'].setAutoDraw(True)
    dispStruct['instructBar'].setAutoDraw(True)
    dispStruct['revolSlots'][0].setAutoDraw(True)
    instructClock = core.Clock()
    while instructClock.getTime() < 1.5:
        dispStruct['revolSlots'][0].phase += 0.3
        dispStruct['screen'].flip()
    dispStruct['revolSlots'][0].setAutoDraw(False)
    dispStruct['instructBar'].setAutoDraw(False)
    # once the reels stop spinning, show the reward
    dispStruct['fbTrial']['Win'].setAutoDraw(True)
    dispStruct['instructBarWin'].setAutoDraw(True)
    dispStruct['instructBar'].setAutoDraw(True)
    dispStruct['screen'].flip()
    # Clear screen for next instructions
    dispStruct['Instruct']['page42_head'].setAutoDraw(False)
    dispStruct['Instruct']['page42_text1'].setAutoDraw(False)
    dispStruct['Instruct']['textNav'].setAutoDraw(False)
    for lr in range(2):
        dispStruct['instructFlag'][lr].setAutoDraw(False)
        dispStruct['instructStateName'][lr].setAutoDraw(False)
        dispStruct['machine'][lr].setAutoDraw(False)
        dispStruct['stimTrial'][lr].setAutoDraw(False)
        dispStruct['slotsTrial'][lr].setAutoDraw(False)
    dispStruct['fbTrial']['Win'].setAutoDraw(False)
    dispStruct['pointsBar'].setAutoDraw(False)
    dispStruct['instructBarWin'].setAutoDraw(False)
    dispStruct['instructBar'].setAutoDraw(False)
    # Update instructions current points bar
    dispStruct['instructBarStartLength'] = dispStruct['instructBarWinLength']
    dispStruct['instructBarStartVert'] = [(dispStruct['pointsBarXLeft'],dispStruct['pointsBarYTop']),(dispStruct['instructBarStartLength'],dispStruct['pointsBarYTop']),(dispStruct['instructBarStartLength'],dispStruct['pointsBarYBottom']),(dispStruct['pointsBarXLeft'],dispStruct['pointsBarYBottom'])]
    dispStruct['instructBar'].vertices = dispStruct['instructBarStartVert']
    return(dispStruct)

def Instructions_Casino_43(dispStruct,taskStruct):
    # Instruction header
    dispStruct['Instruct']['page43_head'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.09, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page43_head'].text = '--Instructions 43--'
    dispStruct['Instruct']['page43_head'].pos = [0,0.8]
    # Instruction text 1
    dispStruct['Instruct']['page43_text1'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page43_text1'].text = 'You will see the points bar on roulette trials too.\nChoose the right roulette now.'
    dispStruct['Instruct']['page43_text1'].pos = [0,0.6]
    # Draw page
    dispStruct['Instruct']['page43_head'].draw()
    dispStruct['Instruct']['page43_text1'].draw()
    dispStruct['Instruct']['textNav'].draw()
    for lr in range(2):
        dispStruct['airportName'][lr].draw()
        dispStruct['airportFlag'][lr].draw()
        dispStruct['rouletteTrial'][lr].draw()
    dispStruct['pointsBar'].draw()
    dispStruct['instructBar'].draw()
    dispStruct['screen'].flip()
    return(dispStruct)


def Instructions_Casino_44(dispStruct,taskStruct):
    # Instruction header
    dispStruct['Instruct']['page44_head'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.09, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page44_head'].text = '--Instructions 44--'
    dispStruct['Instruct']['page44_head'].pos = [0,0.8]
    # Instruction text 2
    dispStruct['Instruct']['page44_text1'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page44_text1'].text = 'The bar will update with a red amount if you lose, indicating how many points you lost.'
    dispStruct['Instruct']['page44_text1'].pos = [0,0.5]
    # Draw page
    dispStruct['Instruct']['page44_head'].setAutoDraw(True)
    for lr in range(2):
        dispStruct['airportName'][lr].setAutoDraw(True)
        dispStruct['airportFlag'][lr].setAutoDraw(True)
        dispStruct['rouletteTrial'][lr].setAutoDraw(True)
    dispStruct['pointsBar'].setAutoDraw(True)
    dispStruct['instructBar'].setAutoDraw(True)
    dispStruct['rouletteTrial'][1].setAutoDraw(False)
    instructClock = core.Clock()
    while instructClock.getTime() < 1.5:
        for frames in range(11):
            dispStruct['rotatRoulette'][1].setImage(taskStruct['Dir']['Roulette'] + os.sep + "roulette"+str(frames)+".tiff") # recode here to store all animation frames in mem, then draw from mem
            dispStruct['rotatRoulette'][1].draw()
            dispStruct['screen'].flip()
     # once the reels stop spinning, show the outcome
    dispStruct['rouletteFbTrial'][1].setAutoDraw(True)
    dispStruct['Instruct']['page44_text1'].setAutoDraw(True)
    dispStruct['Instruct']['textNav'].setAutoDraw(True)
    # Show points bar
    dispStruct['instructBar'].setAutoDraw(False)
    dispStruct['instructBar'].lineColor = 'red'
    dispStruct['instructBar'].fillColor = 'red'
    dispStruct['instructBar'].setAutoDraw(True)
    dispStruct['instructBarLoss'].setAutoDraw(True)
    dispStruct['screen'].flip()
    # Clear screen for next instructions
    dispStruct['Instruct']['page44_head'].setAutoDraw(False)
    dispStruct['Instruct']['page44_text1'].setAutoDraw(False)
    dispStruct['Instruct']['textNav'].setAutoDraw(False)
    for lr in range(2):
        dispStruct['airportName'][lr].setAutoDraw(False)
        dispStruct['airportFlag'][lr].setAutoDraw(False)
        dispStruct['rouletteTrial'][lr].setAutoDraw(False)
    dispStruct['rouletteFbTrial'][1].setAutoDraw(False)
    dispStruct['pointsBar'].setAutoDraw(False)
    dispStruct['instructBar'].setAutoDraw(False)
    dispStruct['instructBarLoss'].setAutoDraw(False)
    # Update instructions current points bar
    dispStruct['instructBarStartLength'] = dispStruct['instructBarLossLength']
    dispStruct['instructBarStartVert'] = [(dispStruct['pointsBarXLeft'],dispStruct['pointsBarYTop']),(dispStruct['instructBarStartLength'],dispStruct['pointsBarYTop']),(dispStruct['instructBarStartLength'],dispStruct['pointsBarYBottom']),(dispStruct['pointsBarXLeft'],dispStruct['pointsBarYBottom'])]
    dispStruct['instructBar'].vertices=dispStruct['instructBarStartVert']
    dispStruct['instructBar'].lineColor = 'royalblue'
    dispStruct['instructBar'].fillColor = 'royalblue'
    return(dispStruct)

def Instructions_Casino_45(dispStruct,taskStruct):
    # Instruction header
    dispStruct['Instruct']['page45_head'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.09, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page45_head'].text = '--Instructions 45--'
    dispStruct['Instruct']['page45_head'].pos = [0,0.8]
    # Instruction text 1
    dispStruct['Instruct']['page45_text1'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page45_text1'].text = 'Do your best to win as much as you can on each day. Good luck!'
    dispStruct['Instruct']['page45_text1'].pos = [0,0.2]
    # Instruction text 2
    dispStruct['Instruct']['page45_text2'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page45_text2'].text = 'If anything is unclear, please ask the experimenter to clarify.'
    dispStruct['Instruct']['page45_text2'].pos = [0,-0.2]
    # Draw page
    dispStruct['Instruct']['page45_head'].draw()
    dispStruct['Instruct']['page45_text1'].draw()
    dispStruct['Instruct']['page45_text2'].draw()
    dispStruct['Instruct']['textNav'].draw()
    dispStruct['screen'].flip()
    return(dispStruct)

def Instructions_Casino_46(dispStruct,taskStruct):
    # Instruction header
    dispStruct['Instruct']['page46_head'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.09, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page46_head'].text = '--Instructions 46--'
    dispStruct['Instruct']['page46_head'].pos = [0,0.8]
    # Instruction text
    dispStruct['Instruct']['page46_text1'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page46_text1'].text = 'You will get to take a break every 10 minutes.'
    dispStruct['Instruct']['page46_text1'].pos = [0,0.2]
    # Instruction text
    dispStruct['Instruct']['page46_text2'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page46_text2'].text = 'Please take that time to rest your eyes and relax.'
    dispStruct['Instruct']['page46_text2'].pos = [0,-0.2]
    # Draw page
    dispStruct['Instruct']['page46_head'].draw()
    dispStruct['Instruct']['page46_text1'].draw()
    dispStruct['Instruct']['page46_text2'].draw()
    dispStruct['Instruct']['textNav'].draw()
    dispStruct['screen'].flip()
    return(dispStruct)

def Instructions_Casino_47(dispStruct,taskStruct):
    # Instruction header
    dispStruct['Instruct']['page47_head'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.09, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['page47_head'].text = '--Instructions 47--'
    dispStruct['Instruct']['page47_head'].pos = [0,0.8]
    # Instruction done
    dispStruct['Instruct']['done'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['done'].text = 'Otherwise, please let the experimeter know you are ready to begin.'
    dispStruct['Instruct']['done'].pos = [0,0]
    # Draw page
    dispStruct['Instruct']['page47_head'].draw()
    dispStruct['Instruct']['done'].draw()
    dispStruct['screen'].flip()
    return(dispStruct)



def errRestart(dispStruct):
    # Tell them their response was wrong
    dispStruct['Instruct']['asleep'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.14, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['asleep'].text = 'Oops! Please pay attention!'
    dispStruct['Instruct']['asleep'].pos = [0,0.2]
    # Starting back at page 1
    dispStruct['Instruct']['restart'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['restart'].text = "Let's review the relevant material again..."
    dispStruct['Instruct']['restart'].pos = [0,-0.4]
    # Draw error screen
    dispStruct['Instruct']['asleep'].draw()
    dispStruct['Instruct']['restart'].draw()
    dispStruct['screen'].flip()
    core.wait(2)
    return(dispStruct)

def errWarning(dispStruct):
    # Tell them their response was wrong
    dispStruct['Instruct']['warning'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.14, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['Instruct']['warning'].text = 'Oops! Please try again!'
    dispStruct['Instruct']['warning'].pos = [0,0.2]
    # Draw error screen
    dispStruct['Instruct']['warning'].draw()
    dispStruct['screen'].flip()
    core.wait(2)
    return(dispStruct)

# Extra functions required locally
def feval(defName, *args):
    return eval(defName)(*args)