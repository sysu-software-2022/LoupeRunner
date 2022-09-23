subprocess_call("Step 12: Sorting blast hits", "python SortBLASTHitsInMemory.py -c " + config.LOUPE_CONFIG_TEMPORARYFILES["ProfilesFolder"] +
#                 " -o " + config.LOUPE_CONFIG_TEMPORARYFILES["SortedBLASTHitsFolder"] +
#                 " -p " + config.LOUPE_CONFIG_INPUT["PTYFile"] +
#                 " -i " + config.LOUPE_CONFIG_TEMPORARYFILES["VicinityIDsFileName"] +
#                 " -s " + config.LOUPE_CONFIG_TEMPORARYFILES["SeedsExtractedFileName"] +
#                 " -v " + config.LOUPE_CONFIG_TEMPORARYFILES["VicinityFileName"] +
#                 " -z " + str(config.LOUPE_CONFIG_INPUT["SortingOverlapThreshold"]) +
#                 " -x " + str(config.LOUPE_CONFIG_INPUT["SortingCoverageThresold"]))