from labMTsimple.storyLab import (
    emotionFileReader,
    emotion,
    stopper,
    emotionV,
    shiftHtml,
)
import codecs  # handle utf8

if __name__ == '__main__':
    lang = 'english'
    labMT, labMTvector, labMTwordList = emotionFileReader(stopval=0.0, lang=lang, returnVector=True)

    ## take a look at these guys
    print('the word laughter in the hash has the data:')
    print(labMT['laughter'])
    print('the top 5 scores, and those words, are:')
    print(labMTvector[0:5])
    print(labMTwordList[0:5])

    ## test shift a subsample of two twitter days
    f = codecs.open("data/18.01.14.txt", "r", "utf8")
    saturday = f.read()
    f.close()

    f = codecs.open("data/21.01.14.txt", "r", "utf8")
    tuesday = f.read()
    f.close()

    ## compute valence score
    print('computing happiness...')

    ## compute valence score and return frequency vector for generating wordshift
    saturdayValence, saturdayFvec = emotion(saturday, labMT, shift=True, happsList=labMTvector)
    tuesdayValence, tuesdayFvec = emotion(tuesday, labMT, shift=True, happsList=labMTvector)

    ## but we didn't apply a lens yet, so stop the vectors first
    tuesdayStoppedVec = stopper(tuesdayFvec, labMTvector, labMTwordList, stopVal=1.0)
    saturdayStoppedVec = stopper(saturdayFvec, labMTvector, labMTwordList, stopVal=1.0)

    ## and then apply a lens
    saturdayValence = emotionV(saturdayStoppedVec, labMTvector)
    tuesdayValence = emotionV(tuesdayStoppedVec, labMTvector)

    print('the valence of {} is {:.5}'.format('saturday', saturdayValence))
    print('the valence of {} is {:.5}'.format('tuesday', tuesdayValence))

    writeCsv = False
    if writeCsv:
        f = codecs.open("saturdayFvec.csv", "w", "utf8")
        f.write(f'{saturdayFvec[0]:.0f}')
        for i in range(1, len(saturdayFvec)):
            f.write("\n")
            f.write(f'{saturdayFvec[i]:.0f}')
        f.close()

        f = codecs.open("tuesdayFvec.csv", "w", "utf8")
        f.write(f'{tuesdayFvec[0]:.0f}')
        for i in range(1, len(tuesdayFvec)):
            f.write("\n")
            f.write(f'{tuesdayFvec[i]:.0f}')
        f.close()

        f = codecs.open("labMTvec.csv", "w", "utf8")
        f.write(f'{labMTvector[0]:.8f}')
        for i in range(1, len(labMTvector)):
            f.write("\n")
            f.write(f'{labMTvector[i]:.8f}')
        f.close()

        f = codecs.open("labMTwords.csv", "w", "utf8")
        f.write(labMTwordList[0])
        for i in range(1, len(labMTwordList)):
            f.write("\n")
            f.write(labMTwordList[i])
        f.close()

    filename = "example-002-shift.html"
    shiftHtml(labMTvector, labMTwordList, tuesdayStoppedVec, saturdayStoppedVec, filename)
