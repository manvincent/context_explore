from copy import deepcopy as dcopy
from config import *
import numpy as np

# within-sessio clean data
def cleanDataSession(taskStruct,dispInfo,keyStruct,sI):
    outPack = dict()
    outPack['Task'] = dict()
    outPack['Display'] = dict()
    outPack['Keys'] = dict()
    # Package taskStruct
    for bI in range(taskStruct['blocksPerSession']):
        # delete blockwise image caches
        del taskStruct['sessions'][sI]['blocks'][bI]['imageCache']
    outPack['Task'] = dcopy(taskStruct)
    # Package keyStruct
    outPack['Keys'] = dcopy(keyStruct)
    # Package dispInfo
    outPack['Display'] = dcopy(dispInfo)
    return(outPack)

# within-session convert mat
def convertMatSession(outPack,sI):
    matOut = dict()
    taskStruct = outPack['Task']
    # Package taskStruct
    sessionStack = np.empty(1,dtype=np.object)
    sessionInfoStartStack = np.empty(1,dtype=np.object)
    sessionInfoEndStack = np.empty(1,dtype=np.object)    
    for sI in range(1):
        blockStack =np.empty((taskStruct['blocksPerSession'],),dtype=np.object)
        for bI in range(taskStruct['blocksPerSession']):
            # Stack blocks into numpy object
            blockStack[bI] = taskStruct['sessions'][sI]['blocks'][bI]      
        # Wrap up blocks
        taskStruct['sessions'][sI]['blocks'] = blockStack
        # stack sessions into numpy object
        sessionStack[sI] = taskStruct['sessions'][sI]['blocks']
        sessionInfoStartStack[sI] = taskStruct['sessionInfo']['startTime'][sI]
        sessionInfoEndStack[sI] =  taskStruct['sessionInfo']['endTime'][sI]
    # Save it
    matOut = dcopy(taskStruct)
    return(matOut)

# whole task pack data
def cleanData(taskStruct,dispInfo,keyStruct,startSession,Mode):
    outPack = dict()
    outPack['Task'] = dict()
    outPack['Display'] = dict()
    outPack['Keys'] = dict()
    # Package taskStruct
    if Mode == 'Practice':
        for sI in startSession:
            for bI in range(taskStruct['blocksPerSessionPract']):
                # delete blockwise image caches
                if 'imageCache' in taskStruct['practSession'][sI]['practBlocks'][bI].keys():
                    del taskStruct['practSession'][sI]['practBlocks'][bI]['imageCache']
    elif Mode == 'Task':
        for sI in startSession:
            for bI in range(taskStruct['blocksPerSession']):
                # delete blockwise image caches
                if 'imageCache' in taskStruct['sessions'][sI]['blocks'][bI].keys():
                    del taskStruct['sessions'][sI]['blocks'][bI]['imageCache']
    outPack['Task'] = dcopy(taskStruct)
    # Package keyStruct
    outPack['Keys'] = dcopy(keyStruct)
    # Package dispInfo
    outPack['Display'] = dcopy(dispInfo)
    return(outPack)
    
# whole-task convert mat
def convertMat(outPack,startSession,Mode):
    matOut = dict()
    taskStruct = outPack['Task']
    if Mode == 'Practice':
        # Package taskStruct
        sessionStack = np.empty((len(startSession),),dtype=np.object)
        for sI in startSession:
            blockStack =np.empty((taskStruct['blocksPerSessionPract'],),dtype=np.object)
            for bI in range(taskStruct['blocksPerSessionPract']):
                # Stack blocks into numpy object
                blockStack[bI] = taskStruct['practSession'][sI]['practBlocks'][bI]      
            # Wrap up blocks
            taskStruct['practSession'][sI]['practBlocks'] = blockStack
            # stack sessions into numpy object
            sessionStack[sI] = taskStruct['practSession'][sI]['practBlocks']
        # Wrap up sessions
        taskStruct['practSession'] = sessionStack
    elif Mode == 'Task':
        # Package taskStruct
        sessionStack = np.empty((len(startSession),),dtype=np.object)
        sessionInfoStartStack = np.empty((len(startSession),),dtype=np.object)
        sessionInfoEndStack = np.empty((len(startSession),),dtype=np.object)
        for sI in startSession:
            blockStack =np.empty((taskStruct['blocksPerSession'],),dtype=np.object)
            for bI in range(taskStruct['blocksPerSession']):
                # Stack blocks into numpy object
                blockStack[bI] = taskStruct['sessions'][sI]['blocks'][bI]      
            # Wrap up blocks
            taskStruct['sessions'][sI]['blocks'] = blockStack
            # stack sessions into numpy object
            sessionStack[sI] = taskStruct['sessions'][sI]['blocks']
            sessionInfoStartStack[sI] = taskStruct['sessionInfo']['startTime'][sI]
            sessionInfoEndStack[sI] =  taskStruct['sessionInfo']['endTime'][sI]
        # Wrap up sessions
        taskStruct['sessions'] = sessionStack  
    # Save it
    matOut = dcopy(taskStruct)
    return(matOut)


# remove image cache from memory structure
def cleanDataMemory(memStruct):
    memPack = dict()
    # Package taskStruct
    # delete blockwise image caches
    if 'memImageCache' in memStruct.keys():
        del memStruct['memImageCache']
    memPack['MemoryTask'] = dcopy(memStruct)
    return(memPack)
    



