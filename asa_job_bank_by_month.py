#Scrapes ASA job market postings and lists positions by month
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
        sleep(1)

#download the files
url="http://jobbank.asanet.org/jobbank/job_detail.cfm"



#Loop through files, downloading the ones I don't have.


offers_benefits={}
no_benefits={}
pro_discrimination={}
years={}
months={}
for jobid in range(8450,5,-1):
    request=url+'?jobid=%s' % jobid
    filename='asa_jobid_%s.html' % jobid
    download(request,filename)
    text=file(filename,'rb').read()
    listing_active=re.findall('Listing Active<\/strong>:<br><\/td>\r\n<td class="bodycopy">(.*?) to ',text,re.DOTALL|re.MULTILINE)
    if len(listing_active)>0 and ('assistant professor' in text.lower() and 'tenure' in text.lower() ):
        month=int(listing_active[0].split('/')[0])
        if year not in months:
            months[year]={}
        try:
            months[year][month]+=1
        except:
            months[year][month]=1
    elif len(listing_active)>0 and ('assistant professor' in text.lower() ):
        print jobid





fo = open("assist.csv", "wb")
fo.write('year,month,count\n')
for year in months:
    for month in months[year]:
        fo.write('%s,%s,%s\n' % (year,month,months[year][month]))