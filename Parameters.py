from ParsersClasses import GemmParser
from ParsersClasses import ACCLParser
from ParsersClasses import DarknetParser
from ParsersClasses import FasterRcnnParser
from ParsersClasses import HogParser
from ParsersClasses import HotspotParser
from ParsersClasses import LavaMDParser
from ParsersClasses import NWParser
from ParsersClasses import LudParser
from ParsersClasses import LuleshParser
from ParsersClasses import MergesortParser
from ParsersClasses import QuicksortParser
from ParsersClasses import DarknetV2Parser
from ParsersClasses import DarknetV1Parser
from ParsersClasses import LenetParser
from ParsersClasses import ResnetParser
from ParsersClasses import BezierSurfaceParser

############################################################################################
########################OBJECT DETECTION PARSER PARAMETERS##################################
############################################################################################

LAYERS_GOLD_PATH = '/home/fernando/Dropbox/UFRGS/Pesquisa/fault_injections/sassifi_darknet_v2/gold_layers/'
LAYERS_PATH = '/home/fernando/Dropbox/UFRGS/Pesquisa/fault_injections/sassifi_darknet_v2/found_layers/'

# IMG_OUTPUT_DIR is the directory to where the images with error comparisons will be saved
IMG_OUTPUT_DIR = '/tmp/'

GOLD_BASE_DIR = {
    'carol-ECC-ON': '/home/fernando/Dropbox/UFRGS/Pesquisa/fault_injections/sassifi_darknet_v2/',
    'carol-k401-ECC-OFF': '/home/fernando/Dropbox/LANSCE2017/K40_gold',
    'carol-k201-ECC-OFF': '/home/fernando/Dropbox/LANSCE2017/K20_gold',
    'carol-k401-ECC-ON': '/home/fernando/Dropbox/LANSCE2017/K40_gold',
    'carol-k201-ECC-ON': '/home/fernando/Dropbox/LANSCE2017/K20_gold',
}

############################################################################################
#################################DARKNET PARSER PARAMETERS##################################
############################################################################################
"""This section MUST BE SET ACCORDING THE GOLD PATHS"""

DARKNET_DATASETS = {'caltech.pedestrians.critical.1K.txt': {'dumb_abft': 'gold.caltech.critical.abft.1K.test',
                                                            'no_abft': 'gold.caltech.critical.1K.test'},
                    'caltech.pedestrians.1K.txt': {'dumb_abft': 'gold.caltech.abft.1K.test',
                                                   'no_abft': 'gold.caltech.1K.test'},
                    'voc.2012.1K.txt': {'dumb_abft': 'gold.voc.2012.abft.1K.test', 'no_abft': 'gold.voc.2012.1K.test'}}

############################################################################################
###############################FASTER RCNN PARSER PARAMETERS################################
############################################################################################

FASTER_RCNN_DATASETS = {
    # normal
    'caltech.pedestrians.critical.1K.txt': 'gold.caltech.critical.1K.test',
    'caltech.pedestrians.1K.txt': 'gold.caltech.1K.test',
    'voc.2012.1K.txt': 'gold.voc.2012.1K.test'
}

############################################################################################
################################## HOG PARSER PARAMETERS ###################################
############################################################################################
HOG_GOLD_BASE_DIR = "/home/fernando/Dropbox/UFRGS/Pesquisa/fault_injections/sassifi_results_new/golds/histogram_ori_gradients/"
HOG_DATASETS = 'urbanstreet'

############################################################################################
#####################################LENET PARSER PARAMETERS################################
############################################################################################

LENET_DATASETS = {
    '': '',
    'test': 'foi',
}

LAYERS_GOLD_PATH_LENET = "/home/fernando/Dropbox/UFRGS/Pesquisa/fault_injections/sassifi_lenet/"
LAYERS_PATH_LENET = "/home/fernando/Dropbox/UFRGS/Pesquisa/fault_injections/sassifi_lenet/"

############################################################################################
####################################RESNET PARSER PARAMETERS################################
############################################################################################

RESNET_CLASSES_PATH = "../src/cuda/resnet_torch/fb.resnet.torch/pretrained/imagenet.lua"
#"/home/fernando/git_pesquisa/radiation-benchmarks/src/cuda/resnet_torch/fb.resnet.torch/pretrained/imagenet.lua"

############################################################################################
#################################OVERALL PARAMETERS ########################################
############################################################################################
LOCAL_RADIATION_BENCH = '/mnt/4E0AEF320AEF15AD/PESQUISA/git_pesquisa/radiation-benchmarks'

# if var check_csvs is true this values must have the csvs datapath
# _ecc_on is mandatory only for boards that have ecc memory
SUMMARIES_FILES = {
    'carol-k402_ecc_on': {
        'csv':  # '/home/fernando/Dropbox/UFRGS/Pesquisa/Teste_12_2016/DATASHEETS/CROSSECTION_RESULTS/logs_parsed_lanl/'
            '/home/fernando/Dropbox/UFRGS/Pesquisa/Teste_10_2016/'
            # 'logs_parsed_k40_ecc_on/summaries_k40_ecc_on.csv', 'data': None},
            'k402_ecc_on.csv', 'data': None},
    'carol-k401_ecc_on': {
        'csv':  # '/home/fernando/Dropbox/UFRGS/Pesquisa/Teste_12_2016/DATASHEETS/CROSSECTION_RESULTS/logs_parsed_lanl/'
            '/home/fernando/Dropbox/UFRGS/Pesquisa/Teste_10_2016/'
            # 'logs_parsed_k40_ecc_on/summaries_k40_ecc_on.csv', 'data': None},
            'k402_ecc_on.csv', 'data': None},

    "carol-k401-ECC-OFF": {
        'csv':  # '/home/fernando/Dropbox/UFRGS/Pesquisa/Teste_12_2016/DATASHEETS/CROSSECTION_RESULTS/logs_parsed_lanl/'
            '/home/fernando/Dropbox/UFRGS/Pesquisa/Teste_10_2016/'
            # 'logs_parsed_k40_ecc_on/summaries_k40_ecc_on.csv', 'data': None},
            'k402_ecc_on.csv', 'data': None},
    # 'carol-k402': {
    #     'csv': '/home/fernando/Dropbox/UFRGS/Pesquisa/Teste_12_2016/DATASHEETS/CROSSECTION_RESULTS/logs_parsed_lanl/'
    #            'logs_parsed_k40_ecc_off/summaries_k40_ecc_off.csv', 'data': None},
    # 'carol-tx': {
    #     'csv': '/home/fernando/Dropbox/UFRGS/Pesquisa/Teste_12_2016/DATASHEETS/CROSSECTION_RESULTS/logs_parsed_lanl/'
    #            'logs_parsed_titan_ecc_off/summaries_titan.csv', 'data': None},
    #
    # 'carolx1a': {
    #     'csv': '/home/fernando/Dropbox/UFRGS/Pesquisa/Teste_12_2016/DATASHEETS/CROSSECTION_RESULTS/logs_parsed_lanl/'
    #            'logs_parsed_parsed_x1/summaries_x1.csv', 'data': None},
    #
    # 'carolx1b': {
    #     'csv': '/home/fernando/Dropbox/UFRGS/Pesquisa/Teste_12_2016/DATASHEETS/CROSSECTION_RESULTS/logs_parsed_lanl/'
    #            'logs_parsed_parsed_x1/summaries_x1.csv', 'data': None},
    # 'carolx1c': {
    #     'csv': '/home/fernando/Dropbox/UFRGS/Pesquisa/Teste_12_2016/DATASHEETS/CROSSECTION_RESULTS/logs_parsed_lanl/'
    #            'logs_parsed_parsed_x1/summaries_x1.csv', 'data': None},
}

###############################################################################################


# set all benchmarks to be parsed here
radiationBenchmarks = {}


def setBenchmarks(**kwargs):
    benchmarks = kwargs.pop("benchmarks")
    pr_threshold = float(kwargs.pop("pr_threshold"))
    parse_layers = bool(kwargs.pop("parse_layers"))
    checkCsv = SUMMARIES_FILES if bool(kwargs.pop("check_csv")) else None
    ecc = bool(kwargs.pop("ecc"))
    isFi = bool(kwargs.pop("is_fi"))

    print "Parsing for: ",
    for i in benchmarks:
        benchObj = None
        print i,

        # darknet is the first version of tested darknet, until master degree dissertation
        if i == 'darknet':
            benchObj = DarknetParser.DarknetParser(parseLayers=parse_layers,
                                                   prThreshold=pr_threshold,
                                                   layersGoldPath=LAYERS_GOLD_PATH,
                                                   layersPath=LAYERS_PATH,
                                                   imgOutputDir=IMG_OUTPUT_DIR,
                                                   localRadiationBench=LOCAL_RADIATION_BENCH,
                                                   check_csv=checkCsv,
                                                   ecc=ecc,
                                                   is_fi=isFi,
                                                   goldBaseDir=GOLD_BASE_DIR,
                                                   datasets=DARKNET_DATASETS
                                                   )

        if i == 'darknetv1':
            benchObj = DarknetV1Parser.DarknetV1Parser(parseLayers=parse_layers,
                                                       prThreshold=pr_threshold,
                                                       layersGoldPath=LAYERS_GOLD_PATH,
                                                       layersPath=LAYERS_PATH,
                                                       imgOutputDir=IMG_OUTPUT_DIR,
                                                       localRadiationBench=LOCAL_RADIATION_BENCH,
                                                       check_csv=checkCsv,
                                                       goldBaseDir=GOLD_BASE_DIR,
                                                       datasets=DARKNET_DATASETS
                                                       )
        if i == 'darknetv2':
            benchObj = DarknetV2Parser.DarknetV2Parser(parseLayers=parse_layers,
                                                       prThreshold=pr_threshold,
                                                       layersGoldPath=LAYERS_GOLD_PATH,
                                                       layersPath=LAYERS_PATH,
                                                       imgOutputDir=IMG_OUTPUT_DIR,
                                                       localRadiationBench=LOCAL_RADIATION_BENCH,
                                                       check_csv=checkCsv,
                                                       goldBaseDir=GOLD_BASE_DIR,
                                                       datasets=DARKNET_DATASETS
                                                       )

        if i == 'resnet':
            benchObj = ResnetParser.ResnetParser(imgOutputDir=IMG_OUTPUT_DIR,
                                                 prThreshold=pr_threshold,
                                                 localRadiationBench=LOCAL_RADIATION_BENCH,
                                                 check_csv=checkCsv,
                                                 goldBaseDir=GOLD_BASE_DIR,
                                                 datasets=DARKNET_DATASETS,
                                                 classes_path=RESNET_CLASSES_PATH)

        elif i == 'hotspot':
            benchObj = HotspotParser.HotspotParser(localRadiationBench=LOCAL_RADIATION_BENCH,
                                                   check_csv=checkCsv,
                                                   ecc=ecc)
        elif i == 'hog':
            benchObj = HogParser.HogParser(
                prThreshold=pr_threshold,
                imgOutputDir=IMG_OUTPUT_DIR,
                localRadiationBench=LOCAL_RADIATION_BENCH,
                check_csv=checkCsv,
                ecc=ecc,
                goldBaseDir=HOG_GOLD_BASE_DIR,
                datasets=HOG_DATASETS
            )
        elif i == 'lavamd':
            benchObj = LavaMDParser.LavaMDParser(localRadiationBench=LOCAL_RADIATION_BENCH,
                                                 check_csv=checkCsv,
                                                 ecc=ecc)
        elif i == 'mergesort':
            benchObj = MergesortParser.MergesortParser(localRadiationBench=LOCAL_RADIATION_BENCH,
                                                       check_csv=checkCsv,
                                                       ecc=ecc)
        elif i == 'nw':
            benchObj = NWParser.NWParser(localRadiationBench=LOCAL_RADIATION_BENCH,
                                         check_csv=checkCsv,
                                         ecc=ecc)
        elif i == 'quicksort':
            benchObj = QuicksortParser.QuicksortParser(localRadiationBench=LOCAL_RADIATION_BENCH,
                                                       check_csv=checkCsv,
                                                       ecc=ecc)
        elif i == 'accl':
            benchObj = ACCLParser.ACCLParser(localRadiationBench=LOCAL_RADIATION_BENCH,
                                             check_csv=checkCsv,
                                             ecc=ecc)
        elif i == 'pyfasterrcnn':
            benchObj = FasterRcnnParser.FasterRcnnParser(
                prThreshold=pr_threshold,
                imgOutputDir=IMG_OUTPUT_DIR,
                localRadiationBench=LOCAL_RADIATION_BENCH,
                check_csv=checkCsv,
                ecc=ecc,
                is_fi=isFi,
                goldBaseDir=GOLD_BASE_DIR,
                datasets=FASTER_RCNN_DATASETS
            )
        elif i == 'lulesh':
            benchObj = LuleshParser.LuleshParser(localRadiationBench=LOCAL_RADIATION_BENCH,
                                                 check_csv=checkCsv,
                                                 ecc=ecc)
        elif i == 'lud':
            benchObj = LudParser.LudParser(localRadiationBench=LOCAL_RADIATION_BENCH,
                                           check_csv=checkCsv,
                                           ecc=ecc)
        elif i == 'gemm':
            benchObj = GemmParser.GemmParser(localRadiationBench=LOCAL_RADIATION_BENCH,
                                             check_csv=checkCsv,
                                             ecc=ecc)
        elif i == 'lenet':
            benchObj = LenetParser.LenetParser(parseLayers=parse_layers,
                                               prThreshold=pr_threshold,
                                               layersGoldPath=LAYERS_GOLD_PATH_LENET,
                                               layersPath=LAYERS_PATH_LENET,
                                               imgOutputDir=IMG_OUTPUT_DIR,
                                               localRadiationBench=LOCAL_RADIATION_BENCH,
                                               check_csv=checkCsv,
                                               ecc=ecc,
                                               is_fi=isFi,
                                               goldBaseDir=GOLD_BASE_DIR,
                                               datasets=LENET_DATASETS)
        elif i == 'beziersurface':
            benchObj = BezierSurfaceParser.BezierSurfaceParser()

        elif benchObj == None:
            print "\nERROR: ", i, " is not in the benchmark list, this will probaly crash the system"

        radiationBenchmarks[i] = benchObj

    print ""
