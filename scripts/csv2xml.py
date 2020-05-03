#! /usr/bin/env python

###############################################################################
#
#  Created:    30.03.2020
#  Authors:    Marian Majan, IBL
#              Tom Kralidis, Meteorological Service of Canada
#
###############################################################################


import csv
import os
import glob
from xml.dom import minidom
import xml.etree.ElementTree as ET

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

    with open(fileName) as ifile:
        data = csv.reader(ifile, dialect='custom')
        header = next(data, None)

        xmlFile = ET.Element(rootElement)
        for record in data:
            r = ET.SubElement(xmlFile, recordElement)
            for i, field in enumerate(record):
                ET.SubElement(r, header[i].replace(' ', '-')).text = field

        tree = ET.ElementTree(xmlFile)
        tree.write("xml/" + baseFileName + ".xml")

        rough_string = ET.tostring(xmlFile, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        with open("xml/" + baseFileName + ".xml", 'w') as fh:
            fh.write(reparsed.toprettyxml(indent="  "))
