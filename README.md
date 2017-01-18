# singlepulse
Tools for 3D printing and laser cutting single pulse data

# fold2stl.py
Convert <a href="http://www.atnf.csiro.au/research/pulsar/psrfits/">PSRFITS</a> data to printable STL file.

Requirements:
* astropy
* numpy
* scipy
* PIL
* <a href="https://github.com/thearn/stl_tools">stl_tools</a>

# lasercut.py
Laser cut pulsar data:
* Makes discovery plaques out of <a href="http://www.cv.nrao.edu/~sransom/presto/">PRESTO</a> bestprof files.
* Makes PDF files suitable for laser cutting individual pulsars from <a href="http://www.atnf.csiro.au/research/pulsar/psrfits/">PSRFITS</a> data

Requirements:
* astropy
* numpy
* scipy
* matplotlib

As an example, to make a series of monochrome PDFs out of a PSRFITS file:
```python
import lasercut

# dimensions in inches
material_width=24
material_height=48

filename='profiles/B0329+54.fits'

for color in ['Cyan','Red','#ff7f00','Magenta','Green']:
    sheetnum=0
    sheet=lasercut.LaserCutSheet(material_width, material_height, 'acrylic', 0.125)

    sheet.plotprofile(filename, size=3.72, color=color)
```

# basic_units.py
This is just a clone of matplotlib/examples/units/basic_units.py

