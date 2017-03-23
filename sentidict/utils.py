#!/usr/bin/python
#
# utils.py
#
# written by Andy Reagan
# 2014-03-01

import re
import codecs
import copy
import subprocess
from jinja2 import Template
from numpy import unique,dot,sum,mean,zeros,array,ndarray,arange
from os import mkdir
from os.path import isfile,isdir,abspath,join,dirname

u = lambda x: x

def isarray(x):
    return isinstance(x, ndarray)

def stopper(tmpVec,score_list,word_list,stopVal=1.0,ignore=[],center=5.0):
    """Take a frequency vector, and 0 out the stop words.
  
    Will always remove the nig* words.
    
    Return the 0'ed vector."""

    ignoreWords = ["nigga","nigger","niggaz","niggas"];
    for word in ignore:
        ignoreWords.append(word)
    newVec = copy.copy(tmpVec)
    for i in range(len(score_list)):
        if abs(score_list[i]-center) < stopVal:
            newVec[i] = 0
        if word_list[i] in ignoreWords:
            newVec[i] = 0

    return newVec

def stopper_mat(tmpVec,score_list,word_list,stopVal=1.0,ignore=[],center=5.0):
    """Take a frequency vector, and 0 out the stop words.
  
    A sparse-aware matrix stopper.
    F-vecs are rows: [i,:]
    
    Will always remove the nig* words.
  
    Return the 0'ed matrix, sparse."""

    ignoreWords = ["nigga","nigger","niggaz","niggas"];
    for word in ignore:
        ignoreWords.append(word)
    indices_to_ignore = []
    for i in range(len(score_list)):
        if abs(score_list[i]-center) < stopVal:
            indices_to_ignore.append(i)
        elif word_list[i] in ignoreWords:
            indices_to_ignore.append(i)
    indices_to_ignore = indices_to_ignore
    # print(indices_to_ignore)
    # newVec = copy.copy(tmpVec)
    newVec = copy.deepcopy(tmpVec)
    newVec[:,indices_to_ignore] = 0
  
    return newVec

def emotionV(freq,happs):
    """Given the frequency vector and the score vector, compute the happs."""
    if sum(freq) > 0:
        return dot(freq,happs)/sum(freq)
    else:
        return -1

def shift(refFreq,compFreq,lens,words,sort=True):
    """Compute a shift, and return the results.
    
    If sort=True, will return the three sorted lists, and sumTypes. Else, just the two shift lists, and sumTypes (words don't need to be sorted).
    
    Note: refFreq must be have more than 0 words in it!"""

    if not isarray(refFreq):
        refFreq = array(refFreq)
    if not isarray(compFreq):
        compFreq = array(compFreq)
    if not isarray(lens):
        lens = array(lens)
    if not isarray(words):
        words = array(words)                        

    # normalize frequencies
    # Nref = sum(refFreq)
    # Ncomp = sum(compFreq)
    # for i in range(len(refFreq)):
    #     refFreq[i] = float(refFreq[i])/Nref
    #     compFreq[i] = float(compFreq[i])/Ncomp
    refFreqN = refFreq/refFreq.sum()
    compFreqN = compFreq/compFreq.sum()
    # compute the reference happiness
    # refH = sum([refFreqN[i]*lens[i] for i in range(len(lens))])
    refH = emotionV(refFreq,lens)
    compH = emotionV(compFreq,lens)
    # determine shift magnitude, type
    # shiftMag = [0 for i in range(len(lens))]
    # shiftType = [0 for i in range(len(lens))]
    shiftMag = zeros(lens.shape)
    shiftType = zeros(lens.shape)
    # for i in range(len(lens)):
    #     freqDiff = compFreq[i]-refFreq[i]
    #     shiftMag[i] = (lens[i]-refH)*freqDiff
    #     if freqDiff > 0:
    #         shiftType[i] += 2
    #     if lens[i] > refH:
    #         shiftType[i] += 1
    freqDiff = compFreq-refFreq
    shiftMag = (lens-refH)*freqDiff/compFreq.sum()
    shiftType[freqDiff > 0] = 2
    shiftType[lens > refH] += 1


    # sumTypes = [0.0 for i in range(4)]
    sumTypes = zeros(4)
    # for i in range(len(lens)):
    #     sumTypes[shiftType[i]] += shiftMag[i]
    for i in range(4):
        sumTypes[i] = shiftMag[shiftType == i].sum()
        
    if sort:
        indices = sorted(arange(shiftMag.shape[0]), key=lambda k: abs(shiftMag[k]), reverse=True)    
        sortedMag = shiftMag[indices]
        sortedType = shiftType[indices]
        sortedWords = words[indices]
        return sortedMag,sortedWords,sortedType,sumTypes
    else:
        return shiftMag,shiftType,sumTypes

def copy_static_files():
    """Deprecated method to copy files from this module's static directory into the directory where shifts are being made."""
    # print('copying over static files')
    # for staticfile in ['d3.v3.min.js','plotShift.js','shift.js','example-on-load.js']:
    for staticfile in ['d3.js','jquery-1.11.0.min.js','urllib.js','hedotools.init.js','hedotools.shifter.js','hedotools.shift.css','shift-crowbar.js']:
        if not isfile('static/'+staticfile):
            import shutil
            relpath = abspath(__file__).split('/')[1:-1]
            relpath.append('static')
            relpath.append(staticfile)
            fileName = ''
        for pathp in relpath:
            fileName += '/' + pathp
        shutil.copy(fileName,'static/'+staticfile)

def link_static_files():
    """Same as copy_static_files, but makes symbolic links."""
    # print('copying over static files')
    # for staticfile in ['d3.v3.min.js','plotShift.js','shift.js','example-on-load.js']:
    for staticfile in ['d3.js','jquery-1.11.0.min.js','urllib.js','hedotools.init.js','hedotools.shifter.js','hedotools.shift.css','shift-crowbar.js']:
        if not isfile('static/'+staticfile):
            relpath = abspath(__file__).split('/')[1:-1]
            relpath.append('static')
            relpath.append(staticfile)
            fileName = '/'+'/'.join(relpath)
            subprocess.call("ln -s {0} {1}".format(fileName,'static/'+staticfile),shell=True)

listify_quick = lambda raw: [x.lower() for x in re.findall(r"[\w\@\#\'\&\]\*\-\/\[\=\;]+",raw,flags=re.UNICODE)]

def open_codecs_dictify(file):
    '''Generate a word dict to test.'''
    f = codecs.open(file, "r", "utf8")
    ref_text_raw = f.read()
    f.close()
    replaceStrings = ['---','--','\'\'']
    for replaceString in replaceStrings:
        ref_text_raw = ref_text_raw.replace(replaceString,' ')
    words = [x.lower() for x in re.findall(r"[\w\@\#\'\&\]\*\-\/\[\=\;]+",ref_text_raw,flags=re.UNICODE)]
    test_dict = dict()
    for word in words:
        if word in test_dict:
            test_dict[word] += 1
        else:
            test_dict[word] = 1        
    return test_dict

def openWithPath(filename,mode,codec="utf8"):
    return codecs.open(join(dirname(__file__),filename),mode,codec)
    # def openWithPath(self,filename,mode):
    #     """Helper function for searching for files."""
    #     try:
    #         f = codecs.open(filename,mode,'utf8')
    #         return f
    #     except IOError:
    #         relpath = abspath(__file__).split('/')[:-1]
    #         # relpath.append('data')
    #         relpath.append(filename)
    #         filename = '/'.join(relpath)
    #         f = codecs.open(filename,mode,'utf8')
    #         return f
    #     except:
    #         raise('could not open the needed file')

