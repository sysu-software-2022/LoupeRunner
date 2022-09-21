import os

# Hyper-parameters and Input files
DefenseSystem_Name = "Cas"
DefenseSystem_FilePath = os .path.join("./")  # Your Working Path
GbffFile_Path = "./archaea"
GbffFile_Type = "Cas"

LOUPE_CONFIG_INPUT = {
    "PTYFile": os.path.join("./", "Cas_INPUT/Database/CDS.pty"),
    "PathToDatabase": os.path.join("./", "Cas_INPUT/Database/ProteinDB"),
    "SeedPath":os.path.join("./", "Cas_INPUT/Archaea_Cas.csv"),
    "NeighborhoodVicinitySize": 10000,
    "PermissiveClusteringThreshold": 0.3,
    "SortingOverlapThreshold": 0.4,
    "SortingCoverageThresold": 0.25,
    "ThreadNum": str(os.cpu_count())  # Change global thread number here
}

# Output files
LOUPE_CONFIG_OUTPUT = {
    "ICITYFileName": os .path.join("./" + DefenseSystem_Name+"_OUTPUT", "Relevance_"+DefenseSystem_Name+".tsv"),
    "VicinityClustersFileName": os.path.join("./" + DefenseSystem_Name+"_OUTPUT", "VicinityPermissiveClustsLinear_"+DefenseSystem_Name+".tsv"),
    "RelevanceCategoryName": "RelevanceCategory_" + DefenseSystem_Name + ".csv"
}

# Temporary files
LOUPE_CONFIG_TEMPORARYFILES = {
    "VicinityFileName": os.path.join("./" + DefenseSystem_Name+"_OUTPUT", "Vicinity_"+DefenseSystem_Name+".tsv"),
    "VicinityIDsFileName": os.path.join("./" + DefenseSystem_Name+"_OUTPUT", "VicinityIDs_"+DefenseSystem_Name+".lst"),
    "VicinityFASTAFileName": os.path.join("./" + DefenseSystem_Name+"_OUTPUT", "Vicinity_"+DefenseSystem_Name+".faa"),
    "ProfilesFolder": os.path.join("./" + DefenseSystem_Name+"_OUTPUT", "CLUSTERS_"+DefenseSystem_Name + "/"),
    "SortedBLASTHitsFolder": os.path.join("./" + DefenseSystem_Name+"_OUTPUT", "CLUSTERS_"+DefenseSystem_Name, "Sorted/"),
    "SeedsExtractedFileName": os.path.join("./" + DefenseSystem_Name+"_OUTPUT", "Seeds_" + DefenseSystem_Name + ".tsv"),

}

