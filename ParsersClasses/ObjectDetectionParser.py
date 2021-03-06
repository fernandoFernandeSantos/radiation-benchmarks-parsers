from abc import ABCMeta

from Parser import Parser
import csv
import copy

# build image
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import numpy as np
from sklearn import metrics


class ObjectDetectionParser(Parser):
    __metaclass__ = ABCMeta
    # precisionRecallObj = None
    _prThreshold = None
    _detectionThreshold = 0.2

    # local radiation-benchmarks git
    _localRadiationBench = ""
    # these strings in GOLD_BASE_DIR must be the directory paths of the gold logs for each machine
    _goldBaseDir = None

    # used datasets
    _datasets = None

    # output img dir
    _imgOutputDir = ''

    # img list size
    _imgListSize = 1000

    _iterations = None

    _goldDatasetArray = dict()
    _goldFileName = None
    _imgListPath = None

    _classes = ['__background__',
                'aeroplane', 'bicycle', 'bird', 'boat',
                'bottle', 'bus', 'car', 'cat', 'chair',
                'cow', 'diningtable', 'dog', 'horse',
                'motorbike', 'person', 'pottedplant',
                'sheep', 'sofa', 'train', 'tvmonitor']

    # overiding csvheader
    _csvHeader = ["logFileName", "Machine", "Benchmark", "SDC_Iteration", "#Accumulated_Errors",
                  "#Iteration_Errors", "gold_lines", "detected_lines", "wrong_elements",
                  "precision", "recall", "precision_classes", "recall_classes",
                  "false_negative", "false_positive",
                  "true_positive", "abft_type", "row_detected_errors", "col_detected_errors",
                  "header"]

    _goldLines = None
    _detectedLines = None
    _wrongElements = None
    _precision = None
    _recall = None
    _falseNegative = None
    _falsePositive = None
    _truePositive = None

    # only for darknet
    _abftType = None
    _rowDetErrors = None
    _colDetErrors = None

    # precision and recall classes
    _precisionClasses = None
    _recallClasses = None

    def __init__(self, **kwargs):
        self._extendHeader = False
        Parser.__init__(self, **kwargs)
        self._prThreshold = float(kwargs.pop("prThreshold"))
        self._imgOutputDir = str(kwargs.pop("imgOutputDir"))

        self._localRadiationBench = str(kwargs.pop("localRadiationBench"))
        self._goldBaseDir = kwargs.pop("goldBaseDir")
        self._datasets = kwargs.pop("datasets")

    def _writeToCSV(self, csvFileName):
        self._writeCSVHeader(csvFileName)

        try:

            csvWFP = open(csvFileName, "a")
            writer = csv.writer(csvWFP, delimiter=';')
            # ["logFileName", "Machine", "Benchmark", "imgFile", "SDC_Iteration",
            #     "#Accumulated_Errors", "#Iteration_Errors", "gold_lines",
            #     "detected_lines", "x_center_of_mass", "y_center_of_mass",
            #     "precision", "recall", "false_negative", "false_positive",
            #     "true_positive"]
            outputList = [self._logFileName,
                          self._machine,
                          self._benchmark,
                          self._sdcIteration,
                          self._accIteErrors,
                          self._iteErrors, self._goldLines,
                          self._detectedLines,
                          self._wrongElements,
                          self._precision,
                          self._recall,
                          self._precisionClasses,
                          self._recallClasses,
                          self._falseNegative,
                          self._falsePositive,
                          self._truePositive, self._abftType, self._rowDetErrors,
                          self._colDetErrors,
                          self._header
                          ]

            # if self._abftType != 'no_abft' and self._abftType != None:
            #     outputList.extend([])

            writer.writerow(outputList)
            csvWFP.close()

        except:
            # ValueError.message += ValueError.message + "Error on writing row to " + str(csvFileName)
            print "Error on writing row to " + str(csvFileName)
            raise

    def localityParser(self):
        pass

    def jaccardCoefficient(self):
        pass

    def copyList(self, objList):
        temp = []
        for i in objList: temp.append(copy.deepcopy(i.deepcopy()))
        return temp

    def buildImageMethod(self, imageFile, rectanglesGold, rectanglesFound, logFileName, dir):
        im = np.array(Image.open(imageFile), dtype=np.uint8)

        # Create figure and axes
        fig = plt.figure()
        axG = fig.add_subplot(221)
        axF = fig.add_subplot(222)
        axG.set_axis_off()
        axF.set_axis_off()
        # fig, ax = plt.subplots(1)

        # Display the image
        axG.imshow(im)
        axF.imshow(im)
        # Create a Rectangle patch
        # print str(self.__class__)
        for rG in rectanglesGold:
            if "DarknetV1Parser" in str(self.__class__) or "DarknetV2Parser" in str(
                    self.__class__) or "DarknetV3Parser" in str(self.__class__):
                rect = patches.Rectangle((rG.left, rG.top), rG.width,
                                         rG.height, linewidth=1, edgecolor='g',
                                         facecolor='none')
            else:
                rect = patches.Rectangle((rG.left, rG.bottom), rG.width,
                                         rG.height, linewidth=1, edgecolor='g',
                                         facecolor='none')

            # Add the patch to the Axes
            axG.add_patch(rect)

        axG.title.set_text("gold")

        for rF in rectanglesFound:
            # darknet represents inverted coordinates
            if "DarknetV1Parser" in str(self.__class__) or "DarknetV2Parser" in str(
                    self.__class__) or "DarknetV3Parser" in str(self.__class__):
                rectF = patches.Rectangle((rF.left, rF.top), rF.width,
                                          rF.height, linewidth=1, edgecolor='g',
                                          facecolor='none')
            else:
                rectF = patches.Rectangle((rF.left, rF.bottom), rF.width,
                                          rF.height, linewidth=1, edgecolor='g',
                                          facecolor='none')

            axF.add_patch(rectF)
        axF.title.set_text("found")

        # plt.show()
        saveName = logFileName.split('.')[0] + '.jpg'
        plt.savefig(dir + '/' + saveName)
        plt.cla()
        plt.close()

    """
    perfMeasure calculates falsePositive, truePositive and falseNegative
    where two lists of classes is given
    input:
    found: detected classes
    gold: ground truth and gold
    """

    def _perfMeasure(self, found, gold):
        falsePositive = truePositive = falseNegative = 0
        # # precision
        # outPositive = 0
        # for i in found:
        #     for g in gold:
        #         if g == i:  # (g.jaccard_similarity(i)) >= self.__threshold:
        #             outPositive += 1
        #             break
        #
        # falsePositive = len(found) - outPositive
        #
        # # recall
        # truePositive = 0
        # for i in gold:
        #     for z in found:
        #         if i == z:  # (i.jaccard_similarity(z)) >= self.__threshold:
        #             truePositive += 1
        #             break
        # falseNegative = len(gold) - truePositive
        if len(found) != len(gold):
            raise ValueError("PAU")

        print report['micro avg']['precision'], report['micro avg']['recall']


        return falsePositive, truePositive, falseNegative

    def _precisionAndRecallClasses(self, found, gold):
        # fp, tp, fn = self._perfMeasure(found, gold)
        # if tp + fn == 0:
        #     self._recallClasses = 0
        # else:
        #     self._recallClasses = float(tp) / float(tp + fn)
        #
        # if tp + fp == 0:
        #     self._precisionClasses = 0
        # else:
        #     self._precisionClasses = float(tp) / float(tp + fp)
        pred = found[:]
        if len(pred) < len(gold):
            pred.extend([-1] * (len(gold) - len(pred)))
        report = metrics.classification_report(gold, found, output_dict=True)

        self._precisionClasses, self._recallClasses = report['micro avg']['precision'], report['micro avg']['recall']
