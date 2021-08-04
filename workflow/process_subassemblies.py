# read folder content
# search for assembly.fasta
# get the sample ID form path
# create new file path assemblies/sample_*.fasta
# rename + move the file
import glob
import os

#this will come from snakemake
path = "results/1/assemblies/sample_01"

#files_list = glob.glob(path + "/*")

# TODO add exception
assembly_path = path + "/assembly.fasta"

sample_ID = path[path.rfind("/")+1 :] #should be the ending sample_01
new_path = path[ :path.rfind("/") +1] + sample_ID + ".fasta" #should be the beginnig ending with assemblies/

os.system(f"mv {assembly_path} {new_path}")
