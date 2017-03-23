# note: nose2 will run all functions that begin with test

from sentidict.utils import *
from sentidict.dictionaries import *
from sentidict.functions import *
from sentidict.wordshifts import *
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

ref_dict = {"the": 1, "dude": 1, "abides": 1, "laughs": 1}
comp_dict = {"the": 1, "dude": 1, "does": 1, "not": 1, "abide": 1}

def shiftHtmlJupyter_test(all_sentidicts):
    for my_sentidict in all_sentidicts[:1]:
        ref_word_vec = my_sentidict.wordVecify(ref_dict)
        ref_word_vec_stopped = my_sentidict.stopper(ref_word_vec,stopVal=1.0)
        comp_word_vec = my_sentidict.wordVecify(comp_dict)
        comp_word_vec_stopped = my_sentidict.stopper(comp_word_vec,stopVal=1.0)
        shiftHtmlJupyter(my_sentidict.scorelist,
                         my_sentidict.wordlist,
                         ref_word_vec_stopped,
                         comp_word_vec_stopped,
                         "test-jupyter-wordshift-{}.html".format(my_sentidict.title))

def shiftHtml_test(all_sentidicts):
    for my_sentidict in all_sentidicts[:1]:
        ref_word_vec = my_sentidict.wordVecify(ref_dict)
        ref_word_vec_stopped = my_sentidict.stopper(ref_word_vec,stopVal=1.0)
        comp_word_vec = my_sentidict.wordVecify(comp_dict)
        comp_word_vec_stopped = my_sentidict.stopper(comp_word_vec,stopVal=1.0)
        shiftHtml(my_sentidict.scorelist,
                         my_sentidict.wordlist,
                         ref_word_vec_stopped,
                         comp_word_vec_stopped,
                         "test-wordshift-{}.html".format(my_sentidict.title))

def shiftHtmlPreshifted_test(all_sentidicts):
    for my_sentidict in all_sentidicts[:1]:
        ref_word_vec = my_sentidict.wordVecify(ref_dict)
        ref_word_vec_stopped = my_sentidict.stopper(ref_word_vec,stopVal=1.0)
        comp_word_vec = my_sentidict.wordVecify(comp_dict)
        comp_word_vec_stopped = my_sentidict.stopper(comp_word_vec,stopVal=1.0)
        shiftHtmlPreshifted(my_sentidict.scorelist,
                         my_sentidict.wordlist,
                         ref_word_vec_stopped,
                         comp_word_vec_stopped,
                         "test-wordshift-preshifted-{}.html".format(my_sentidict.title))

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

def dict_vs_marisa_test(my_senti_dict,my_senti_marisa,test_dict,v=True):
    """Make sure that the dict and the marisa implementations agree."""

    print("loading {0}".format(my_senti_dict.title))
    
    dict_score = my_senti_dict.score(test_dict)
    dict_word_vec = my_senti_dict.wordVecify(test_dict)
    marisa_score = my_senti_marisa.score(test_dict)
    marisa_word_vec = my_senti_marisa.wordVecify(test_dict)
    if v:
        print(dict_score)
        print(marisa_score)
    
    if my_senti_dict.stems:
        assert len(dict_word_vec) == len(marisa_word_vec)
        if v:
            # print(dict_word_vec,marisa_word_vec)
            print(my_senti_dict.fixedwords[0])
            print(my_senti_marisa.fixedwords[0])
            print(my_senti_dict.stemwords[0])
            print(my_senti_marisa.stemwords[0])
    else:
        assert abs(dict_score-marisa_score) < TOL
        diff = dict_word_vec - marisa_word_vec
        if v:
            # print(dict_word_vec,marisa_word_vec)
            print(my_senti_dict.fixedwords[0])
            print(my_senti_marisa.fixedwords[0])
            print(len(my_senti_dict.stemwords))
            print(len(my_senti_marisa.stemwords))
        assert (dict_word_vec == marisa_word_vec).all()

    # let's find the index of the word happy in each
    # this is really a word-by-word test, because
    # of the stem matching
    word = "happy"
    print("checking on {0}".format(word))
    happy_dict = {word: 1}
    happy_vec = my_senti_marisa.wordVecify(happy_dict)
    if my_senti_marisa.matcherTrieBool(word):
        print("happy is in the list")
        assert sum(happy_vec) == 1
        happy_index = list(happy_vec).index(1)
        if v:
            print("index of the happy match: {0}".format(happy_index))
            # 3,30,222,2221,2818,5614    
            print("length of fixed words: {0}".format(len(my_senti_marisa.fixedwords)))
            print("count in word vec of happy: {0}".format(marisa_word_vec[happy_index]))
            print("count in the test:")
            print(test_dict["happy"])
            print(test_dict["happyy"])
            print(test_dict["happyyy"])
        # checked that no dictionaries match anything beyond happy in the stems
        # so, they must match it fixed
        # => check it right against the straight count
        assert test_dict[word] == marisa_word_vec[happy_index]
        if happy_index > len(my_senti_marisa.fixedwords):
            print("matched by a stem")
            print(my_senti_marisa.stemwords[happy_index-len(my_senti_marisa.fixedwords)])
        else:
            print("matched by a fixed word")
            print(my_senti_marisa.fixedwords[happy_index])
    else:
        print("{} is *NOT* in the list".format(word))

    word = "abide"
    print("checking on {0}".format(word))
    happy_dict = {word: 1}
    happy_vec = my_senti_marisa.wordVecify(happy_dict)
    if my_senti_marisa.matcherTrieBool(word):
        my_index = list(happy_vec).index(1)
        print(my_index)
        print(marisa_word_vec[my_index])
        print("the dude abides!")
    else:
        print("the dude does not abide by this word list")
        
def test_dict_vs_marisa_all():
    # ref_dict = open_codecs_dictify("examples/data/18.01.14.txt")
    # comp_dict = open_codecs_dictify("examples/data/21.01.14.txt")
    ref_dict = {"the": 1, "dude": 1, "abides": 1, "happy": 5, "happyy": 2, "happyyy": 1}
    comp_dict = {"the": 1, "dude": 1, "abides": 1, "happy": 1, "happyy": 0, "happyyy": 0}

    all_sentidicts = load_26(datastructure="dict",v=True)
    all_sentimarisas = load_26(datastructure="marisa_trie",v=True)

    for senti_dict,senti_marisa in zip(all_sentidicts,all_sentimarisas):
        dict_vs_marisa_test(senti_dict,senti_marisa,ref_dict)

def test_extended_features():
    f = codecs.open("test/example-tweets.json" ,"r", "utf8")
    i = 0
    for line in f:
        tweet = loads(line)
        tweet_features = all_features(tweet['text'],tweet['user']['id'],tweet['id'],-1)
        assert len(tweet_features) == 75
    f.close()

def test_speedy_all():
    """Test all of the speedy dictionaries on scoring some dict of words."""
    all_sentidicts = load_26()
    assert len(all_sentidicts) == 26
    write_tables(all_sentidicts)
    shiftHtmlJupyter_test(all_sentidicts)
    shiftHtml_test(all_sentidicts)
    shiftHtmlPreshifted_test(all_sentidicts)
    # cleanup()

def cleanup():
    '''Remoove all test files.'''
    print("removing all test files generated...go comment the \"cleanup()\" call to keep them")
    subprocess.call("\\rm -r test-* static *.tex",shell=True)

class Dummy(sentiDict):
    title="dummy"
    url="lmgtfy.com"
    note="note"
    license="license"
    construction_note="const note"
    citation_key="citekey"
    citation="""@article{myarticle,}"""
    stems=False
    center=5.0
    score_range_type="integer"

    def loadDict(self,bananas,lang):
        return {"happy": (0,5.5), "sad": (1,2.5),}

def test_init():
    d = Dummy()
    d = Dummy(v=True)
    assert d.datastructure == "dict"
    d = Dummy(v=True,datastructure="auto")
    assert d.datastructure == "dict"
    d = Dummy(v=True,datastructure="marisatrie")
    assert d.datastructure == "marisatrie"
    d = Dummy(v=True,datastructure="dict")
    assert d.datastructure == "dict"    


    
def test_init_stems():
    
    class Dummy2(Dummy):
        stems=True
        def loadDict(self,bananas,lang):
            return {"happy": (1,5.5), "sad*": (0,2.5),}
        
    d = Dummy2()
    d = Dummy2(v=True)
    assert d.datastructure == "marisatrie"
    d = Dummy2(v=True,datastructure="auto")
    assert d.datastructure == "marisatrie"
    d = Dummy2(v=True,datastructure="marisatrie")
    assert d.datastructure == "marisatrie"
    d = Dummy2(v=True,datastructure="dict")
    assert d.datastructure == "dict"
    assert len(d.stemwords) == 1
    assert len(d.fixedwords) == 1
    assert d.fixedwords[0] == "happy"
    assert d.stemwords[0] == "sad"
    assert len(d.data) == 2
    d = Dummy2(v=True,datastructure="dict",stopVal=.5)
    assert len(d.data) == 2
    d = Dummy2(v=True,datastructure="dict",stopVal=.501)
    assert len(d.data) == 1
    assert "sad*" in d.data
    
    class Dummy3(Dummy2):
        center=2.5
        
    d = Dummy3(v=True,datastructure="dict",stopVal=0.0)
    assert len(d.data) == 2
    assert "sad*" in d.data
    d = Dummy3(v=True,datastructure="dict",stopVal=1.0)
    assert len(d.data) == 1
    assert "happy" in d.data
    
    d = Dummy2(v=True,datastructure="auto",stopVal=0.0)
    assert d.matcherTrieBool("saddd")
    assert d.matcherTrieBool("sad")
    assert d.matcherTrieBool("happy")
    assert d.matcherBool("saddd")
    assert d.matcherBool("sad")
    assert d.matcherBool("happy")

    d = Dummy2(v=True,datastructure="dict",stopVal=0.0)
    assert not d.matcherBool("saddd")
    # expected
    assert not d.matcherBool("sad")
    # this seems to be a problem...need to make sure to use tries for this method!
    # warning is raised by the method
    assert d.matcherBool("sad*")
    assert d.matcherBool("happy")

class Dummy4(Dummy):
    def loadDict(self,bananas,lang):
        return {"happy": (0, 6.),"remove": (1, 8.),"niggas": (2, 8.) ,"neutral": (3, 5.)}

def test_sentidict_stopper():
    d = Dummy4()
    test_f = [1,1,1,1]
    # print(d.scorelist)
    # print(d.wordlist)
    assert (d.stopper(test_f) == np.array([1,1,0,0])).all()
    assert (d.stopper(test_f,ignore=["remove"]) == np.array([1,0,0,0])).all()
    assert (d.stopper(test_f,ignore=["remove"],stopVal=2.0) == np.array([0,0,0,0])).all()
    assert (d.stopper(test_f,ignore=["remove"],stopVal=0.0) == np.array([1,0,0,1])).all()
    class Dummy5(Dummy4):
        center=7.0
    d = Dummy5()        
    assert (d.stopper(test_f,stopVal=1.0) == np.array([1,1,0,1])).all()
    assert (d.stopper(test_f,stopVal=2.0) == np.array([0,0,0,1])).all()

def test_wordVecify():
    ref_dict = {"the": 1, "dude": 1, "abides": 1, "happy": 5, "happyy": 2, "happyyy": 1}
    d = Dummy4()
    assert (d.wordVecify({}) == zeros(4)).all()
    assert (d.wordVecify(ref_dict) == array([5,0,0,0])).all()
    # add stems to the mix
    class Dummy6(Dummy):
        stems = True
        def loadDict(self,bananas,lang):
            return {"happy*": (0, 6.),"remove": (1, 8.),"niggas": (2, 8.) ,"neutral": (3, 5.)}
    d = Dummy6(v=True)
    assert (d.wordVecify({}) == zeros(4)).all()
    assert (d.wordVecify(ref_dict) == array([8,0,0,0])).all()

def test_score():
    ref_dict = {"neutral": 1, "dude": 1, "niggas": 2, "happy": 5, "happyy": 2, "happyyy": 1}
    d = Dummy4()
    assert d.score({}) == 5.0
    assert d.score({},center=-1) == -1
    fixed_score = d.score(ref_dict)
    assert fixed_score != 5.0
    # add stems to the mix
    class Dummy6(Dummy):
        stems = True
        def loadDict(self,bananas,lang):
            return {"happy*": (0, 6.),"remove": (1, 8.),"niggas": (2, 8.) ,"neutral": (3, 5.)}
    d = Dummy6(v=True)
    assert d.score({}) == 5.0
    assert d.score({},center=-1) == -1
    # should move closer to 6
    assert np.abs(d.score(ref_dict) - 6) < np.abs(fixed_score - 6)
    # it's also not blocking the word list...
    ref_dict = {"neutral": 1, "dude": 1, "niggas": 8, "happy": 5, "happyy": 0, "happyyy": 0}
    assert np.abs(d.score(ref_dict) - 8) < np.abs(fixed_score - 8)

    


