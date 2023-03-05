from nltk import DiscourseTester, CfgReadingCommand

dt = DiscourseTester(['Robot move a box',
                      'Robot move a red box',
                      'Robot move all boxes'],
                     CfgReadingCommand('./grammar/discourse.fcfg'))
dt.sentences()
dt.readings()
