import pandas as pd

configfile: "config/config.yaml"

samples = pd.read_csv("config/pep/documents.csv").set_index("sample_name", drop=False)
samples.index.names = ["sample_name"]

## helper functions

def get_all_ids():
    return pep.sample_table["sample_name"].to_list()

def get_nanopore_reads(wildcards):
    return pep.sample_table.loc[wildcards.id][["nanopore_reads"]]

def get_genome_size(wildcards):
    return pep.sample_table.loc[wildcards.id]["species_genome_size"]
