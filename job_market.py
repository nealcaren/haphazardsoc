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

def clean(line):
    ugly_html=['\xe2\x80\xa2\t','<br>\n','<br>\n<br>\n','\xe2\x80\x99','sociology','applicants','candidates','College','Sociology','Department','University','applications','position','tenure-track','Assistant Professor',
               'assistant','professor','university']
    for crap in ugly_html:
        line=line.replace(crap,'')
    return line

#download the files
url="http://jobbank.asanet.org/jobbank/job_detail.cfm"



#Loop through files, downloading the ones I don't have.
descriptions=[]
for jobid in range(8440,8250,-1):
    request=url+'?jobid=%s' % jobid
    filename='asa_jobid_%s.html' % jobid
    download(request,filename)
    text=file(filename,'rb').read()
    description=re.findall('Job Description<\/strong>:<br><\/td>\r\n<td class="bodycopy">\r\n\r\n(.*?)\r\n<\/td',text,re.DOTALL|re.MULTILINE)[0]
    description=description.split('<br>')
    description=[line for line in description if len(line)>30][:3] #keeping only the first three paragraphs
    description=' '.join(description)
    descriptions.append(description)

descriptions=[clean(description) for description in descriptions if 'tenure' in description and 'ssistant' in description] #keep only junion jobs

#Get rid of duplicates
dupe_check={}
deduped=[]
for d in descriptions:
    if d not in dupe_check:
        deduped.append(d)
    dupe_check[d]=True

print 'Count of jobs:',len(deduped)
print 'Criminal:',len([description for description in descriptions if 'riminal' in description])

#output the results
outfile=file('descriptions.txt', 'wb')
outfile.write("\n".join(deduped))




