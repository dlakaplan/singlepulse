import lasercut

# dimensions in inches
material_width=24
material_height=18


Data=[['J0355+28','Renee Spiewak','10/27/15','GBNCC','365','49','guppi_57379_0355+28_0001_0001_364.93ms_Cand.pfd.bestprof'],
      ['J0534-13','Renee Spiewak','5/4/16','GBNCC','979','34','guppi_57538_0534-13_0002_0001_979.42ms_Cand.pfd.bestprof'],
      ['J1611-29','Joe Swiggum','10/26/15','GBNCC','9.6','83','guppi_57379_J1611-29_0094_PSR_1611-29.pfd.bestprof'],
      ['J2022+25','Joe Swiggum','5/12/16','GBNCC','2.65','54','guppi_57538_2022+25_0260_0001_2.65ms_Cand.pfd.bestprof'],
      ['J2150-03','Kaleb Maraccini','4/30/16','GBNCC','3.51','21','guppi_57509_2150-03_0002_0001_3.51ms_Cand.pfd.bestprof'],
      ['J1529-26','Robert Bavisotto','5/5/16','GBNCC','799','45','guppi_57539_1529-26_0162_0001_798.64ms_Cand.pfd.bestprof'],
      ['J1536-30','Robert Bavisotto','5/5/16','GBNCC','1901','63','guppi_57539_1536-30_0163_0001_1900.62ms_Cand.pfd.bestprof'],
      ['J1638-35','Robert Bavisotto','5/5/16','GBNCC','705','115','guppi_57539_1638-35_0165_0001_705.11ms_Cand.pfd.bestprof']
      #['J1819-37','Robert Bavisotto','5/5/16','632','68']
     ]


prefix='UWMdiscoveries'

#for color in [None]:
for color in ['Cyan','Red','Orange','Magenta','Green']:
    sheetnum=0
    sheet=lasercut.LaserCutSheet(material_width, material_height, 'acrylic',0.125)

    row=0
    col=0
    for line in Data:
        for repeat in xrange(2):
            sheet.addplaque(line[-1],
                            'PSR %s' % line[0],
                            line[4],
                            line[5],
                            datetime.datetime.strptime(line[2],
                                                       '%m/%d/%y').strftime('%b %-d, %Y'),
                            line[1],
                            'UW Milwaukee',
                            line[3],
                            col=col,
                            row=row,
                            color=color)
            col+=1
            if col==3:
                row+=1
                col=0

                if row==2:
                    if color is not None:
                        sheet.save('%s_%d_%s.pdf' % (prefix,sheetnum,color))
                    else:
                        sheet.save('%s_%d.pdf' % (prefix,sheetnum))
                    sheet=LaserCutSheet(material_width, material_height, 'acrylic',0.125)

                    sheetnum+=1
                    row=0
                    col=0

    if color is None:
        sheet.save('%s_%d.pdf' % (prefix,sheetnum))
    else:        
        sheet.save('%s_%d_%s.pdf' % (prefix,sheetnum,color))
