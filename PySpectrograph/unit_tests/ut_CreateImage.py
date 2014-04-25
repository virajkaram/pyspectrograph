"""Test CreateImage is a task to produce a 2D image generated by a spectrograph

HISTORY
20100601 SMC  First written by SM Crawford

Limitations:

"""
import os 

import math
import pyfits
import numpy as np
from PySpectrograph.Spectrograph.CreateImage import *

from PySpectrograph.Spectra.Spectrum import *
from PySpectrograph.Models import RSSModel


from pylab import *

inimg='fmbxpP200610180009.fits'
infile='Xe.dat'
outfile='out.fits'

def test_CreateImage():    

   #read in the data
   hdu=pyfits.open(inimg)
   im_arr=hdu[1].data
   hdu.close()

   #set up the spectrum
   stype='line'
   w,s=np.loadtxt('Xe.dat', usecols=(0,1),unpack=True)
   spec=Spectrum(w, s, wrange=[4000, 5000], dw=0.1, stype='line')

   #set up the spectrograph
   dx=2*0.015*8.169
   dy=2*0.015*0.101
   #set up the spectrograph
   #rssmodel=RSSModel.RSSModel(grating_name='PG0900', gratang=13.625, camang=27.25, slit=1.0, xbin=2, ybin=2, xpos=dx, ypos=dy)
   rssmodel=RSSModel.RSSModel(grating_name='PG3000', gratang=43.625, camang=87.25, slit=2.0, xbin=2, ybin=2, xpos=dx, ypos=dy)

   rssmodel.set_camera(name='RSS', focallength=330.0)
   rss=rssmodel.rss

   #set up the outfile
   if os.path.isfile(outfile): os.remove(outfile)
   
   arr=im_arr.copy()
   arr=CreateImage(spec, rss)
   arr=arr*im_arr.max()/spec.flux.max()
   writeout(arr, outfile)

test_CreateImage()
