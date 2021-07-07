rule fastp_nanopore:
    input:
        get_nanopore_reads
    params:
        filtered = "results/{id}/fastp/MIN_out.fastq.gz"
    output:
        trimmed = "results/{id}/fastp/MIN_trimmed.fastq.gz",
        json = "results/{id}/fastp/MIN_fastp.json",
        html= "results/{id}/fastp/MIN_fastp.html",
    shell:
        "fastp --in1 {input} --out1 {output.trimmed} --failed_out {params.filtered} --json {output.json} --html {output.html}"

rule fastp_illumina:
    input:
        r1 = get_illumina_reads1,
        r2 = get_illumina_reads2
    params:
        filtered = "results/{id}/fastp/BMH_out.fastq.gz"
    output:
        trimmed_r1 = "results/{id}/fastp/BMH_r1_trimmed.fastq.gz",
        trimmed_r2 = "results/{id}/fastp/BMH_r2_trimmed.fastq.gz",
        json = "results/{id}/fastp/BMH_fastp.json",
        html= "results/{id}/fastp/BMH_fastp.html",
    shell:
        "fastp --in1 {input.r1} --in2 {input.r2} --out1 {output.trimmed_r1} --out2 {output.trimmed_r2} --failed_out {params.filtered} --json {output.json} --html {output.html}"

rule multiqc:
    input:
        "results/{id}/"
    output:
        directory("results/{id}/multiqc/")
    shell:
        "multiqc {input} -o {output}"