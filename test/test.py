# note: nose2 will run all functions that begin with test

from sentidict.utils import *
from sentidict.dictionaries import *
from sentidict.functions import *
import  numpy as np
from scipy.sparse import csr_matrix,issparse
# import subprocess
# import codecs
from json import loads
# from jinja2 import Template

# this has some useful functions
# sys.path.append("/Users/andyreagan/tools/python/")
# from kitchentable.dogtoys import *

TOL = 1e-3

def test_stopper():
    test_f = [1,1,1,1]
    test_words = ["happy","remove","niggas","neutral"]
    test_scores = [6.,8.,8.,5.]
    assert stopper(test_f,test_scores,test_words) == [1,1,0,0]
    assert stopper(test_f,test_scores,test_words,ignore=["remove"]) == [1,0,0,0]
    assert stopper(test_f,test_scores,test_words,ignore=["remove"],stopVal=2.0) == [0,0,0,0]
    assert stopper(test_f,test_scores,test_words,ignore=["remove"],stopVal=0.0) == [1,0,0,1]
    assert stopper(test_f,test_scores,test_words,stopVal=1.0,center=7.0) == [1,1,0,1]
    assert stopper(test_f,test_scores,test_words,stopVal=2.0,center=7.0) == [0,0,0,1]
    test_scores = np.array([6.,8.,8.,5.])
    test_f = np.array([1,1,1,1])
    assert (stopper(test_f,test_scores,test_words) == np.array([1,1,0,0])).all()
    assert (stopper(test_f,test_scores,test_words,ignore=["remove"]) == np.array([1,0,0,0])).all()
    assert (stopper(test_f,test_scores,test_words,ignore=["remove"],stopVal=2.0) == np.array([0,0,0,0])).all()
    assert (stopper(test_f,test_scores,test_words,ignore=["remove"],stopVal=0.0) == np.array([1,0,0,1])).all()
    assert (stopper(test_f,test_scores,test_words,stopVal=1.0,center=7.0) == np.array([1,1,0,1])).all()
    assert (stopper(test_f,test_scores,test_words,stopVal=2.0,center=7.0) == np.array([0,0,0,1])).all()

def test_stopper_mat():
    test_f = np.matrix([[1,1,1,1],[1,1,1,1]])
    test_words = ["happy","remove","niggas","neutral"]
    test_scores = [6.,8.,8.,5.]
    assert (stopper_mat(test_f,test_scores,test_words) == np.matrix([[1,1,0,0],[1,1,0,0]])).all()
    assert (stopper_mat(test_f,test_scores,test_words,ignore=["remove"]) == np.matrix([[1,0,0,0],[1,0,0,0]])).all()
    assert (stopper_mat(test_f,test_scores,test_words,ignore=["remove"],stopVal=2.0) == np.matrix([[0,0,0,0],[0,0,0,0]])).all()
    # print(stopper_mat(test_f,test_scores,test_words,ignore=["remove"],stopVal=0.0))
    assert (stopper_mat(test_f,test_scores,test_words,ignore=["remove"],stopVal=0.0) == np.matrix([[1,0,0,1],[1,0,0,1]])).all()
    assert (stopper_mat(test_f,test_scores,test_words,stopVal=1.0,center=7.0) == np.matrix([[1,1,0,1],[1,1,0,1]])).all()
    assert (stopper_mat(test_f,test_scores,test_words,stopVal=2.0,center=7.0) == np.matrix([[0,0,0,1],[0,0,0,1]])).all()
    # make sure it still works with sparse
    test_f = csr_matrix([[1,1,1,1],[1,1,1,1]])
    assert (stopper_mat(test_f,test_scores,test_words) == np.matrix([[1,1,0,0],[1,1,0,0]])).all()
    assert (stopper_mat(test_f,test_scores,test_words,ignore=["remove"]) == np.matrix([[1,0,0,0],[1,0,0,0]])).all()
    assert (stopper_mat(test_f,test_scores,test_words,ignore=["remove"],stopVal=2.0) == np.matrix([[0,0,0,0],[0,0,0,0]])).all()
    # print(stopper_mat(test_f,test_scores,test_words,ignore=["remove"],stopVal=0.0))
    # print(test_f)
    assert (stopper_mat(test_f,test_scores,test_words,ignore=["remove"],stopVal=0.0) == np.matrix([[1,0,0,1],[1,0,0,1]])).all()
    assert (stopper_mat(test_f,test_scores,test_words,stopVal=1.0,center=7.0) == np.matrix([[1,1,0,1],[1,1,0,1]])).all()
    assert (stopper_mat(test_f,test_scores,test_words,stopVal=2.0,center=7.0) == np.matrix([[0,0,0,1],[0,0,0,1]])).all()    
    assert issparse(stopper_mat(test_f,test_scores,test_words,stopVal=2.0,center=7.0))

def test_emotionV():
    # not really much to test here...
    test_f = np.array([1,1,1,1])
    test_words = ["happy","remove","niggas","neutral"]
    test_scores = [6.,8.,8.,5.]
    assert emotionV(test_f,test_scores) == np.sum(test_scores)/4
    assert emotionV(np.zeros(4),test_scores) == -1

def test_shift():
    test_f = np.array([2,1,2,1])
    test_words = ["happy","remove","niggas","neutral"]
    test_scores = np.array([6.,8.,8.,5.])
    refH = emotionV(test_f,test_scores)
    compH = emotionV(np.ones(4),test_scores)
    assert np.abs(refH - 6.83) < .01
    assert np.abs(compH - 6.75) < .01
    mag,words,types,stypes = shift(test_f,np.ones(4),test_scores,test_words,sort=True)
    assert np.abs(np.sum(mag) == (compH-refH)) < .001

def test_shiftHtmlJupyter():
    pass

def test_shiftHtml():
    pass

def shiftHtmlPreshifted():
    pass

def test_labMT_english():
    """Test as much of sentidict as possible, using the labMT dictionary subclass.

    Basically an extended example."""
    
    my_labMT = LabMT(lang='english')

    # make sure the words got loaded in correctly in the dictionary
    assert my_labMT.data["test"][1] == 4.06
    # make sure the vector is aligned
    index = my_labMT.data["test"][0]
    assert my_labMT.wordlist[index] == 'test'
    assert my_labMT.scorelist[index] == 4.06

    return 1

    # f = codecs.open("examples/data/18.01.14.txt", "r", "utf8")
    # ref_text_raw = f.read()
    # f.close()
    # f = codecs.open("examples/data/21.01.14.txt", "r", "utf8")
    # comp_text_raw = f.read()
    # f.close()
    
    # ref_happs, ref_freq = emotion(ref_text_raw, my_labMT, shift=True, happsList=my_labMTvector)
    # comp_happs, comp_freq = emotion(comp_text_raw, my_labMT, shift=True, happsList=my_labMTvector)

    # ref_freq_stopped = stopper(ref_freq, my_labMTvector, my_labMTwordList, stopVal=1.0)
    # # make sure that it blocked "the" and "nigger"
    # index = int(my_labMT["the"][0])-1
    # assert ref_freq_stopped[index] == 0    
    # index = int(my_labMT["nigger"][0])-1
    # assert ref_freq_stopped[index] == 0

    # ref_freq_stopped = stopper(ref_freq, my_labMTvector, my_labMTwordList, stopVal=1.0, ignore=["laughter"])
    # # make sure that it blocked "the" and "nigger" still
    # index = int(my_labMT["the"][0])-1
    # assert ref_freq_stopped[index] == 0    
    # index = int(my_labMT["nigger"][0])-1
    # assert ref_freq_stopped[index] == 0
    # # also check that it now blocked laughter    
    # index = int(my_labMT["laughter"][0])-1
    # assert ref_freq_stopped[index] == 0

    # ref_freq_stopped = stopper(ref_freq, my_labMTvector, my_labMTwordList, stopVal=1.0)
    
    # comp_freq_stopped = stopper(comp_freq, my_labMTvector, my_labMTwordList, stopVal=1.0)

    # ref_happs_from_vector = emotionV(ref_freq, my_labMTvector)
    # # make sure this is the same as from emotion
    # print(ref_happs_from_vector)
    # print(ref_happs)
    # assert abs(ref_happs_from_vector - ref_happs) < TOL

    # comp_happs_stopped = emotionV(comp_freq_stopped, my_labMTvector)

    # ref_happs_stopped = emotionV(ref_freq_stopped, my_labMTvector)
        
    # # without stop words
    # assert abs(ref_happs - 5.51733944613) < TOL
    # assert ref_freq[5000] == 409

    # # with stop words
    # assert abs(ref_happs_stopped - 6.01346892642) < TOL
    # assert ref_freq_stopped[5000] == 0

    # print("-"*80)
    # print(ref_happs)
    # print(ref_happs_stopped)
    # print(comp_happs)
    # print(comp_happs_stopped)
    # print("-"*80)    

    # outFile = "test.html"
    # shiftHtml(my_labMTvector, my_labMTwordList, ref_freq, comp_freq, outFile)

    # outFile = "test-stopped.html"    
    # shiftHtml(my_labMTvector, my_labMTwordList, ref_freq_stopped, comp_freq_stopped, outFile)
    
    # # # also make the inkscape version
    # # shiftHtml(my_labMTvector, my_labMTwordList, ref_freq, comp_freq, "test-inkscape.html")
    # # generateSVG("test-inkscape.html")
    # # generatePDF("test-inkscape.svg",program="inkscape")
    # # subprocess.call("open test-inkscape.pdf",shell=True)
    
    # sortedMag,sortedWords,sortedType,sumTypes = shift(ref_freq, comp_freq, my_labMTvector, my_labMTwordList)

    # assert sortedMag[0] < 0
    # assert sortedWords[0] == "love"
    
    # shiftMag,shiftType,sumTypes = shift(ref_freq, comp_freq, my_labMTvector, my_labMTwordList, sort=False)

def speedy_dict_marisa_test(my_senti_dict,my_senti_marisa,test_dict):
    """Speedy test."""

    # lang = "english"
    # dictionary = "LabMT"
    print("loading {0}".format(my_senti_dict.title))
    
    dict_score = my_senti_dict.score(test_dict)
    dict_word_vec = my_senti_dict.wordVecify(test_dict)
    marisa_score = my_senti_marisa.score(test_dict)
    marisa_word_vec = my_senti_marisa.wordVecify(test_dict)

    print(dict_score)
    print(marisa_score)
    if not my_senti_dict.stems:
        assert abs(dict_score-marisa_score) < TOL
        diff = dict_word_vec - marisa_word_vec
        print(dict_word_vec,marisa_word_vec)
        print(my_senti_dict.fixedwords[0])
        print(my_senti_marisa.fixedwords[0])
        print(len(my_senti_dict.stemwords))
        print(len(my_senti_marisa.stemwords))
        assert (dict_word_vec == marisa_word_vec).all()
    else:
        assert len(dict_word_vec) == len(marisa_word_vec)
        print(dict_word_vec,marisa_word_vec)
        print(my_senti_dict.fixedwords[0])
        print(my_senti_marisa.fixedwords[0])
        print(my_senti_dict.stemwords[0])
        print(my_senti_marisa.stemwords[0])

    # check that they all match happy
    if my_senti_marisa.matcherTrieBool(u"happy"):
        print("happy is in the list")
    else:
        print("happy is *NOT* in the list")

    # let's find the index of the word happy in each
    # this is really a word-by-word test, because
    # of the stem matching
    word = u"happy"
    happy_dict = {word: 1}
    happy_vec = my_senti_marisa.wordVecify(happy_dict)
    assert sum(happy_vec) == 1
    index = list(happy_vec).index(1)
    print("index of the happy match: {0}".format(index))
    # 3,30,222,2221,2818,5614    
    print("length of fixed words: {0}".format(len(my_senti_marisa.fixedwords)))

    word = u"abide"
    print("checking on {0}".format(word))
    happy_dict = {word: 1}
    happy_vec = my_senti_marisa.wordVecify(happy_dict)
    if my_senti_marisa.matcherTrieBool(word):
        my_index = list(happy_vec).index(1)
        print(my_index)
        print(marisa_word_vec[my_index])
        print("the dude abides!")
    
    print("count in test text: {0}".format(marisa_word_vec[index]))
    print(test_dict["happy"])
    print(test_dict["happyy"])
    print(test_dict["happyyy"])

    # checked that no dictionaries match anything beyond happy in the stems
    # so, they must match it fixed
    # => check it right against the straight count
    assert test_dict["happy"] == marisa_word_vec[index]

    if index > len(my_senti_marisa.fixedwords):
        print("matched by a stem")
        print(my_senti_marisa.stemwords[index-len(my_senti_marisa.fixedwords)])
    else:
        print("matched by a fixed word")
        print(my_senti_marisa.fixedwords[index])
        
def speedy_dict_marisa_test(all_sentidicts):
    ref_dict = open_codecs_dictify("examples/data/18.01.14.txt")
    comp_dict = open_codecs_dictify("examples/data/21.01.14.txt")

    # this test the loading for each
    stopVal = 1.0
    for senti_dict in all_sentidicts:
        pass
    
        # my_test_speedy(senti_dict,senti_marisa,ref_dict)

        # # build it out here
        # ref_word_vec = senti_marisa.wordVecify(ref_dict)
        # ref_word_vec_stopped = senti_marisa.stopper(ref_word_vec,stopVal=stopVal)
        # comp_word_vec = senti_marisa.wordVecify(comp_dict)
        # comp_word_vec_stopped = senti_marisa.stopper(comp_word_vec,stopVal=stopVal)        
        # shiftHtml(senti_marisa.scorelist, senti_marisa.wordlist, ref_word_vec_stopped, comp_word_vec_stopped, "test-shift-{0}.html".format(senti_dict.title),corpus=senti_marisa.corpus)
        # shiftHtml(senti_marisa.scorelist, senti_marisa.wordlist, ref_word_vec, comp_word_vec, "test-shift-titles.html".format(senti_dict.title),customTitle=True,title="Insert title here",ref_name="bananas",comp_name="apples")

def load_26():
    all_sentiment_dictionaries = [LabMT(),
                                  ANEW(),
                                  LIWC07(),
                                  MPQA(),
                                  OL(),
                                  WK(),
                                  LIWC01(),
                                  LIWC15(),
                                  PANASX(),
                                  Pattern(),
                                  SentiWordNet(),
                                  AFINN(),
                                  GI(),
                                  WDAL(),
                                  EmoLex(),
                                  MaxDiff(),
                                  HashtagSent(),
                                  Sent140Lex(),
                                  SOCAL(),
                                  SenticNet(),
                                  Emoticons(),
                                  SentiStrength(),
                                  VADER(),
                                  Umigon(),
                                  USent(),
                                  EmoSenticNet()]
    # MaxDiff(),HashtagSent(),
    # SASA(),WNA(),SANN()
    return all_sentiment_dictionaries

def write_table(all_sentiment_dictionaries):
    for sentiment_dictionary in all_sentiment_dictionaries:
        sentiment_dictionary.computeStatistics(0.0)

    table_template = Template(r'''{\scriptsize
  \begin{tabular*}{\linewidth}{ l | l | l | l | l | l}
  %% \begin{tabular*}{l}{ l | l | l | l | l | l | l | l | l | l}
    \hline
    Dictionary & \# Entries & Range & Construction & License & Ref.\\
    \hline
    \hline{% for sentiment_dictionary in all_sentiment_dictionaries %}{% if loop.index is equalto 7 %}
    \hline{% endif %}
    {{ sentiment_dictionary.title }} & {{ sentiment_dictionary.n_total | int }} & {{ sentiment_dictionary.score_range_str }} & {{ sentiment_dictionary.construction_note }} & {{ sentiment_dictionary.license }} & \cite{ {{- sentiment_dictionary.citation_key -}} }\\{% endfor %}
\end{tabular*}}
''')

    f = open("tex/all-dictionary-table-automatic-short.tex","w")
    f.write(table_template.render({"all_sentiment_dictionaries": all_sentiment_dictionaries}))
    f.close()
    
    f = open("tex/all-dictionary-table-automatic.tex","w")
    f.write(r"""  {\scriptsize
  \begin{tabular*}{\linewidth}{ l | l | l | l | l | l | l | l | l | l}
    \hline
    Dictionary & \# Fixed & \# Stems & Total & Range & \# Pos & \# Neg & Construction & License & Ref.\\
    \hline
    \hline
""")
    
    for i,sentiment_dictionary in enumerate(all_sentiment_dictionaries):
        print(i+1,sentiment_dictionary.title)
        if i==6:
            f.write("\\hline\n")
        f.write("    {0} & {1:.0f} & {2:.0f} & {3:.0f} & {4} & {5:.0f} & {6:.0f} & {7} & {8} & \\cite{{{9}}}\\\\\n".format(sentiment_dictionary.title,
                                                            sentiment_dictionary.n_fixed,
                                                            sentiment_dictionary.n_stem,
                                                            sentiment_dictionary.n_total,
                                                            sentiment_dictionary.score_range_str,
                                                            sentiment_dictionary.n_pos,
                                                            sentiment_dictionary.n_neg,
                                                            sentiment_dictionary.construction_note,
                                                            sentiment_dictionary.license,
                                                            sentiment_dictionary.citation_key))
    f.write("""  \end{tabular*}}
""")
    f.close()
    
    f = open("tex/all-dictionaries-list-description.tex","w")
    f.write(r"""\begin{description} \itemsep1pt \parskip1pt \parsep0pt
""")
    for i,sentiment_dictionary in enumerate(all_sentiment_dictionaries):
        f.write("    \\item[{0}] --- {1} \\cite{{{2}}}.\n".format(sentiment_dictionary.title,
                                                            sentiment_dictionary.note,
                                                            sentiment_dictionary.citation_key))
    f.write(r"""  \end{description}
""")
    f.close()
    
def test_speedy_all():
    """Test all of the speedy dictionaries on scoring some dict of words."""

    test_all_features()
    all_sentidicts = load_26()
    write_table(all_sentidicts)
    speedy_dict_marisa_test(all_sentidicts)
    # cleanup()
    
def cleanup():
    '''Remove all test files.'''
    print("removing all test files generated...go comment the \"cleanup()\" call to keep them")
    subprocess.call("\\rm -r test-* static",shell=True)

def test_all_features():
    f = codecs.open("test/example-tweets.json" ,"r", "utf8")
    i = 0
    for line in f:
        tweet = loads(line)
        tweet_features = all_features(tweet['text'],tweet['user']['id'],tweet['id'],-1)
        # print(tweet['text'])
        # print(tweet_features)
        
    f.close()
    
    # f = open("example_grams.json" ,"r", "utf8")
    # for line in f:
    #     gram = loads(line)
    #     gram_features = all_features(gram['text'],gram['user']['id'],-1,gram['id'])
    # f.close()

