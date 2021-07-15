rule flye:
    input:
        "results/{id}/fastp/ONT_trimmed.fastq.gz"
    output:
        directory("results/{id}/flye/")
    log:
        "logs/{id}/flye.log"
    shell:
        "flye --nano-raw {input} -o {output}"

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
