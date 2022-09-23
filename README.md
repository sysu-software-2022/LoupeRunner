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



### **Step4: Extracting CDS**

This step is commented in the code, coding sequence(CDS) file is optional, if you need to extract seeds from CDS file, this step offers you a direct way to do so.



### **Step5: Extracting seeds**

- Input: `Archaea_Cas.csv`,  `CDS.pty`

Fetching seeds of interest (e.g. Archaea_Cas.csv) in from (e.g. CDS.pty) provided in database, essential attribute includes: 

assembly_accession, locus_tag, product_accession, contigID, start, end.

Our example show in the table below: 

> Archaea_Cas.csv (partial)

| Assembly_accession | Locus_tag      | Product_accession | ContigID | Start   | End     |
| ------------------ | -------------- | ----------------- | -------- | ------- | ------- |
| GCA_000230715.3    | Natgr_1399     | AFZ72610.1        | NULL     | 1390703 | 1391386 |
| GCA_000970265.1    | MSLAZ_2290     | AKB75551.1        | NULL     | 2975643 | 2978066 |
| GCA_900079115.1    | SSOP1_1525     | SAI85079.1        | NULL     | 1340732 | 1341376 |
| GCA_000189935.2    | AABMKBHA_00165 | AABMKBHA_00165    | NULL     | 33470   | 34630   |
| GCA_000979385.1    | EO92_18095     | KKG11218.1        | NULL     | 53457   | 54251   |





- Output:  `Seeds_Cas.tsv`

> Seeds_Cas.tsv (partial)

| Assembly        | LociID        | Accession      | ContigID          | Start   | End     |
| :-------------- | ------------- | -------------- | ----------------- | ------- | ------- |
| GCF_001729285.1 | A9507_RS00880 | WP_069582310.1 | NZ_LZPM01000003.1 | 122396  | 122990  |
| GCF_000214725.1 | MSWAN_RS07020 | WP_013825929.1 | NC_015574.1       | 1538607 | 1539333 |
| GCF_900095295.1 | MCBB_RS06490  | MCBB_RS06490   | NZ_LT607756.1     | 1386026 | 1387868 |
| GCF_900095295.1 | MCBB_RS06465  | WP_071908025.1 | NZ_LT607756.1     | 1380806 | 1381325 |
| GCF_000302455.1 | A994_RS11405  | WP_004031769.1 | NZ_AMPO01000012.1 | 2073    | 2592    |







### **Step6:  Selecting neighborhoods**

Select neighborhood around seeds

- Input:  `Seeds_Cas.tsv`
  - Parameter: 
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



### **Step7: Collecting protein IDs**

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





### **Step8: Fetching protein sequences**

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







### **Step9:  Clustering protein seqiences**



- Input:  `Vicinity_Cas.faa`
  - Parameter:
  
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



### **Step10: Making profiles** (Parallalized)

Tool `blastdbcmd`, `muscle` required

- Input:  `VicinityPermissiveClustsLinear_Cas.tsv`, Database

















- Output: ``CLUSTERS_Cas/CLUSTER_*.ali``

> CLUSTER_5.ali

```
>ref|WP_071907103.1| NFACT family protein [Methanobacterium congolense]
MKTMSNVDVYAICTELKDTLKDARVDKAYQPTKDTVLIRFHIPGKGRTDVVFQAGTRVHTTQYPPENPKIPPSFPMLLRK
HLKGGTITDVRQHHFDRIMELDIQKEHRYTLVVELFSKGNIILVDEEGTIILPLKRKLWQDRKISSKEIYKYPPENEFNP
LKAEKEDIKKLFMDSDRDVVRTLAGSGLGGLYAEEIVLRSDVDKKKSATDLEEAELEAIYNAFQELFQPLKDHAFHPRII
SGEKEDVLPLELRKYEGFESKTFETYNQAADEFYSSRVGEDIKKVHEDIWAREIGKYEKRMKIQLETLENFKKTIVESTI
KGDALYAHYHEVQDMINTIMEARKNYSWAEVSSTIKKAKKHGAAGLESIEAVDKMGVMDLNLEGVRVQVDSNIGIPENAE
KYYNKGKKAKRKINGVNIAIEKTQAEIDKAKNKREIAMEKVLVPQKRVRKELKWFEKLRWFVSSDGNLVIGGRDATTNEM
VVKKHLENRDVYFHSDIHGAASVVVKGGEGEISEETLIEAASFSASFSSAWQKGFSTHDVYWVHPDQVSKTPQSGEFVAK
GAFIIRGSRNYMRGVPLLVAVGIVDYEGERVMAGPPEAVSAYTDNYAVIKPGYTKKEEMARQIRNKIDNEGVLSIEDVVR
VLPSGKCDFVDKRSLKW----KR
>ref|WP_013644342.1| NFACT family protein [Methanobacterium lacus]
MKAMSNVDVYAICKELGEVLKDARVQKAYQPTKDTVLIRFHVPGKGRVDVVFQAGFRVHTTQYPPQNPKIPPNFPMLLRK
YIKGGTVTAVKQHNFDRIMRIDIQKEEKFSLVVELFAKGNIILLDHEDKIILPLKRKVWQDRKISSKEEYKYPPERGMNP
LEVDKEELKTILTNSDRDIIRTLARNGLGGLYAEEIALRSDVAKNKTADEITDEDVEAIQSAINSIFDPLKTFNFNPQIV
KGKKEDVLPLDLLMYKDFEKESFESFNDAADEFYSSIVGEDIVNVNEEVWSGEVGKFEKRLNIQLETLEKFEKTVKDSKI
KGEAIYSDYQAIENILNIIHSARETNSWLEIIATVKKAKKDKVPGLEIIESIDKMGVLTLNLDGVRVNIDSSMGIPENAE
IYYNKGKKAKRKIKGVHIAIEKTRKEIDKAKNKREIEMEKVLVPQKRVKKDLKWYEKLRWFVTSDGLLAIGGRDATTNEM
VVKKHMENRDIYFHSDIHGASSVILKAGEGEIPERSINETAAFAACFSSAWSKGLGSTDVYWVHPEQVSKTPQSGEFVAK
GAFIIRGSRNYMRGLPLTLSLGIVDYEGSRIMAGPPEAVSNLTEKYVTVKPGYIKKEEIARQIRNNIDDEKLLSIEDVVR
VLPSGKCDFLDSKGFKR--NKKR
>ref|WP_013826017.1| NFACT family protein [Methanobacterium paludis]
MKAMSNVDIYTICNELKEILKDARVDKAYQPTRDTVLIRFHVPGKGRVDVVFQAGLRVHTTQYPPENPQIPPSFPMILRK
HLKGGNVTCVKQHNFDRILKINIQKEHKYSLVIELFAKGNIILLDEEGTIIMPLKRKLWEDRNISSKEEYKYPPERGINP
LEVTKEELETLFAESDRDLIRTLASSGLGGLYAEEVMLRSGVKKDKPSSDITPEELDFIHNAMSDVFSPLKTAQFHPQII
SSEKDDVLPLNLTKYEKYEKKTFETFNQAADEFYSSIVGDDIKQVHEDVWAAEVGKFEKRLKIQMETLEKFKDTIVKTKI
KGEAIYSNYQNIQNILDIIHNARETYSWLDIIDIIKKGKKEKVSGLDIIESLDKMGVLTLNLDGTIVNVDSNMSIPENAE
IYYNKGKKAKRKISGVNIAIEKTMKEVERAKNKREIAMEKVLVPQKRVRKELKWFEKLRWFLSSDGLLVIGGRDATTNEM
IVKKHMENRDIYFHSDIHGAASVVVKAGEGEVPESTLNETASFAGSFSSAWSAGFGSTDVYWVHPDQVSKTPQSGEFVGK
GAFIIRGSRNFIRNAPLLVAVGIVDYEGKRIMAGPPEALVKYTDNYVVIKPGYTKKEEMARQIRHKIDEEKLLSIEDVVR
VLPSGKCDFVDKRQFKGRDFKRK

```



### **Step11: Running PSI-BLAST for profiles** (Parallalized)

- Input:  ``CLUSTERS_Cas/CLUSTER_*.ali``, Database
  - Parameter:  
    - ThreadNum


















- Output: ``CLUSTERS_Cas/CLUSTER_*.hits``

> CLUSTER_1.hits

```
# PSIBLAST 2.13.0+
# Iteration: 1
# Query: ref|WP_013825920.1| hypothetical protein [Methanobacterium paludis]
# Database: ./Cas_INPUT/Database/ProteinDB
# Fields: query id, subject id, subject length, s. start, s. end, evalue, query seq, subject seq, q. start, q. end, score
# 29 hits found
ref|WP_013825920.1|	ref|WP_013825920.1|	251	1	251	0.0	MGLQLHPIISIPFGVITTIVFLQVFGIPTLPLGGNAGILILIPVAIIFGGFTATYFTDTNDKKIIYSICVGIIISFITLILGLKEYIGYNDVVVMFISFCVMAGIGGFLGKIADEVNRKILEIKYKILSNISESKKNILKNVLISILFVGMMSFIFVGLIFMPFGNPDIIIIQSSGFSPNSTLISPSTVTWINNDTKIHRVVSDYGLFDSGNITPGQSYSHYFRDVKAYPYHDSIDPSMKGTVLLPMSPGE	MGLQLHPIISIPFGVITTIVFLQVFGIPTLPLGGNAGILILIPVAIIFGGFTATYFTDTNDKKIIYSICVGIIISFITLILGLKEYIGYNDVVVMFISFCVMAGIGGFLGKIADEVNRKILEIKYKILSNISESKKNILKNVLISILFVGMMSFIFVGLIFMPFGNPDIIIIQSSGFSPNSTLISPSTVTWINNDTKIHRVVSDYGLFDSGNITPGQSYSHYFRDVKAYPYHDSIDPSMKGTVLLPMSPGE	1	251	1286
ref|WP_013825920.1|	ref|WP_004031972.1|	114	6	112	4.61e-27	VLISILFVGMMSFIFVGLIFMPFGNPDIIIIQSSGFSPNSTLISPSTVTWINNDTKIHRVVSDYGLFDSGNITPGQSYSHYF--RDVKAYPYHDSIDPSMKGTVLLPMSPG	LLIGLPIFGVCLLLLLGLHDIPAE----IYVGNSGFDPNVTNIYPSKVTWTNNDSQIHRIISDDGLFDSGNLSPGENYTYDFSYHKNKIYKYHDSTNTSLKGTIQIEMGPG	142	250	251
ref|WP_013825920.1|	ref|WP_008517151.1|	114	27	112	1.08e-24	PDIIIIQSSGFSPNSTLISPSTVTWINNDTKIHRVVSDYGLFDSGNITPGQSYSHYF--RDVKAYPYHDSIDPSMKGTVLLPMSPG	PTEIYVGNSGFDLNVTNIYPSKVTWTNNDSQIHRIVSDDGLFDSGNLSPGENYTYDFSYHKNRIYKYHDSTNTSLKGTIQIEMGPG	167	250	235
ref|WP_013825920.1|	ref|WP_052374236.1|	116	2	112	1.86e-22	KKNILKNVLISILFVGMMSFIFVGLIFMPFGNP--DIIIIQSSGFSPNSTLISP--STVTWINNDTKIHRVVSDYGLFDSGNITPGQSYSHYFRDVKAYPYHDSIDPSMKGTVLLPMSP	KRNLSVWIVLSILFV-------VGISGCTFKQPTNDTVVIQNEGFSP-SALIVPVNTTVTWINKDPVTQNLVSDTGLFESGNLSNGQSFNYTFNQTGSYHYYSNLYPNMKGSIIVTTSP	135	249	220
ref|WP_013825920.1|	ref|WP_223790141.1|	128	4	106	7.56e-21	SILFVGMMSFIFVGLIFMP---FGNPDIIIIQSSGFSPNSTLISP-STVTWINNDTKIHRVVSDYGLFDSGNITPGQSYSHYFRDVKAYPYHDSIDPSMKGTVLL	NLIFVGV--FLIFGIVAVSGCTSSQTSIVTIQNSSFNPSTLNVQVGTTVTWINKDTTTHDVVSDTGLFNSGNLTNGMSYNYTFNQTGSFAYHSAIQPSMTGTIVV	145	245	210
ref|WP_013825920.1|	ref|WP_081882600.1|	130	4	108	8.80e-19	SILFVGMMSFIFVGLIFMPF-----GNPDIIIIQSSGFSPNSTLISP-STVTWINNDTKIHRVVSDYGLFDSGNITPGQSYSHYFRDVKAYPYHDSIDPSMKGTVLL	NLIFVGV--FLVLGIVAVSGCTSNQTSGNTVTIQNMAFNPSTLNVKVGTTVTWINKDSVTHDVVSDTGLFNSGNLTNGMSYNYTFNQTGSFPYHCAIHPSMTGTIVV	145	245	196
ref|WP_013825920.1|	ref|WP_081882599.1|	128	31	110	3.19e-18	IIIQSSGFSPNSTLISP-STVTWINNDTKIHRVVSDYGLFDSGNITPGQSYSHYFRDVKAYPYHDSIDPSMKGTVLLPMS	VTIQNMAFNPSTLNVQVGTTVMWINKDSTTHHVVSDTGVFDSGDLATGQSYNYTFNQTGSFPYHCSIHPSMTGTIVVSTS	170	248	192
ref|WP_013825920.1|	ref|WP_052374129.1|	161	4	109	7.24e-17	ISILFVGMMSFIFVGLIFMPFGNPDIIIIQSSGFSPNSTLISPST-VTWINNDTKIHRVVSDYGLFDSGNITPGQSYSHYFRDVKAYPYHDSIDPSMKGTVLLPMS	INFIFLGILLTIGIVAVSGCTSQSSTVTIQNMAFNPSTVHITGSTTIIWINKDNIEHEVVSDTGLFDSGVLAPGESFNYTFNQAGDYAYHCAIHPSMVGIIVVSSS	144	248	185
ref|WP_013825920.1|	ref|WP_223792080.1|	98	10	90	4.31e-16	NPDII--IIQSSGFSPNSTLISP--STVTWINNDTKIHRVVSDYGLFDSGNITPGQSYSHYFRDVKAYPYHDSIDPSMKGTV	NPQTIQLLYKIEAFSP-STLIVPVNTTVTWINKDPVTQNLVSDTGLFESGNLSNGQSFNYTFNQTGSYHYHSNIHPNIKGSI	166	243	175
ref|WP_013825920.1|	ref|WP_052375909.1|	145	68	144	5.14e-15	IIIQSSGFSPNS-TLISPSTVTWINNDTKIHRVVSDYGLFDSGNITPGQSYSHYFRDVKAYPYHDSIDPSMKGTVLL	ISIQNMAFNPNKITVKSGTNVQWINNDNTQHQIVSDSGAFQSNTLNPGDSYNFFFDKTGIYGYHDALNSTITGTIVV	170	245	171
ref|WP_013825920.1|	ref|WP_069583285.1|	145	68	144	1.37e-13	IIIQSSGFSPNS-TLISPSTVTWINNDTKIHRVVSDYGLFDSGNITPGQSYSHYFRDVKAYPYHDSIDPSMKGTVLL	ISIGNMAFNPNKITVKSGTNVQWINNDNTQHQIVSDTGAFQSTILNPGDSYNFFFAKTGIYGYHDALNSTITGTIIV	170	245	161
ref|WP_013825920.1|	ref|WP_071906376.1|	370	1	145	2.85e-13	LQLHPIISIPFGVITTIVFLQVFGIPTLPLG-------GNAGILILIPVAIIFGGFTATYFTDTNDKKIIYSICVGIIISFITLILGLKEYIGYNDVVVMFISFCVMAGIGGFLGKIADEVNRKILEIKYKILSNISESKKNILKNVLISILFVGMMSFIFVGL	MKFHPAISIILGIVTILMWFILAGILGLDFSKSISNTSGGATLIILI-----LGGFVATYFTE--DKKIRYSIYEGLIF---TAFVGLSKNLKL--IFAAFIAYVLFIGIGGFIGKMTDNKERQNFK-------NHFEKGFNPIITIVMGFIVANFFYYLLLGI	3	159	167
ref|WP_013825920.1|	ref|WP_071906376.1|	370	123	313	1.07e-11	HPIISIPFG-VITTIVFLQVFGIPTLPLGGN--AGILILIPVAIIFGGFTATYFTDTNDKKIIYSICVGIIISFITLILGLKE---YIGYNDVVVMFISFCVMAGIGGFLGKIADEVNRKILEIKYKILSNISESKKNILKNVLISILFVGMMSFIFVGLIFMPFGNPDIIIIQSSGFSPNSTLISPSTVTWINNDTKIHRVVSDYGLF	NPIITIVMGFIVANFFYYLLLGITNIYTSYNIKTAALTIAVISNVIGGFTATFFA--KEKKIQYGIYTGLIILISSLAMKLIHGTLHVNYSSISI--VEYLLFAGIGGFIGKITDNTGRQSLK---KRFNNGYNPIITIVMGYFIATFFNNSILLITCTYNSNPFGVTQFIV------AAISFVIGGFTATFFAKEKKI-----QYGIY	6	208	155
ref|WP_013825920.1|	ref|WP_071906376.1|	370	249	359	4.74e-07	HPIISIPFGVITTIVFLQVFGIPTLPLGGNA-GILILIPVAIIF--GGFTATYFTDTNDKKIIYSICVGIIISFITLIL----GLKEYIGYNDVVVMFISFCVMAGIGGFLGK	NPIITIVMGYFIATFFNNSILLITCTYNSNPFGVTQFIVAAISFVIGGFTATFFA--KEKKIQYGIYTGMIILIVNLVLQLIYGPTIHEPYYIKIGKIAGYLIASGIGGYLGK	6	111	119
ref|WP_013825920.1|	ref|WP_048082919.1|	253	1	147	8.06e-13	LQLHPIISIPFGVITTIVFLQVFGIPTLPLGGNAGILILIPVAI-IFGGFTATYFTDTNDKKIIYSICVGIIIS--FITLILGLKEYIGYNDVVVMFISFCVM--AGIGGFLGKIADEVNRKILEIKYKILSNISESKKNILKNVLISILFVGM	MKVHPVISIILGIIAGIILLI---ISIKLFSGNALVSAATNFAISIIGGFIATYFA--KEKKIRYGIYEGIILSIMFISLVSLIHTTYIYFLIALVGIIFEMLLPATIGGFIGKMTEGNNRKSFKMKY--LNRNLHPIITIIAGILVTIVLMSL	3	151	161
ref|WP_013825920.1|	ref|WP_048082919.1|	253	128	243	6.37e-11	LHPIISIPFGVITTIVFLQVFGIPTLPLGGNAGILILIPVAIIFGGFTATYFTDTNDKKIIYSICVGII-------ISFITLILGLKEYIGYNDVVVMFISFCVMAGIGGFLGKIADE	LHPIITIIAGILVTIVLMSLFGSFHLKISMGITYFLMATIFFAAGGFVTAFL--AREKKMLYGIYEGIVAVIYTILARYIGIIMGLNTTVDYYLIIGAVIGYFLAAAIGSYLGKAAGE	5	115	147
ref|WP_013825920.1|	ref|WP_069584028.1|	141	1	106	2.36e-12	LQLHPIISIPFGVITTIVFLQ---VFGIPTLPLGGNAGILILIPVAIIFGGFTATYFTDTNDKKIIYSICVGIIISFITLILGLKEYIGYND---VVVMFISFCVMAGIGGFLGKI	MKLHPLISIILGLFVTLLLVMIPLVFDAP--PLVGNAMFIF----AFILGGFIATYF--SKDKKIRYSIYMGLIAAVLFSIIESPD--GFNKLPAILLGFIQFPGMSLIGGLPGKI	3	112	152
ref|WP_013825920.1|	ref|WP_052374005.1|	111	30	109	2.26e-11	IIIIQSSGFSPNSTLISPSTVTWINNDTKI-HRVVSDYGL--FDSGNITPGQSYSHYFRDVKAYPYHDSIDPSMKGTVLL	IIIAHETLTWTNSTIKVGNNVTWINHDFAVNHEIVSDSANYPFDSGVLKNGQSYNLTFTQPGTYNYHDKLNPNLKGTIIV	169	245	143
ref|WP_013825920.1|	ref|WP_052375935.1|	109	3	108	2.98e-11	MSFIFVGLIFMPFG-----------NPDIIIIQSSGFSPNSTLISPSTVT-WINNDTKIHRVVSDYGLFDSGNITPGQSYSHYFRDVKAYPYHDSIDPSMKGTVLL	LNFIRIGIILLVIGVISISGCTQEKQTNTIIIQNFTFKPNPMHVKAGDVVRWTSHDNAPHKIVSDTGNFESPDLNNGDTFTYTFDKKGEFNYHDELDSSIKGKVIV	152	245	142
ref|WP_013825920.1|	ref|WP_157197598.1|	120	3	117	7.33e-11	QLHPIISIPFGVITTIVFLQV-FGIPTLPLGGNAGIL--ILIPVAIIFGGFTATYFTDTNDKKIIYSICVGIIISFI--TLILGLKEYIGYNDVVVMFISFCVMAGIGGFLGKIADEVNR	KFNPVISIISGIIVTITMAYVGFLIIDTP---NFGILDIILLCFSLVIGGFISTYFTE--KRRIVYGVCEGLILSIMCATYVVGTGKGLSYINYIAAYINVALGFVSATYIGSILGRKNR	4	118	140
ref|WP_013825920.1|	ref|WP_069583157.1|	356	1	110	1.14e-10	LQLHPIISIPFGVITTIVFLQVFGIPTLPLGGNAGILILIPVAIIFGGFTATYFTDTNDKKIIYSICVGII--ISFIT--LILGLKEYIGYNDVVVMFIS----FCVMAGIGGFLGKI	MRLHPIKSIIIGAVTAITLL---GISTLTFYNSLAFGILNFAAPLIGGFIATYF--TSKRMVRYGACAGIISAAAFVAFEFILG---NIGLEAIPLMFISSSIIFGVIAGLGGITGEI	3	112	147
ref|WP_013825920.1|	ref|WP_169740445.1|	93	16	92	2.74e-10	IIIQSSGFSPNSTLISPSTVT-WINNDTKIHRVVSDYGLFDSGNITPGQSYSHYFRDVKAYPYHDSIDPSMKGTVLL	IIIQNFTFKPNPMHVKAGDVVRWTSHDNAPHKIVSDTGNFESPDLNNGDTFTYTFDKKGEFNYHDELDSSIKGKVIV	170	245	134
ref|WP_013825920.1|	ref|WP_048082918.1|	356	1	115	3.03e-09	LQLHPIISIPFGVITTIVFLQVFGIPTLPLGGNAGILILIPVAIIFGGFTATYFTDTNDKKIIYSICVGII--ISFIT--LILGLKEYIGYNDVVVMFISFCVMAG-IGGFLGKIADEVNRKI	MRLHPIKSIILGAVIAITLL---GISALVFYNSLAFGILNFVAPLIGGFIATYF--TSKRMARYGACAGIISAAAFVAFEFILG---NIGEDAIIIMFISFSFIFGVIAGLIGIIGGIISNRV	3	120	136
ref|WP_013825920.1|	ref|WP_069585799.1|	375	1	172	7.70e-09	LHPIISIPFGVITTIVFLQVFGIPTLPLGGNAGILILIPVAIIFGGFTATYFTDTNDKKIIYSICVGIIISFITLILGLKEYIGYNDVVVMFISFCVMAGIGGFLGKIADEVNRKILEIKYKILSNISESKKNILKNVLISILFVGMMSFIFVGLIFMPFGNPDIIIIQSSGFSPNSTLISPSTVTWINNDTKIHRVVSDYGLF	MKPFLSIILALITTIL-LFICEI-SLSVALNIYLGSLTVFLFILGGGIATWFAA--GKKIRYSIYYGLILAVITLVLG--------DYRVLIFA-PIFAGIGGFLGKMADKDSRQTFNGYHPVIAIIVGIIVMYIYNVFLGSV-TGAYDLSSSGLIGFVIG---AITLAVGGF----------TTTFLSKEKKI-----QYGIY	5	208	133
ref|WP_013825920.1|	ref|WP_145975997.1|	117	5	107	2.23e-08	HPIISIPFGVITTIVFLQVFGIPTLPLGGNAGILILIPVAIIFGGFTATYFTDTNDKKI-IYSICVGIIISFITLILGLKEYIGYNDVVVMFISFCVMAGIGGFLGK	HPVIAIILGNIIT-GFLGGFVI-ILPISLLSHILVIF--IFVLGGFSATYLSRTNKATIGFYNSLLYSISSLIGAIFIFKTGLTPNKVLILFIYFPILGLIGGFIAK	6	111	122
ref|WP_013825920.1|	ref|WP_223790876.1|	127	46	125	7.08e-08	IIIIQSSGFSPNSTLISPSTVTWINNDTKI-HRVVSDYG--LFDSGNITPGQSYSHYFRDVKAYPYHDSIDPSMKGTVLL	IIITHETLTWNNSTIKVGNNITWINRDFAIEHEIVSNTSNYAFDSGVLKNGQSFSLNFTKAGTYNYYDKLHPNLSGIIIV	169	245	119
ref|WP_013825920.1|	ref|WP_218105063.1|	123	7	88	1.23e-07	VFGIPTLPLGGNAGILILIPVAIIFGGFTATYFTDTNDKKIIYSICVGIIISFITLILGLKEYIGYND---VVVMFISFCVMAGIGGFLGKI	VFDAP--PLVGNAMFIF----AFILGGFIATYF--SKDKKIRYSIYMGLIAAVLFSIIESPD--GFNKLPAILLGFIQFPGMSLIGGLPGKI	24	112	117
ref|WP_013825920.1|	ref|WP_223790185.1|	243	3	114	4.11e-07	QLHPIISIPFGVITTIVFLQVFG--IPTLPLGGNAG---ILILIPVAIIFGGFTATYFTDTNDKKIIYSICVGIIISFITLILGLKEYIGYNDVVVMFISFCVMAG----IGGFL	RFHPVIAIITGSFFIFIINQIMNYIFDSIPINGMLGSELITILVPVLLILGGFITAFITNRN--RLLCAFCVGLFFPIINNAINI-AYLNSISAIVLFVLGALFAALITTLGGFI	4	109	118
ref|WP_013825920.1|	ref|WP_156095866.1|	66	3	64	6.14e-07	STVTWINNDTKI-HRVVSDYG--LFDSGNITPGQSYSHYFRDVKAYPYHDSIDPSMKGTVLL	NNITWINRDFAIEHEIVSNTSNYAFDSGVLKNGQSFSLNFTKAGTYNYYDKLHPNLSGIIIV	187	245	108
# BLAST processed 1 queries

```



### **Step12: Sorting blast hits** 

- Input:  ``CLUSTERS_Cas/CLUSTER_*.ali``, `CDS.pty `, `VicinityIDs_Cas.lst`, `Seeds_Cas.tsv`, `Vicinity_Cas.tsv`

  - Parameters: 

    - (1) SortingOverlapThreshold:

      

    - (2) SortingCoverageThresold:

    














- Output: `Cas_OUTPUT/CLUSTERS_Cas/Sorted/CLUSTER_*.hits_sorted`

> CLUSTER_1.hits_sorted

```
WP_013825920.1	1286	1	251	MGLQLHPIISIPFGVITTIVFLQVFGIPTLPLGGNAGILILIPVAIIFGGFTATYFTDTNDKKIIYSICVGIIISFITLILGLKEYIGYNDVVVMFISFCVMAGIGGFLGKIADEVNRKILEIKYKILSNISESKKNILKNVLISILFVGMMSFIFVGLIFMPFGNPDIIIIQSSGFSPNSTLISPSTVTWINNDTKIHRVVSDYGLFDSGNITPGQSYSHYFRDVKAYPYHDSIDPSMKGTVLLPMSPGE	CLUSTER_1	NC_015574.1	1	1526093	1526849	6
WP_004031972.1	251	142	250	LLIGLPIFGVCLLLLLGLHDIPAE----IYVGNSGFDPNVTNIYPSKVTWTNNDSQIHRIISDDGLFDSGNLSPGENYTYDFSYHKNKIYKYHDSTNTSLKGTIQIEMGPG	CLUSTER_1	NZ_AMPO01000013.1	0	61551	61896	10000
WP_052374236.1	220	135	249	KRNLSVWIVLSILFV-------VGISGCTFKQPTNDTVVIQNEGFSP-SALIVPVNTTVTWINKDPVTQNLVSDTGLFESGNLSNGQSFNYTFNQTGSYHYYSNLYPNMKGSIIVTTSP	CLUSTER_1	NZ_JQLY01000001.1	0	1098608	1098959	10000
WP_223790141.1	210	145	245	NLIFVGV--FLIFGIVAVSGCTSSQTSIVTIQNSSFNPSTLNVQVGTTVTWINKDTTTHDVVSDTGLFNSGNLTNGMSYNYTFNQTGSFAYHSAIQPSMTGTIVV	CLUSTER_1	NZ_JAIOUQ010000001.1	0	17461	17848	10000
WP_081882600.1	196	145	245	NLIFVGV--FLVLGIVAVSGCTSNQTSGNTVTIQNMAFNPSTLNVKVGTTVTWINKDSVTHDVVSDTGLFNSGNLTNGMSYNYTFNQTGSFPYHCAIHPSMTGTIVV	CLUSTER_1	NZ_JQLY01000001.1	0	807416	807809	10000
WP_052374129.1	185	144	248	INFIFLGILLTIGIVAVSGCTSQSSTVTIQNMAFNPSTVHITGSTTIIWINKDNIEHEVVSDTGLFDSGVLAPGESFNYTFNQAGDYAYHCAIHPSMVGIIVVSSS	CLUSTER_1	NZ_JQLY01000001.1	0	784336	784822	10000
WP_071906376.1	167	3	159	MKFHPAISIILGIVTILMWFILAGILGLDFSKSISNTSGGATLIILI-----LGGFVATYFTE--DKKIRYSIYEGLIF---TAFVGLSKNLKL--IFAAFIAYVLFIGIGGFIGKMTDNKERQNFK-------NHFEKGFNPIITIVMGFIVANFFYYLLLGI	CLUSTER_1	NZ_LT607756.1	0	613477	614590	10000
WP_048082919.1	161	3	151	MKVHPVISIILGIIAGIILLI---ISIKLFSGNALVSAATNFAISIIGGFIATYFA--KEKKIRYGIYEGIILSIMFISLVSLIHTTYIYFLIALVGIIFEMLLPATIGGFIGKMTEGNNRKSFKMKY--LNRNLHPIITIIAGILVTIVLMSL	CLUSTER_1	NZ_KN050803.1	0	147173	147935	10000
WP_069584028.1	152	3	112	MKLHPLISIILGLFVTLLLVMIPLVFDAP--PLVGNAMFIF----AFILGGFIATYF--SKDKKIRYSIYMGLIAAVLFSIIESPD--GFNKLPAILLGFIQFPGMSLIGGLPGKI	CLUSTER_1	NZ_LMVM01000040.1	0	182744	183170	10000
WP_052375935.1	142	152	245	LNFIRIGIILLVIGVISISGCTQEKQTNTIIIQNFTFKPNPMHVKAGDVVRWTSHDNAPHKIVSDTGNFESPDLNNGDTFTYTFDKKGEFNYHDELDSSIKGKVIV	CLUSTER_1	NZ_JQKN01000008.1	0	54678	55008	10000
WP_157197598.1	140	4	118	KFNPVISIISGIIVTITMAYVGFLIIDTP---NFGILDIILLCFSLVIGGFISTYFTE--KRRIVYGVCEGLILSIMCATYVVGTGKGLSYINYIAAYINVALGFVSATYIGSILGRKNR	CLUSTER_1	NZ_JQKN01000011.1	0	42549	42912	10000
WP_069583157.1	147	3	112	MRLHPIKSIIIGAVTAITLL---GISTLTFYNSLAFGILNFAAPLIGGFIATYF--TSKRMVRYGACAGIISAAAFVAFEFILG---NIGLEAIPLMFISSSIIFGVIAGLGGITGEI	CLUSTER_1	NZ_LMVM01000037.1	0	122575	123646	10000
WP_048082918.1	136	3	120	MRLHPIKSIILGAVIAITLL---GISALVFYNSLAFGILNFVAPLIGGFIATYF--TSKRMARYGACAGIISAAAFVAFEFILG---NIGEDAIIIMFISFSFIFGVIAGLIGIIGGIISNRV	CLUSTER_1	NZ_KN050803.1	0	145938	147009	10000
WP_069585799.1	133	5	208	MKPFLSIILALITTIL-LFICEI-SLSVALNIYLGSLTVFLFILGGGIATWFAA--GKKIRYSIYYGLILAVITLVLG--------DYRVLIFA-PIFAGIGGFLGKMADKDSRQTFNGYHPVIAIIVGIIVMYIYNVFLGSV-TGAYDLSSSGLIGFVIG---AITLAVGGF----------TTTFLSKEKKI-----QYGIY	CLUSTER_1	NZ_LMVM01000039.1	0	64659	65787	10000
WP_145975997.1	122	6	111	HPVIAIILGNIIT-GFLGGFVI-ILPISLLSHILVIF--IFVLGGFSATYLSRTNKATIGFYNSLLYSISSLIGAIFIFKTGLTPNKVLILFIYFPILGLIGGFIAK	CLUSTER_1	NZ_LT607756.1	0	613074	613428	10000

```







### **Step13: Calculating LOUPE metric** (Parallalized)

- Input: `Cas_OUTPUT/CLUSTERS_Cas/Sorted/CLUSTER_*.hits_sorted`, `VicinityPermissiveClustsLinear_Cas.tsv`, Database
  - Parameter:	
    - ThreadNum:














- Output:  `Relevance_Cas.tsv`

> Relevance_Cas.tsv

```
CLUSTER_1	1	21	9	0.047619047619047616
CLUSTER_10	2	6	6	0.3333333333333333
CLUSTER_100	1	18	3	0.05555555555555555
CLUSTER_101	1	12	4	0.08333333333333333
CLUSTER_102	1	4	2	0.25
CLUSTER_103	7	10	0	0.7
CLUSTER_104	2	4	2	0.5
CLUSTER_105	2	11	2	0.18181818181818182
CLUSTER_106	1	13	4	0.07692307692307693
CLUSTER_107	7	9	0	0.7777777777777778
CLUSTER_108	1	7	4	0.14285714285714285
CLUSTER_109	3	12	4	0.25
CLUSTER_11	2	12	12	0.16666666666666666
CLUSTER_110	1	1	1	1.0
CLUSTER_111	1	3	3	0.3333333333333333
CLUSTER_112	3	20	7	0.15
CLUSTER_113	2	12	4	0.16666666666666666
CLUSTER_114	3	10	3	0.3
CLUSTER_115	1	9	5	0.1111111111111111
CLUSTER_116	2	28	7	0.07142857142857142
CLUSTER_117	1	2	7	0.5
CLUSTER_118	3	11	4	0.2727272727272727
CLUSTER_119	2	67	5	0.029850746268656716
CLUSTER_12	1	9	5	0.1111111111111111
CLUSTER_120	3	12	3	0.25
CLUSTER_121	2	11	5	0.18181818181818182
CLUSTER_122	3	21	2	0.14285714285714285
CLUSTER_123	2	3	0	0.6666666666666666
CLUSTER_124	1	3	13	0.3333333333333333
CLUSTER_125	1	3	8	0.3333333333333333
CLUSTER_126	2	11	5	0.18181818181818182
CLUSTER_127	3	8	0	0.375
CLUSTER_128	2	10	6	0.2
CLUSTER_129	2	10	3	0.2
CLUSTER_13	1	2	2	0.5
CLUSTER_130	1	2	3	0.5
CLUSTER_131	1	1	3	1.0
CLUSTER_132	5	301	6	0.016611295681063124
CLUSTER_133	2	59	8	0.03389830508474576
CLUSTER_134	3	9	1	0.3333333333333333
CLUSTER_135	2	11	7	0.18181818181818182
CLUSTER_136	3	13	2	0.23076923076923078
CLUSTER_137	1	10	6	0.1
CLUSTER_138	1	7	2	0.14285714285714285
CLUSTER_139	1	54	2	0.018518518518518517
CLUSTER_14	1	1	8	1.0
CLUSTER_140	1	16	10	0.0625
CLUSTER_141	1	2	13	0.5
CLUSTER_142	1	2	8	0.5
CLUSTER_143	1	1	6	1.0
CLUSTER_144	1	55	1	0.01818181818181818
CLUSTER_145	3	13	1	0.23076923076923078
CLUSTER_146	2	56	1	0.03571428571428571
CLUSTER_147	1	12	11	0.08333333333333333
CLUSTER_148	2	13	13	0.15384615384615385
CLUSTER_149	2	18	12	0.1111111111111111
CLUSTER_15	1	38	8	0.02631578947368421
CLUSTER_150	1	1	2	1.0
CLUSTER_151	1	3	13	0.3333333333333333
CLUSTER_152	1	12	12	0.08333333333333333
CLUSTER_153	1	3	11	0.3333333333333333
CLUSTER_154	1	4	7	0.25
CLUSTER_155	3	3	0	1.0
CLUSTER_156	1	20	7	0.05
CLUSTER_157	2	5	7	0.4
CLUSTER_158	1	6	9	0.16666666666666666
CLUSTER_159	2	22	4	0.09090909090909091
CLUSTER_16	1	1	1	1.0
CLUSTER_160	3	5	11	0.6
CLUSTER_161	1	9	4	0.1111111111111111
CLUSTER_162	2	133	2	0.015037593984962405
CLUSTER_163	2	28	3	0.07142857142857142
CLUSTER_164	1	6	8	0.16666666666666666
CLUSTER_165	1	10	9	0.1
CLUSTER_166	1	5	10	0.2
CLUSTER_167	1	11	3	0.09090909090909091
CLUSTER_168	5	5	1	1.0
CLUSTER_169	1	2	4	0.5
CLUSTER_17	3	12	7	0.25
CLUSTER_170	3	10	12	0.3
CLUSTER_171	1	10	4	0.1
CLUSTER_172	1	1	7	1.0
CLUSTER_173	1	6	10	0.16666666666666666
CLUSTER_174	1	5	1	0.2
CLUSTER_175	5	11	5	0.45454545454545453
CLUSTER_176	2	32	10	0.0625
CLUSTER_177	1	10	4	0.1
CLUSTER_178	5	16	5	0.3125
CLUSTER_179	1	11	6	0.09090909090909091
CLUSTER_18	1	8	1	0.125
CLUSTER_180	2	14	8	0.14285714285714285
CLUSTER_181	1	12	14	0.08333333333333333
CLUSTER_182	1	8	4	0.125
CLUSTER_183	1	7	11	0.14285714285714285
CLUSTER_184	2	38	9	0.05263157894736842
CLUSTER_185	1	50	9	0.02
CLUSTER_186	1	1	5	1.0
CLUSTER_187	3	9	6	0.3333333333333333
CLUSTER_188	1	2	4	0.5
CLUSTER_189	1	6	6	0.16666666666666666
CLUSTER_19	1	13	7	0.07692307692307693
CLUSTER_190	1	8	3	0.125
CLUSTER_191	3	12	0	0.25
CLUSTER_192	1	5	1	0.2
CLUSTER_193	3	13	5	0.23076923076923078
CLUSTER_194	1	5	15	0.2
CLUSTER_195	1	10	8	0.1
CLUSTER_196	2	13	2	0.15384615384615385
CLUSTER_197	6	21	8	0.2857142857142857
CLUSTER_198	3	13	4	0.23076923076923078
CLUSTER_199	1	7	2	0.14285714285714285
CLUSTER_2	2	3	8	0.6666666666666666
CLUSTER_20	2	16	2	0.125
CLUSTER_200	1	5	6	0.2
CLUSTER_201	1	11	8	0.09090909090909091
CLUSTER_202	2	11	0	0.18181818181818182
CLUSTER_203	1	11	2	0.09090909090909091
CLUSTER_204	1	3	0	0.3333333333333333
CLUSTER_205	1	2	14	0.5
CLUSTER_206	1	8	6	0.125
CLUSTER_207	2	5	5	0.4
CLUSTER_208	2	13	3	0.15384615384615385
CLUSTER_209	1	1	4	1.0
CLUSTER_21	1	11	8	0.09090909090909091
CLUSTER_210	1	9	1	0.1111111111111111
CLUSTER_211	1	3	7	0.3333333333333333
CLUSTER_212	2	10	5	0.2
CLUSTER_213	1	11	1	0.09090909090909091
CLUSTER_214	3	184	2	0.016304347826086956
CLUSTER_215	1	2	0	0.5
CLUSTER_216	1	2	13	0.5
CLUSTER_217	3	10	2	0.3
CLUSTER_218	1	8	5	0.125
CLUSTER_219	1	2	11	0.5
CLUSTER_22	1	12	4	0.08333333333333333
CLUSTER_220	2	12	4	0.16666666666666666
CLUSTER_221	1	3	3	0.3333333333333333
CLUSTER_222	3	10	6	0.3
CLUSTER_223	2	2	6	1.0
CLUSTER_224	1	5	4	0.2
CLUSTER_225	1	8	3	0.125
CLUSTER_226	4	4	1	1.0
CLUSTER_227	1	2	0	0.5
CLUSTER_228	1	10	2	0.1
CLUSTER_229	1	1	2	1.0
CLUSTER_23	2	10	5	0.2
CLUSTER_230	1	1	14	1.0
CLUSTER_231	1	12	5	0.08333333333333333
CLUSTER_232	1	70	2	0.014285714285714285
CLUSTER_233	3	8	7	0.375
CLUSTER_234	1	2	3	0.5
CLUSTER_235	1	26	4	0.038461538461538464
CLUSTER_236	1	2	0	0.5
CLUSTER_237	3	12	9	0.25
CLUSTER_238	2	46	6	0.043478260869565216
CLUSTER_239	1	1	0	1.0
CLUSTER_24	1	35	2	0.02857142857142857
CLUSTER_240	1	5	1	0.2
CLUSTER_241	1	7	6	0.14285714285714285
CLUSTER_242	1	9	1	0.1111111111111111
CLUSTER_243	3	7	8	0.42857142857142855
CLUSTER_244	2	29	5	0.06896551724137931
CLUSTER_245	1	23	9	0.043478260869565216
CLUSTER_246	2	2	5	1.0
CLUSTER_247	1	1	0	1.0
CLUSTER_25	1	30	7	0.03333333333333333
CLUSTER_26	1	2	12	0.5
CLUSTER_27	1	1	11	1.0
CLUSTER_28	1	13	8	0.07692307692307693
CLUSTER_29	1	4	7	0.25
CLUSTER_3	2	25	3	0.08
CLUSTER_30	1	2	13	0.5
CLUSTER_31	1	9	9	0.1111111111111111
CLUSTER_32	1	4	11	0.25
CLUSTER_33	2	13	7	0.15384615384615385
CLUSTER_34	1	11	10	0.09090909090909091
CLUSTER_35	2	13	12	0.15384615384615385
CLUSTER_36	3	19	6	0.15789473684210525
CLUSTER_37	2	4	2	0.5
CLUSTER_38	1	10	10	0.1
CLUSTER_39	1	12	12	0.08333333333333333
CLUSTER_4	1	4	3	0.25
CLUSTER_40	3	13	3	0.23076923076923078
CLUSTER_41	2	12	11	0.16666666666666666
CLUSTER_42	2	8	2	0.25
CLUSTER_43	1	3	1	0.3333333333333333
CLUSTER_44	3	5	0	0.6
CLUSTER_45	3	11	2	0.2727272727272727
CLUSTER_46	1	14	5	0.07142857142857142
CLUSTER_47	1	8	3	0.125
CLUSTER_48	1	12	5	0.08333333333333333
CLUSTER_49	3	13	1	0.23076923076923078
CLUSTER_5	2	19	9	0.10526315789473684
CLUSTER_50	2	7	1	0.2857142857142857
CLUSTER_51	3	8	1	0.375
CLUSTER_52	2	10	3	0.2
CLUSTER_53	1	1	8	1.0
CLUSTER_54	1	10	7	0.1
CLUSTER_55	2	2	1	1.0
CLUSTER_56	2	7	12	0.2857142857142857
CLUSTER_57	7	11	0	0.6363636363636364
CLUSTER_58	2	7	8	0.2857142857142857
CLUSTER_59	1	126	7	0.007936507936507936
CLUSTER_6	1	8	10	0.125
CLUSTER_60	1	9	8	0.1111111111111111
CLUSTER_61	3	14	10	0.21428571428571427
CLUSTER_62	1	14	9	0.07142857142857142
CLUSTER_63	1	22	6	0.045454545454545456
CLUSTER_64	1	1	0	1.0
CLUSTER_65	3	10	1	0.3
CLUSTER_66	1	3	6	0.3333333333333333
CLUSTER_67	1	13	9	0.07692307692307693
CLUSTER_68	3	5	0	0.6
CLUSTER_69	3	13	8	0.23076923076923078
CLUSTER_7	1	36	6	0.027777777777777776
CLUSTER_70	4	4	2	1.0
CLUSTER_71	3	11	11	0.2727272727272727
CLUSTER_72	4	65	10	0.06153846153846154
CLUSTER_73	2	23	9	0.08695652173913043
CLUSTER_74	6	8	0	0.75
CLUSTER_75	1	29	3	0.034482758620689655
CLUSTER_76	1	3	5	0.3333333333333333
CLUSTER_77	2	4	0	0.5
CLUSTER_78	3	10	10	0.3
CLUSTER_79	8	117	2	0.06837606837606838
CLUSTER_8	1	1	3	1.0
CLUSTER_80	3	6	0	0.5
CLUSTER_81	1	3	11	0.3333333333333333
CLUSTER_82	2	10	2	0.2
CLUSTER_83	1	5	1	0.2
CLUSTER_84	2	7	9	0.2857142857142857
CLUSTER_85	1	6	4	0.16666666666666666
CLUSTER_86	1	13	1	0.07692307692307693
CLUSTER_87	3	10	7	0.3
CLUSTER_88	2	7	4	0.2857142857142857
CLUSTER_89	1	48	4	0.020833333333333332
CLUSTER_9	1	2	3	0.5
CLUSTER_90	2	18	1	0.1111111111111111
CLUSTER_91	3	11	5	0.2727272727272727
CLUSTER_92	1	11	2	0.09090909090909091
CLUSTER_93	1	5	3	0.2
CLUSTER_94	3	23	6	0.13043478260869565
CLUSTER_95	1	1	6	1.0
CLUSTER_96	1	19	5	0.05263157894736842
CLUSTER_97	1	14	1	0.07142857142857142
CLUSTER_98	1	13	3	0.07692307692307693
CLUSTER_99	6	7	0	0.8571428571428571

```



### **Step14: Sorting Relevance**















## 💡Reference

**1.Shmakov, S.A., Faure, G., Makarova, K.S. *et al.* Systematic prediction of functionally linked genes in bacterial and archaeal genomes. *Nat Protoc* 14, 3013–3031 (2019). https://doi.org/10.1038/s41596-019-0211-1**
