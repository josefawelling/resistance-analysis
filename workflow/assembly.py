# create subsets with trycycler
# trycycler subsample --reads results/1/fastp/MIN_trimmed.fastq.gz --out_dir results/1/subsets/
# assemble them with flye
# flye --nano-raw results/1/subsets/sample_01.fastq -o results/1/assemblies/sample_01/
# move + rename the assembly.fasta 
#
import os
import glob

input = "results/1/fastp/MIN_trimmed.fastq.gz" #snakemake.input
sample_id = "1" #snakemake.params

out_dir = f"results/{sample_id}/"

subsets_dir = out_dir + "subsets/"
if len(glob.glob(subsets_dir)) == 0:
    os.system(f"mkdir {subsets_dir}")

assemblies_dir = out_dir + "assemblies/"
if len(glob.glob(assemblies_dir)) == 0:
    os.system(f"mkdir {assemblies_dir}")

def create_subsets(input, subsets_dir):
    # create subsets with trycycler
    os.system(f"trycycler subsample --reads {input} --out_dir {subsets_dir}")

def assemble_subsets(out_dir, subsets_dir, assemblies_dir):
    #create read.fasta.gz
    reads_path = out_dir + "reads.fastq.gz"
    os.system(f"> {reads_path}")

    fastqs = glob.glob(subsets_dir + "*")
    for fastq in fastqs:
        os.system(f"gzip {fastq}")
    
    subsets = glob.glob(subsets_dir + "*.gz")

    for subset in subsets:
        subset_id = subset[subset.rfind("/")+1 : subset.rfind(".fast")]
        subset_dir = assemblies_dir + subset_id + "/"
        os.system(f"mkdir {subset_dir}")
        os.system(f"flye --nano-raw {subset} -o {subset_dir}")

        # write subset reads to reads.fasta
        os.system(f"cat {subset}  >> {reads_path}")

        subset_assembly_path = subset_dir + "*.fasta" #"assembly.fasta"
        new_subset_assembly_path = assemblies_dir + subset_id + ".fasta"

        os.system(f"mv {subset_assembly_path} {new_subset_assembly_path}")
    
#create_subsets(input, subsets_dir)
#assemble_subsets(out_dir, subsets_dir,assemblies_dir)

