import os
import argparse
import subprocess


# Relevance.tsv
CLUSTER_NAME = 0
NUMBER_IN_VICINTY = 1
NUMBER_IN_ENTIRE = 2
DISTANCE_TO_SEED = 3
DS3P = 4



# 阈值暂定，需要使用统计得到一个有说服力的数值
DS3P_threshold = 0.0

# CLUSTER.hits_sorted

PROTEIN_ACCESSION = 0

# Seed.tsv
SEED_ACCESSION = 2


# Reading arguments from command line
ap = argparse.ArgumentParser(description = "SortRelevance")
ap.add_argument("-n", help = "DefenseSystemName", required = True)
ap.add_argument("-p", help = "DefenseSystemFilePath", required = True)

opts = ap.parse_args()



# 修改文件位置
DefenseSystem_Name = opts.n
DefenseSystem_FilePath = opts.p

SeedAccession_Filename = DefenseSystem_FilePath+ DefenseSystem_Name + '_OUTPUT/Seeds_' + DefenseSystem_Name + '.tsv'
CLUSTERS_Filepath = DefenseSystem_FilePath + DefenseSystem_Name + '_OUTPUT/CLUSTERS_' + DefenseSystem_Name
Vicinity_Filename = (os.path.split(DefenseSystem_FilePath+ DefenseSystem_Name + '_OUTPUT/Vicinity_'+ DefenseSystem_Name + '.faa')[1])
Relevance_Filenpath = DefenseSystem_FilePath + DefenseSystem_Name + '_OUTPUT/Relevance_' + DefenseSystem_Name + '.tsv'
Relevance_CategoryName = 'Relevance_Sorted_'+ DefenseSystem_Name + '_Category.csv'
CLUSTERHitsSorted_path = DefenseSystem_FilePath + DefenseSystem_Name + '_OUTPUT/CLUSTERS_' + DefenseSystem_Name + '/Sorted/'


DefenseSystem_Function_1 = 'abortive infection'
DefenseSystem_Function_2 = 'restriction-modification'
DefenseSystem_Function_3 = 'toxin'
DefenseSystem_Function_4 = 'argonaute'
DefenseSystem_Function_5 = 'Dnd'
Dir = "ACCESSION_A"

if not os.path.exists(Dir):
    os.mkdir(Dir)


subprocess.call("cat " + CLUSTERS_Filepath + "/CLUSTER_*.ali  | grep ref | awk -F \"|\" '{print $2, \"|\", $NF}'" + " > ACCESSION_A/ACCESSION_"+ DefenseSystem_Name+'.txt',
shell= True)
subprocess.call('cat ACCESSION_A/ACCESSION_'+ DefenseSystem_Name + '.txt | grep \''+ DefenseSystem_Function_1 +'\' | awk \'{print $0\" |  1\" }\' > ACCESSION_A/ACCESSION_ONLY_'+ DefenseSystem_Name +'.txt',
shell= True)
subprocess.call('cat ACCESSION_A/ACCESSION_' + DefenseSystem_Name + '.txt | grep -E \"'+ DefenseSystem_Function_2 + '|CRISPR|'+ DefenseSystem_Function_3 +'|'+DefenseSystem_Function_4+'|'+DefenseSystem_Function_5+'\" | awk \'{print $0  \" |  2\" }\' > ACCESSION_A/ACCESSION_Other_DefenseGene_'+ DefenseSystem_Name +'.txt',
shell= True)
subprocess.call('cat ACCESSION_A/ACCESSION_'+ DefenseSystem_Name +'.txt | grep -v \"toxin\|CRISPR\|abortive infection\|restriction-modification\|hypothetical\|argonaute\Dnd" | awk \'{print $0  \" |  3\" }\' > ACCESSION_A/ACCESSION_HouseKeepingGene_'+ DefenseSystem_Name + '.txt',
shell= True)
subprocess.call('cat ACCESSION_A/ACCESSION_'+ DefenseSystem_Name + '.txt | grep \'hypothetical\' | awk \'{print $0  \" |  4\" }\' > ACCESSION_A/ACCESSION_hypothetical_'+ DefenseSystem_Name + '.txt',
shell= True)




# 配合使用ACCESSION.sh 得到分类文件,不同抗性系统需要修改文件路径
Accession_All_FileName = 'ACCESSION_A/ACCESSION_' + DefenseSystem_Name + '.txt'
Accession_Category_Target_FileName = 'ACCESSION_A/ACCESSION_ONLY_'+ DefenseSystem_Name + '.txt'
Accession_Category_Hypothetical_FileName = 'ACCESSION_A/ACCESSION_hypothetical_'+ DefenseSystem_Name + '.txt'
ACCESSION_HouseKeepingGene_FileName = 'ACCESSION_A/ACCESSION_HouseKeepingGene_'+ DefenseSystem_Name + '.txt'
ACCESSION_Other_DefenseGene_FileName = 'ACCESSION_A/ACCESSION_Other_DefenseGene_'+ DefenseSystem_Name + '.txt'

with open(Relevance_Filenpath,'r') as F:
    Relevance = dict()
    for Line in F:
        LineValue = Line[:-1].split('\t')
        Relevance[LineValue[CLUSTER_NAME]] = [LineValue[CLUSTER_NAME], LineValue[NUMBER_IN_VICINTY], LineValue[NUMBER_IN_ENTIRE], LineValue[DISTANCE_TO_SEED], LineValue[DS3P]]

Relevance_Sorted_Target = dict()
for r in Relevance:
    if int(Relevance[r][NUMBER_IN_ENTIRE]) >= 1:
        if float(Relevance[r][DS3P]) > DS3P_threshold:
            Relevance_Sorted_Target[r] = Relevance[r]
    else:
        continue


for n in Relevance_Sorted_Target:
    CLUSTERHitsSorted_Filename = CLUSTERHitsSorted_path + n + '.hits_sorted'
    with open(CLUSTERHitsSorted_Filename,'r') as F:
        ProteinAccession = []
        for Line in F:
            LineValue = Line[:-1].split('\t')
            ProteinAccession.append(LineValue[PROTEIN_ACCESSION])
    
    Relevance_Sorted_Target[n] = [Relevance_Sorted_Target[n], ProteinAccession]


# 构建字典，引入分类符
# 与输入数据一致的防御基因--1
# 其他防御基因--2
# 管家基因--3
# 未知基因--4
Accession_Category_Target = dict()
Accession_Category_Hypothetical = dict()
Accession_Category_OtherDefense = dict()
Accession_Category_HouseKeeping = dict()

with open(Accession_Category_Target_FileName,'r') as T:
    for Line in T:
        LineValue = Line[:-1].split(' |  ')
        Accession_Category_Target[LineValue[0]] = [LineValue[1], LineValue[2]]

with open(ACCESSION_Other_DefenseGene_FileName,'r') as T:
    for Line in T:
        LineValue = Line[:-1].split(' |  ')
        Accession_Category_HouseKeeping[LineValue[0]] = [LineValue[1], LineValue[2]]

with open(ACCESSION_HouseKeepingGene_FileName,'r') as T:
    for Line in T:
        LineValue = Line[:-1].split(' |  ')
        Accession_Category_OtherDefense[LineValue[0]] = [LineValue[1], LineValue[2]]

with open(Accession_Category_Hypothetical_FileName,'r') as T:
    for Line in T:
        LineValue = Line[:-1].split(' |  ')
        Accession_Category_Hypothetical[LineValue[0]] = [LineValue[1], LineValue[2]]

Relevance_Sorted_Target_Category = dict()
for id in Relevance_Sorted_Target:
    # 每个Cluster 里多个 Accession 的功能可能不同，若不同，选取顺序如下: 1>2>3>4
    Accession_Category= {}
    for ac in Relevance_Sorted_Target[id][1]:
        if ac in Accession_Category_Target:
            Accession_Category[ac] = 1
            continue
        elif ac in Accession_Category_OtherDefense:
            Accession_Category[ac] = 2
            continue
        elif ac in Accession_Category_HouseKeeping:
            Accession_Category[ac] = 3
            continue
        elif ac in Accession_Category_Hypothetical:
            Accession_Category[ac] = 4
            continue
        else:
            Accession_Category[ac] = 5
    Cluster_Category_Name = min(Accession_Category, key= Accession_Category.get)
    Cluster_Category_Value = min(Accession_Category.values())
    if Cluster_Category_Value == 1:
        Relevance_Sorted_Target_Category[id] = [Relevance_Sorted_Target[id][0], Accession_Category_Target[Cluster_Category_Name][1]]
    elif Cluster_Category_Value == 2:
        Relevance_Sorted_Target_Category[id] = [Relevance_Sorted_Target[id][0], Accession_Category_OtherDefense[Cluster_Category_Name][1]]
    elif Cluster_Category_Value == 3:
        Relevance_Sorted_Target_Category[id] = [Relevance_Sorted_Target[id][0], Accession_Category_HouseKeeping[Cluster_Category_Name][1]]
    elif Cluster_Category_Value == 4:
        Relevance_Sorted_Target_Category[id] = [Relevance_Sorted_Target[id][0], Accession_Category_Hypothetical[Cluster_Category_Name][1]]


# 计算物种保守性（属-种分开算）
def CalConservation(Accession_Taxonomy):
        count = 0
        if not 'None' in Accession_Taxonomy:
            for key in Accession_Taxonomy.keys():
                count = count + 1/len(Accession_Taxonomy[key])
            return count/len(Accession_Taxonomy)
        else:
            for key in Accession_Taxonomy.keys():
                if key != 'None':
                    count = count + 1/len(Accession_Taxonomy[key])
            return count/len(Accession_Taxonomy)
    
# 引入物种分类信息（属-种）
Relevance_Taxonomy = dict()
Relevance_Sorted_Target_Taxonomy = dict()

with open(Accession_All_FileName,'r') as T:
    for Line in T:
        LineValue = Line[:-1].split(' |  ')
        TaxonomyID = LineValue[1].split('[')[1][:-1]
        TaxonomyID = TaxonomyID.split(' ',1)
        Relevance_Taxonomy[LineValue[0]] = TaxonomyID

for id in Relevance_Sorted_Target:
    Accession_Taxonomy_genus = {}
    Accession_Taxonomy_species = {}

    for ac in Relevance_Sorted_Target[id][1]:
        if ac in Relevance_Taxonomy:
            Accession_Taxonomy_genus[ac] = Relevance_Taxonomy[ac][0]
            # 部分Accession缺少species的注释
            try:
                Accession_Taxonomy_species[ac] = Relevance_Taxonomy[ac][1]
            except IndexError:
                Accession_Taxonomy_species[ac] = 'None'

        flipped_genus = {}
        flipped_species = {}

        for key,value in Accession_Taxonomy_genus.items():
            if value not in flipped_genus:
                flipped_genus[value] = list()
                flipped_genus[value].append(key)
            else:
                flipped_genus[value].append(key)

        for key,value in Accession_Taxonomy_species.items():   
            if value not in flipped_species:
                flipped_species[value] = list()
                flipped_species[value].append(key)
            else:
                flipped_species[value].append(key)
    if flipped_genus == {}:
        continue
    else:
        Relevance_Sorted_Target_Taxonomy[id] = [CalConservation(flipped_genus),CalConservation(flipped_species)]


with open(Relevance_CategoryName,'w') as f:
 for i in Relevance_Sorted_Target_Category:
    for element in Relevance_Sorted_Target_Category[i][0]:
        f.write(element)
        f.write(',')
    f.write(Relevance_Sorted_Target_Category[i][1])
    for n in Relevance_Sorted_Target_Taxonomy[i]:
        f.write(',')
        f.write(str(n))
        
    f.write("\n")


