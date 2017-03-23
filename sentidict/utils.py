#!/usr/bin/python
#
# utils.py
#
# written by Andy Reagan
# 2014-03-01

import os
import re
import codecs
import copy
import subprocess
from jinja2 import Template
from numpy import unique,dot,sum,mean,zeros,array,ndarray,arange

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

def shiftHtmlJupyter(scoreList,wordList,refFreq,compFreq,outFile,corpus="LabMT",advanced=False,customTitle=False,title="",ref_name="reference",comp_name="comparison",ref_name_happs="",comp_name_happs="",isare="",saveFull=True,selfshift=False,bgcolor="white"):
    """Shifter that generates HTML in two pieces, designed to work inside of a Jupyter notebook.

    Saves the filename as given (with .html extension), and sneaks in a filename-wrapper.html, and the wrapper file has the html headers, everything to be a standalone file. The filenamed html is just the guts of the html file, because the complete markup isn't need inside the notebook."""

    import random
    divnum = int(random.uniform(0,9999999999))
    if len(ref_name_happs) == 0:
        ref_name_happs = ref_name.capitalize()
    if len(comp_name_happs) == 0:
        comp_name_happs = comp_name.capitalize()

    if not customTitle:
        title = "Example shift using {0}".format(corpus)
    
    if not os.path.exists('static'):
        os.mkdir('static')

    # strip off the .html
    outFileShort = outFile
    if outFile[-5:] == ".html":
        outFileShort = outFile[:-5]
      
    # write out the template
    lens_string = ','.join(map(lambda x: '{0:.12f}'.format(x),scoreList))
    words_string = ','.join(map(lambda x: '"{0}"'.format(x),wordList))
    refFreq_string = ','.join(map(lambda x: '{0:.0f}'.format(x),refFreq))
    compFreq_string = ','.join(map(lambda x: '{0:.0f}'.format(x),compFreq))

    wrapper = Template(open("templates/simple.html","r").read())

    # dump out a static shift view page
    template = Template(open("templates/template.html","r").read())

    if isare == "":
        isare = " is "
        if list(comp_name)[-1] == "s":
            isare = " are "
    f = codecs.open(outFile,'w','utf8')
    inner=template.render(lens=lens_string, words=words_string,
                            refF=refFreq_string, compF=compFreq_string,
                            title=title, ref_name=ref_name, comp_name=comp_name,
                            ref_name_happs=ref_name_happs, comp_name_happs=comp_name_happs,
                            isare=isare,divnum=divnum,selfshift=selfshift,bgcolor=bgcolor)
    f.write(inner)
    f.close()
    print("wrote shift to {}".format(outFile))

    if saveFull:
        f = codecs.open(outFileShort+"-wrapper.html",'w','utf8')
        f.write(wrapper.render(inner=inner))
        f.close()
        print("wrote wrapped shift html to {}".format(outFileShort+"-wrapper.html"))
    
def shiftHtml(scoreList,wordList,refFreq,compFreq,outFile,corpus="LabMT",advanced=False,customTitle=False,title="",ref_name="reference",comp_name="comparison",ref_name_happs="",comp_name_happs="",isare=""):
    """Make an interactive shift for exploring and sharing.

    The most insane-o piece of code here (lots of file copying,
    writing vectors into html files, etc).
    
    Accepts a score list, a word list, two frequency files 
    and the name of an HTML file to generate
    
    ** will make the HTML file, and a directory called static
    that hosts a bunch of .js, .css that is useful."""

    if len(ref_name_happs) == 0:
        ref_name_happs = ref_name.capitalize()
    if len(comp_name_happs) == 0:
        comp_name_happs = comp_name.capitalize()

    if not customTitle:
        title = "Example shift using {0}".format(corpus)
    
    if not os.path.exists('static'):
        os.mkdir('static')

    outFileShort = outFile.split('.')[0]
      
    # write out the template
    lens_string = ','.join(map(lambda x: '{0:.2f}'.format(x),scoreList))
    words_string = ','.join(map(lambda x: '"{0}"'.format(x),wordList))
    refFreq_string = ','.join(map(lambda x: '{0:.0f}'.format(x),refFreq))
    compFreq_string = ','.join(map(lambda x: '{0:.0f}'.format(x),compFreq))
    
    # dump out a static shift view page
    template = Template(open("templates/template-full.html","r").read())

    if isare == "":
        isare = " is "
        if list(comp_name)[-1] == "s":
            isare = " are "
    f = codecs.open(outFile,'w','utf8')
    f.write(template.render(outFileShort=outFileShort,
                            lens=lens_string, words=words_string,
                            refF=refFreq_string, compF=compFreq_string,
                            title=title, ref_name=ref_name, comp_name=comp_name,
                            ref_name_happs=ref_name_happs, comp_name_happs=comp_name_happs,
                            isare=isare))
    f.close()
    print("wrote shift to {}".format(outFile))
    # copy_static_files()
    link_static_files()

def shiftHtmlPreshifted(scoreList,wordList,refFreq,compFreq,outFile,corpus="LabMT",advanced=False,customTitle=False,title="",ref_name="reference",comp_name="comparison",ref_name_happs="",comp_name_happs="",isare=""):
    """Make an interactive shift for exploring and sharing.

    The most insane-o piece of code here (lots of file copying,
    writing vectors into html files, etc).
    
    Accepts a score list, a word list, two frequency files 
    and the name of an HTML file to generate
    
    ** will make the HTML file, and a directory called static
    that hosts a bunch of .js, .css that is useful."""

    if len(ref_name_happs) == 0:
        ref_name_happs = ref_name.capitalize()
    if len(comp_name_happs) == 0:
        comp_name_happs = comp_name.capitalize()

    if not customTitle:
        title = "Example shift using {0}".format(corpus)
    
    if not os.path.exists('static'):
        os.mkdir('static')

    sortedMag,sortedWords,sortedType,sumTypes = shift(refFreq,compFreq,scoreList,wordList,sort=True)

    outFileShort = outFile.split('.')[0]
      
    # write out the template
    sortedMag_string = ','.join(map(lambda x: '{0:.12f}'.format(x),sortedMag[:200]))
    sortedWords_string = ','.join(map(lambda x: '"{0}"'.format(x),sortedWords[:200]))
    sortedType_string = ','.join(map(lambda x: '{0:.0f}'.format(x),sortedType[:200]))
    sumTypes_string = ','.join(map(lambda x: '{0:.3f}'.format(x),sumTypes))

    # normalize frequencies
    Nref = float(sum(refFreq))
    Ncomp = float(sum(compFreq))
    for i in range(len(refFreq)):
        refFreq[i] = float(refFreq[i])/Nref
        compFreq[i] = float(compFreq[i])/Ncomp
    # compute the reference happiness
    refH = "{0:.4}".format(sum([refFreq[i]*scoreList[i] for i in range(len(scoreList))]))
    compH = "{0:.4}".format(sum([compFreq[i]*scoreList[i] for i in range(len(scoreList))]))
    
    # dump out a static shift view page
    template = Template(open("templates/template-preshifted.html","r").read())

    if isare == "":
      isare = " is "
      if list(comp_name)[-1] == "s":
          isare = " are "
    f = codecs.open(outFile,'w','utf8')
    f.write(template.render(outFileShort=outFileShort,
                          sortedMag=sortedMag_string, sortedWords=sortedWords_string,
                          sortedType=sortedType_string, sumTypes=sumTypes_string,
                          title=title, ref_name=ref_name, comp_name=comp_name,
                          ref_name_happs=ref_name_happs, comp_name_happs=comp_name_happs,
                          refH=refH,compH=compH,
                          isare=isare))
    f.close()
    print("wrote shift to {}".format(outFile))
    # copy_static_files()
    link_static_files()

def copy_static_files():
    """Deprecated method to copy files from this module's static directory into the directory where shifts are being made."""
    # print('copying over static files')
    # for staticfile in ['d3.v3.min.js','plotShift.js','shift.js','example-on-load.js']:
    for staticfile in ['d3.js','jquery-1.11.0.min.js','urllib.js','hedotools.init.js','hedotools.shifter.js','hedotools.shift.css','shift-crowbar.js']:
        if not os.path.isfile('static/'+staticfile):
            import shutil
            relpath = os.path.abspath(__file__).split('/')[1:-1]
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
        if not os.path.isfile('static/'+staticfile):
            relpath = os.path.abspath(__file__).split('/')[1:-1]
            relpath.append('static')
            relpath.append(staticfile)
            fileName = '/'+'/'.join(relpath)
            subprocess.call("ln -s {0} {1}".format(fileName,'static/'+staticfile),shell=True)


def all_features(rawtext,uid,tweet_id,gram_id):
    '''Return the feature vector for a given tweets.

    Be careful about indexing!
    Assuming here that we're taking in text of the tweet/gram'''

    my_LIWC_stopped = LIWC(stopVal=0.5)
    my_LIWC = LIWC()
    my_LabMT = LabMT(stopVal=1.0)
    my_ANEW = ANEW(stopVal=1.0)
    
    # create  simple list for the result
    result = [0 for i in range(75)]
    # the first field, tableID, is not included (leaving 75)
    result[0] = tweet_id
    result[1] = gram_id
    result[2] = uid

    words = listify(rawtext)
    word_dict = dictify(words)
    result[3] = len(words)

    # load the classes that we need

    # print(len(my_LIWC.data))
    # print(len(my_LIWC.scorelist))
    my_word_vec = my_LIWC_stopped.wordVecify(word_dict)
    # print(len(my_word_vec))
    # print(sum(my_word_vec))
    happs = my_LIWC_stopped.score(word_dict)
    # print(len(my_LIWC.data))
    # print(len(my_LIWC.scorelist))
    # print(happs)
    result[4] = sum(my_word_vec)
    result[5] = happs

    my_word_vec = my_LabMT.wordVecify(word_dict)
    happs = my_LabMT.score(word_dict)
    # print(len(my_word_vec))
    # print(sum(my_word_vec))
    # print(happs)
    result[6] = sum(my_word_vec)
    result[7] = happs
    my_word_vec = my_ANEW.wordVecify(word_dict)
    happs = my_ANEW.score(word_dict)
    # print(len(my_word_vec))
    # print(sum(my_word_vec))
    # print(result)
    result[8] = sum(my_word_vec)
    result[9] = happs

    # make a word vector
    my_word_vec = my_LIWC.wordVecify(word_dict)
    all_features = zeros(len(my_LIWC.data["happy"])-2)
    for word in my_LIWC.data:
        all_features += array(my_LIWC.data[word][2:])*my_word_vec[my_LIWC.data[word][0]]
    for i,score in enumerate(all_features):
        result[10+i] = all_features[i]

    return result

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



