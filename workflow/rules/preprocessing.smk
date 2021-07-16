rule fastp_nanopore:
    input:
        get_nanopore_reads
    params:
        filtered = "results/{id}/fastp/ONT_out.fastq.gz"
    output:
        trimmed = "results/{id}/fastp/ONT_trimmed.fastq.gz",
        json = "results/{id}/fastp/ONT_fastp.json",
        html= "results/{id}/fastp/ONT_fastp.html",
    log:
        "logs/{id}/fastp_nanopore.log"
    shell:
        "fastp --in1 {input} --out1 {output.trimmed} --failed_out {params.filtered} --json {output.json} --html {output.html}"

rule fastp_illumina:
    input:
        r1 = get_illumina_reads1,
        r2 = get_illumina_reads2
    params:
        filtered = "results/{id}/fastp/BMH_out.fastq.gz"
    output:
        trimmed_r1 = "results/{id}/fastp/IL-r1_trimmed.fastq.gz",
        trimmed_r2 = "results/{id}/fastp/IL-r2_trimmed.fastq.gz",
        json = "results/{id}/fastp/IL_fastp.json",
        html= "results/{id}/fastp/IL_fastp.html",
    log:
        "logs/{id}/fastp_illumina.log"
    shell:
        "fastp --in1 {input.r1} --in2 {input.r2} --out1 {output.trimmed_r1} --out2 {output.trimmed_r2} --failed_out {params.filtered} --json {output.json} --html {output.html}"

rule multiqc:
    input:
        expand("results/{{id}}/fastp/{platform}_fastp.json", platform=get_platforms())
    output:
        directory("results/{id}/multiqc/")
    log:
        "logs/{id}/multiqc.log"
    shell:
        "multiqc --force {input} -o {output}"