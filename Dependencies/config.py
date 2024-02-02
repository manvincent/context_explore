from __future__ import division
from PIL import Image
import pickle
import os
from copy import deepcopy as dcopy

def save_obj(obj, name ):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name ):
    with open(name, 'rb') as f:
        return pickle.load(f)


def keyConfig(taskStruct):
    keyStruct = dict()
    # input information - define keycodes (according to pyglet backend)
    keyStruct['pulseKeyCode'] = '5'
    keyStruct['respKeyRight'] = '4'
    taskStruct['respKeyRightName'] = keyStruct['respKeyRight']
    keyStruct['respKeyLeft'] = '1'
    taskStruct['respKeyLeftName'] = keyStruct['respKeyLeft']
    # stimuli are drawn from left to right, so index left as 0
    keyStruct['respLeftID'] = 0
    keyStruct['respRightID'] = 1
    # confidence lock keys
    keyStruct['respKeyConf'] = '7'
    taskStruct['respKeyConfName'] = keyStruct['respKeyConf']
    # Instruction set allowable keys
    keyStruct['instrKeyPrev'] ='2'
    taskStruct['instrKeyPrevName'] = keyStruct['instrKeyPrev']
    keyStruct['instrKeyNext'] = '3'
    taskStruct['instrKeyNextName'] = keyStruct['instrKeyNext']
    keyStruct['instrKeyDone'] = 'space'
    keyStruct['instrAllowable'] = [keyStruct['instrKeyPrev'],keyStruct['instrKeyNext'],'escape']
    # Convert custom mutable to dictionary object
    return(keyStruct,taskStruct)

# Set up functions used here

def counterbalance(expInfo):
    if is_odd(expInfo['SubNo']):
        expInfo['sub_cb'] = 1
    elif not is_odd(expInfo['SubNo']):
        expInfo['sub_cb'] = 2
    else:
        print "Error! Did not specify subject number correctly!"
        core.wait(3)
        core.quit()

    return expInfo

def is_odd(num):
   return num % 2 != 0

def rescaleStim(imageObj, normScale,dispStruct):
    # get raw image dimensions
    with Image.open(imageObj.image) as im:
        imSize = im.size
    # convert to 'norm' scale
    normSize = pix2norm(imSize,dispStruct)
    # resize according to input
    rescaledSize = [normSize[0]*normScale,normSize[1]*normScale]
    return rescaledSize

def rescale(image, normScale):
    scale = normScale
    imageRatio = image.size[1] / image.size[0]
    rescaledSize = (scale, scale*imageRatio)
    return rescaledSize

def pix2norm(sizePix,dispStruct):
    normX = (2.0*sizePix[0]/dispStruct['monitorX'])*dispStruct['screenScaling']
    normY = (2.0*sizePix[1]/dispStruct['monitorY'])*dispStruct['screenScaling']
    return [normX,normY]

# Reloading function
def reloadInit(taskStruct,homeDir,expInfo):
    del taskStruct
    taskStruct = load_obj(homeDir + os.sep + 'Output' + os.sep + 'Supplementary' + os.sep + 'Inits' + os.sep + str(expInfo['SubNo']) + '_Init.pkl')
    return(taskStruct)

def reloadPrevSess(taskStruct,homeDir,expInfo):
    del taskStruct
    taskStruct = load_obj(homeDir + os.sep + 'Output' + os.sep + 'Task' + os.sep + 'Sessions' + os.sep + str(expInfo['SubNo']) + '_Data_sess' + str(int(expInfo['Starting Run']) - 1) + '.pkl')
    return(taskStruct)

def reloadMemInstruct(taskStruct,homeDir,expInfo):
    del taskStruct
    taskStruct = load_obj(homeDir + os.sep + 'Output' + os.sep + 'Supplementary' + os.sep + str(expInfo['SubNo']) + '_Practice_Data.pkl')
    return(taskStruct)

def reloadMemTask(taskStruct,homeDir,expInfo):
    del taskStruct
    taskStruct = load_obj(homeDir + os.sep + 'Output' + os.sep + 'Task' + os.sep + str(expInfo['SubNo']) + '_Data_All.pkl')
    return(taskStruct)

def scalePoints(taskStruct,points):
    scaled = (points - taskStruct['minPoints']) / (taskStruct['maxPoints'] - taskStruct['minPoints'])
    return(scaled)

def payment(realMoney,scaledPointsTotal):
    if scaledPointsTotal > 1:
        scaledPointsTotal = 1
    totalMoney = realMoney * scaledPointsTotal
    payOut = round(totalMoney,2)
    return(payOut)