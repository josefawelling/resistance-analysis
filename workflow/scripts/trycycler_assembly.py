# create subsets with trycycler
# trycycler subsample --reads results/1/fastp/MIN_trimmed.fastq.gz --out_dir results/1/subsets/
# assemble them with flye
# flye --nano-raw results/1/subsets/sample_01.fastq -o results/1/assemblies/sample_01/
# move + rename the assembly.fasta 
#

sys.stderr = open(snakemake.log[0], "w")

import sys
import os
import glob

def create_dir(dir):
    if len(glob.glob(dir)) == 0:
        os.system(f"mkdir -p {dir}")

def create_subsets(input_reads, subsets_dir, genome_size):
    # create subsets with trycycler
    os.system(f"trycycler subsample --reads {input_reads} --out_dir {subsets_dir} --genome_size {genome_size}")

def assemble_subsets(subsets_dir, assemblies_dir):

    subsets = glob.glob(subsets_dir + "sample*.fastq")

    for subset in subsets:
        subset_id = subset[subset.rfind("/sample")+7 : subset.rfind(".fastq")]
        subset_dir = f"{assemblies_dir}subassembly{subset_id}/"
        create_dir(subset_dir)

        os.system(f"flye --nano-raw {subset} -o {subset_dir}")

        # copy all subassemblies in one folder, renamed with the subsetnr to identify
        os.system(f"cp {subset_dir}assembly.fasta {assemblies_dir}assembly{subset_id}.fasta")

def checkm_subassemblies(assemblies_dir, reports_dir):

    reports_folder = f"{reports_dir}checkm_subassemblies/"
    create_dir(reports_folder)
    subassembly_folder = glob.glob("{assemblies_dir}subassembly*")

    for subassembly in subassembly_folder:
        output = reports_folder + subassembly[subassembly.rfind("/sub")+1 : subset.rfind("/")] #subassembly01-12
        create_dir(output)
        os.system(f"checkm lineage_wf -x fasta {subassembly} {output}")


input_reads = snakemake.input[0] #"results/bc01/filtlong/bc01_flite.fastq"
out_dir = snakemake.output[0] #"results/bc01/trycycler/"
reports_dir = snakemake.params.reports_dir #"results/bc01/reports/"
e_coli_size = "4600000" #snakemake.params.genome_size

subsets_dir = out_dir + "/subsets/"
create_dir(subsets_dir)

create_subsets(input_reads, subsets_dir, e_coli_size) # -> outdir/sample_*.fastq

assemblies_dir = out_dir + "/assemblies/"
create_dir(assemblies_dir)

assemble_subsets(subsets_dir,assemblies_dir)

checkm_subassemblies(assemblies_dir, reports_dir)

""""
assemblies_path = assemblies_dir + "*.fasta"

trycycler_dir = out_dir + "trycycler/"

os.system(f"trycycler cluster --assemblies {assemblies_path} --reads {input_reads} --out_dir {trycycler_dir}")

for cluster in glob.glob(trycycler_dir + "cluster_*"):
    os.system(f"trycycler reconcile --reads {reads_path} --cluster_dir {cluster}")
    os.system(f"trycycler msa --cluster_dir {cluster}")
"""


