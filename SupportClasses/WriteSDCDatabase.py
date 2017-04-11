#!/usr/bin/env python

import sys
import re
import os
import copy
from glob import glob
import shelve


class WriteSDCDatabase():

    def startProgress(self,title):
        global progress_x
        sys.stdout.write(title + ": [" + "-" * 40 + "]" + chr(8) * 41)
        sys.stdout.flush()
        progress_x = 0


    def progress(self,x):
        global progress_x
        x = int(x * 40 // 100)
        sys.stdout.write("#" * (x - progress_x))
        sys.stdout.flush()
        progress_x = x


    def endProgress(self):
        sys.stdout.write("#" * (40 - progress_x) + "]\n")
        sys.stdout.flush()


    def generateSDCList(self,fi):
        sdc_item_list = []
        sdc_iter = 0  # number of iterations with error
        iter_err_count = 0  # number of wrong elements inside one iteration
        acc_err = 0
        header = "unknown"
        errors = []

        lines = open(fi, "r")
        fileName = fi
        m = re.match(".*/(.*.log)", fi)
        if m:
            fileName = m.group(1)

        for line in lines:

            m = re.match(".*HEADER(.*)", line)
            if m:
                header = m.group(1)


            m = re.match(".*SDC.*Ite:(\d+) .*KerErr:(\d+) .*AccErr:(\d+).*", line)
            #for old nw logs
            if m == None:
                m = re.match(".*SDC.*it:(\d+).*k_err:(\d+).*acc_err:(\d+).*", line)
            # SDC Ite:3439 KerTime:0.200894 AccTime:676.249022 KerErr:1 AccErr:1
            if m:  # ocorre o SDC no log apos todos os erros da execucao terem sido printados no log
                sdc_iter = m.group(1)
                iter_err_count = m.group(2)
                acc_err = m.group(3)
                if len(errors) > 0:
                    sdc_item_list.append([fileName, header, sdc_iter, iter_err_count, acc_err, copy.deepcopy(errors)])
                errors = []

            m = re.match("(.*ERR.*)", line)
            if m:
                errors.append(m.group(1))
            else:
                #INF abft_type: dumb image_list_position: [151] row_detected_errors: 1 col_detected_errors: 1
                m = re.match("(.*INF.*)", line)
                if m:
                    errors.append(m.group(1))

        #check if file finish or not
        if any('END' in word for word in lines):
            sdc_item_list.append('END')

        return sdc_item_list

    ######### main
    # pega todos os arquivos .log na pasta onde esta sendo
    # executado, e nas subpastas tambem
    ###########################################
    # MAIN
    ###########################################'

    def execute(self):
        print("Retrieving file list...")
        all_logs = [y for x in os.walk(".") for y in glob(os.path.join(x[0], '*.log'))]

        # vai ordenar por data, "pelo nome do arquivo que eh uma data"
        all_logs.sort()

        benchmarks_dict = dict()

        total_files = len(all_logs)
        i = 1
        # percorre todos os arquivos .log
        for fi in all_logs:
            progress = "{0:.2f}".format(i / total_files * 100)
            sys.stdout.write("\rProcessing file " + str(i) + " of " + str(total_files) + " - " + progress + "%")
            sys.stdout.flush()
            # verifica se o arquivo eh um arquivo de log dos nossos
            m = re.match(".*/(\d+)_(\d+)_(\d+)_(\d+)_(\d+)_(\d+)_(.*)_(.*).log", fi)
            if m:
                benchmark = m.group(7)
                machine_name = m.group(8)

                sdcs_list = self.generateSDCList(fi)

                if len(sdcs_list) > 0:
                    if benchmark + "_" + machine_name not in benchmarks_dict:
                        benchmarks_dict[benchmark + "_" + machine_name] = []
                    benchmarks_dict[benchmark + "_" + machine_name].extend(sdcs_list)
            i += 1
        sys.stdout.write("Processing file " + str(i) + " of " + str(total_files) + " - 100%                     " + "\n")

        db = shelve.open("errors_log_database")
        # for k, v in benchmarks_dict.iteritems(): #python2.*
        print("writing to database ...")
        for k, v in benchmarks_dict.items():  # python3
            db[k] = v
            print("key: ", k, "; size of v:", len(v))
        # print("key: ",k,"\n\n")
        # i = 0
        # for val in v:
        #	print ("value[",i,"]: ",val)
        #	i += 1
        # print("\n\n\n")

        db.close()
        print("database written!")
        sys.exit(0)

def writeToFile(db, filename):
    outFile = open(filename, 'w')
    for benchmarkname_machinename, sdcItem in db.iteritems():
        try:
            if 'PyFasterRcnn' in benchmarkname_machinename or 'Darknet' in benchmarkname_machinename:
                outFile.write("BENCHMARK_AND_MACHINE_NAME:" + str(benchmarkname_machinename))
                outFile.write("\n")
                print benchmarkname_machinename
                for item in sdcItem:
                    logFileName = item[0]
                    sdcIteration = item[2]
                    iteErrors = item[3]
                    # accIteErrors = item[4]
                    errList = item[5]
                    outFile.write("log_name:" + str(logFileName) + "\n")
                    outFile.write("sdc_iteration:" + str(sdcIteration) + "\n")
                    outFile.write("it_errors:"+str(iteErrors) + "\n")
                    # outFile.write("acc_it_errors:" + str(accIteErrors) + "\n")
                    outFile.write("ERROR_LIST\n")
                    for i in errList:
                        outFile.write(str(i) + "\n")

                    outFile.write("\n")

        except:
            print "error somewhere"
    outFile.close()




# open ecc on
dbEccON = shelve.open("/home/fernando/Dropbox/UFRGS/Pesquisa/Teste_12_2016/ECC_ON/errors_log_database_ecc_on")

print "Saving ECC ON"
writeToFile(db=dbEccON, filename="/home/fernando/Dropbox/ANONYMOUS_DATA_REPO/ecc_on")

dbEccON.close()

dbEccOFF = shelve.open("/home/fernando/Dropbox/UFRGS/Pesquisa/Teste_12_2016/ECC_OFF/errors_log_database_ecc_off")

print "Saving ECC OFF"
writeToFile(db=dbEccOFF, filename="/home/fernando/Dropbox/ANONYMOUS_DATA_REPO/ecc_off")

dbEccOFF.close()

dbINST = shelve.open("/home/fernando/Dropbox/UFRGS/Pesquisa/Fault_Injections/sassifi_darknet_paper_micro/inst/errors_log_database_inst")

print "Saving INST"
writeToFile(db=dbINST, filename="/home/fernando/Dropbox/ANONYMOUS_DATA_REPO/sassifi_inst")

dbINST.close()

dbRF = shelve.open("/home/fernando/Dropbox/UFRGS/Pesquisa/Fault_Injections/sassifi_darknet_paper_micro/rf/errors_log_database_rf")

print "Saving RF"
writeToFile(db=dbRF, filename="/home/fernando/Dropbox/ANONYMOUS_DATA_REPO/sassifi_rf")

dbRF.close()