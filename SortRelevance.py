import os
import subprocess
import argparse
import pandas as pd
import numpy as np
import sklearn
from imblearn.over_sampling import SMOTE
from collections import Counter
from sklearn.preprocessing import LabelEncoder,OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score, accuracy_score, plot_confusion_matrix
from sklearn.model_selection import GridSearchCV
from sklearn import preprocessing

from sklearn.neural_network import MLPClassifier
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier,AdaBoostClassifier,BaggingClassifier,\
                            ExtraTreesClassifier,GradientBoostingClassifier,HistGradientBoostingClassifier


CLUSTER_NAME = 0
NUMBER_IN_VICINTY = 1
NUMBER_IN_ENTIRE = 2
DISTANCE_TO_SEED = 3
DS3P = 4



DS3P_threshold = 0.0


PROTEIN_ACCESSION = 0

SEED_ACCESSION = 2

class NotDefenseSystem(Exception): pass

# Reading arguments from command line
ap = argparse.ArgumentParser(description = "SortRelevance")
ap.add_argument("-n", help = "DefenseSystemName", required = True)
ap.add_argument("-p", help = "DefenseSystemFilePath", required = True)
ap.add_argument("-d", help = "Database Path", required = True)

opts = ap.parse_args()



DefenseSystem_Name = opts.n
DefenseSystem_FilePath = opts.p
PathToDatabase = opts.d


SeedAccession_Filename = DefenseSystem_FilePath+ DefenseSystem_Name + '_OUTPUT/Seeds_' + DefenseSystem_Name + '.tsv'
CLUSTERS_Filepath = DefenseSystem_FilePath + DefenseSystem_Name + '_OUTPUT/CLUSTERS_' + DefenseSystem_Name 
CLUSTERHitsSorted_path = DefenseSystem_FilePath + DefenseSystem_Name + '_OUTPUT/CLUSTERS_' + DefenseSystem_Name + '/Sorted/'
Vicinity_Filename=(os.path.split(DefenseSystem_FilePath+ DefenseSystem_Name + '_OUTPUT/Vicinity_'+ DefenseSystem_Name + '.faa')[1])
Relevance_Filenpath = DefenseSystem_FilePath+DefenseSystem_Name + '_OUTPUT/Relevance_' + DefenseSystem_Name + '.tsv'
Relevance_CategoryName = DefenseSystem_FilePath+DefenseSystem_Name + '_OUTPUT/Relevance_Sorted_'+ DefenseSystem_Name + '_Category.csv'
CLUSTERS_Filenpath = DefenseSystem_FilePath + DefenseSystem_Name + '_OUTPUT/CLUSTERS_' + DefenseSystem_Name 



def makecategoryfile(DefenseSystem_Name, DefenseSystem_Function):
    tmplist = [DefenseSystem_Function_1,DefenseSystem_Function_2,DefenseSystem_Function_3,DefenseSystem_Function_4,DefenseSystem_Function_5]
    tmpname = ''
    for i in tmplist:
        if i != DefenseSystem_Function:
            tmpname = tmpname + i + '|'
    subprocess.call("cat " + CLUSTERS_Filepath + "/CLUSTER_*.ali  | grep ref | awk -F \"|\" '{print $2, \"|\", $NF}'" + " > ACCESSION_A/ACCESSION_"+ DefenseSystem_Name+'.txt',
    shell= True)
    subprocess.call('cat ACCESSION_A/ACCESSION_'+ DefenseSystem_Name + '.txt | grep \''+ DefenseSystem_Function +'\' | awk \'{print $0\" |  1\" }\' > ACCESSION_A/ACCESSION_ONLY_'+ DefenseSystem_Name +'.txt',
    shell= True)
    subprocess.call('cat ACCESSION_A/ACCESSION_' + DefenseSystem_Name + '.txt | grep -E \"'+ tmpname[:-1] +'\" | awk \'{print $0  \" |  2\" }\' > ACCESSION_A/ACCESSION_Other_DefenseGene_'+ DefenseSystem_Name +'.txt',
    shell= True)
    subprocess.call('cat ACCESSION_A/ACCESSION_'+ DefenseSystem_Name +'.txt | grep -v \"toxin\|CRISPR\|abortive infection\|restriction-modification\|hypothetical\|argonaute\Dnd" | awk \'{print $0  \" |  3\" }\' > ACCESSION_A/ACCESSION_HouseKeepingGene_'+ DefenseSystem_Name + '.txt',
    shell= True)
    subprocess.call('cat ACCESSION_A/ACCESSION_'+ DefenseSystem_Name + '.txt | grep \'hypothetical\' | awk \'{print $0  \" |  4\" }\' > ACCESSION_A/ACCESSION_hypothetical_'+ DefenseSystem_Name + '.txt',
    shell= True)


DefenseSystem_Function_1 = 'abortive infection'
DefenseSystem_Function_2 = 'restriction-modification'
DefenseSystem_Function_3 = 'toxin'
DefenseSystem_Function_4 = 'Dnd'
DefenseSystem_Function_5 = 'CRISPR'
Dir = "ACCESSION_A"

if not os.path.exists(Dir):
    os.mkdir(Dir)


if 'ABI' in DefenseSystem_Name:
        makecategoryfile(DefenseSystem_Name, DefenseSystem_Function_1)
elif 'RM' in DefenseSystem_Name:
        makecategoryfile(DefenseSystem_Name, DefenseSystem_Function_2)
elif 'TA' in DefenseSystem_Name:
        makecategoryfile(DefenseSystem_Name, DefenseSystem_Function_3)
elif 'DND' in DefenseSystem_Name:
        makecategoryfile(DefenseSystem_Name, DefenseSystem_Function_4)
elif 'Cas' in DefenseSystem_Name:
        makecategoryfile(DefenseSystem_Name, DefenseSystem_Function_5)
else:
        raise NotDefenseSystem("No related defense system is included")



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



def visualize(pred_y, test_y):
    print("precision:", precision_score(pred_y, test_y))
    print("recall:", recall_score(pred_y, test_y))
    print("f1:", f1_score(pred_y, test_y))
    print("accuracy:", accuracy_score(pred_y, test_y))
  
    
def predict_unknown(clf, unknown):
    np_unk = unknown.values
    res = clf.predict(np_unk)
    return res    
    

def binary_cls_analysis(filename, outname):
    df = pd.read_csv(filename, header=None)
    df.columns = [chr(ord('A')+i) for i in range(len(df.columns))]
    x = df['A']
    x = [int(xx.split('_')[-1]) for xx in x]
    df['A'] = x

    pos = df[(df.F == 1) | (df.F == 2)]
    neg = df[df.F == 3]
    unknown = df[df.F == 4]
    del pos['F']
    del neg['F']
    del unknown['F']

    np_pos = pos.values
    np_neg = neg.values

    train_target = np.array([1 for _ in range(np_pos.shape[0])] + [0 for _ in range(np_neg.shape[0])]).reshape(-1, 1)
    train_data = np.concatenate((np_pos, np_neg), axis=0)

    tsz = 0.1
    seed = 42
    use_smote = True
    if use_smote:
        smo = SMOTE(random_state=42)
        train_data, train_target = smo.fit_resample(train_data, train_target)

    train_data,train_target = shuffle(train_data,train_target,random_state=seed)
    train_X,test_X,train_y,test_y = train_test_split(train_data,train_target,test_size=tsz,random_state=seed)

    models = {
        "mlp": MLPClassifier(),
        "svm": svm.SVC(kernel = 'linear'),
        "randomforest": RandomForestClassifier(),
        "adaboost": AdaBoostClassifier(),
    }
   
    name = "randomforest"
    clf = models[name]
    clf.fit(train_X, train_y.ravel())
    pred_y = clf.predict(test_X)
    visualize(pred_y, test_y)

    pred_unk = predict_unknown(clf, unknown)
    known = unknown.copy()
    known['result'] = ['pos' if p == 1 else 'neg' for p in pred_unk]

    known_pos = known[known.result == 'pos']

    reduce_known_pos = known_pos['A']
    reduce_known_pos = reduce_known_pos.reset_index(drop=True)
    reduce_known_pos.to_csv(outname,index= False)
    
    
if __name__ == '__main__':
    filename = Relevance_CategoryName
    outname = DefenseSystem_FilePath+DefenseSystem_Name + '_OUTPUT/output_Relevance_Sorted_'+ DefenseSystem_Name + '_Category.csv'
    binary_cls_analysis(filename, outname)



NewGene_ClusterIDs = pd.read_csv(outname)
NewGeneFile = DefenseSystem_FilePath + DefenseSystem_Name + '_OUTPUT/NewGene_' + DefenseSystem_Name


if not os.path.exists(NewGeneFile):
    os.mkdir(NewGeneFile)

for n in NewGene_ClusterIDs["A"]:
    n = str(n)
    NewGeneList = NewGeneFile + '/' + DefenseSystem_Name + '_' +'CLUSTER_'+ n + '.lst'
    with open(NewGeneList, 'w') as f:
        for i in range(len(Relevance_Sorted_Target['CLUSTER_' + n][1])):
            f.write(Relevance_Sorted_Target['CLUSTER_' + n][1][i])
            f.write('\n')

    subprocess.call('blastdbcmd -db ' + PathToDatabase + ' -entry_batch ' + NewGeneList +
                    ' -long_seqids > ' + NewGeneFile + '/' + DefenseSystem_Name + '_' + 'CLUSTER_' + n + '.faa',
                    shell=True)






