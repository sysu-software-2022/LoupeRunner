# ICityTool	

[![PyPI version](https://img.shields.io/badge/pypi-v0.1-yellowgreen?logo=pypi&logoColor=yellow)](https://badge.fury.io/py/ICityTool) [![Python 3.6](https://img.shields.io/badge/python-3.6%7C3.7%7C3.8%7C3.9-yellowgreen?style=flat&logo=python&logoColor=yellow&color=blue)](https://badge.fury.io/py/ICityTool)[![Python 3.6](https://img.shields.io/badge/GitHub-repository-yellowgreen?style=flat&logo=github&logoColor=white&color=blue)](https://github.com/sysu-software-2022/ICityTool)

**An integrate python package version of ICityRunner**

## 🌟Download

```python
pip install ICityTool
```



## 🔌Dependences Installation

The following **5** tools and **2** python packages are significantly critical for your successful execution of ICityTool.

We strongly recommend you run **ICityTool** in **Linux** or **macOS**.



#### 1.blast+

- ##### Install with source code package & Configuration

You can click [Latest blast+](https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/) and choose corresponding package (**suffix: tar.gz**) which is applicable to your OS (Linux/macOS)

Or you can just use `wget` to install your package:



> Linux

```shell
wget https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/ncbi-blast-2.13.0+-x64-linux.tar.gz
tar -zxvf ncbi-blast-2.13.0+-x64-linux.tar.gz
```



```shell
mv ncbi-blast-2.13.0+ blast
echo "export PATH=$(pwd)/blast/bin:\$PATH" >> ~/.bashrc
source ~/.bashrc
```



> macOS

```shell
wget https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/ncbi-blast-2.13.0+-x64-macosx.tar.gz
tar -zxvf ncbi-blast-2.13.0+-x64-macosx.tar.gz
```



```shell
mv ncbi-blast-2.13.0+ blast
echo "export PATH=$(pwd)/blast/bin:\$PATH" >> ~/.zshrc
source ~/.zshrc
```

**!  `$(pwd)` is the path where you installed blast+ in.**





#### 2.muscle (v5.1)

See [muscle Version 5.1](https://github.com/rcedgar/muscle/releases/tag/v5.1) for installation.

Then type the following commands:

> Linux

```shell
chmod +x muscle5.1.linux_intel64
mv muscle5.1.linux_intel64 muscle
ln -s muscle /etc/bin
```



> macOS

```shell
chmod + muscle5.1.macos_arm64 # or muscle5.1.macos_intel64
mv muscle5.1.macos_arm64 muscle
ln -s muscle /usr/local/bin

```

For more details see [Muscle5](https://drive5.com/muscle5/)



#### 3.MMseqs2

Please refer to official installation user guide [MMseqs2 User Guide](https://github.com/soedinglab/mmseqs2/wiki#installation)



#### 4.parallel

> Linux 

```shell
sudo apt install parallel
```



> macOS

```shell
brew install parallel
```



#### 5.Python Packages:

##### bio, pandas, numpy, sklearn



You can install these python packages by running `pip install -r requirements.txt`



## 👾Quick Example
> config.py
```python
# Input files and Hyper-parameters
import os
DefenseSystem_Name = "TA_A"
DefenseSystem_FilePath = os .path.join("./")  # Your Working Path
GbffFile_Path = "./archaea"
GbffFile_Type = "TA_A"

ICITY_CONFIG_INPUT = {
    "PTYFile": os.path.join("./", "DemoInput/Database/CDS.pty"),
    "PathToDatabase": os.path.join("./", "DemoInput/Database/ProteinDB"),
    "CdsPath": os.path.join("./", "DemoInput/Database/CDS.pty"),
    "SeedPath":os.path.join("./", "DemoInput/Archaea_Cas.csv"),
    "NeighborhoodVicinitySize": 10000,
    "PermissiveClusteringThreshold": 0.3,
    "SortingOverlapThreshold": 0.4,
    "SortingCoverageThresold": 0.25,
    "ThreadNum": "48"   # Change global thread number here
}

# Output files
ICITY_CONFIG_OUTPUT = {
    "ICITYFileName": os .path.join("./" + DefenseSystem_Name+"_OUTPUT", "Relevance_"+DefenseSystem_Name+".tsv"),
    "VicinityClustersFileName": os.path.join("./" + DefenseSystem_Name+"_OUTPUT", "VicinityPermissiveClustsLinear_"+DefenseSystem_Name+".tsv"),
    "RelevanceCategoryName": "RelevanceCategory_" + DefenseSystem_Name + ".csv"
}

# Temporary files
ICITY_CONFIG_TEMPORARYFILES = {
    "VicinityFileName": os.path.join("./" + DefenseSystem_Name+"_OUTPUT", "Vicinity_"+DefenseSystem_Name+".tsv"),
    "VicinityIDsFileName": os.path.join("./" + DefenseSystem_Name+"_OUTPUT", "VicinityIDs_"+DefenseSystem_Name+".lst"),
    "VicinityFASTAFileName": os.path.join("./" + DefenseSystem_Name+"_OUTPUT", "Vicinity_"+DefenseSystem_Name+".faa"),
    "ProfilesFolder": os.path.join("./" + DefenseSystem_Name+"_OUTPUT", "CLUSTERS_"+DefenseSystem_Name + "/"),
    "SortedBLASTHitsFolder": os.path.join("./" + DefenseSystem_Name+"_OUTPUT", "CLUSTERS_"+DefenseSystem_Name, "Sorted/"),
    "SeedsExtractedFileName": os.path.join("./" + DefenseSystem_Name+"_OUTPUT", "Seeds_" + DefenseSystem_Name + ".tsv"),


}



```

##### I. Parameters guide:

1. DefenseSystem_Name: ABI, RM, TA, DND, Cas.
2. DefenseSystem_FilePath: Your working directory.
3. SeedPath: your seed **csv** file path
4. ThreadNum: thread number should be contingent on your **CPU core number**.

hint: the most convinient way of managing these relevant paths is create a new directory for processing your data or use exsiting one and include all your files in this directory.



##### II. For users:

For processing large **seeds** by executing **ICityTool,** you may have to wait for longer time, which is contingent on your CPU core number (some bottleneck steps in **ICityTool** are optimized by **parallelization** and the performance is positively correlated with the CPU core number)











## 🧩Documentation





## 💡Reference
