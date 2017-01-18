from astropy.io import fits
import matplotlib as mpl,matplotlib.pyplot as plt
import sys,os
import scipy.misc
from scipy.ndimage import gaussian_filter
import numpy
from basic_units import cm, inch

##################################################
# colors used by the UWM RP lab laser cutters
# defined for different materials and thicknesses
# see https://uwm.edu/sarup/resources/shop-rp-lab/
##################################################
lightscorecolor='Cyan'
darkscorecolor='Magenta'
engravecolor='#ff7f00'
cutcolor={'chipboard': {0.03125: 'Red',
                        0.0625: 'Green',
                        0.125: 'Red'},
          'cardboard': {0.03125: 'Red',
                        0.0625: 'Green',
                        0.125: 'Red'},
          'museumboard': {0.03125: 'Red',
                          0.0625: 'Green'},
          'paper': {None: 'Red'},
          'cardstock': {None: 'Green'},
          'plywood': {0.0625: 'Red',
                      0.125: 'Green',
                      0.25: 'Yellow'},
          'basswood': {0.03125: 'Red',
                       0.0625: 'Green',
                       0.125: 'Yellow',
                       0.25: 'Blue'},
          'masonite': {0.125: 'Red'},
          'mdf': {0.25: 'Green',
                  0.375: 'Yellow',
                  0.5: 'Blue'},
          'hardwood': {0.03125: 'Red',
                       0.0625: 'Green',
                       0.125: 'Yellow',
                       0.25: 'Blue'},
          
          'acrylic': {0.125: 'Red',
                      0.1875: 'Green',
                      0.25: 'Yellow',
                      0.375: 'Blue'}}

##################################################
# class Colorset()
# deals with the appropriate colors for laser cutting
# in the UWM RPlab
##################################################
class Colorset():
    """
    c=Colorset(material, thickness)
    can then call:
    c.cut
    c.engrage
    c.lightscore
    c.darkscore
    
    """
    
    def __init__(self, material, thickness):
        self.material=material
        self.thickness=thickness
        self.lightscore=lightscorecolor
        self.darkscore=darkscorecolor
        self.engrave=engravecolor
        if not self.material in cutcolor.keys():
            raise KeyError(self.material)
        if not self.thickness in cutcolor[self.material].keys():
            raise KeyError(self.thickness)
        self.cut=cutcolor[self.material][self.thickness]
        
##################################################
# class LaserCutSheet()
# has methods for plotting pulsar data as laser-cut
#   sheet=LaserCutSheet(material_width, material_height, 'acrylic',0.125)
# 
# addplaque() makes discovery plaques identify who discovered a pulsar
#   sheet.addplaque(bestprof, pulsarname, P, DM, date, studentname, studentinstitution, telescope)
# 
# plotprofile() plots each individual pulse separately for cutting
#   sheet.plotprofile(psrfits, size)
#
# both methods can take a color as a named argument
# this will output a PDF of only a single color at a time (useful for layering)
##################################################                
class LaserCutSheet():
    def __init__(self, width, height, material, thickness, padding=0.25):
        # dimensions in inches
        self.material_width=width
        self.material_height=height
        self.padding=padding
        self.material=material
        self.thickness=thickness

        self.colors=Colorset(self.material,
                             self.thickness)

        plt.clf()
        self.figure=plt.gcf()
        self.figure.set_size_inches([self.material_width,
                                     self.material_height])
        

        self.axes=plt.axes([0,0,1,1],frameon=False)
        # this is just a guide    
        self.axes.plot([0,self.material_width,self.material_width,0,0],
                       [0,0,self.material_height,self.material_height,0],
                       color='k',xunits=inch,yunits=inch)
    ##################################################
    def addplaque(self,
                  bestprof,
                  pulsarname,
                  P,
                  DM,
                  date,
                  studentname,
                  studentinstitution,
                  telescope,
                  fontsize1=30,
                  fontsize2=48,
                  fontname='Vera',
                  row=0,
                  col=0,
                  color=None):

        width=(self.material_width-4*self.padding)/3
        height=width

        if color is None or color==self.colors.cut:
            self.axes.plot(self.padding+(self.padding+width)*col+numpy.array([0,width,width,0,0]),
                           self.padding+(self.padding+height)*row+numpy.array([0,0,height,height,0]),
                           color=self.colors.cut)
        xd,yd=numpy.loadtxt(bestprof,unpack=True)
        xd=(xd-xd.min())/(xd.max()-xd.min())
        yd=(yd-yd.min())/(yd.max()-yd.min())

        id=numpy.where(yd==yd.max())[0][0]
        yd=numpy.roll(yd,len(yd)/2-id)

        ystart1=self.padding+(self.padding+height)*row+0.25*(height)
        profileheight=0.5*height

        if color is None or color==self.colors.engrave:
            self.axes.plot(self.padding+(self.padding+width)*col+(width)*xd,
                           ystart1+profileheight*yd,
                           color=self.colors.engrave)
        if color is None or color==self.colors.lightscore:
            self.axes.fill_between(self.padding+(self.padding+width)*col+(width)*xd,
                                   ystart1+profileheight*yd,
                                   ystart1+profileheight,
                                   color=self.colors.lightscore)
        t=numpy.linspace(0,2*numpy.pi)
        if color is None or color==self.colors.cut:
            self.axes.plot(self.padding+(self.padding+width)*col+width/2+0.125*numpy.cos(t),
                           self.padding+(self.padding+height)*row+height-0.25+0.125*numpy.sin(t),
                           color=self.colors.cut)
        
        
        pulsarname=pulsarname.replace('-','$-$')
        pulsarname=pulsarname.replace('+','$+$')
        xtext=self.padding+(self.padding+width)*col+0.02*width                       
        
        if color is None or color==self.colors.darkscore:
            self.axes.text(xtext,
                           self.padding+(self.padding+height)*row+0.9*height,
                           pulsarname,
                           verticalalignment='top',
                           horizontalalignment='left',
                           fontsize=fontsize2,
                           color=self.colors.darkscore,
                           fontname=fontname)
            self.axes.text(xtext,
                           self.padding+(self.padding+height)*row+0.8*height,
                           'Period=%s ms; DM=%s pc/cc' % (P,DM),
                           verticalalignment='top',
                           horizontalalignment='left',
                           fontsize=fontsize1,
                           color=self.colors.darkscore,
                           fontname=fontname)
            self.axes.text(xtext,
                           self.padding+(self.padding+height)*row+0.23*height,
                           '%s discovery made by:' % telescope,
                           verticalalignment='top',
                           horizontalalignment='left',
                           fontsize=fontsize1,
                           color=self.colors.darkscore,
                           fontname=fontname)
            self.axes.text(xtext,
                           self.padding+(self.padding+height)*row+0.18*height,
                           '%s' % studentname,
                           verticalalignment='top',
                           horizontalalignment='left',
                           fontsize=fontsize2,
                           color=self.colors.darkscore,
                           fontname=fontname)
            t=self.axes.text(xtext,
                             self.padding+(self.padding+height)*row+0.08*height,
                             '%s, %s' % (studentinstitution,date),
                             verticalalignment='top',
                             horizontalalignment='left',
                             fontsize=fontsize1,
                             color=self.colors.darkscore,
                             fontname=fontname)


    ##################################################
    def plotprofile(self, file, size, rcircle=0.125, nrows=11, ncols=5, color=None, prefix='', fontsize=10,smooth=2):
        self.filename=file
        f=fits.open(file)
        data=scipy.misc.imresize(f[-1].data['DATA'].squeeze(),2.0)
        data=gaussian_filter(data,(0,smooth))
        x=numpy.arange(data.shape[1])
        x=x/float(x.max())

        theta=numpy.linspace(0,2*numpy.pi)
        
        j=0
        i=0
        while i < data.shape[0]:
            for col in xrange(ncols):
                for row in xrange(nrows):
                    try:
                        y=numpy.float32(data[i])/1.05/data.max()+0.1
                        x0=self.padding+col*(size+self.padding)
                        y0=self.padding+row*(size+self.padding)
                        if color is None or color==self.colors.cut:
                            self.axes.plot(x0+size*numpy.r_[x,x.max(),x.min(),x.min()],
                                           y0+size*numpy.r_[y,0,0,y[0]],color=self.colors.cut)
                            self.axes.plot(x0+size/6.+rcircle*numpy.cos(theta),
                                           y0+size/20.+rcircle*numpy.sin(theta),
                                           color=self.colors.cut)
                            self.axes.plot(x0+size-size/6.+rcircle*numpy.cos(theta),
                                           y0+size/20.+rcircle*numpy.sin(theta),
                                           color=self.colors.cut)
                        if color is None or color==self.colors.engrave:
                            self.axes.text(x0+0.02*size,
                                           y0+0.02*size,'%03d' % i,color=self.colors.engrave,
                                           fontsize=fontsize)
                        
                        if i==0:
                            if color is None or color==self.colors.engrave:
                                self.axes.text(x0+0.25*size,y0+0.1*size,
                                               'PSR %s: %s' % (f[0].header['SRC_NAME'],
                                                               f[0].header['DATE-OBS'].split('T')[0]),
                                               color=self.colors.engrave,
                                               fontsize=fontsize)
                        i+=1
                    except:
                        pass

            if color is None:
                self.save(os.path.join(prefix,'%s_%03d.pdf' % (os.path.splitext(self.filename)[0],
                                                                    j)))
            else:
                self.save(os.path.join(prefix,'%s_%03d_%s.pdf' % (os.path.splitext(self.filename)[0],
                                                                    j,color)))

            self.axes.cla()
            self.axes.plot([0,self.material_width,self.material_width,0,0],
                           [0,0,self.material_height,self.material_height,0],
                           color='k',xunits=inch,yunits=inch)

            j+=1



    def save(self, filename):
        self.axes.set_xticks([])
        self.axes.set_yticks([])
        self.axes.axis('off')
        self.axes.axis('image')
        self.figure.savefig(filename,transparent=True,facecolor='none')
