import os
import argparse

ap = argparse.ArgumentParser(description="Extracting seeds from CDS file")
ap.add_argument("-p", help="Working Path", required=True)
ap.add_argument("-s", help="Type", required=True)
opts = ap.parse_args()

# 搜索 gbff 文件，返回 gbff 文件路径
def GbffContext(path, types):
    file_path  = path + types
    files_path = os.path.abspath(file_path)
    all_files = os.listdir(files_path)
    context = []
    for file in all_files:
        if file.endswith("gbff"):
            gbff_file_path = file_path + '/' + file
            context.append(gbff_file_path)

    return context

# 提前下载 Biopython 包
from Bio import SeqIO

#产生 cds.pty 文件
def CdsCoordinate(path, type):
    record_iterator = SeqIO.parse(path, 'genbank')
    cds_file = '_'.join([type,"cds.pty"])

    with open(cds_file,'a') as f:
        try:
            while(True):
                record = next(record_iterator)
                t = record.features
                for t_cds in t:
                    # cds 注释中必然含有 protein_id 的 key
                    if t_cds.qualifiers.__contains__('protein_id'):
                        f.write(str(t_cds.qualifiers["locus_tag"])[2:-2])# locus_tag, [2:-2]为了去掉括号和引号，下文同理
                        f.write('\t')

                        f.write(str(t_cds.location)[1:-4]) # ORFStart..ORFStop
                        f.write('\t')

                        f.write(str(t_cds.location)[-2])# Strand
                        f.write('\t')

                        f.write(record.description.split(',')[0])
                        f.write('-')
                        f.write(str(record.dbxrefs[-1])[9:]) # OrganismID
                        f.write('\t')

                        f.write(record.id)# ContigID
                        f.write('\t')
                        
                        f.write(str(t_cds.qualifiers["protein_id"])[2:-2])# Accession number
                        f.write("\n")
        except StopIteration as e:
            print("已经完成", path, "CDS内容的搜索")
    f.close()


# 输入参数
if __name__ == "__main__":
    path = opts.p
    type = opts.s

    gbff_context = GbffContext(path, type)
    for gbff in gbff_context:  
        print(gbff)
        CdsCoordinate(gbff, type)

