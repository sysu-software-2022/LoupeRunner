#Default configurations

"""
Configs for @Icity Runner.
[Archaea_RM] processing in default, which can be changed by requirements.
"""
# Input files and Hyper-parameters
import os
DefenseSystem_Name = "RM_A"
DefenseSystem_FilePath = "/root/ICityRunnerPackage/"  # Your Working Path
GbffFile_Path = "/mnt/data/archaea"
GbffFile_Type = "Archaea"

ICITY_CONFIG_INPUT = {
    "PTYFile": "Database/archaea_cds.pty",
    "PathToDatabase": "Database/ArchaeaProt",
    "CdsPath": "Database/archaea_cds.pty",
    "SeedPath": "Archaea_RM.xlsx",
    "NeighborhoodVicinitySize": 10000,
    "PermissiveClusteringThreshold": 0.3,
    "SortingOverlapThreshold": 0.4,
    "SortingCoverageThresold": 0.25,
    "ThreadNum": "48"   # Change global thread number here
}

# Output files
ICITY_CONFIG_OUTPUT = {
    "ICITYFileName": os .path.join("./" + DefenseSystem_Name+"_OUTPUT", "Relevance_"+DefenseSystem_Name+".tsv"),
    "VicinityClustersFileName": "VicinityPermissiveClustsLinear" + DefenseSystem_Name + ".tsv",
    "RelevanceCategoryName": "RelevanceCategory_" + DefenseSystem_Name + ".csv"
}

# Temporary files
ICITY_CONFIG_TEMPORARYFILES = {
    "VicinityFileName": os.path.join("./" + DefenseSystem_Name+"_OUTPUT", "Vicinity_"+DefenseSystem_Name+".tsv"),
    "VicinityIDsFileName": os.path.join("./" + DefenseSystem_Name+"_OUTPUT", "VicinityIDs_"+DefenseSystem_Name+".lst"),
    "VicinityFASTAFileName": os.path.join("./" + DefenseSystem_Name+"_OUTPUT", "Vicinity_"+DefenseSystem_Name+".faa"),
    "VicinityClustersFileName": os.path.join("./" + DefenseSystem_Name+"_OUTPUT", "VicinityPermissiveClustsLinear_"+DefenseSystem_Name+".tsv"),
    "ProfilesFolder": os.path.join("./" + DefenseSystem_Name+"_OUTPUT", "CLUSTERS_"+DefenseSystem_Name + "/"),
    "SortedBLASTHitsFolder": os.path.join("./" + DefenseSystem_Name+"_OUTPUT", "CLUSTERS_"+DefenseSystem_Name, "Sorted/"),
    "SeedsExtractedFileName": os.path.join("./" + DefenseSystem_Name+"_OUTPUT", "Seeds_" + DefenseSystem_Name + ".tsv"),
    # "SeedsExtractedFileName": "Seeds.tsv"   # DEMO

}
