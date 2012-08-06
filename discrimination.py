#Silly little file for scraping the ASA Job Bank
#Neal Caren
#neal.caren@unc.edu
#August 2, 2012

import urllib
from time import sleep
import re


def download(url,filename):
    try:
        x=open(filename,'rb')
    except:
        urllib.urlretrieve(url,filename)
        sleep(.5)

#download the files
url="http://jobbank.asanet.org/jobbank/job_detail.cfm"



#Loop through files, downloading the ones I don't have.
descriptions=[]
for jobid in range(8440,8250,-1):
    request=url+'?jobid=%s' % jobid
    filename='asa_jobid_%s.html' % jobid
    download(request,filename)
    text=file(filename,'rb').read()
    discrimination=re.findall('Discrimination Policy<',text,re.DOTALL|re.MULTILINE)
    print discrimination

