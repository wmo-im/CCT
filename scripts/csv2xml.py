#! /usr/bin/env python

#################################################################################################
##
##  Created:    30.03.2020
##  Authors:    Marian Majan, IBL
##
#################################################################################################



import csv
import os
import glob

rootElement = "dataroot"
# recordElement set as a filename
# recordElement = "BUFRCREX_33_0_0_CodeFlag_en"

csv.register_dialect('custom',
                     delimiter=',',
                     doublequote=True,
                     escapechar=None,
                     quotechar='"',
                     quoting=csv.QUOTE_MINIMAL,
                     skipinitialspace=False)

files = glob.glob("*.csv")
for fileName in files:
    baseFileName, fileExtension = os.path.splitext(fileName)
    recordElement = baseFileName

    xmlFile = open(baseFileName + ".xml", "w")

    with open(fileName) as ifile:
        data = csv.reader(ifile, dialect='custom')
        header = next(data, None)
        xmlFile.write("<%s>\n" % rootElement)
        for record in data:
            xmlFile.write("   <%s>\n" % recordElement)
            for i, field in enumerate(record):
                xmlFile.write("      <%s>%s</%s>\n" % (header[i], field, header[i]))
            xmlFile.write("   </%s>\n" % recordElement)
        xmlFile.write("</%s>" % rootElement)

    xmlFile.close()
