# LoupeRunner	

[![PyPI version](https://img.shields.io/badge/pypi-v0.1-yellowgreen?logo=pypi&logoColor=yellow)](https://badge.fury.io/py/LoupeTool) [![Python 3.6](https://img.shields.io/badge/python-3.6%7C3.7%7C3.8%7C3.9-yellowgreen?style=flat&logo=python&logoColor=yellow&color=blue)](https://badge.fury.io/py/LoupeTool) [![Python 3.6](https://img.shields.io/badge/GitHub-repository-yellowgreen?style=flat&logo=github&logoColor=white&color=blue)](https://github.com/sysu-software-2022/LoupeTool)

**A modularized LoupeRunner with step by step functions**

You can run **LoupeRunner** step by step with your customized parameters.

 We strongly recommend you execute **LoupeRunner** on **high performance computing platform.**



## 🌟Or download the python package

```python
pip install LoupeTool
```

For details see [LoupeTool](https://github.com/sysu-software-2022/LoupeTool)



## 🔌Dependences Installation (CRITICAL)

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

First and foremost, you should configure all parameters in `config.py`, an example showed in below.

> config.py 

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
                    ThreadNum=os.cpu_count())

```

After configuration, execute `LoupeRunner.py`,  your data will be processed automatically, if you have no idea of configuring these parameters, please read the following guides:



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



> e.g. 48 CPU cores usage in high performance computing platform when processing bulk data during paralleled period.

![image-20220921131936389](./public/htop.jpg)

 You can download **htop** to monitor **LoupeRunner** processing real-time situation just like the above.







## 🧩Documentation

### Experimental Design

> Input and Output files path can be specified in `config.py`

The entire procedure of **LoupeRunner** can be separated into 14 steps pipeline:

- In order to demonstrate every steps precisely, input and output file names are referenced from our example data.



#### **Step1**

#### **Step2**

#### **Step3**



#### **Step4: Extracting CDS**

This step is commented in the code, coding sequence(CDS) file is optional, if you need to extract seeds from CDS file, this step offers you a direct way to do so.



#### **Step5: Extracting seeds**

- Input: `Archaea_Cas.csv`,  `CDS.pty`

Fetching seeds of interest (e.g. Archaea_Cas.csv) in from (e.g. CDS.pty) provided in database, essential attribute includes: 

assembly_accession, locus_tag, product_accession, contigID, start, end.

Our example show in the table below: 

> Archaea_Cas.csv (partial)

| assembly_accession | locus_tag      | product_accession | contigID | start   | end     |
| ------------------ | -------------- | ----------------- | -------- | ------- | ------- |
| GCA_000230715.3    | Natgr_1399     | AFZ72610.1        |          | 1390703 | 1391386 |
| GCA_000970265.1    | MSLAZ_2290     | AKB75551.1        |          | 2975643 | 2978066 |
| GCA_900079115.1    | SSOP1_1525     | SAI85079.1        |          | 1340732 | 1341376 |
| GCA_000189935.2    | AABMKBHA_00165 | AABMKBHA_00165    |          | 33470   | 34630   |
| GCA_000979385.1    | EO92_18095     | KKG11218.1        |          | 53457   | 54251   |





- Output:  `Seeds_Cas.tsv`

| Assembly        | LociID        | Accession      | ContigID          | Start   | End     |
| :-------------- | ------------- | -------------- | ----------------- | ------- | ------- |
| GCF_001729285.1 | A9507_RS00880 | WP_069582310.1 | NZ_LZPM01000003.1 | 122396  | 122990  |
| GCF_000214725.1 | MSWAN_RS07020 | WP_013825929.1 | NC_015574.1       | 1538607 | 1539333 |
| GCF_900095295.1 | MCBB_RS06490  | MCBB_RS06490   | NZ_LT607756.1     | 1386026 | 1387868 |
| GCF_900095295.1 | MCBB_RS06465  | WP_071908025.1 | NZ_LT607756.1     | 1380806 | 1381325 |
| GCF_000302455.1 | A994_RS11405  | WP_004031769.1 | NZ_AMPO01000012.1 | 2073    | 2592    |







#### **Step6:  Selecting neighborhoods**

Select neighborhood around seeds

- Input:  `Seeds_Cas.tsv`
  - NeighborhoodVicinitySize(default: 10000): change the bidirectional search domain of seed(i.e. offset), if this increase, the search domain will be expand correspondingly. 



- Output: `Vicinity_Cas` (list of proteins in vicinity of seeds)

```
===
WP_013644337.1	708731..710093	+	Methanobacterium lacus-GCF_000191585.1	NC_015216.1
WP_013644338.1	710089..710788	+	Methanobacterium lacus-GCF_000191585.1	NC_015216.1
WP_013644339.1	711103..711739	+	Methanobacterium lacus-GCF_000191585.1	NC_015216.1
WP_013644340.1	711758..712142	+	Methanobacterium lacus-GCF_000191585.1	NC_015216.1
WP_013644341.1	712125..712428	+	Methanobacterium lacus-GCF_000191585.1	NC_015216.1
WP_013644342.1	712458..714444	-	Methanobacterium lacus-GCF_000191585.1	NC_015216.1
WP_013644343.1	714508..714814	+	Methanobacterium lacus-GCF_000191585.1	NC_015216.1
WP_013644344.1	714975..716799	-	Methanobacterium lacus-GCF_000191585.1	NC_015216.1
WP_013644345.1	717225..717567	+	Methanobacterium lacus-GCF_000191585.1	NC_015216.1
WP_013644346.1	717609..718158	+	Methanobacterium lacus-GCF_000191585.1	NC_015216.1
WP_013644347.1	718126..718936	+	Methanobacterium lacus-GCF_000191585.1	NC_015216.1
WP_013644348.1	718970..719564	-	Methanobacterium lacus-GCF_000191585.1	NC_015216.1
WP_013644349.1	719950..720817	+	Methanobacterium lacus-GCF_000191585.1	NC_015216.1
WP_013644350.1	720894..721371	+	Methanobacterium lacus-GCF_000191585.1	NC_015216.1
WP_013644351.1	721367..722756	-	Methanobacterium lacus-GCF_000191585.1	NC_015216.1
WP_013644352.1	723448..724663	+	Methanobacterium lacus-GCF_000191585.1	NC_015216.1
WP_013644353.1	724962..725496	-	Methanobacterium lacus-GCF_000191585.1	NC_015216.1
WP_013644354.1	725806..726502	+	Methanobacterium lacus-GCF_000191585.1	NC_015216.1
WP_013644355.1	726503..726824	+	Methanobacterium lacus-GCF_000191585.1	NC_015216.1
WP_013644356.1	726849..727638	+	Methanobacterium lacus-GCF_000191585.1	NC_015216.1
WP_013644357.1	728039..728633	+	Methanobacterium lacus-GCF_000191585.1	NC_015216.1
WP_013644358.1	728644..729043	+	Methanobacterium lacus-GCF_000191585.1	NC_015216.1
WP_013644359.1	729210..732126	+	Methanobacterium lacus-GCF_000191585.1	NC_015216.1
===
WP_013825920.1	1526093..1526849	+	Methanobacterium paludis-GCF_000214725.1	NC_015574.1
WP_013825921.1	1527015..1527132	+	Methanobacterium paludis-GCF_000214725.1	NC_015574.1
WP_013825922.1	1527204..1527612	+	Methanobacterium paludis-GCF_000214725.1	NC_015574.1
WP_013825923.1	1527926..1528274	-	Methanobacterium paludis-GCF_000214725.1	NC_015574.1
WP_013825924.1	1528859..1529774	-	Methanobacterium paludis-GCF_000214725.1	NC_015574.1
WP_013825925.1	1529770..1530721	-	Methanobacterium paludis-GCF_000214725.1	NC_015574.1
WP_013825926.1	1536731..1536995	-	Methanobacterium paludis-GCF_000214725.1	NC_015574.1
WP_048188005.1	1537000..1537945	-	Methanobacterium paludis-GCF_000214725.1	NC_015574.1
WP_048188364.1	1538060..1538582	-	Methanobacterium paludis-GCF_000214725.1	NC_015574.1
WP_013825929.1	1538607..1539333	-	Methanobacterium paludis-GCF_000214725.1	NC_015574.1
WP_013825930.1	1539392..1541603	-	Methanobacterium paludis-GCF_000214725.1	NC_015574.1
WP_013825931.1	1541612..1542230	-	Methanobacterium paludis-GCF_000214725.1	NC_015574.1
WP_013825932.1	1542226..1543225	-	Methanobacterium paludis-GCF_000214725.1	NC_015574.1
WP_013825933.1	1543225..1544599	-	Methanobacterium paludis-GCF_000214725.1	NC_015574.1
WP_013825934.1	1545276..1546743	-	Methanobacterium paludis-GCF_000214725.1	NC_015574.1
WP_052296851.1	1546885..1547275	+	Methanobacterium paludis-GCF_000214725.1	NC_015574.1
WP_013825936.1	1547556..1548792	-	Methanobacterium paludis-GCF_000214725.1	NC_015574.1
WP_013825937.1	1549070..1550777	-	Methanobacterium paludis-GCF_000214725.1	NC_015574.1
WP_013825938.1	1551299..1552286	-	Methanobacterium paludis-GCF_000214725.1	NC_015574.1
WP_013825939.1	1552375..1553728	-	Methanobacterium paludis-GCF_000214725.1	NC_015574.1
WP_013825940.1	1553724..1554780	-	Methanobacterium paludis-GCF_000214725.1	NC_015574.1
===
```



#### **Step7: Collecting protein IDs**

- Input:  `Vicinity_Cas` (list of proteins in vicinity of seeds)

Extract and sort proteins in vicinity of seeds in ascending order forming VicinityIDs in `.lst` file.



- Output: `VicinityIDs_Cas.lst  ` (partial)

```
WP_004030635.1
WP_004030636.1
WP_004030637.1
WP_004030638.1
WP_004030640.1
WP_004030642.1
WP_004030643.1
WP_004030644.1
WP_004030645.1
WP_004030646.1
.....
```





#### **Step8: Fetching protein sequences**

Tool `blastdbcmd`required

- Input: `VicinityIDs_Cas.lst`, Database

using the file generated in Step 7 ( `VicinityIDs_Cas.lst`) to get protein sequences from database.





- Output: `Vicinity_Cas.faa` (partial)

```
>ref|WP_004030635.1| glycosyltransferase family 4 protein [Methanobacterium formicicum]
MDKIAISVVVDIFDDEGTTVRPKRVAELLKNNFDTCFINRSSSDLKEINGIPVHIVKPAGTKLWNIKLFGLLSGNDFDFV
YCSSDWFGFLTYFMLKRFYDYKIIFEAHTIISEEFKERKAHPFKVFFFQVLEKFAIKHSDYVVALSENIYDYYSYNKNIE
LVHVFIDEELFISDVKRKINDDKKVIGLIGPFDEFSNQYFLEFLRKNIDQFDDRISFRIIGKCQDKIQHPRIEYTGYMNS
IHDYVNVLSSLDGLLVPSRVATLGPLNKIIEAMACSVPVFTTPKGIVGLYNIKPGQEIYVLEEDDLVCGLNNHVFSDELI
NIAKNARLYVEKYYSKKANEKKLLRIFNRLNEG
>ref|WP_004030636.1| glycosyltransferase family 4 protein [Methanobacterium formicicum]
MIIGYFSSTFPYSVSNPKYFCGGSSLATHSLVNEISNSDIDIKVFTTSADSEDHLDMDGRMGIYRYATKIKLLTSPISLG
LFHKPLEHDVDLVHVSFDMPPGPFAAYRYARKKSLPLILTYHGDWDPDYGSFVRKVGVSINNKFVSDLLSYADIIISPSK
LYAKKSKYLSKYLDKIRVIPNGIDLDEFQLNYSQSECREKLNLPLECKIILFFGYLTPYKGPDILLGAFREVLKNQPDTV
LLFAGNGNMEDELKKLARQWNIQDNVIFAGFVDKKMRSLYYKSADIFCLPSTMSTECYPLAILEAMASGVPVVASDIGGI
PDIIENNVNGLLVTPTNPEKLEDNLNLLLQNPEIRAKFSENALKGIKKYSWKNIATETLKLYESLLENR
```







#### **Step9:  Clustering protein seqiences**



- Input:  `Vicinity_Cas.faa`
  - PermissiveClusteringThreshold(default: 0.3)

Run the following command to cluster protein sequences contained in the file  `Vicinity_Cas.faa` using a
sequence similarity cutoff value of 0.3 and save results in the `VicinityPermissiveClustsLinear_Cas.tsv` file:

​	

- Output: `VicinityPermissiveClustsLinear_Cas.tsv` (partial)

```
WP_013825920.1	WP_013	825920.1
WP_023991503.1	WP_023991503.1
WP_048191534.1	WP_048191534.1 WP_004030642.1 WP_023992731.1
WP_071906989.1	WP_071906989.1
WP_071907103.1	WP_071907103.1 WP_013644342.1 WP_013826017.1
WP_095651991.1	WP_095651991.1
WP_100907657.1	WP_100907657.1
WP_004031781.1	WP_004031781.1 WP_100906549.1
WP_013825921.1	WP_013825921.1 WP_095651998.1 WP_100906253.1 WP_095651996.1 WP_023992734.1 WP_013826664.1 WP_095651994.1 WP_095651997.1 WP_179288731.1 WP_023992735.1 WP_100906252.1 WP_023992122.1 WP_232727999.1
WP_013826016.1	WP_013826016.1 WP_013644343.1 WP_071907102.1
```



#### **Step10: Making profiles **(Parallalized)

Tool `blastdbcmd`, `muscle` required

- Input: 













- Output: 



#### **Step11: Running PSI-BLAST for profiles** (Parallalized)

- Input: 













- Output: 



#### **Step12: Sorting blast hits** 

- Input: 













- Output: 



#### **Step13: Calculating LOUPE metric** (Parallalized)

- Input: 













- Output: 



#### **Step14: Sorting Relevance**















## 💡Reference

**1.Shmakov, S.A., Faure, G., Makarova, K.S. *et al.* Systematic prediction of functionally linked genes in bacterial and archaeal genomes. *Nat Protoc* 14, 3013–3031 (2019). https://doi.org/10.1038/s41596-019-0211-1**
