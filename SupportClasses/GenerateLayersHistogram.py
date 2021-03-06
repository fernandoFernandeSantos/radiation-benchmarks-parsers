#!/usr/bin/env python
import csv
import numpy as np
import struct
import os


class GenerateLayersHistogram():
    csvFilePath = ""
    csvFile = None
    writer = None
    finalInfo = []
    __layerDimentions = None

    def __init__(self, **kwargs):
        self.csvFilePath = kwargs.pop("csvFile")
        fieldnames = kwargs.pop("fieldnames")
        self.__layerDimentions = kwargs.pop("layerDim")
        fileExists = os.path.isfile(self.csvFilePath)

        self.csvFile = open(self.csvFilePath, "a")
        self.writer = csv.DictWriter(self.csvFile, fieldnames=fieldnames, delimiter=';')

        if not fileExists:
            self.writer.writeheader()

    def closeCsv(self):
        self.csvFile.close()

    def tupleToArray(self, layerContents, layerSize):
        layer = np.ndarray(shape=(layerSize), dtype=float)
        for i in range(0, layerSize):
            layer[i] = layerContents[i]
        return layer

    # returns the opened layers if files were found
    # an empty dict otherwise
    def openLayersImg(self, imgNumber, layersFilePath, imgName):
        lineDict = {}
        for i in self.__layerDimentions:
            # V1
            # goldName = layersFilePath + "gold_layer_" + str(i) + "_img_" + str(imgNumber) + "_test_it_0.layer"
            # V2
            # gold_layer_darknet_v2_14_img_1_test_it_0.layer
            goldName = layersFilePath + os.path.basename(self._txtList) + "_gold_layer_darknet_v2_" + str(i) + "_img_" + str(
                imgNumber) + "_test_it_0.layer"
            width, height, depth = self.__layerDimentions[i]
            layerSize = width * height * depth

            fi = open(goldName, "rb")
            # logLayerContents = struct.unpack('f' * layerSize, fi.read(4 * layerSize))
            # logLayerArray = self.tupleToArray(layerContents=logLayerContents, layerSize=layerSize)
            logLayerArray = np.fromfile(fi, dtype='float32', count=layerSize)
            fi.close()

            # calculate the min an max values
            sortedArray = np.sort(logLayerArray, kind='mergesort')

            if layerSize > 0:
                lineDict[i] = {'min': sortedArray[0], 'max': sortedArray[len(sortedArray) - 1], 'imgNumber': imgNumber,
                               'imgName': imgName.rstrip(), 'layer': i}
            else:
                lineDict[i] = {'min': 0, 'max': 0, 'imgNumber': imgNumber, 'imgName': imgName.rstrip(), 'layer': i}

        return lineDict

    def writeToCSV(self):
        # for i in self.lineDict:
        #     # print self.lineDict[i]
        #     self.writer.writerow(self.lineDict[i])
        localMin = [0] * 32
        localMax = [0] * 32
        localMaxImg = [0] * 32
        localMaxImgPath = [""] * 32
        localLayer = [0] * 32

        for i in self.finalInfo:
            for j in self.__layerDimentions:
                min_l = i[j]['min']
                max_l = i[j]['max']

                new_min = localMin[j]
                new_max = localMax[j]
                if new_min > min_l:
                    localMin[j] = min_l
                    localMaxImg[j] = i[j]['imgNumber']
                    localMaxImgPath[j] = i[j]['imgName']
                    localLayer[j] = i[j]['layer']

                if new_max < max_l:
                    localMax[j] = max_l
                    localMaxImg[j] = i[j]['imgNumber']
                    localMaxImgPath[j] = i[j]['imgName']
                    localLayer[j] = i[j]['layer']

        for i in xrange(0, 32):
            self.writer.writerow({'min': localMin[i], 'max': localMax[i], 'imgNumber': localMaxImg[i], 'imgName': localMaxImgPath[i], 'layer': localLayer[i]})

    def generateInfo(self, lines, layers, txtList):
        for i, line in enumerate(lines):
            print "Processing layers from img:", line.rstrip(), "i:", i
            # hist.writeToCSV(i, layersPath, line)
            self._txtList = txtList
            self.finalInfo.append(hist.openLayersImg(i, layers, line))


###########################################
# MAIN
###########################################'
if __name__ == '__main__':
    cnnDim = {
        0: [224, 224, 64],
        1: [112, 112, 64],
        2: [112, 112, 192],
        3: [56, 56, 192],
        4: [56, 56, 128],
        5: [56, 56, 256],
        6: [56, 56, 256],
        7: [56, 56, 512],
        8: [28, 28, 512],
        9: [28, 28, 256],
        10: [28, 28, 512],
        11: [28, 28, 256],
        12: [28, 28, 512],
        13: [28, 28, 256],
        14: [28, 28, 512],
        15: [28, 28, 256],
        16: [28, 28, 512],
        17: [28, 28, 512],
        18: [28, 28, 1024],
        19: [14, 14, 1024],
        20: [14, 14, 512],
        21: [14, 14, 1024],
        22: [14, 14, 512],
        23: [14, 14, 1024],
        24: [14, 14, 1024],
        25: [7, 7, 1024],
        26: [7, 7, 1024],
        27: [7, 7, 1024],
        28: [7, 7, 256],
        29: [12544, 1, 1],
        30: [1175, 1, 1],
        31: [1175,1,1]}

    # to set vars
    csvFilePath = "temp.csv"
    layersPath = "/var/radiation-benchmarks/data/"
    texts = ["/home/carol/radiation-benchmarks/data/networks_img_list/caltech.pedestrians.100.txt",
            "/home/carol/radiation-benchmarks/data/networks_img_list/urban.street.100.txt",
            "/home/carol/radiation-benchmarks/data/networks_img_list/voc.2012.100.txt"
    ]

    ##################
    fieldnames = ['min', 'max', 'imgNumber', 'imgName', 'layer']
    hist = GenerateLayersHistogram(csvFile=csvFilePath, fieldnames=fieldnames, layerDim=cnnDim)

    for txtList in texts:
        # read lines
        lines = open(txtList, "r").readlines()
        hist.generateInfo(lines, layersPath, txtList)

    hist.writeToCSV()

    hist.closeCsv()
