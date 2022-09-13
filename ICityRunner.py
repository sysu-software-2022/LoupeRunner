import config
import subprocess
import argparse
import shutil
import os
import sys


def subprocess_call(Stage, CallText):

    print(Stage)
    print(CallText)
    try:
        # print("Calling: ", CallText)
        devnull = open(os.devnull, 'wb')
        subprocess.check_call(CallText, shell=True, stdout=devnull, stderr=devnull)
        '''
        # Fetch print std
        process = subprocess.Popen(CallText, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE )
        while True:
            if process.poll() is None:
                line = process.stdout.readline().strip()
                print(line)
       '''
    except subprocess.CalledProcessError as e:
        print(str(e))
        print(Stage + " failed")
        sys.exit(1)

def CheckDependencies():
    DependenciesMissing = False
    if shutil.which("mmseqs") is None:
        print("mmseqs not available")
        DependenciesMissing = True

    if shutil.which("psiblast") is None:
        print("psiblast not available")
        DependenciesMissing = True

    if shutil.which("blastdbcmd") is None:
        print("blastdbcmd not available")
        DependenciesMissing = True

    if shutil.which("python") is None:
        print("python not available")
        DependenciesMissing = True

    if shutil.which("muscle") is None:
        print("muscle not available")
        DependenciesMissing = True

    if DependenciesMissing:
        print("required software missing")
        sys.exit(1)

    return

ap = argparse.ArgumentParser(description = "ICITY pipeline. Provides analysis of protein neighborhoods around " +
                                           "specified seeds (coordinates for list of loci of interest), using " +
                                           "spatial information of ORFs and their protein sequrncrs, to search for " +
                                           "protein families associated to the seeds. Input informstion - config ot input with default?")

opts = ap.parse_args()
CheckDependencies()
Dir = config.DefenseSystem_Name + "_OUTPUT"
if not os.path.exists(Dir):
    os.mkdir(Dir)

# Run steps here

subprocess_call("Step 4: Extracting CDS", "python CDS_extract.py" +
                " -p " + config.GbffFile_Path +
                " -s " + config.GbffFile_Type)


subprocess_call("Step 5: Extracting seeds", "python HashSeedExtract.py -c " + config.ICITY_CONFIG_INPUT["PTYFile"] +
                " -s " + config.ICITY_CONFIG_INPUT["SeedPath"] +
                " -o " + config.ICITY_CONFIG_TEMPORARYFILES["SeedsExtractedFileName"])


subprocess_call("Step 6: Selecting neighborhoods", "python FindNeighborhood.py -c " + config.ICITY_CONFIG_INPUT["PTYFile"] +
                " -s " + config.ICITY_CONFIG_TEMPORARYFILES["SeedsExtractedFileName"] +
                " -o " + config.ICITY_CONFIG_TEMPORARYFILES["VicinityFileName"] +
                " -d " + str(config.ICITY_CONFIG_INPUT["NeighborhoodVicinitySize"]))

subprocess_call("Step 7: Collecting protein IDs", "grep -v \"===\" " + config.ICITY_CONFIG_TEMPORARYFILES["VicinityFileName"] + " | cut -f1 | sort -u > " +
                config.ICITY_CONFIG_TEMPORARYFILES["VicinityIDsFileName"])

subprocess_call("Step 8: Fetching protein sequences", "blastdbcmd -db " + config.ICITY_CONFIG_INPUT["PathToDatabase"] +
                " -entry_batch " + config.ICITY_CONFIG_TEMPORARYFILES["VicinityIDsFileName"] +
                " -long_seqids > " + config.ICITY_CONFIG_TEMPORARYFILES["VicinityFASTAFileName"])

subprocess_call("Step 9: Clustering protein seqiences", "bash RunClust.sh " + config.ICITY_CONFIG_TEMPORARYFILES["VicinityFASTAFileName"] + " " +
                str(config.ICITY_CONFIG_INPUT["PermissiveClusteringThreshold"]) + " " +
                config.ICITY_CONFIG_OUTPUT["VicinityClustersFileName"])

subprocess_call("Step 10: Making profiles", "python MakeProfiles.py -f " + config.ICITY_CONFIG_OUTPUT["VicinityClustersFileName"] +
                " -c " + config.ICITY_CONFIG_TEMPORARYFILES["ProfilesFolder"] +
                " -d " + config.ICITY_CONFIG_INPUT["PathToDatabase"])


subprocess_call("Step 11: Running PSI-BLAST for profiles", "python RunPSIBLAST.py -c " + config.ICITY_CONFIG_TEMPORARYFILES["ProfilesFolder"] +
               " -d " + config.ICITY_CONFIG_INPUT["PathToDatabase"] + " -t " + config.ICITY_CONFIG_INPUT["ThreadNum"]
                 )

subprocess_call("Step 12: Sorting blast hits", "python SortBLASTHitsInMemory.py -c " + config.ICITY_CONFIG_TEMPORARYFILES["ProfilesFolder"] +
                " -o " + config.ICITY_CONFIG_TEMPORARYFILES["SortedBLASTHitsFolder"] +
                " -p " + config.ICITY_CONFIG_INPUT["PTYFile"] +
                " -i " + config.ICITY_CONFIG_TEMPORARYFILES["VicinityIDsFileName"] +
                " -s " + config.ICITY_CONFIG_TEMPORARYFILES["SeedsExtractedFileName"] +
                " -v " + config.ICITY_CONFIG_TEMPORARYFILES["VicinityFileName"] +
                " -z " + str(config.ICITY_CONFIG_INPUT["SortingOverlapThreshold"]) +
                " -x " + str(config.ICITY_CONFIG_INPUT["SortingCoverageThresold"]))

subprocess_call("Step 13: Calculating ICITY metric", "bash Cal.sh " +
                config.ICITY_CONFIG_TEMPORARYFILES["SortedBLASTHitsFolder"] + " " +
                config.ICITY_CONFIG_INPUT["PathToDatabase"] + " " +
                config.ICITY_CONFIG_OUTPUT["VicinityClustersFileName"] + " " +
                config.ICITY_CONFIG_OUTPUT["ICITYFileName"] + " " +
                config.ICITY_CONFIG_INPUT["ThreadNum"]
                )

subprocess_call("Step 14: Sorting Relevance", "python SortRelevance.py -n " + config.DefenseSystem_Name+
                " -p " + config.DefenseSystem_FilePath
                )
