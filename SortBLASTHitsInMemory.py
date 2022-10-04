import os
import argparse

# Reading arguments from command line
ap = argparse.ArgumentParser(description = "Collecting all PSIBLAST hits in specified folder and sorting them between clusters. Marking hits that are nearby seeds and storing distance to the seeds.")
ap.add_argument("-c", help = "Folder name where hits stored", required = True)
ap.add_argument("-o", help = "Folder name where sorted result hits stored", required = True)
ap.add_argument("-p", help = "PTY file containing coordinates of ORFs of genomic database", required = True)
ap.add_argument("-i", help = "List of protein IDs in vicinity of baits", required = True)
ap.add_argument("-s", help = "Baits coordinates", required = True)
ap.add_argument("-v", help = "Vicinity around the baits, needed to calculate distances to the baits", required = True)
ap.add_argument("-z", default=0.4, help = "Overlap threshold, hits are subject to sort between two profiles if they are overlapping for more than threshold value", required = False)
ap.add_argument("-x", default=0.25, help = "Coverage threshold, hits are stored if they cover original profile for more than threshold value", required = False)

opts = ap.parse_args()
ClustersHitsFolder = opts.c
SortedHitsFolder = opts.o
PTYFileName = opts.p
VicinityProteinIDsFileName = opts.i
SeedsFileName = opts.s
VicinityFileName = opts.v
MIN_COVERAGE_FILTER = float(opts.x)
MIN_OVERLAP_FILTER = float(opts.z)


HIT_Score = 1
HIT_Cluster = 5
HIT_ALIGNMENT_START = 2
HIT_ALIGNMENT_STOP = 3
HIT_ALIGNMENT_Sequence = 4
HIT_Protein_ID = 0

INFO_CONTIG = 0
INFO_BAITED = 1
INFO_ORF_START = 2
INFO_ORF_STOP = 3
INFO_ORF_DISTANCE_TO_BAIT = 4


def AddHitToDict(TargetHitsDict, Hit):
    BetterHitExists = False

    for DictHit in TargetHitsDict[Hit[HIT_Protein_ID]]:
        InterCoverage = min(Hit[HIT_ALIGNMENT_STOP],
                            DictHit[HIT_ALIGNMENT_STOP] - max(Hit[HIT_ALIGNMENT_START], DictHit[HIT_ALIGNMENT_START]))
        MinLength = min(Hit[HIT_ALIGNMENT_STOP] - Hit[HIT_ALIGNMENT_START],
                        DictHit[HIT_ALIGNMENT_STOP] - DictHit[HIT_ALIGNMENT_START])

        if InterCoverage / MinLength > MIN_COVERAGE_FILTER:
            if Hit[HIT_Score] > DictHit[HIT_Score]:
                TargetHitsDict[Hit[HIT_Protein_ID]].remove(DictHit)
            else:
                BetterHitExists = True
                break

    if not BetterHitExists:
        TargetHitsDict[Hit[HIT_Protein_ID]].append(Hit)

    return TargetHitsDict



def AddTargetHitsValues(TargetHitsFileName, TargetHitsDict, ProteinInfoDict):  # TargetHitsDict):
    BLAST_FORMAT_ALIGNMENT_TARGET_PROTEIN_ID = 1
    BLAST_FORMAT_ALIGNMENT_START = 8
    BLAST_FORMAT_ALIGNMENT_STOP = 9
    BLAST_FORMAT_ALIGNMENT_SCORE = 10
    BLAST_FORMAT_ALIGNMENT_SEQUENCE = 7

    TargetValues = []
    BestScoreLine = []
    MaxScore = 0
    ClusterId = os.path.splitext(os.path.basename(TargetHitsFileName))[0]

    with open(TargetHitsFileName, "r") as TargetHitsFile:
        for Line in TargetHitsFile:
            if Line[0] == "#":
                continue

            LineValues = Line.split("\t")
            LineValues[-1] = LineValues[-1][:-1]

            # Alignment Data
            Start = int(LineValues[BLAST_FORMAT_ALIGNMENT_START])
            Stop = int(LineValues[BLAST_FORMAT_ALIGNMENT_STOP])
            Score = int(LineValues[BLAST_FORMAT_ALIGNMENT_SCORE])
            if "|" in LineValues[BLAST_FORMAT_ALIGNMENT_TARGET_PROTEIN_ID]:
                ProteinID = LineValues[BLAST_FORMAT_ALIGNMENT_TARGET_PROTEIN_ID].split("|")[
                    1]  # Accession|ID| format expected
            else:
                ProteinID = LineValues[BLAST_FORMAT_ALIGNMENT_TARGET_PROTEIN_ID]

            HitLine = [ProteinID, Score, Start, Stop, LineValues[BLAST_FORMAT_ALIGNMENT_SEQUENCE], ClusterId]
            HitLine.extend(ProteinInfoDict[ProteinID])

            if Score > MaxScore:
                BestScoreLine = HitLine
                MaxScore = Score

            TargetValues.append(HitLine)

    if len(TargetValues) > 0:  # no hits
        # max length of alignment is taken as selflength to filter by coverage
        # this value is used as representative length of alignment
        BestScoreLength = len(BestScoreLine[HIT_ALIGNMENT_Sequence].replace("-", ""))

        for Hit in TargetValues:
            if len(Hit[HIT_ALIGNMENT_Sequence].replace("-",
                                                       "")) / BestScoreLength >= MIN_OVERLAP_FILTER:  # filtering by coverage
                if Hit[HIT_Protein_ID] in TargetHitsDict:
                    TargetHitsDict = AddHitToDict(TargetHitsDict, Hit)
                else:
                    TargetHitsDict[Hit[HIT_Protein_ID]] = [Hit]

    return ClusterId

def GetDistToSeedDict(AnnotationFileName, SeedsDict):
    LOCI_PROTEIN_ID = 0
    LOCI_CONTIG_ID = 4
    LOCI_COORDINATES = 1

    DistToSeed = dict()

    Accessions = dict()
    IslandSeeds = []
    for Line in open(AnnotationFileName, "r"):
        LineValues = Line[:-1].split("\t")

        if LineValues[LOCI_PROTEIN_ID] == "===":
            if len(Accessions) > 0:
                if len(IslandSeeds) == 0:
                    raise "NoSeedFound"
                else:
                    for Accession in Accessions:
                        DistToSeed[Accession] = min([abs(x - Accessions[Accession]) for x in IslandSeeds])

            Accessions = dict()
            IslandSeeds = []
        else:
            Accessions[LineValues[LOCI_PROTEIN_ID]] = len(Accessions) + 1

            StartStop = LineValues[LOCI_COORDINATES].split("..")
            if IsInSeeds(LineValues[LOCI_CONTIG_ID], int(StartStop[0]), int(StartStop[1]), SeedsDict):
                IslandSeeds.append(len(Accessions))

    if len(Accessions) > 0:
        if len(IslandSeeds) == 0:
            raise "NoSeedFound"
        else:
            for Accession in Accessions:
                DistToSeed[Accession] = min([abs(x - Accessions[Accession]) for x in IslandSeeds])

    return DistToSeed

def LoadProteinInfoDict(PTYFileName, VicinityProteinIDs, LociDists):
    PTY_PROTEIN_ID = 5
    PTY_CONTIG_ID = 4
    PTY_COORDINATES = 1

    ProteinInfoDict = dict()

    for Line in open(PTYFileName):
        LineValues = Line[:-1].split("\t")

        StartStop = LineValues[PTY_COORDINATES].split(":")

        if LineValues[PTY_PROTEIN_ID] in VicinityProteinIDs:
            InVicinity = "1"
        else:
            InVicinity = "0"

        if LineValues[PTY_PROTEIN_ID] in LociDists:
            Dist = LociDists[LineValues[PTY_PROTEIN_ID]]
        else:
            Dist = 10000

        # in assumption that Protein IDs are unique
        ProteinInfoDict[LineValues[PTY_PROTEIN_ID]] = [LineValues[PTY_CONTIG_ID], InVicinity,
                                                       StartStop[0], StartStop[1], Dist]

    return ProteinInfoDict

def LoadList(FileName):
    ListValues = []
    for Line in open(FileName):
        ListValues.append(Line[:-1])
    return ListValues

def LoadSeedsDict(SeedsFileName):
    Seeds = dict()
    ContigField = 3
    StartField = 4
    EndField = 5
    Offset = 0

    return AddSeedsDictByFields(SeedsFileName, Seeds, ContigField, StartField, EndField, Offset)

def AddSeedsDictByFields(FileName, SeedDict, ContigField, StartField, EndField, Offset):
    with open(FileName, "r") as File:
        for Line in File:
            LineValues = Line.split("\t")
            LineValues[-1] = LineValues[-1][:-1]
            ID = LineValues[0]

            Start, End = minmax(int(LineValues[StartField]), int(LineValues[EndField]))
            if LineValues[ContigField] in SeedDict:
                SeedDict[LineValues[ContigField]].append([max(Start - Offset, 0), End + Offset, ID, LineValues])
            else:
                SeedDict[LineValues[ContigField]] = [[max(Start - Offset, 0), End + Offset, ID, LineValues]]

    for Key in SeedDict:
        SeedDict[Key] = sorted(SeedDict[Key], key = lambda e: e[0])

    return SeedDict

def minmax(X, Y):
    return min(X, Y), max(X, Y)

def IsInSeeds(ContiAccessionD, Start, Stop, SeedsDict):
    Seed = GetSeed(ContiAccessionD, Start, Stop, SeedsDict)
    if len(Seed) == 0:
        return False
    return True

def GetSeed(ContiAccessionD, Start, Stop, SeedsDict):
    if not ContiAccessionD in SeedsDict:
        return []

    for ORF in SeedsDict[ContiAccessionD]:
        if (Start <= ORF[1]) and (Stop >= ORF[0]):
            return ORF

    return []

VicinityProteinIDs = set(LoadList(VicinityProteinIDsFileName))
Seeds = LoadSeedsDict(SeedsFileName)
LociDists = GetDistToSeedDict(VicinityFileName, Seeds)
ProteinInfoDict = LoadProteinInfoDict(PTYFileName, VicinityProteinIDs, LociDists)

if not os.path.exists(SortedHitsFolder):
    os.makedirs(SortedHitsFolder)

ProteinHitsDict = dict()
Clusters = []
for FileName in os.listdir(ClustersHitsFolder):
    if not FileName.endswith(".hits"):
        continue

    ClusterId = AddTargetHitsValues(ClustersHitsFolder + FileName, ProteinHitsDict, ProteinInfoDict)
    Clusters.append(ClusterId)

print("Loading BLAST hits complete.")

ClusterHitsDict = dict()
for ProteinID in ProteinHitsDict:
    for Hit in ProteinHitsDict[ProteinID]:
        if Hit[HIT_Cluster] in ClusterHitsDict:
            ClusterHitsDict[Hit[HIT_Cluster]].append(Hit)
        else:
            ClusterHitsDict[Hit[HIT_Cluster]] = [Hit]

print("Moving sorting hits by clusters complete.")

for ClusterId in Clusters:
    if ClusterId in ClusterHitsDict:
        with open(SortedHitsFolder + str(ClusterId) + ".hits_sorted", "w") as SortedFile:
            for Hit in ClusterHitsDict[ClusterId]:
                ResLine = "\t".join([str(x) for x in Hit])

                SortedFile.write(ResLine + "\n")
    else: # empty file
        with open(SortedHitsFolder + str(ClusterId) + ".hits_sorted", "w") as SortedFile:
            SortedFile.write("")
