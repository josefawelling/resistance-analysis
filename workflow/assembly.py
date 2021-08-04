# create subsets with trycycler
# trycycler subsample --reads results/1/fastp/MIN_trimmed.fastq.gz --out_dir results/1/subsets/
# assemble them with flye
# flye --nano-raw results/1/subsets/sample_01.fastq -o results/1/assemblies/sample_01/
# move + rename the assembly.fasta 
#

#sys.stderr = open(snakemake.log[0], "w")

import sys
import os
import glob

def create_dir(dir):
    if len(glob.glob(dir)) == 0:
        os.system(f"mkdir {dir}")

def create_subsets(input, subsets_dir):
    # create subsets with trycycler
    os.system(f"trycycler subsample --reads {input} --out_dir {subsets_dir}")

def assemble_subsets(reads_path, subsets_dir, assemblies_dir):
    #create read.fasta.gz
    #os.system(f"> {reads_path}")

    fastqs = glob.glob(subsets_dir + "*")
    for fastq in fastqs:
        os.system(f"gzip {fastq}")
    
    subsets = glob.glob(subsets_dir + "*.gz")

    for subset in subsets:
        subset_id = subset[subset.rfind("/")+1 : subset.rfind(".fast")]
        subset_dir = assemblies_dir + subset_id + "/"
        create_dir(subset_dir)

        os.system(f"flye --nano-raw {subset} -o {subset_dir}")

        # write subset reads to reads.fasta
        #os.system(f"cat {subset}  >> {reads_path}")

        subset_assembly_path = subset_dir + "*.fasta" #"assembly.fasta"
        new_subset_assembly_path = assemblies_dir + subset_id + ".fasta"

        os.system(f"mv {subset_assembly_path} {new_subset_assembly_path}")
    
    os.system(f"cat {subsets} > {reads_path}")


#input = "results/1/fastp/MIN_trimmed.fastq.gz" #snakemake.input
sample_id = "3" #snakemake.params

out_dir = f"results/{sample_id}/"

#subsets_dir = out_dir + "subsets/"
#create_dir(subsets_dir)

assemblies_dir = out_dir + "assemblies/"
create_dir(assemblies_dir)

reads_path = out_dir + "reads.fastq.gz"

assemblies_path = assemblies_dir + "*.fasta"

trycycler_dir = out_dir + "trycycler/"

os.system(f"trycycler cluster --assemblies {assemblies_path} --reads {reads_path} --out_dir {trycycler_dir}")
""""
for cluster in glob.glob(trycycler_dir + "cluster_*"):
    os.system(f"trycycler reconcile --reads {reads_path} --cluster_dir {cluster}")
    os.system(f"trycycler msa --cluster_dir {cluster}")
"""
#create_subsets(input, subsets_dir)
#assemble_subsets(reads_path, subsets_dir,assemblies_dir)

