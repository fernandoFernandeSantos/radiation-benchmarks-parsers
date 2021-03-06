import re
from abc import ABCMeta, abstractmethod
import struct
from sklearn.metrics import jaccard_similarity_score
import os
import errno
import collections
import csv
import warnings
from datetime import datetime

"""Base class for parser, need to be implemented by each benchmark"""


class Parser:
    __metaclass__ = ABCMeta
    # error bounds for relative error analysis, default is 0%, 2% and 5%
    __errorLimits = [0.0, 2.0, 5.0]
    _keys = []
    # it will keep the first threshold key
    __firstKey = ""

    # errorsParsed
    _errors = {}
    # for relErrLowerLimit
    _relErrLowerLimit = {}
    # for localityParser2D
    _locality = {}
    # for jaccardCoefficient
    _jaccardCoefficientDict = {}

    # if the processing database is generated from a fault injection
    _isFaultInjection = False

    # this will contains the csv that dictates the if the processing log is valid or not
    _checkRunsCsv = None

    # ecc on or off
    # it is valid only for older logfiles version, the ones which does not
    # contain the ECC word in the self._logfilename
    _ecc = False

    # specific atributes for CSV write
    # log filename str which contains date, and benchmark name
    _logFileName = ""
    # str which indentify the device
    _machine = ""
    # benchmark name as string
    _benchmark = None
    # logfilename header, all special characters were replaced by -
    _header = ""
    # iteration where an sdc appeared
    _sdcIteration = -1
    # acc time when an SDC appeared
    _accIteErrors = -1
    _iteErrors = -1

    # support attributes
    # build locality images
    _buildImages = False
    # if header was already written
    _headerWritten = False
    # raw error list
    _errList = []
    # header without - separator
    _pureHeader = ""
    _logFileNameNoExt = ""
    _dirName = ""

    # test if it is not necessary to extend header
    _extendHeader = True

    # size must be set on the child classes
    # size will be the name of each benchmark dir
    _size = ""

    # count errors
    _countErrors = 0

    # output error list information
    _outputListError = None

    # csv output header, stay calm, this will be write once on each csv file generated by
    _csvHeader = ["logFileName", "Machine", "Benchmark", "Header", "SDC Iteration", "#Accumulated Errors",
                  "#Iteration Errors", "Max Relative Error", "Min Rel Error",
                  "Average Rel Err", "zeroOut", "zeroGold", "errorsCount"]

    # relative error types
    __relativeErrorTypes = ["cubic", "square", "line", "single", "random"]

    # for relativeErrorParser
    _maxRelErr = 0
    _minRelErr = 0
    _avgRelErr = 0
    _zeroOut = 0
    _zeroGold = 0

    # for benchmarks which have a third dimention this attribute must be set on the child process
    _hasThirdDimention = False

    def __init__(self, **kwargs):
        # keys must be set according to CAIO's approach
        try:
            parseForHistogram = kwargs.pop("parse_err_histogram")
        except:
            parseForHistogram = None

        # this is necessary for CAIO's approach
        if parseForHistogram:
            precision = int(parseForHistogram["PRECISION"])
            limitRange = int(parseForHistogram["LIMIT_RANGE"])
            self.__errorLimits = [float(i) / precision for i in range(0, precision * limitRange + 1)]

            self._keys = ["errorLimit" + str(i) for i in self.__errorLimits]
            self.__firstKey = self._keys[0]

            if "relative_errors_<=_" + str(self.__errorLimits[0]) not in self._csvHeader and self._extendHeader:
                # for python list interpretation is faster than a concatenated loop
                self._csvHeader.extend("relative_errors_<=_" + str(threshold) for threshold in self.__errorLimits)
                self._csvHeader.extend("jaccard_>_" + str(threshold) for threshold in self.__errorLimits)
                self._csvHeader.extend(
                    t + "_>" + str(threshold) for threshold in self.__errorLimits for t in self.__relativeErrorTypes)

        try:
            self._isFaultInjection = bool(kwargs.pop("is_fi"))
        except:
            self._isFaultInjection = False

        try:
            self._checkRunsCsv = kwargs.pop("check_csv")
        except:
            self._checkRunsCsv = None

        try:
            self._ecc = bool(kwargs.pop("ecc"))
        except:
            self._ecc = False

    """
    debug method, only print the class attributes
    """

    def debugAttPrint(self):
        print("*******Var values*******")
        print("log file", self._logFileName)
        print("machine", self._machine)
        print("acc ite errors", self._accIteErrors)
        print("bencharmk", self._benchmark)
        print("header", self._header)
        print("sdcIterators", self._sdcIteration)
        print("iteErrors", self._iteErrors)
        print("size", self._size)
        print("dir name", self._dirName)
        print("third dimention", self._hasThirdDimention)

    """
    This method will set all attributes that were first defined by Daniel on the first script
    they are very helpful, and they also are used when csv file is generated
    """

    def setDefaultValues(self, logFileName, machine, benchmark, header, sdcIteration, accIteErrors, iteErrors, errList,
                         logFileNameNoExt, pureHeader):
        self._logFileName = logFileName
        self._machine = machine
        self._benchmark = benchmark
        self._header = header
        self._sdcIteration = sdcIteration
        self._accIteErrors = accIteErrors

        self._iteErrors = iteErrors
        self._errList = errList

        self._pureHeader = pureHeader
        self._logFileNameNoExt = logFileNameNoExt

        # self._size = \
        self.setSize(self._pureHeader)

        self._makeDirName()

        # for csv run check
        if self._checkRunsCsv:
            # for i in self._checkRunsCsv:
            board_key = str(self._machine) + ("_ecc_on" if self._ecc else '')

            csvObjFile = open(self._checkRunsCsv[board_key]["csv"])

            # to check the delimiter
            dialect = csv.Sniffer().sniff(csvObjFile.read(), delimiters=';,')
            csvObjFile.seek(0)
            readerTwo = csv.reader(csvObjFile, dialect=dialect)
            self._checkRunsCsv[board_key]["data"] = [j for j in readerTwo]
            csvObjFile.close()
            # ----------------

    """
    call to the private method paseerrMethod
    for each errString in _errList
    """

    def parseErr(self):
        self._errors[self.__firstKey] = []
        for errString in self._errList:
            if self._isLogValid:
                err = self.parseErrMethod(errString)
                if err is not None:
                    self._errors[self.__firstKey].append(err)

    """
    _relativeErrorParser caller, if you want override _relativeErrorParse
     only put all errors on self._errors[self.__firstKey] so
    it will be parsed by your _relativeErrorParse
    """

    def relativeErrorParser(self):
        self._relativeErrorParser(self._errors[self.__firstKey])

    @abstractmethod
    def parseErrMethod(self, errString):
        raise NotImplementedError()

    """
        build image, based on object parameters
        ***is not mandatory anymore***
    """

    def buildImageMethod(self, *args):
        return False

    """
    this method is very important, it must set self._size attribute
    with a string that contains a setup configuration
    for example: I have a dgemm with 2048 x 2048
    so my self._size = str(size_m_size_n),
    where m == 2048 and n == 2048
    """

    @abstractmethod
    def setSize(self, header):
        raise NotImplementedError()

    """
    relative error with a generic range of tolerated values
    input:
    relError: error found in the SDC
    err: list of elements in the locality classification

    """

    def _placeRelativeError(self, relError, err):
        for key, threshold in zip(self._keys, self.__errorLimits):
            if relError < threshold:
                self._relErrLowerLimit[key] += 1
            else:
                self._errors[key].append(err)

    """
    to clean all relative errors attributes for the class
    attributes to be cleaned:
    relErrLowerLimit
    _errors = {}
    _relErrLowerLimit = {}
    """

    def _cleanRelativeErrorAttributes(self):
        for key in self._keys:
            # to store all error parsed values
            self._errors[key] = []
            self._relErrLowerLimit[key] = 0
            self._jaccardCoefficientDict[key] = 0

    """
    if you want other relative error parser this method must be override
    return [highest relative error, lowest relative error, average relative error,
    # zeros in the output,
    #zero in the GOLD,
    #errors with relative errors lower than limit(toleratedRelErr) for each _errorLimits value,
    """

    def _relativeErrorParser(self, errList):
        relErrorList = []
        zeroGold = 0
        zeroOut = 0
        self._cleanRelativeErrorAttributes()
        # need to calculate how many elements for each dimentions
        # i need to compare
        # default first element is 2, [posx, posy, read, expected]
        firstElement = 2
        lastElement = 3

        # [posX, posY, posZ, vr, ve, xr, xe, yr, ye, zr, ze]
        if self._hasThirdDimention:
            firstElement = 3
            lastElement = 10

        self._countErrors = len(errList)
        self._errValueAverage = 0
        for err in errList:
            relError = 0.0
            # this is only to support N dimentional errors
            for i in range(firstElement, lastElement + 1, 2):
                if err[i] is None or err[i + 1] is None:
                    continue
                read = float(err[i])
                expected = float(err[i + 1])

                absoluteErr = abs(expected - read)
                if abs(read) < 1e-6:
                    zeroOut += 1
                if abs(expected) < 1e-6:
                    zeroGold += 1
                else:
                    relError += abs(absoluteErr / expected) * 100

                # error average calculation
                self._errValueAverage += read / float(self._countErrors)

            if relError > 0.0:
                relErrorList.append(relError)
                # generic way to parse for many error threshold
                self._placeRelativeError(relError, err)

        if len(relErrorList) > 0:
            self._maxRelErr = max(relErrorList)
            self._minRelErr = min(relErrorList)
            self._avgRelErr = sum(relErrorList) / float(len(relErrorList))

        self._zeroOut = zeroOut
        self._zeroGold = zeroGold

    """
    jaccardCoefficient caller method
    this method only calls _jaccardCoefficient method, once _jaccardCoefficient could
    be implemented for many benchmarks
    """

    def jaccardCoefficient(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)
            for keys, values in self._errors.items():
                self._jaccardCoefficientDict[keys] = self._jaccardCoefficient(values)

    """
    jaccardCoefficient parser. This method could be overwritten if necessary
    input:
    errListJaccard: list of errors
    """

    def _jaccardCoefficient(self, errListJaccard):
        expected = []
        read = []
        for err in errListJaccard:
            try:
                readGStr = ''.join(bin(ord(c)).replace('0b', '').rjust(8, '0') for c in struct.pack('!f', err[2]))
                expectedGStr = ''.join(
                    bin(ord(c)).replace('0b', '').rjust(8, '0') for c in struct.pack('!f', err[3]))
            except OverflowError:
                readGStr = ''.join(bin(ord(c)).replace('0b', '').rjust(8, '0') for c in struct.pack('!d', err[2]))
                expectedGStr = ''.join(
                    bin(ord(c)).replace('0b', '').rjust(8, '0') for c in struct.pack('!d', err[3]))

            read.extend([n for n in readGStr])
            expected.extend([n for n in expectedGStr])

        try:
            jac = jaccard_similarity_score(expected, read)
            dissimilarity = float(1.0 - jac)
            return dissimilarity
        except:
            return None

    """
    locality caller method 2d, and 3d if it's avaliable
    """

    def localityParser(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)
            for key, value in self._errors.items():
                if self._hasThirdDimention:
                    self._locality[key] = self._localityParser3D(value)
                else:
                    self._locality[key] = self._localityParser2D(value)

    """
    locality parser for 2d benchmarks
    input:
    errList: list of errors parsed by parseErr
    """

    def _localityParser2D(self, errList):
        if len(errList) < 1:
            return [0, 0, 0, 0, 0]
        elif len(errList) == 1:
            return [0, 0, 0, 1, 0]
        else:
            allXPositions = [x[0] for x in errList]  # Get all positions of X
            allYPositions = [x[1] for x in errList]  # Get all positions of Y
            counterXPositions = collections.Counter(allXPositions)  # Count how many times each value is in the list
            counterYPositions = collections.Counter(allYPositions)  # Count how many times each value is in the list
            rowError = any(
                x > 1 for x in counterXPositions.values())  # Check if any value is in the list more than one time
            colError = any(
                x > 1 for x in counterYPositions.values())  # Check if any value is in the list more than one time
            if rowError and colError:  # square error
                return [0, 1, 0, 0, 0]
            elif rowError or colError:  # row/col error
                return [0, 0, 1, 0, 0]
            else:  # random error
                return [0, 0, 0, 0, 1]

    """
    locality parser for 3d benchmarks
    input:
    errList: list of errors parsed by parseErr
    """

    def _localityParser3D(self, errList):
        if len(errList) < 1:
            return [0, 0, 0, 0, 0]
        elif len(errList) == 1:
            return [0, 0, 0, 1, 0]
        else:
            allXPositions = [x[0] for x in errList]  # Get all positions of X
            allYPositions = [x[1] for x in errList]  # Get all positions of Y
            allZPositions = [x[2] for x in errList]  # Get all positions of Y
            counterXPositions = collections.Counter(allXPositions)  # Count how many times each value is in the list
            counterYPositions = collections.Counter(allYPositions)  # Count how many times each value is in the list
            counterZPositions = collections.Counter(allZPositions)  # Count how many times each value is in the list
            rowError = any(
                x > 1 for x in counterXPositions.values())  # Check if any value is in the list more than one time
            colError = any(
                x > 1 for x in counterYPositions.values())  # Check if any value is in the list more than one time
            heightError = any(
                x > 1 for x in counterZPositions.values())  # Check if any value is in the list more than one time
            if rowError and colError and heightError:  # cubic error
                return [1, 0, 0, 0, 0]
            if (rowError and colError) or (rowError and heightError) or (heightError and colError):  # square error
                return [0, 1, 0, 0, 0]
            elif rowError or colError or heightError:  # line error
                return [0, 0, 1, 0, 0]
            else:  # random error
                return [0, 0, 0, 0, 1]

    """
    write a list as a row to CSV
    if you want other type of write to csv,
    atribute __csvHeader and _outputListError must be changed
    """

    def writeToCSV(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)
            csvFileName = self._dirName + "/logs_parsed_" + self._machine + ".csv"

            # check if csvheader is already written
            if not os.path.isfile(csvFileName):
                self._writeCSVHeader(csvFileName)
                self._headerWritten = True

            try:
                csvWFP = open(csvFileName, "a")
                writer = csv.writer(csvWFP, delimiter=';')
                self._placeOutputOnList()
                writer.writerow(self._outputListError)
                csvWFP.close()

            except:
                print("Error on writing row to " + str(csvFileName))
                raise

    """
    ALL PARSED INFORMATION MUST will be in outputListError
    to write a parsed line result only put all errors in _csvHeader order into
    _outputListError
    """

    def _placeOutputOnList(self):
        self._outputListError = [self._logFileName,
                                 self._machine,
                                 self._benchmark,
                                 self._header,
                                 self._sdcIteration,
                                 self._accIteErrors,
                                 self._iteErrors,
                                 self._maxRelErr,
                                 self._minRelErr,
                                 self._avgRelErr,
                                 self._zeroOut,
                                 self._zeroGold,
                                 self._countErrors]

        self._outputListError.extend(self._relErrLowerLimit[key] for key in self._keys)
        self._outputListError.extend(self._jaccardCoefficientDict[key] for key in self._keys)
        for key in self._keys:
            self._outputListError.extend(self._locality[key])

    """
    writes a csv header, and create the log_parsed directory
    input:
    csvFilename: output filename for csv, this will be generated using what is produced by setSize method
    """

    def _writeCSVHeader(self, csvFileName):
        if not os.path.isfile(csvFileName):
            if not os.path.exists(os.path.dirname(csvFileName)):
                try:
                    os.makedirs(os.path.dirname(csvFileName))
                except OSError as exc:  # Guard against race condition
                    if exc.errno != errno.EEXIST:
                        raise

            csvWFP = open(csvFileName, "a")
            writer = csv.writer(csvWFP, delimiter=';')
            writer.writerow(self._csvHeader)
            csvWFP.close()

    """
    makes the csv output directory, for each config, for each Device, for each size
    this method will use self._size attribute which is produced by setSize method
    """

    def _makeDirName(self):
        self._dirName = os.getcwd() + "/" + self._machine + "/" + self._benchmark + "/" + str(self._size) + "/"
        if not os.path.exists(os.path.dirname(self._dirName)):
            try:
                os.makedirs(os.path.dirname(self._dirName))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

    """
    this method check if the processing log is on a valid
    radiation test run
    if self._isFaultInjection is True this method will always return true
    """

    @property
    def _isLogValid(self):
        if self._isFaultInjection or self._checkRunsCsv is None:
            return True
        board_key = str(self._machine) + ("_ecc_on" if self._ecc else '')
        currentData = self._checkRunsCsv[board_key]["data"]
        # process data
        # 2016_12_13_19_00_34_cudaDarknet_carol-k402.log
        m = re.match("(\d+)_(\d+)_(\d+)_(\d+)_(\d+)_(\d+)_(.*)_(.*).log", self._logFileName)
        if m:
            year = m.group(1)
            month = m.group(2)
            day = m.group(3)
            hour = m.group(4)
            minutes = m.group(5)
            second = m.group(6)

            # assuming microsecond = 0
            currDate = datetime(int(year), int(month), int(day), int(hour), int(minutes), int(second))
            for j in currentData:
                # startDate = j["start timestamp"]
                # endDate = j["end timestamp"]
                # doing it I can use daniel raw summaries-fission.csv file
                try:
                    startDate = j[0]
                    endDate = j[1]
                    validBench = j[2] in self._benchmark or self._benchmark in j[2]

                    startDate = datetime.strptime(startDate, "%c")
                    endDate = datetime.strptime(endDate, "%c")
                    if startDate <= currDate <= endDate and validBench:
                        return True
                except:
                    pass

        return False
