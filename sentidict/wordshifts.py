from IPython.display import Javascript, display, publish_display_data
from os.path import isfile,isdir,abspath,join,dirname
from .utils import *
from .dictionaries import *
from jinja2 import FileSystemLoader
from jinja2.environment import Environment

env = Environment()
env.loader = FileSystemLoader(dirname(__file__))

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
    
    if not isdir('static'):
        mkdir('static')

    # strip off the .html
    outFileShort = outFile
    if outFile[-5:] == ".html":
        outFileShort = outFile[:-5]
      
    # write out the template
    lens_string = ','.join(map(lambda x: '{0:.12f}'.format(x),scoreList))
    words_string = ','.join(map(lambda x: '"{0}"'.format(x),wordList))
    refFreq_string = ','.join(map(lambda x: '{0:.0f}'.format(x),refFreq))
    compFreq_string = ','.join(map(lambda x: '{0:.0f}'.format(x),compFreq))

    template = Template(openWithPath("templates/template.html.jinja2","r").read())

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

    # wrapper = Template(openWithPath("templates/wrapper.html.jinja2","r").read())
    # wrapper = Template(openWithPath("templates/wrapper-include.html.jinja2","r").read())
    wrapper = env.get_template('templates/wrapper-include.html.jinja2')

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
    
    if not isdir('static'):
        mkdir('static')

    outFileShort = outFile.split('.')[0]
      
    # write out the template
    lens_string = ','.join(map(lambda x: '{0:.2f}'.format(x),scoreList))
    words_string = ','.join(map(lambda x: '"{0}"'.format(x),wordList))
    refFreq_string = ','.join(map(lambda x: '{0:.0f}'.format(x),refFreq))
    compFreq_string = ','.join(map(lambda x: '{0:.0f}'.format(x),compFreq))
    
    # dump out a static shift view page
    template = Template(openWithPath("templates/template-full.html.jinja2","r").read())

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
    copy_static_files()

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
    
    if not isdir('static'):
        mkdir('static')

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
    template = Template(openWithPath("templates/template-preshifted.html.jinja2","r").read())

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
    copy_static_files()
