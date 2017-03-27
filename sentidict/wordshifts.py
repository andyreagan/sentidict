from IPython.display import Javascript,HTML,publish_display_data
from IPython import get_ipython
from os.path import isfile,isdir,abspath,join,dirname
from .utils import *
from .dictionaries import *
from jinja2 import FileSystemLoader
from jinja2.environment import Environment

env = Environment(
    loader=FileSystemLoader(dirname(__file__)))

# borrowed from MPLD3
WWW_JS_DIR = "https://andyreagan.github.io/hedotools/js/"
# don't include version, that's handled by hedotools
D3_URL = WWW_JS_DIR + "d3"
HEDOTOOLS_URL = WWW_JS_DIR + "hedotools"

# we'll have copied to the _working directory_
LOCAL_JS_DIR = "static" # join(getcwd(), "static")
D3_LOCAL = join(LOCAL_JS_DIR, "d3.min.js")
HEDOTOOLS_LOCAL = join(LOCAL_JS_DIR,"hedotools.min.js")

def require_JS(local=False):
    if local:
        flat = {"application/javascript": env.get_template("templates/jupyter-require.js").render({"d3_url": D3_LOCAL, "hedotools_url": HEDOTOOLS_LOCAL})}
    else:
        flat = {"application/javascript": env.get_template("templates/jupyter-require.js").render({"d3_url": D3_URL, "hedotools_url": HEDOTOOLS_URL})}
    publish_display_data(flat)
    
# try:
#     __IPYTHON__
#     require_JS()
# except:
#     pass
# a cleaner way to do this
ip = get_ipython()
if ip:
    require_JS()

def shiftHtml(scoreList,wordList,refFreq,compFreq,outFile,corpus="LabMT",advanced=False,customTitle=False,title="",ref_name="reference",comp_name="comparison",ref_name_happs="",comp_name_happs="",isare="",selfshift=False,bgcolor="white",preshift=False,link=False):
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

    if isare == "":
        isare = " is "
        if list(comp_name)[-1] == "s":
            isare = " are "

    template = env.get_template("templates/wordshift-base.html","r")
    f = codecs.open(outFile,'w','utf8')
    
    if preshift:
        sortedMag,sortedWords,sortedType,sumTypes = shift(refFreq,compFreq,scoreList,wordList,sort=True)
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

        f.write(template.render(sortedMag=sortedMag_string, sortedWords=sortedWords_string,
                                sortedType=sortedType_string, sumTypes=sumTypes_string,
                                title=title, ref_name=ref_name, comp_name=comp_name,
                                ref_name_happs=ref_name_happs, comp_name_happs=comp_name_happs,
                                refH=refH,compH=compH,
                                isare=isare,divnum=divnum,link=link,preshift=preshift))

    else:
        # write out the template
        lens_string = ','.join(map(lambda x: '{0:.12f}'.format(x),scoreList))
        words_string = ','.join(map(lambda x: '"{0}"'.format(x),wordList))
        refFreq_string = ','.join(map(lambda x: '{0:.0f}'.format(x),refFreq))
        compFreq_string = ','.join(map(lambda x: '{0:.0f}'.format(x),compFreq))

        f.write(template.render(lens=lens_string, words=words_string,
                                refF=refFreq_string, compF=compFreq_string,
                                title=title, ref_name=ref_name, comp_name=comp_name,
                                ref_name_happs=ref_name_happs, comp_name_happs=comp_name_happs,
                                isare=isare,divnum=divnum,selfshift=selfshift,bgcolor=bgcolor))

    f.close()        
    print("wrote shift to {}".format(outFile))
    if link:
        copy_static_files()

def inject_shift(html,js):
    publish_display_data({"text/html": html})
    publish_display_data({"application/javascript": js})

def shiftHtmlJupyter(scoreList,wordList,refFreq,compFreq,corpus="LabMT",advanced=False,customTitle=False,title="",ref_name="reference",comp_name="comparison",ref_name_happs="",comp_name_happs="",isare="",selfshift=False,bgcolor="white"):
    """Shifter that generates HTML <div> and JS call in two pieces, designed to work inside of a Jupyter notebook.
    
    Assumes that that D3, jquery, hedotools already loaded. In iPython (Jupyter) this should have happened on import of the wordshift module."""

    import random
    divnum = int(random.uniform(0,9999999999))
    
    if len(ref_name_happs) == 0:
        ref_name_happs = ref_name.capitalize()
    if len(comp_name_happs) == 0:
        comp_name_happs = comp_name.capitalize()

    if not customTitle:
        title = "Example shift using {0}".format(corpus)

    if isare == "":
        isare = " is "
        if list(comp_name)[-1] == "s":
            isare = " are "

    body = env.get_template("templates/wordshift-body.html")
    js = env.get_template("templates/wordshift-body.js")
    
    lens_string = ','.join(map(lambda x: '{0:.12f}'.format(x),scoreList))
    words_string = ','.join(map(lambda x: '"{0}"'.format(x),wordList))
    refFreq_string = ','.join(map(lambda x: '{0:.0f}'.format(x),refFreq))
    compFreq_string = ','.join(map(lambda x: '{0:.0f}'.format(x),compFreq))

    this_html = body.render(lens=lens_string, words=words_string,
                        refF=refFreq_string, compF=compFreq_string,
                        title=title, ref_name=ref_name, comp_name=comp_name,
                        ref_name_happs=ref_name_happs, comp_name_happs=comp_name_happs,
                        isare=isare,divnum=divnum,selfshift=selfshift,bgcolor=bgcolor)
    this_js = js.render(lens=lens_string, words=words_string,
              refF=refFreq_string, compF=compFreq_string,
              title=title, ref_name=ref_name, comp_name=comp_name,
              ref_name_happs=ref_name_happs, comp_name_happs=comp_name_happs,
              isare=isare,divnum=divnum,selfshift=selfshift,bgcolor=bgcolor)
    
    inject_shift(this_html,this_js)

def shiftHtmlJupyterSentidict(my_sentidict,refFreq,compFreq,**kwargs):
    """Wrapper over shiftHtmlJupyter to limit the inputs to my_sentidict,refFreq,compFreq and the keyword arguments passed through."""
    shiftHtmlJupyter(my_sentidict.scorelist,my_sentidict.wordlist,refFreq,compFreq,**kwargs)
