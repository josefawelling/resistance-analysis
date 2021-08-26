rule nanoqc_before_trim:
    input:
        get_nanopore_reads
    output:
        directory("results/{id}/reports/before_trim/nanoqc/")
    log:
        "logs/nanoqc/{id}_before_trim.log"
    shell:
        "mkdir -p {output} && "
        "nanoQC -o {output} {input} 2> {log}"

rule nanoplot_before_trim:
    input:
        get_nanopore_reads
    output:
        directory("results/{id}/reports/before_trim/nanoplot/")
    log:
        "logs/nanoplot/{id}_before_trim.log"
    shell:
        "NanoPlot --fastq {input} --outdir {output} 2> {log}"

rule porechop:
    input:
        get_nanopore_reads
    output:
        #must be a file not a folder
        "results/{id}/porechop/{id}_trim.fastq.gz"
    log:
        "logs/porechop/{id}.log"
    shell:
        "porechop -i {input} -o {output} 2> {log}"

rule filtlong_lite:
    input:
        reads = "results/{id}/porechop/{id}_trim.fastq.gz"
    output:
        "results/{id}/filtlong/{id}_flite.fastq"
    params:
        extra=" --min_length 1000 --keep_percent 95",
        target_bases = 0
    log:
        "logs/filtlong/{id}_flite.log"
    wrapper:
        "0.77.0/bio/filtlong"

rule nanoqc_after_flite:
    input:
        "results/{id}/filtlong/{id}_flite.fastq"
    output:
        directory("results/{id}/reports/after_flite/nanoqc/")
    log:
        "logs/nanoqc/{id}_after_flite.log"
    shell:
        "mkdir -p {output} && "
        "nanoQC -o {output} {input} 2> {log}"

rule nanoplot_after_flite:
    input:
        "results/{id}/filtlong/{id}_flite.fastq"
    output:
        directory("results/{id}/reports/after_flite/nanoplot/")
    log:
        "logs/nanoplot/{id}_after_flite.log"
    shell:
        "NanoPlot --fastq {input} --outdir {output} 2> {log}"