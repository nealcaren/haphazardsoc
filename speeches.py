# !/usr/local/bin/python
# -*- coding: utf8 -*-

import re
from string import punctuation
import urllib2


def analyze(url):
    #Function to count how many times something appears in ()
    speeches=load_times(url)
    reactions=re.findall('\((.*?)\)',speeches.lower())
    reaction_dict={'applause':0,'boos':0,'cheers':0,'chuckles':0,'chanting':0,'laughter':0,'chanting':0}
    for reaction in reactions:
        for r in reaction_dict:
            if r in reaction:
                reaction_dict[r]+=1
    reaction_dict['laughter']=reaction_dict['laughter']+reaction_dict['chuckles']
    del reaction_dict['chuckles']
    for reaction in reaction_dict:
        reaction_dict[reaction]=1000*reaction_dict[reaction]/float(len(speeches.split()))
    return reaction_dict




def load_times(url):
    #Function to pull out the text of the transcripts from the New York Times
    raw=urllib2.urlopen(url)
    raw=raw.read()
    start=raw.index('[')
    end=raw.index(']')
    speeches=raw[start:end]
    return speeches


#Get both parties
republican=analyze('http://graphics8.nytimes.com/packages/js/newsgraphics/2012/0823-convention-speeches/data.js')
democratic=analyze('http://graphics8.nytimes.com/newsgraphics/2012/09/04/convention-speeches/0aaaea5489031beaef112440855ff471a40cacda/index.js')

#Combine dictionaries to create sort order
combo={item:republican[item]+democratic[item] for item in democratic}

#Print results
print 'Emotion         Rep     Dem'

demtotal=0
reptotal=0
for reaction in sorted(combo,key=combo.get, reverse=True):
    fill=' '*(10-len(reaction))
    rp=reaction[0].upper()+reaction[1:]
    print '%s%s\t%.2f\t%.2f' % (rp,fill,republican[reaction],democratic[reaction])
    demtotal+=democratic[reaction]
    reptotal+=republican[reaction]
print 'D',demtotal
print 'R',reptotal