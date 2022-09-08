import argparse
import multiprocessing
import subprocess
import os
import time
from multiprocessing import Pool

ap = argparse.ArgumentParser(description = "Creates protein profiles in specified folder for clusters in given file")
ap.add_argument("-f", help = "Clusters file name", required = True)
ap.add_argument("-c", help = "Folder name where profiles will be saved", required = True)
ap.add_argument("-d", help = "Path to protein database", required = True)

cpu_cnt = os.cpu_count()

opts = ap.parse_args()
ClustersFileName = opts.f
ClustersFolderName = opts.c
Database = opts.d

ClusterNo = 0

if not os.path.exists(ClustersFolderName):
    subprocess.call("mkdir " + ClustersFolderName, shell = True)



def generator(ClusterNo, Sequence):
    ClusterIDs = Sequence[:-1].split("\t")[1].split(" ")
    writer(ClusterIDs, ClusterNo)
    return Sequence


def writer(ClusterIDs, ClusterNo):
    global cpu_cnt
    ClusterProfileFileName = "CLUSTER_" + str(ClusterNo + 1) + ".ali"
    
    """
       Critical Section
    """

    TmpIDsFileName = "Tmp_IDs" + "_" + str(ClusterNo) + ".lst"
    TmpFASTAFileName = "Tmp_FASTA" + "_" + str(ClusterNo) + ".faa"

    with open(TmpIDsFileName, "w") as IDsFile:
        IDsFile.write("\n".join(ClusterIDs))

    subprocess.call("blastdbcmd -db " + Database + " -entry_batch " + TmpIDsFileName + " -long_seqids > " + TmpFASTAFileName
                    , shell=True)

    subprocess.call("muscle -align " + TmpFASTAFileName + " -output " + ClustersFolderName + "/" + ClusterProfileFileName
                    , shell=True)

    
    subprocess.call("rm " + TmpIDsFileName, shell=True)

    subprocess.call("rm " + TmpFASTAFileName, shell=True)

 

def multi_process():
    global cpu_cnt
    
    with open(ClustersFileName, 'r') as File, Pool(cpu_cnt) as pool:
        Sequences = File.readlines(); Length = len(Sequences)
        for ClusterNo, Sequence in enumerate(Sequences):
            pool.apply_async(generator, (ClusterNo, Sequence))

        pool.close()
        pool.join()


if __name__ == '__main__':
    t1 = time.time()
    cnt = 0
    multi_process()

    t2 = time.time()


    print("Work Done !")
    print("Used time: ", t2 - t1, "s")
