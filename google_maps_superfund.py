from __future__ import division
import random
import csv
import urllib
from time import sleep
import os

try:
    import Image
    combine=True
except:
    print "Images will not be combined. Trying installing Image http://www.pythonware.com/library/pil/handbook/image.htm"
    combine=False


sites=csv.reader(open('nc_superfund.csv', 'rb'))

#prepair blank picture for pasting picture
if combine:
    blank_image = Image.new("RGB", (800, 1200))
    x=0
    y=0

counter=1
for site in sites:
        #no id, so I make one up with 'counter'
        filename='superfund'+str(counter)+'.png'
        url='http://maps.googleapis.com/maps/api/staticmap?center=%s,%s&zoom=15&size=200x250&maptype=satellite&sensor=false&key=AIzaSyBqGbHrf6m8_6K671FLofG2sFV7sL4ECTc' % (site[0],site[1])

        #This script runs if you don't have Image. It just downloads the image if you don't have it.
        if combine==False:
            try:
                check=open(filename)
            except:
                urllib.urlretrieve(url,filename)
                square= Image.open(filename)

        #Otherwise, this script runs, which downloads the image and then adds it to the blank image
        #The downloads could be combined, but adding the ability to download but not process was a late addition.
        else:
            try:
                square= Image.open(filename)
            except:
                urllib.urlretrieve(url,filename)
                square= Image.open(filename)


            if os.path.getsize(filename)>4000: #Files smaller than the error message, which is more common in the streetview, but not unheard of it you zoom too much.
                square=square.crop((0,0,200,200)) #crop out the Google logo
                blank_image.paste(square, (x,y)) #paste into the blank image
                x+=200 #increment the x position in the picture
                if x>800: #but if you reach the edge, start over and move the y ahead
                    x=0
                    y+=200
        counter+=1

blank_image.save("superfund_nc.png")
