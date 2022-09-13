import time
import numpy as np
import pandas as pd
import argparse


# Hyper-parameters
i = 0
cnt = 0
read_time_e = 0
read_time_s = 0
t1 = 0
t2 = 0

# Reading arguments from command line
ap = argparse.ArgumentParser(description = "Extracting seeds from CDS file")
ap.add_argument("-s", help = "SeedsFileName, seeds csv file", required = True)
ap.add_argument("-c", help = "CDSFileName, cds pty file, containing seed information", required = True)
ap.add_argument("-o", help = "ResultFileName, output tsv file", required = True)
opts = ap.parse_args()

seed_path = opts.s  # Archaea_RM.csv
cds_path = opts.c  # archaea_cds.pty
seeds_name = opts.o   # Seeds_RM_A.tsv


# O(n)构建哈希表
def create_hash_table(cds_find):
    hash_table = dict()
    for idx, row in enumerate(cds_find.itertuples()):
        if getattr(row, 'cds_accession') not in hash_table.keys():
            hash_table.update({getattr(row, 'cds_accession'): idx + 1})
    return hash_table


def SeedExtract(seed_path, cds_path):
    global i, read_time_s, read_time_e, t1, t2
    info_alloc = pd.DataFrame()
    read_time_s = time.time()
    cds_file = pd.read_table(cds_path, names=['LociID', 'ORFStart_ORFStop',
                                              'Strand', 'OrganismID', 'ContigID', 'product_accession'])

    cds_file[['Start', 'Stop']] = cds_file["ORFStart_ORFStop"].str.split(':', n=1, expand=True)
    cds_file['Stop'] = cds_file['Stop'].str.replace('>', '')
    cds_file[['OrganismID', 'assembly_accession']] = cds_file['OrganismID'].str.rsplit('-', n=1, expand=True)
    cds_file = cds_file.drop(labels='ORFStart_ORFStop', axis=1)
    cds_file = cds_file.drop(labels='OrganismID', axis=1)

    cds_accession = cds_file.assembly_accession
    cds_end = cds_file.Stop
    cds_find = pd.concat([cds_accession, cds_end], axis=1); cds_find.columns = ['cds_accession', 'cds_end']

    hash_table = create_hash_table(cds_find)
    hash_table_values = list(hash_table.values())
    print("----------------------------HASH TABLE----------------------------",flush=True)
    print(hash_table, flush=True)
    print("HASH_TABLE LENGTH = ", len(hash_table), flush=True)

    cds_find = cds_find.to_numpy()

    seed_file = pd.read_csv(seed_path)
    seed_assembly_accession = seed_file.assembly_accession.str.replace("GCA", "GCF")
    seed_end = seed_file.end
    seed_find = pd.concat([seed_assembly_accession, seed_end], axis=1)

    read_time_e = time.time()

    print("------------------------Processing Starting Now------------------------", flush=True)
    t1 = time.time()
    for id, end in zip(seed_find.assembly_accession, seed_find.end):
        if id not in hash_table.keys():
            continue
        if hash_table_values.index(hash_table[id]) + 1 < len(hash_table_values):
            l2 = hash_table_values[hash_table_values.index(hash_table[id]) + 1]
        else:
            l2 = len(cds_file)
        l1 = int(hash_table[id])  # Starting Point
        length = l2 - l1
        print(id, ' ---------> Search length =', length, '[Start =', l1, ', Stop =', l2, ']', flush=True)
        accession_list = cds_find[int(hash_table[id]): int(hash_table[id]) + length + 1]

        for idx, item in enumerate(accession_list):
            if (item == np.array([id, str(end)])).all():
                print('No.', i, ' Seed Found: ', id, str(end), flush=True)
                # Process the corresponding items
                data = cds_file.loc[idx + l1, ['assembly_accession',
                                        'LociID', 'product_accession', 'ContigID', 'Start', 'Stop']]
                data = data.to_dict()
                data = pd.DataFrame(data, index=[i]); i += 1
                info_alloc = pd.concat([info_alloc, data])
        t2 = time.time()
    info_alloc.drop_duplicates(inplace=True)
    print("------------------------Processing Finished------------------------",flush=True)
    print(info_alloc,flush=True)
    print('----------------------------', i, 'Seeds in total----------------------------',flush=True)
    info_alloc.to_csv(seeds_name, index=False, sep='\t', header=False, )


# Hit it!
SeedExtract(seed_path, cds_path)
print("---------------------------------Performance Attributes---------------------------------")
print('File saved as ' + seeds_name)
print('Reading files and creating hash table used time = %.3fs' %(read_time_e - read_time_s))
print('Searching used time = %.3fs' %(t2 - t1))
print("Total used time = %.3fs" %(read_time_e - read_time_s + t2 - t1))
print("Seed Extraction Done!!")

