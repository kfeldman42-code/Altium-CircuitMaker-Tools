#!/usr/bin/python
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
from PIL import Image

inFile = 'C:\\Users\\kfeld\\OneDrive\\MAKE\\CIRCUITMAKER\\IMAGES\\BMP-BRD CONVERT\\9MM.bmp'
modelFile = 'C:\\Users\\kfeld\\OneDrive\\MAKE\\CIRCUITMAKER\\IMAGES\\BMP-BRD CONVERT\\blank.brd'
outFile = 'C:\\Users\\kfeld\\OneDrive\\MAKE\\CIRCUITMAKER\\IMAGES\\BMP-BRD CONVERT\\converted.brd'

#Notable layers:
#1:  Top
#16: Bottom
#21: tPlace (Top silkscreen)
#22: bPlace (Bottom silkscreen)
#29: tStop (Top solder)
#30: bStop (Bottom solder)
#31: tCream
#32: bCream
#39: tKeepout
#40: bKeepout
layer = '1'

#Internal units are 0.1um, or 1/10000
#So 1 pixel =
#1 mm:  10000
#1 mil: 254
scale = 423


class BmpToBrd(object):

    def __init__(self, inFile, modelFile, outFile, layer = '1', scalingFactor = 1):
        img = Image.open(inFile)
        if img.mode !='1':
            print ("Try again with Index Mode 1-bit colour!")
            img = img.convert(mode='1')
        self.scalingFactor = scalingFactor / 10000.0
        self.layer = layer
        self.componentElement = []
        
        self.outFile = outFile
        self.Read_Lines(img)
        self.Update_Brd(modelFile)

    def Read_Lines(self, img):
        print("Image dimensions: {}".format(img.size))
        print("Writing to: {}".format(self.outFile))
    
        pixel_count = 0
        match_count = 0
    
        for y in range(img.size[1]):
            start = -1
            for x in range(img.size[0]):
                pixel = img.getpixel((x, y))
                pixel_count += 1
                if pixel == 0:
                    match_count += 1
                    if start == -1:
                        start = x
                    end = x + 1
                elif start != -1:
                    self.Append_Square(start, end, y)
                    start = -1

    def Append_Square(self, start, end, y):
        x1 = "{}".format(start * self.scalingFactor)
        y1 = "{}".format(y * self.scalingFactor)
        x2 = "{}".format(end * self.scalingFactor)
        y2 = "{}".format((y+1) * self.scalingFactor)
        
        self.componentElement.append(ET.Element('rectangle', attrib = {'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2, 'layer': self.layer}))
        
    def Update_Brd(self, modelFile):
        tree = ET.parse(modelFile)
        root = tree.getroot()
        
        tree.write(self.outFile)
                
    def Write_Brd(self, filename):
        f = open(filename, 'w+')
        
        for line in self.componentData:
            f.write(line)
            
        f.close()

        print("Writing to: {}".format(self.outFile))

if __name__ == "__main__":
    obj = BmpToBrd(inFile, modelFile, outFile, layer, scale)
