#!/usr/bin/env python

"""
Example usage:
python fold2stl.py --phase=0.3 --height=200 --smooth=1 --subtract --tmax=500 --text --fontsize=16 --fontname="/Library/Fonts/Arial Black.tt" J0034-0721.rf

"""



from astropy.io import fits
import sys,os
import scipy.misc
from stl_tools import numpy2stl
import numpy
# https://github.com/thearn/stl_tools
from optparse import OptionParser,OptionGroup
from scipy.ndimage import gaussian_filter
from PIL import ImageDraw, ImageFont
from PIL import Image

_version_=0.1


######################################################################
def text2array(text, fontname=None, fontsize=16):
    if fontname is None:
        font=ImageFont.load_default()
    else:
        try:
            font = ImageFont.truetype(fontname, fontsize)
        except:
            sys.stderr.write('Unable to find font %s\n' % fontname)
            font=ImageFont.load_default()

    img = Image.new('RGB', (200, 100))
    dr = ImageDraw.Draw(img)
    dr.text((0, 0), text, fill=(255, 0, 0), font=font)
    text_width, text_height = dr.textsize(text, font=font)
    img = Image.new('RGB', (text_width+10, text_height+10),(255,255,255))
    dr = ImageDraw.Draw(img)
    dr.text((5, 5), text, fill=(128, 128, 128), font=font)
    textdata=numpy.array(img).mean(axis=2)
    return textdata

######################################################################
def fold2stl(filename, height=0.2, phase=1, size=1, smooth=0, subtract=False, tmax=None, dotext=False,
             fontsize=16, fontname=None):
    """
    stlfile=fold2stl(filename, height=0.2, phase=1, size=1, smooth=0, subtract=False, tmax=None, dotext=False,
             fontsize=16, fontname=None)
    """
    
    try:
        f=fits.open(filename)
    except Exception,e:
        sys.stderr.write('Unable to open file %s: %s\n' % (filename,e))
        return None
    

    rawdata=(f[-1].data['DATA'].squeeze().T*f[-1].data['DAT_SCL']+f[-1].data['DAT_OFFS']).T
    if subtract:
        background=rawdata.mean(axis=1)
        rawdata=(rawdata.T-background).T

    rawdata=(rawdata-rawdata.min())/(rawdata.max()-rawdata.min())
    
    print 'Raw data has size (%d,%d)' % rawdata.shape
    if size != 1:
        data=scipy.misc.imresize(rawdata, float(size)).astype(rawdata.dtype)
        print "Resized to (%d,%d)" % data.shape
    else:
        data=rawdata
    if smooth>0:
        data=gaussian_filter(data, smooth)
    summeddata=data.mean(axis=0)
    x=numpy.linspace(0,1,len(summeddata))
    phasemax=x[summeddata==summeddata.max()]
    print 'Identified pulse maximum at phase=%.2f' % phasemax
    if phase<1:
        data=data[:,numpy.abs(x-phasemax)<phase/2]
        print 'Restricted to phase window +/- %.2f around max; size is now %s' % (phase/2,data.shape)
    outfile=os.path.splitext(filename)[0] + '.stl'

    if tmax is not None and tmax>0:
        data=data[:tmax]


    if dotext:
        text='Source: %s\nTelescope: %s\nObserver: %s\nDate: %s' % (f[0].header['SRC_NAME'],
                                                                    f[0].header['TELESCOP'],
                                                                    f[0].header['OBSERVER'],
                                                                    f[0].header['DATE-OBS'].split('T')[0])    
        textarray=text2array(text, fontsize=fontsize, fontname=fontname)/255
        data[:textarray.shape[1],:textarray.shape[0]]*=numpy.fliplr(textarray.T)
    
    if os.path.exists(outfile):
        os.remove(outfile)
    numpy2stl(data, outfile, scale=height, solid=True)
    print 'Wrote %s' % outfile
    return outfile

######################################################################
def main():

    usage="Usage: %prog [options]\n"
    parser = OptionParser(usage=usage,version=_version_)
    
    parser.add_option('--height',dest="height",default=0.2,
                      type=float,
                      help="Height ratio [default=%default]")
    parser.add_option('--phase',dest='phase',default=1,
                      type=float,
                      help="Phase window around peak [default=%default]")
    parser.add_option('--size',dest='size',
                      default=1.0,
                      type=float,
                      help='Size ratio of output [default=%default]')
    parser.add_option('--smooth',dest='smooth',default=0,
                      type=float,
                      help='Smoothing kernel [default=%default]')
    parser.add_option('--subtract',dest='subtract',default=False,
                      action="store_true",
                      help='Subtract background?')
    parser.add_option('--tmax',dest='tmax',default=None,
                      type=int,
                      help='Max pulse number [default=%default]')
    parser.add_option('--text',dest='text',default=False,
                      action="store_true",
                      help='Include text?')
    parser.add_option('--fontsize',dest='fontsize',default=16,type='int',
                      help="Font size for text [default=%default]")
    parser.add_option('--fontname',dest='fontname',default=None,
                      type='str',
                      help="Font name for text")
    
    (options, args) = parser.parse_args()
    if len(args)==0:
        sys.stderr.write("Must supply >=1 FITS files\n")
        sys.exit(-1)
    for file in args:
        if not os.path.exists(file):
            sys.stderr.write('File %s does not exist\n' % file)
            sys.exit(-1)
        if options.text and (options.fontname is not None and not os.path.exists(options.fontname)):
            sys.stderr.write('Font file %s does not exist; will use default\n' % options.fontname)
            options.fontname=None
        out=fold2stl(file, height=options.height,
                     phase=options.phase,
                     size=options.size,
                     smooth=options.smooth,
                     subtract=options.subtract,
                     tmax=options.tmax,
                     dotext=options.text,
                     fontsize=options.fontsize,
                     fontname=options.fontname)
        
        
######################################################################

if __name__=="__main__":
    main()
