rule flye:
    input:
        "results/{id}/fastp/*ONT_trimmed.fast*"
    output:
        directory("results/{id}/flye/")
    log:
        "logs/{id}/flye.log
    shell:
        "flye --nano-raw {input} -o {output}"