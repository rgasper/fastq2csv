# fastq2csv
Simple CLI App to convert .fq (FastQ) files to .csv 

Won't load the entire FastQ file into memory, so should be suitable for very large files.

Handles about 12 Million fastq records (~3GB) per minute on my macbook.

```console
python fastq2csv.py my_fq_file.fq
```

## Pre-Commit

This repo uses [pre-commit](https://pre-commit.com/) for maintaining code quality. Set it up in this repo by running
`pre-commit install`.
