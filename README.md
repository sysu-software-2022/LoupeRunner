# LoupeRunner	

[![PyPI version](https://img.shields.io/badge/pypi-v0.1-yellowgreen?logo=pypi&logoColor=yellow)](https://badge.fury.io/py/LoupeTool) [![Python 3.6](https://img.shields.io/badge/python-3.6%7C3.7%7C3.8%7C3.9-yellowgreen?style=flat&logo=python&logoColor=yellow&color=blue)](https://badge.fury.io/py/LoupeTool) [![Python 3.6](https://img.shields.io/badge/GitHub-repository-yellowgreen?style=flat&logo=github&logoColor=white&color=blue)](https://github.com/sysu-software-2022/LoupeTool)

**A modularized LoupeRunner with step by step functions**

You can run **LoupeRunner** step by step with your customized parameters.

 

## 🌟Or download the python package

```python
pip install LoupeTool
```

For details see [LoupeTool](https://github.com/sysu-software-2022/LoupeTool)



## 🔌Dependences Installation

The following **4** tools and **5** python packages are significantly critical for your successful execution of LoupeTool.

We strongly recommend you run **LoupeTool** in **Linux** or **macOS**.



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

##### bio, pandas, numpy, sklearn, imblearn

You can install these python packages by running `pip install -r requirements.txt`





## 👾Quick Example

**! Make sure you have already downloaded all dependencies**

```python
from LoupeTool import Loupe
import os
Loupe.LoupeRunner(DefenseSystem_Name="Cas",
                    DefenseSystem_FilePath="./",
                    PTYFile=os.path.join("./", "Cas_INPUT/Database/CDS.pty"),
                    PathToDatabase=os.path.join("./", "Cas_INPUT/Database/ProteinDB"),
                    SeedPath=os.path.join("./", "Cas_INPUT/Archaea_Cas.csv"),
                    NeighborhoodVicinitySize=10000,
                    PermissiveClusteringThreshold=0.3,
                    SortingOverlapThreshold=0.4,
                    SortingCoverageThresold=0.25,
                    ThreadNum="48")

```



##### I. Parameters guide:

1. DefenseSystem_Name: ABI, RM, TA, DND, Cas;
2. DefenseSystem_FilePath: Your working directory;
3. PTYFile: your **.pty** file path;
4. SeedPath: your seed **.csv** file path;
5. NeighborhoodVicinitySize: change the bidirectional search domain of seed, if this increase, the search domain will be expand correspondingly. Our Suggestion Value: CRISPR-Cas: 10000，TA: 2000
6. PermissiveClusteringThreshold: this adjust mmseqs cluster parameter(i.e. --min-seq-id) in **step 9**, this will affect sequence similarity. For more details, see:  [MMseqs2 User Guide](https://github.com/soedinglab/mmseqs2/wiki)
7. SortingOverlapThreshold and SortingCoverageThresold: this twos parameters are used to filter **Low matching hit** produced by **PSIBLAST** in **step12**, increase them will result in the spurt of specificity.
8. ThreadNum: thread number should be contingent on your **CPU core number**.

hint: the most convenient way of managing these relevant paths is create a new directory for processing your data or use existing one and include all your files in this directory.



##### II. For users:

For processing large **seeds** by executing **LoupeTool,** you may have to wait for longer time, which is contingent on your CPU core number (some bottleneck steps in **LoupeTool** are optimized by **parallelization** and the performance is positively correlated with the CPU core number)











## 🧩Documentation





## 💡Reference
