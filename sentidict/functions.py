from .utils import *
from .dictionaries import *

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

