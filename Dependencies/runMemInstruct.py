from psychopy import visual, gui, data, core, event, logging, info
from psychopy.constants import * 
import numpy as np # whole numpy lib is available, prepend 'np.'
import os
from config import *

def runMemInstruct(dispStruct,keyStruct,taskStruct,expInfo):
    pages = range(13)
    # Set up instruction display dictionary 
    dispStruct['MemInstruct'] = dict()
    # Initialize instruction keys and display 
    dispStruct = initMemInstDisplay(dispStruct,keyStruct,taskStruct)
    currPage = 1
    while True:
        # Run instruction function
        dispStruct = feval('MemInstructions_Casino_' + str(currPage),dispStruct,taskStruct)
        # wait for response
        if currPage == 7:
            response = event.waitKeys(keyList=[keyStruct['respKeyLeft'],keyStruct['respKeyRight'],'escape'])
            if expInfo['sub_cb'] == 1:
                if keyStruct['respKeyRight'] in response:
                    dispStruct = memFB(dispStruct)
                    # Move forward a screen
                    currPage = min(len(pages), currPage+1)
                    print "Page " + str(currPage)
            elif expInfo['sub_cb'] == 2:
                if keyStruct['respKeyLeft'] in response:
                    dispStruct = memFB(dispStruct)
                    # Move forward a screen
                    currPage = min(len(pages), currPage+1)
                    print "Page " + str(currPage)
        elif currPage == 8:
            response = event.waitKeys(keyList=[keyStruct['respKeyLeft'],keyStruct['respKeyRight'],'escape'])
            if expInfo['sub_cb'] == 1:
                if keyStruct['respKeyLeft'] in response:
                    dispStruct = memFB(dispStruct)
                    # Move forward a screen
                    currPage = min(len(pages), currPage+1)
                    print "Page " + str(currPage)
            elif expInfo['sub_cb'] == 2:
                if keyStruct['respKeyRight'] in response:
                    dispStruct = memFB(dispStruct)
                    # Move forward a screen
                    currPage = min(len(pages), currPage+1)
                    print "Page " + str(currPage)
        elif currPage == 10:
            response = event.waitKeys(keyList=([taskStruct['respKeyLeftName'],taskStruct['instrKeyPrevName'],taskStruct['instrKeyNextName'],taskStruct['respKeyRightName'],'escape']))
            if expInfo['sub_cb'] == 1:
                if keyStruct['respKeyLeft'] in response:
                    dispStruct = memFB(dispStruct)
                    # Move forward a screen
                    currPage = min(len(pages), currPage+1)
                    print "Page " + str(currPage)
            elif expInfo['sub_cb'] == 2:
                if keyStruct['respKeyRight'] in response:
                    dispStruct = memFB(dispStruct)
                    # Move forward a screen
                    currPage = min(len(pages), currPage+1)
                    print "Page " + str(currPage)
        elif currPage == 11:
            response = event.waitKeys(keyList=[keyStruct['respKeyLeft'],keyStruct['respKeyRight'],'escape'])
            if expInfo['sub_cb'] == 1:
                if keyStruct['respKeyRight'] in response:
                    dispStruct = memFB(dispStruct)
                    # Move forward a screen
                    currPage = min(len(pages), currPage+1)
                    print "Page " + str(currPage)
            elif expInfo['sub_cb'] == 2:
                if keyStruct['respKeyLeft'] in response:
                    dispStruct = memFB(dispStruct)
                    # Move forward a screen
                    currPage = min(len(pages), currPage+1)
                    print "Page " + str(currPage)
        elif currPage == 12:
            response = event.waitKeys(keyList=([taskStruct['respKeyLeftName'],taskStruct['instrKeyPrevName'],taskStruct['instrKeyNextName'],taskStruct['respKeyRightName'],'escape']))
            if expInfo['sub_cb'] == 1:
                if taskStruct['instrKeyNextName'] in response:
                    dispStruct = memFB(dispStruct)
                    # Move forward a screen
                    currPage = min(len(pages), currPage+1)
                    print "Page " + str(currPage)
            elif expInfo['sub_cb'] == 2:
                if taskStruct['instrKeyPrevName'] in response:
                    dispStruct = memFB(dispStruct)
                    # Move forward a screen
                    currPage = min(len(pages), currPage+1)
                    print "Page " + str(currPage)
        elif currPage == len(pages):
            response = event.waitKeys(keyList=keyStruct['instrKeyDone'])
            if keyStruct['instrKeyDone'] in response:
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
def initMemInstDisplay(dispStruct,keyStruct,taskStruct):
    # Instruction text nav
    dispStruct['MemInstruct']['textNav'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.05, font = dispStruct['textFont'], wrapWidth = 1.8)
    dispStruct['MemInstruct']['textNav'].text = 'Navigate through the instructions with the "' + taskStruct['instrKeyPrevName'] + '" (previous) and "' + taskStruct['instrKeyNextName'] + '" (next) keys'
    dispStruct['MemInstruct']['textNav'].pos = [0,-0.9]
    # Look at practice set and randomly choose one of the old stim IDs (familiarity > 0)
    practOldIDSet = taskStruct['practStimID'][np.where(taskStruct['practFamiliarity'] > 0)[0]]
    practOldID = np.random.choice(practOldIDSet,size=1,replace=False)[0]
    # Look at practice set and identify the new stim ID (familiarity = 0)
    practNewIDSet = taskStruct['practStimID'][np.where(taskStruct['practFamiliarity'] == 0)[0]]
    practNewID =  np.random.choice(practNewIDSet,size=1,replace=False)[0]
    # Initialize a sample memory stim for the instruction set 
    dispStruct['iMemStimOld'] = visual.ImageStim(dispStruct['screen'])
    dispStruct['iMemStimOld'].setImage(taskStruct['Dir']['StimCues'] + os.sep + "p" + str(practOldID) + ".bmp")
    dispStruct['iMemStimOld'].rescaledSize = rescaleStim(dispStruct['iMemStimOld'],dispStruct['memStimSize'],dispStruct)
    dispStruct['iMemStimOld'].setSize(dispStruct['iMemStimOld'].rescaledSize)
    dispStruct['iMemStimOld'].pos = dispStruct['memStimPos']
    # Initialize another sample memory stim for the instruction set 
    dispStruct['iMemStimNew'] = visual.ImageStim(dispStruct['screen'])
    dispStruct['iMemStimNew'].setImage(taskStruct['Dir']['StimCues'] + os.sep + "p" + str(practNewID) + ".bmp")
    dispStruct['iMemStimNew'].rescaledSize = rescaleStim(dispStruct['iMemStimNew'],dispStruct['memStimSize'],dispStruct)
    dispStruct['iMemStimNew'].setSize(dispStruct['iMemStimNew'].rescaledSize)
    dispStruct['iMemStimNew'].pos = dispStruct['memStimPos']
    return(dispStruct)

def MemInstructions_Casino_1(dispStruct,taskStruct):
    # Instruction header 
    dispStruct['MemInstruct']['page1_head'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.09, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['MemInstruct']['page1_head'].text = '--Instructions 1--'
    dispStruct['MemInstruct']['page1_head'].pos = [0,0.8]
    # Instruction text 1
    dispStruct['MemInstruct']['page1_text1'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['MemInstruct']['page1_text1'].text = 'Now we would like to ask you whether you remember seeing specific machines or not.'
    dispStruct['MemInstruct']['page1_text1'].pos = [0,0.2]
    # Draw page
    dispStruct['MemInstruct']['page1_head'].draw()
    dispStruct['MemInstruct']['page1_text1'].draw()
    dispStruct['MemInstruct']['textNav'].draw()
    dispStruct['screen'].flip()
    return(dispStruct)


def MemInstructions_Casino_2(dispStruct,taskStruct):
    # Instruction header 
    dispStruct['MemInstruct']['page2_head'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.09, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['MemInstruct']['page2_head'].text = '--Instructions 2--'
    dispStruct['MemInstruct']['page2_head'].pos = [0,0.8]
    # Instruction text 1
    dispStruct['MemInstruct']['page2_text1'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['MemInstruct']['page2_text1'].text = 'You will see a number of different slot machines, one at a time.'
    dispStruct['MemInstruct']['page2_text1'].pos = [0,0.2]
    # Instruction text 2
    dispStruct['MemInstruct']['page2_text2'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['MemInstruct']['page2_text2'].text = "You will be asked if that is an old machine that you've seen before, or a new one that you have not seen before."
    dispStruct['MemInstruct']['page2_text2'].pos = [0,-0.2]
    # Draw page 
    dispStruct['MemInstruct']['page2_head'].draw()
    dispStruct['MemInstruct']['page2_text1'].draw()
    dispStruct['MemInstruct']['textNav'].draw()      
    dispStruct['screen'].flip()
    return(dispStruct)

def MemInstructions_Casino_3(dispStruct,taskStruct):
    # Instruction header 
    dispStruct['MemInstruct']['page3_head'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.09, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['MemInstruct']['page3_head'].text = '--Instructions 3--'
    dispStruct['MemInstruct']['page3_head'].pos = [0,0.8]
    # Instruction text 1
    dispStruct['MemInstruct']['page3_text1'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['MemInstruct']['page3_text1'].text = 'You will also be asked how sure you are of your choice.'
    dispStruct['MemInstruct']['page3_text1'].pos = [0,0.2]
    # Draw page 
    dispStruct['MemInstruct']['page3_head'].draw()
    dispStruct['MemInstruct']['page3_text1'].draw()
    dispStruct['MemInstruct']['textNav'].draw()
    dispStruct['screen'].flip()
    return(dispStruct)

def MemInstructions_Casino_4(dispStruct,taskStruct):
    # Instruction header 
    dispStruct['MemInstruct']['page4_head'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.09, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['MemInstruct']['page4_head'].text = '--Instructions 4--'
    dispStruct['MemInstruct']['page4_head'].pos = [0,0.8]
    # Instruction text 1
    dispStruct['MemInstruct']['page4_text1'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['MemInstruct']['page4_text1'].text = 'This is what you will see:'
    dispStruct['MemInstruct']['page4_text1'].pos = [0,0.6]
    # Draw page 
    dispStruct['MemInstruct']['page4_head'].draw()
    dispStruct['MemInstruct']['page4_text1'].draw()
    dispStruct['MemInstruct']['textNav'].draw()
    dispStruct['memMachine'].setAutoDraw(True)
    dispStruct['memMachineSlots'].setAutoDraw(True)
    dispStruct['iMemStimOld'].setAutoDraw(True)
    dispStruct['screen'].flip()
    return(dispStruct)

def MemInstructions_Casino_5(dispStruct,taskStruct):
    # Instruction header 
    dispStruct['MemInstruct']['page5_head'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.09, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['MemInstruct']['page5_head'].text = '--Instructions 5--'
    dispStruct['MemInstruct']['page5_head'].pos = [0,0.8]
    # Instruction text 1
    dispStruct['MemInstruct']['page5_text1'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['MemInstruct']['page5_text1'].text = 'First, you will see a slot machine and be asked if you remember seeing that machine anytime during your gambling trip.'
    dispStruct['MemInstruct']['page5_text1'].pos = [0,0.6]
    # Draw page 
    dispStruct['MemInstruct']['page5_head'].draw()
    dispStruct['MemInstruct']['page5_text1'].draw()
    dispStruct['MemInstruct']['textNav'].draw()
    dispStruct['memMachine'].setAutoDraw(True)
    dispStruct['memMachineSlots'].setAutoDraw(True)
    dispStruct['iMemStimOld'].setAutoDraw(True)
    dispStruct['screen'].flip()
    return(dispStruct)

def MemInstructions_Casino_6(dispStruct,taskStruct):
    dispStruct['OldNewScaleQ'].reset()
    # Instruction header 
    dispStruct['MemInstruct']['page6_head'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.09, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['MemInstruct']['page6_head'].text = '--Instructions 6--'
    dispStruct['MemInstruct']['page6_head'].pos = [0,0.8]
    # Instruction text 1
    dispStruct['MemInstruct']['page6_text1'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['MemInstruct']['page6_text1'].text = 'Press ' + taskStruct['respKeyLeftName'] + ' to select the option on the left, or ' +  taskStruct['respKeyRightName'] + ' to select the option on the right.'
    dispStruct['MemInstruct']['page6_text1'].pos = [0,0.6]
    # Draw page 
    dispStruct['MemInstruct']['page6_head'].draw()
    dispStruct['MemInstruct']['page6_text1'].draw()
    dispStruct['MemInstruct']['textNav'].draw()
    dispStruct['memMachine'].setAutoDraw(True)
    dispStruct['memMachineSlots'].setAutoDraw(True)
    dispStruct['iMemStimOld'].setAutoDraw(True)
    dispStruct['OldNewScaleQ'].setAutoDraw(True)
    dispStruct['screen'].flip()
    return(dispStruct)

def MemInstructions_Casino_7(dispStruct,taskStruct):
    dispStruct['OldNewScaleQ'].reset()
    # Instruction header 
    dispStruct['MemInstruct']['page7_head'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.09, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['MemInstruct']['page7_head'].text = '--Instructions 7--'
    dispStruct['MemInstruct']['page7_head'].pos = [0,0.8]
    # Instruction text 1
    dispStruct['MemInstruct']['page7_text1'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['MemInstruct']['page7_text1'].text = "Select 'Old' if you have seen this machine in any of the casinos. Please select 'Old' now."
    dispStruct['MemInstruct']['page7_text1'].pos = [0,0.6]
    # Draw page 
    dispStruct['MemInstruct']['page7_head'].draw()
    dispStruct['MemInstruct']['page7_text1'].draw()
    dispStruct['memMachine'].setAutoDraw(True)
    dispStruct['memMachineSlots'].setAutoDraw(True)
    dispStruct['iMemStimOld'].setAutoDraw(True)
    dispStruct['OldNewScaleQ'].setAutoDraw(True)
    dispStruct['OldNewScaleKeys'].setAutoDraw(True)
    dispStruct['screen'].flip()
    return(dispStruct)

def MemInstructions_Casino_8(dispStruct,taskStruct):
    dispStruct['OldNewScaleQ'].reset()
    # Instruction header 
    dispStruct['MemInstruct']['page8_head'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.09, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['MemInstruct']['page8_head'].text = '--Instructions 8--'
    dispStruct['MemInstruct']['page8_head'].pos = [0,0.8]
    # Instruction text 1
    dispStruct['MemInstruct']['page8_text1'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['MemInstruct']['page8_text1'].text = "Select 'New' if you have never seen this machine. Please select 'New' now."
    dispStruct['MemInstruct']['page8_text1'].pos = [0,0.6]
    # Draw page 
    dispStruct['MemInstruct']['page8_head'].draw()
    dispStruct['MemInstruct']['page8_text1'].draw()
    dispStruct['memMachine'].setAutoDraw(True)
    dispStruct['memMachineSlots'].setAutoDraw(True)
    dispStruct['iMemStimNew'].setAutoDraw(True)
    dispStruct['OldNewScaleQ'].setAutoDraw(True)
    dispStruct['OldNewScaleKeys'].setAutoDraw(True)
    dispStruct['screen'].flip()
    return(dispStruct)

def MemInstructions_Casino_9(dispStruct,taskStruct):
    dispStruct['ConfScaleQ'].reset()
    # Instruction header 
    dispStruct['MemInstruct']['page9_head'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.09, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['MemInstruct']['page9_head'].text = '--Instructions 9--'
    dispStruct['MemInstruct']['page9_head'].pos = [0,0.8]
    # Instruction text 1
    dispStruct['MemInstruct']['page9_text1'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['MemInstruct']['page9_text1'].text = 'Then you will be asked how sure you are of your choice.'
    dispStruct['MemInstruct']['page9_text1'].pos = [0,0.6]
    # Instruction text 1
    dispStruct['MemInstruct']['page9_text2'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['MemInstruct']['page9_text2'].text = dispStruct['ConfScaleKeys'].text
    dispStruct['MemInstruct']['page9_text2'].pos = [0,0.5]
    # Draw page 
    dispStruct['MemInstruct']['page9_head'].draw()
    dispStruct['MemInstruct']['page9_text1'].draw()
    dispStruct['MemInstruct']['textNav'].draw()
    dispStruct['memMachine'].draw()
    dispStruct['memMachineSlots'].draw()
    dispStruct['iMemStimNew'].draw()
    dispStruct['ConfScaleQ'].draw()
    dispStruct['ConfScale'].draw()  
    dispStruct['screen'].flip()
    return(dispStruct)

def MemInstructions_Casino_10(dispStruct,taskStruct):
    dispStruct['ConfScaleQ'].reset()
    # Instruction header 
    dispStruct['MemInstruct']['page10_head'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.09, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['MemInstruct']['page10_head'].text = '--Instructions 10--'
    dispStruct['MemInstruct']['page10_head'].pos = [0,0.8]
    # Instruction text 1
    dispStruct['MemInstruct']['page10_text1'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['MemInstruct']['page10_text1'].text = 'Please indicate now that you are SURE it was a NEW machine.'
    dispStruct['MemInstruct']['page10_text1'].pos = [0,0.6]
    # Draw page 
    dispStruct['MemInstruct']['page10_head'].draw()
    dispStruct['MemInstruct']['page10_text1'].draw()
    dispStruct['memMachine'].setAutoDraw(True)
    dispStruct['memMachineSlots'].setAutoDraw(True)
    dispStruct['iMemStimNew'].setAutoDraw(True)
    dispStruct['ConfScaleQ'].setAutoDraw(True)
    dispStruct['ConfScale'].setAutoDraw(True)  
    dispStruct['ConfScaleKeys'].setAutoDraw(True)
    dispStruct['screen'].flip()
    return(dispStruct)

def MemInstructions_Casino_11(dispStruct,taskStruct):
    dispStruct['OldNewScaleQ'].reset()
    # Instruction header 
    dispStruct['MemInstruct']['page11_head'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.09, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['MemInstruct']['page11_head'].text = '--Instructions 11--'
    dispStruct['MemInstruct']['page11_head'].pos = [0,0.8]
    # Instruction text 1
    dispStruct['MemInstruct']['page11_text1'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['MemInstruct']['page11_text1'].text = "Here is a machine that you have seen before again. Again, please indicate that it is 'old'."
    dispStruct['MemInstruct']['page11_text1'].pos = [0,0.6]
    # Draw page 
    dispStruct['MemInstruct']['page11_head'].draw()
    dispStruct['MemInstruct']['page11_text1'].draw()
    dispStruct['memMachine'].setAutoDraw(True)
    dispStruct['memMachineSlots'].setAutoDraw(True)
    dispStruct['iMemStimOld'].setAutoDraw(True)
    dispStruct['OldNewScaleQ'].setAutoDraw(True)
    dispStruct['OldNewScaleKeys'].setAutoDraw(True)
    dispStruct['screen'].flip()
    return(dispStruct)

def MemInstructions_Casino_12(dispStruct,taskStruct):
    dispStruct['ConfScaleQ'].reset()
    # Instruction header 
    dispStruct['MemInstruct']['page12_head'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.09, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['MemInstruct']['page12_head'].text = '--Instructions 12--'
    dispStruct['MemInstruct']['page12_head'].pos = [0,0.8]
    # Instruction text 2
    dispStruct['MemInstruct']['page12_text1'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['MemInstruct']['page12_text1'].text = 'Please indicate now that you are NOT SURE it was an OLD machine.'
    dispStruct['MemInstruct']['page12_text1'].pos = [0,0.6]
    # Draw page 
    dispStruct['MemInstruct']['page12_head'].draw()
    dispStruct['MemInstruct']['page12_text1'].draw()
    dispStruct['memMachine'].setAutoDraw(True)
    dispStruct['memMachineSlots'].setAutoDraw(True)
    dispStruct['iMemStimOld'].setAutoDraw(True)
    dispStruct['ConfScaleQ'].setAutoDraw(True)
    dispStruct['ConfScale'].setAutoDraw(True)
    dispStruct['ConfScaleKeys'].setAutoDraw(True)
    dispStruct['screen'].flip()
    return(dispStruct)

def MemInstructions_Casino_13(dispStruct,taskStruct):
    # Instruction header 
    dispStruct['MemInstruct']['page13_head'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.09, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['MemInstruct']['page13_head'].text = '--Instructions 13--'
    dispStruct['MemInstruct']['page13_head'].pos = [0,0.8]
    # Instruction text 2
    dispStruct['MemInstruct']['page13_text1'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['MemInstruct']['page13_text1'].text = 'Respond as quickly and as accurately as you can.'
    dispStruct['MemInstruct']['page13_text1'].pos = [0,0.4]
    # Instruction text 3
    dispStruct['MemInstruct']['page13_text2'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['MemInstruct']['page13_text2'].text = 'Please ask the experimenter if anything is unclear now.'
    dispStruct['MemInstruct']['page13_text2'].pos = [0,0]
    # Instruction text 4
    dispStruct['MemInstruct']['page13_text3'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.07, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['MemInstruct']['page13_text3'].text = 'Otherwise let the experimenter know you are ready to begin.'
    dispStruct['MemInstruct']['page13_text3'].pos = [0,-0.4]    
    # Draw page 
    dispStruct['MemInstruct']['page13_head'].draw()
    dispStruct['MemInstruct']['page13_text1'].draw()
    dispStruct['MemInstruct']['page13_text2'].draw()
    dispStruct['MemInstruct']['page13_text3'].draw()    
    dispStruct['screen'].flip()
    return(dispStruct)

def memFB(dispStruct):
    # Draw feedback:
    dispStruct['memFB'].draw()
    dispStruct['OldNewScaleQ'].setAutoDraw(False)
    dispStruct['OldNewScaleKeys'].setAutoDraw(False)
    dispStruct['ConfScaleQ'].setAutoDraw(False)
    dispStruct['ConfScale'].setAutoDraw(False)
    dispStruct['ConfScaleKeys'].setAutoDraw(False)
    dispStruct['screen'].flip()
    core.wait(0.5)
    # Stop drawing screen
    dispStruct['memMachine'].setAutoDraw(False)
    dispStruct['memMachineSlots'].setAutoDraw(False)
    dispStruct['iMemStimOld'].setAutoDraw(False)
    dispStruct['iMemStimNew'].setAutoDraw(False)
    return(dispStruct)

def errWarning(dispStruct):
    # Tell them their response was wrong
    dispStruct['MemInstruct']['warning'] = visual.TextStim(dispStruct['screen'], color = 'black', height =0.14, font = dispStruct['textFont'], wrapWidth = 1.8, alignHoriz='center')
    dispStruct['MemInstruct']['warning'].text = 'Oops! Please try again!'
    dispStruct['MemInstruct']['warning'].pos = [0,0.2]
    # Draw error screen
    dispStruct['MemInstruct']['warning'].draw()
    dispStruct['screen'].flip()
    core.wait(2)
    return(dispStruct)

# Extra functions required locally
def feval(defName, *args):
    return eval(defName)(*args)