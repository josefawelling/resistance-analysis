"""
rule trycycler_create_subsets:
    input:
        "results/{id}/filtlong/{id}_flite.fastq"
    params:
        genome_size = get_genome_size
    output:
        outdir = directory("results/{id}/trycycler/subsets"), 
        outfiles = expand("results/{id}/trycycler/subsets/{subset_id}.fastq",subset_id=get_subset_ids())
    log:
        "logs/trycycler/create_subset_{id}.log"
    shell:
        "trycycler subsample --genome_size {params.genome_size} --reads {input} --out_dir {output.outdir} 2> {log}"

rule subset_flye:
    input:
        "results/{id}/trycycler/subsets/sample_{subset_id}.fastq"
    output:
        outdir = directory("results/{id}/trycycler/assemblies/{subset_id}/"),
        assembly = "results/{id}/trycycler/assemblies/assembly_{subset_id}.fasta"
    params:
        "results/{id}/trycycler/assemblies/{subset_id}/assembly.fasta"
    log:
        "logs/trycycler/{id}_subset_flye/{subset_id}.log"
    shell:
        "flye --nano-raw {input} --plasmids -o {output.outdir} && mv {params} {output.assembly} 2> {log}"

rule checkm:
    input:
        "results/{id}/flye/"
    output:
        directory("results/{id}/checkm/")
    log:
        "logs/{id}/checkm.log"
    shell:
        # run the lineage workflow, -x to change the file extension
        "checkm lineage_wf -x fasta {input} {output}"
"""
rule trycycler:
    input:
        "results/{id}/filtlong/{id}_flite.fastq"
    output:
        directory("results/{id}/trycycler/")
    params:
        genome_size = get_genome_size,
        reports_dir = "results/{id}/reports/"
    log:
        "logs/trycycler/{id}.log"
    script:
        "../scripts/trycycler_assembly.py"
