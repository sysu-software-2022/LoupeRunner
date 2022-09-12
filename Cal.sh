#!/bin/bash



if [ "$1" == "" ]
then
    echo "Folder name with sorted clusters as first parameter needed"
	exit 1
fi

FolderName="$1"

if [ "$2" == "" ]
then
    echo "Path to protein database as second parameter needed"
	exit 1
fi

DBPath="$2"


if [ "$3" == "" ]
then
    echo "Linear clusters file name is needed as third parameter"
	exit 1
fi

ClustersFileName="$3"

if [ "$4" == "" ]
then
    echo "Output file name for relevance metrics is needed as fourth parameter"
	exit 1
fi

ResultFileName="$4"

thread_num="$5"

# Parallelization Here
begin=$(date +%s)
# Creating .hits_sorted file name table
find $FolderName/*.hits_sorted > CLUSTER_File_Name.txt

find $FolderName/*.hits_sorted | parallel -j $thread_num "echo Processing {};python GetIcityForBLASTHits.py -f {} -o {.}.tsv -d $DBPath -c $ClustersFileName"
cat $FolderName/*.tsv > $ResultFileName
end=$(date +%s)
spend=$(expr $end - $begin)
rm Tmp_*
echo "Work Done!! Used time: $spend s"

