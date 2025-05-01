from jinja2 import Template
from .utils import openWithPath, listify_quick
from .dictionaries import (
    LabMT,
    WK,
    ANEW,
    MPQA,
    OL,
    LIWC01,
    GI,
    LIWC07,
    EmoLex,
    LIWC15,
    PANASX,
    Sent140Lex,
    SOCAL,
    USent,
    MaxDiff,
    Umigon,
    VADER,
    AFINN,
    Emoticons,
    SentiWordNet,
    LIWC,
    Pattern,
    WDAL,
    SenticNet,
    HashtagSent,
    EmoSenticNet,
    SentiStrength,
)
from numpy import zeros, array


def all_features(rawtext, uid, tweet_id, gram_id):
    """Return the feature vector for a given tweets.

    Be careful about indexing!
    Assuming here that we're taking in text of the tweet/gram"""

    my_LIWC_stopped = LIWC(stopVal=0.5)
    my_LIWC = LIWC()
    my_LabMT = LabMT(stopVal=1.0)
    my_ANEW = ANEW(stopVal=1.0)

    # create  simple list for the result
    result = zeros(75)
    # the first field, tableID, is not included (leaving 75)
    result[0] = tweet_id
    result[1] = gram_id
    result[2] = uid

    words = listify_quick(rawtext)
    word_dict = dict()
    for word in words:
        if word in word_dict:
            word_dict[word] += 1
        else:
            word_dict[word] = 1
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
    all_features = zeros(len(my_LIWC.data["happy"]) - 2)
    for word in my_LIWC.data:
        all_features += array(my_LIWC.data[word][2:]) * my_word_vec[my_LIWC.data[word][0]]
    for i, score in enumerate(all_features):
        result[10 + i] = all_features[i]

    return result


def load_26(datastructure="auto", stopVal=0.0, v=False):
    all_sentiment_dictionaries = [
        LabMT(datastructure=datastructure, stopVal=stopVal, v=v),
        ANEW(datastructure=datastructure, stopVal=stopVal, v=v),
        LIWC07(datastructure=datastructure, stopVal=stopVal, v=v),
        MPQA(datastructure=datastructure, stopVal=stopVal, v=v),
        OL(datastructure=datastructure, stopVal=stopVal, v=v),
        WK(datastructure=datastructure, stopVal=stopVal, v=v),
        LIWC01(datastructure=datastructure, stopVal=stopVal, v=v),
        LIWC15(datastructure=datastructure, stopVal=stopVal, v=v),
        PANASX(datastructure=datastructure, stopVal=stopVal, v=v),
        Pattern(datastructure=datastructure, stopVal=stopVal, v=v),
        SentiWordNet(datastructure=datastructure, stopVal=stopVal, v=v),
        AFINN(datastructure=datastructure, stopVal=stopVal, v=v),
        GI(datastructure=datastructure, stopVal=stopVal, v=v),
        WDAL(datastructure=datastructure, stopVal=stopVal, v=v),
        EmoLex(datastructure=datastructure, stopVal=stopVal, v=v),
        MaxDiff(datastructure=datastructure, stopVal=stopVal, v=v),
        HashtagSent(datastructure=datastructure, stopVal=stopVal, v=v),
        Sent140Lex(datastructure=datastructure, stopVal=stopVal, v=v),
        SOCAL(datastructure=datastructure, stopVal=stopVal, v=v),
        SenticNet(datastructure=datastructure, stopVal=stopVal, v=v),
        Emoticons(datastructure=datastructure, stopVal=stopVal, v=v),
        SentiStrength(datastructure=datastructure, stopVal=stopVal, v=v),
        VADER(datastructure=datastructure, stopVal=stopVal, v=v),
        Umigon(datastructure=datastructure, stopVal=stopVal, v=v),
        USent(datastructure=datastructure, stopVal=stopVal, v=v),
        EmoSenticNet(datastructure=datastructure, stopVal=stopVal, v=v),
    ]
    # MaxDiff(datastructure=datastructure,stopVal=stopVal,v=v),
    # HashtagSent(datastructure=datastructure,stopVal=stopVal,v=v),
    # SASA(datastructure=datastructure,stopVal=stopVal,v=v),
    # WNA(datastructure=datastructure,stopVal=stopVal,v=v),
    # SANN(datastructure=datastructure,stopVal=stopVal,v=v)
    return all_sentiment_dictionaries


def write_tables(sentiment_dictionaries):
    for sentiment_dictionary in sentiment_dictionaries:
        sentiment_dictionary.computeStatistics(0.0)

    table_template = Template(openWithPath("templates/table-short.tex", "r").read())

    f = open("all-dictionary-table-automatic-short.tex", "w")
    f.write(table_template.render({"all_sentiment_dictionaries": sentiment_dictionaries}))
    f.close()

    table_template = Template(openWithPath("templates/table.tex", "r").read())

    f = open("all-dictionary-table-automatic.tex", "w")
    f.write(table_template.render({"all_sentiment_dictionaries": sentiment_dictionaries}))
    f.close()

    template = Template(openWithPath("templates/descriptions.tex", "r").read())

    f = open("all-dictionaries-list-description.tex", "w")
    f.write(template.render({"all_sentiment_dictionaries": sentiment_dictionaries}))
    f.close()
