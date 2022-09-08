import argparse
import re
def LoadSeedDirt(SeedFileName, NoID =False):
    Seeds = dict()

    ContigID = 3
    Start = 4
    End = 5
    Offset = 0

    return AddSeedDictFields(SeedFileName, Seeds, ContigID, Start, End, Offset, NoID)

def AddSeedDictFields(SeedFileName, Seeds, ContigID, Start, End, Offset, NoID=False):
    with open(SeedFileName, 'r') as File:
        for Line in File:
            LineValues = Line.split('\t')
            LineValues[-1] = LineValues[-1][:-1]

            if not NoID:
                ID = LineValues[2]
            else:
                ID = 'Seed'

            ORF_start, ORF_end = minmax(int(LineValues[Start]), int(LineValues[End]))
            if LineValues[ContigID] in Seeds:
                Seeds[LineValues[ContigID]].append([max(ORF_start - Offset, 0), ORF_end + Offset, ID, LineValues])
            else:
                Seeds[LineValues[ContigID]] = [[max(ORF_start - Offset, 0), ORF_end + Offset, ID, LineValues]]
            
        for Key in Seeds:
            Seeds[Key] = sorted(Seeds[Key], key= lambda e:e[0])
    return Seeds

def minmax(X, Y):
    return min(X, Y), max(X, Y)

# CDS PTY tsv file columns
PTY_LocusTag = 0
PTY_Coordinates = 1
PTY_Strand = 2
PTY_SpecieName = 3
PTY_ContigId = 4
PTY_AccessionNo = 5

def GetSeed(ContigID, Start, End, Seeds):
    if not ContigID in Seeds:
        return []
    
    for ORF in Seeds[ContigID]:
        if(Start <= ORF[1]) and (End >= ORF[0]):
            return ORF

    return []

def IsInSeeds(ContigID, Start, End, Seeds):
    InSeed = GetSeed(ContigID, Start, End, Seeds)
    if len(InSeed) == 0:
        return False
    return True

def WriteSeedIslands(SeedIslandPTYLines, ResultFile):

    if len(SeedIslandPTYLines) > 0:
        ResultFile.write('===\n')
        for LineValues in SeedIslandPTYLines:
            ResultFile.write(
            LineValues[0] + '\t' + 
            LineValues[1].replace(':','..') + '\t' +
            LineValues[2] + '\t' + 
            LineValues[3] + '\t' +
            LineValues[4] + '\n')


def WriteIslands(ContigLines, ResultFile, ContigID, Seeds, SeedIslandOffset):
    if ContigID not in Seeds:
        return
    if len(Seeds[ContigID]) == 0:
        return 
    
    
    ContigLines = sorted(ContigLines, key= lambda e:e[0])

    SeedIslandPTYLines = []
    for Line in ContigLines:
        LineValues = Line[1]

        Coordinates = LineValues[PTY_Coordinates].split(":")
        
        
        try:
            Start = int(Coordinates[0])
            End = int(Coordinates[1])
        except ValueError:
            continue

        if IsInSeeds(ContigID, Start - SeedIslandOffset, End + SeedIslandOffset, Seeds):
            SeedIslandPTYLines.append(
                [LineValues[PTY_AccessionNo], LineValues[PTY_Coordinates], LineValues[PTY_Strand],
                LineValues[PTY_SpecieName], LineValues[PTY_ContigId]])
        else:
            if len(SeedIslandPTYLines) > 0:
                WriteSeedIslands(SeedIslandPTYLines, ResultFile)

            SeedIslandPTYLines = []
    
    if len(SeedIslandPTYLines) > 0:
        WriteSeedIslands(SeedIslandPTYLines, ResultFile)

if __name__ == "__main__":
    # Reading arguments from command line
    ap = argparse.ArgumentParser(description="Extracting seeds from CDS file")
    ap.add_argument("-c", help="CDSFileName, cds pty file, containing seed information", required=True)
    ap.add_argument("-s", help="SeedsFileName, seeds tsv file", required=True)
    ap.add_argument("-o", help="ResultFileName, output tsv file", required=True)
    ap.add_argument("-d", help="Offset around seed (base pairs)", required=True)
    opts = ap.parse_args()

    SeedFileName = opts.s  # Archaea_Seeds_RM_A.tsv
    PTYDataFileName = opts.c  # archaea_cds.pty
    ResultFileName = opts.o  # Vicinity.tsv

    SeedIslandOffset = int(opts.d)
    Seeds = LoadSeedDirt(SeedFileName)

    ContigID = ''
    ContigLines = []
    with open(ResultFileName, 'w') as ResultFile:
        with open(PTYDataFileName,'r') as PTYData:
            for Line in PTYData:
                Line = Line[:-1]
                LineValues = Line.split('\t')

                if ContigID != LineValues[PTY_ContigId]:
                    WriteIslands(ContigLines, ResultFile, ContigID, Seeds, SeedIslandOffset)
                    ContigLines =[]

                ContigID = LineValues[PTY_ContigId]
                Coordinates = LineValues[PTY_Coordinates].split(':')
                Coordinates[0] = re.findall(r'\d+', Coordinates[0])[0]
                Start = int(Coordinates[0])


                ContigLines.append([Start, LineValues])

            WriteIslands(ContigLines, ResultFile, ContigID, Seeds, SeedIslandOffset)
