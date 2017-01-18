import lasercut

# dimensions in inches
material_width=24
material_height=48

filename='profiles/B0329+54.fits'

for color in ['Cyan','Red','#ff7f00','Magenta','Green']:
    sheetnum=0
    sheet=lasercut.LaserCutSheet(material_width, material_height, 'acrylic', 0.125)

    sheet.plotprofile(filename, size=3.72, color=color)
