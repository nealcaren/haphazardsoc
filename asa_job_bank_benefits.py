#Scrapes ASA job market postings and lists positions by employment benefits
#Neal Caren
#neal.caren@unc.edu
#August 6, 2012

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


offers_benefits={}
no_benefits={}
pro_discrimination={}

for jobid in range(8450,8200,-1):
    request=url+'?jobid=%s' % jobid
    filename='asa_jobid_%s.html' % jobid
    download(request,filename)
    text=file(filename,'rb').read()
    date=re.findall('Date Position is Available(.*?)<\/tr>',text,re.DOTALL|re.MULTILINE)
    valid=False
    if len(date)>0:
        if '2013' in date[0]:
            valid=True

    if valid:
        company=re.findall('<strong>Company</strong>:<br><\/td>\r\n<td class="bodycopy">(.*?)\r\n<br',text,re.DOTALL|re.MULTILINE)[0]
        discrimination=re.findall('Discrimination Policy<\/strong>:<br><\/td>  \r\n<td class="bodycopy">\r\n\r\n\t(.*?)\r\n\r\n<br>',text,re.DOTALL|re.MULTILINE)[0]
        benefits=re.findall('Domestic Partner Benefits</strong>:<br><\/td>\r\n<td class="bodycopy">\r\n\r\n\t(.*?)\r\n\r\n<br',text,re.DOTALL|re.MULTILINE)[0]

        title=re.findall('Job Listing Title.*?"bodycopy">(.*?)<br',text,re.DOTALL|re.MULTILINE)[0]

    #    if 'This employer prohibits' not in discrimination:
    #        print jobid,company,discrimination
        if 'Central Connecticut State Univ.' not in company and 'TEST' not in title:
            if 'offers employment' in benefits:
                try:
                    offers_benefits[company].append(title)
                except:
                    offers_benefits[company]=[title]

            elif 'does not offer employment' in benefits:
                try:
                    no_benefits[company].append(title)
                except:
                    no_benefits[company]=[title]
            if 'does not prohibit' in discrimination:
                try:
                    pro_discrimination[company].append(title)
                except:
                    pro_discrimination[company]=[title]



print '\n\nEmployers offering benefits (n=%i)' % len(offers_benefits)
for school in sorted([school for school in offers_benefits]):
    print '%s (%s)' % (school,', '.join(list(set(offers_benefits[school]))))

print '\n\nEmployers not offering benefits (n=%i)' % len(no_benefits)
for school in sorted([school for school in no_benefits]):
    print '%s (%s)' % (school,', '.join(list(set(no_benefits[school]))))

print '\n\nEmployers discriminating (n=%i)' % len(pro_discrimination)
for school in sorted([school for school in pro_discrimination]):
    print '%s (%s)' % (school,', '.join(list(set(pro_discrimination[school]))))


