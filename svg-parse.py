#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import xml.etree.ElementTree as ET
from svg.path import parse_path, Line
import tkinter as tk
from tkinter import filedialog

outfolder = 'C:\\Users\\kfeld\\OneDrive\\MAKE\\CIRCUITMAKER\\IMAGES\\SvgToPoly\\'

class SvgToPoly(object):

    def __init__(self, filename, outFolder='out', curveResolution=1, scalingFactor=2.54):
        tree = ET.parse(filename)
        self.root = tree.getroot()
        self.outFolder = outFolder
        self.curveResolution = curveResolution
        self.scalingFactor = scalingFactor

    def Parse(self):
        print("Starting Parse")
        for g in self.root.findall('{http://www.w3.org/2000/svg}g'):
            print(f"Found g: {g.get('id')}")
            for data in g.findall('{http://www.w3.org/2000/svg}path'):
                csvList = self.ConvertPath(data)
                self.WriteCsv(csvList, data.get('id'))

    def ConvertPath(self, data):
        name = data.get('id')
        print('-----', name)
        path = data.get('d')
        csvList = []
        pathSegments = parse_path(path)
        
        origin_x = None
        origin_y = None
        
        for segment in pathSegments:
            if not isinstance(segment, Line):
                segment = self.StraightenCurve(segment, self.curveResolution)
            
            x = segment.start.real * self.scalingFactor
            y = -1 * segment.start.imag * self.scalingFactor
            
            if origin_x is None:  # first point becomes the origin
                origin_x = x
                origin_y = y
            
            csvList.append((x - origin_x, y - origin_y))
    
        return csvList

    def StraightenCurve(self, data, samples):
        line = Line(data.point(0), data.point(1))
        return line

    def WriteCsv(self, data, filename):
        if not os.path.exists(self.outFolder):
            os.makedirs(self.outFolder)

        outpath = os.path.join(self.outFolder, filename + '.csv')  # ✅ safe path joining
        print(f'Writing: {outpath}')

        with open(outpath, 'w+') as f:
            f.write('"Index","X (mil)","Y (mil)","Arc Angle (Neg = CW)"\n')
            for i, coordinate in enumerate(data):  # ✅ i now increments
                f.write(f'"{i}","{coordinate[0]}","{coordinate[1]}",""\n')


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    filenames = filedialog.askopenfilenames(
        initialdir='C:\\Users\\kfeld\\OneDrive\\MAKE\\CIRCUITMAKER\\IMAGES\\SvgToPoly\\',
        title='Select SVG files',
        filetypes=[('SVG files', '*.svg')]
    )
    outfolder = filedialog.askdirectory(
        initialdir='C:\\Users\\kfeld\\OneDrive\\MAKE\\CIRCUITMAKER\\IMAGES\\SvgToPoly\\',
        title='Select output folder'
    )
    if filenames and outfolder:
        for filename in filenames:
            print(f"Processing: {filename}")
            obj = SvgToPoly(filename, outFolder=outfolder)
            obj.Parse()
    else:
        print("No files or output folder selected")

    input("Press Enter to exit...")