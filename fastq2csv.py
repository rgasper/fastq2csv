import argparse
import logging
from typing import List
import re
import dataclasses
import os.path
from itertools import zip_longest as izip_longest

def grouper(iterable, n:int, fillvalue=None):
    args = [iter(iterable)] * n
    return izip_longest(*args, fillvalue=fillvalue)



@dataclasses.dataclass()
class FastQRecord:
    seq_id: str
    description: str
    sequence: str
    quality: str

    @staticmethod
    def csv_header() -> str:
        return "id,description,sequence,quality\n"

    def to_csv(self) -> str:
        return f'"{self.seq_id}","{self.description}","{self.sequence}","{self.quality}"\n'


def from_fastq_lines(lines: List[str]) -> FastQRecord:
    lines = [l.strip() for l in lines] 
    seq_id, desc = re.split(r'\s', lines[0], maxsplit=1)
    seq = lines[1]
    # for some reason a line is a plus sign with no significance
    quality = lines[3]
    return FastQRecord(seq_id=seq_id, description= desc, sequence=seq, quality=quality)


def fastq2csv(fastqfile, csvfile):
    csvfile.write(FastQRecord.csv_header())
    
    for fastqreclines in grouper(fastqfile, 4):
        FQRecord = from_fastq_lines(fastqreclines)
        csvfile.write(FQRecord.to_csv())

def get_csv_fname(fqfilepath: str) -> str:
    return os.path.splitext(fqfilepath)[0] + '.csv'

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert FastQ file to CSV.")
    parser.add_argument("fqfile", type=str)
    args = parser.parse_args()
    if '.fq' not in args.fqfile:
        raise ValueError('must input a fastq file')
    outpath = get_csv_fname(args.fqfile)
    with open(args.fqfile, 'r') as fqfile, open(outpath, 'w') as csvfile:
        fastq2csv(fqfile, csvfile)
