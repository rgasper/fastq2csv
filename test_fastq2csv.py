import unittest

from fastq2csv import FastQRecord, from_fastq_lines, get_csv_fname, grouper


class TestFastqParsing(unittest.TestCase):
    """ unit tests for fastq record parsing """

    def test_lines_to_fqrecord_unix_linesep(self):
        seq_id = "@D00780:495:CDB21ANXX:6:1212:1167:1947"
        description = "1:N:0:2"
        sequence = (
            "ANTTTCGTTCATGGGTCATGTAGCTGCCTAAGCAGTTTGTATGCCCGCTTAAGTGGCCCTACTTTGGCTATCCTGGCTGAGGCGGTTGAAGATCGGAAGAG"
        )
        quality = (
            "B#<BBFFFFFFFFFFFFFFFFFFFFFFFFFFFBFFFFFFFFFFFFBFFFFFFFFFFFFFFFFFFFFFFFFFFFBFFFFFBFFFFFFF</FF<F/FB<BFFF"
        )
        expected = FastQRecord(seq_id=seq_id, description=description, sequence=sequence, quality=quality)

        lines = [
            "@D00780:495:CDB21ANXX:6:1212:1167:1947 1:N:0:2\n",
            "ANTTTCGTTCATGGGTCATGTAGCTGCCTAAGCAGTTTGTATGCCCGCTTAAGTGGCCCTACTTTGGCTATCCTGGCTGAGGCGGTTGAAGATCGGAAGAG\n",
            "+\n",
            "B#<BBFFFFFFFFFFFFFFFFFFFFFFFFFFFBFFFFFFFFFFFFBFFFFFFFFFFFFFFFFFFFFFFFFFFFBFFFFFBFFFFFFF</FF<F/FB<BFFF\n",
        ]

        self.assertEqual(expected, from_fastq_lines(lines))

    def test_lines_to_fqrecord_win_linesep(self):
        seq_id = "@D00780:495:CDB21ANXX:6:1212:1167:1947"
        description = "1:N:0:2"
        sequence = (
            "ANTTTCGTTCATGGGTCATGTAGCTGCCTAAGCAGTTTGTATGCCCGCTTAAGTGGCCCTACTTTGGCTATCCTGGCTGAGGCGGTTGAAGATCGGAAGAG"
        )
        quality = (
            "B#<BBFFFFFFFFFFFFFFFFFFFFFFFFFFFBFFFFFFFFFFFFBFFFFFFFFFFFFFFFFFFFFFFFFFFFBFFFFFBFFFFFFF</FF<F/FB<BFFF"
        )
        expected = FastQRecord(seq_id=seq_id, description=description, sequence=sequence, quality=quality)

        lines = [
            "@D00780:495:CDB21ANXX:6:1212:1167:1947 1:N:0:2\r\n",
            "ANTTTCGTTCATGGGTCATGTAGCTGCCTAAGCAGTTTGTATGCCCGCTTAAGTGGCCCTACTTTGGCTATCCTGGCTGAGGCGGTTGAAGATCGGAAGAG\r\n",
            "+\r\n",
            "B#<BBFFFFFFFFFFFFFFFFFFFFFFFFFFFBFFFFFFFFFFFFBFFFFFFFFFFFFFFFFFFFFFFFFFFFBFFFFFBFFFFFFF</FF<F/FB<BFFF\r\n",
        ]

        self.assertEqual(expected, from_fastq_lines(lines))

    def test_lines_to_fqrecord_cleaned_lines(self):
        seq_id = "@D00780:495:CDB21ANXX:6:1212:1167:1947"
        description = "1:N:0:2"
        sequence = (
            "ANTTTCGTTCATGGGTCATGTAGCTGCCTAAGCAGTTTGTATGCCCGCTTAAGTGGCCCTACTTTGGCTATCCTGGCTGAGGCGGTTGAAGATCGGAAGAG"
        )
        quality = (
            "B#<BBFFFFFFFFFFFFFFFFFFFFFFFFFFFBFFFFFFFFFFFFBFFFFFFFFFFFFFFFFFFFFFFFFFFFBFFFFFBFFFFFFF</FF<F/FB<BFFF"
        )
        expected = FastQRecord(seq_id=seq_id, description=description, sequence=sequence, quality=quality)

        lines = [
            "@D00780:495:CDB21ANXX:6:1212:1167:1947 1:N:0:2",
            "ANTTTCGTTCATGGGTCATGTAGCTGCCTAAGCAGTTTGTATGCCCGCTTAAGTGGCCCTACTTTGGCTATCCTGGCTGAGGCGGTTGAAGATCGGAAGAG",
            "+",
            "B#<BBFFFFFFFFFFFFFFFFFFFFFFFFFFFBFFFFFFFFFFFFBFFFFFFFFFFFFFFFFFFFFFFFFFFFBFFFFFBFFFFFFF</FF<F/FB<BFFF",
        ]

        self.assertEqual(expected, from_fastq_lines(lines))

    def test_handles_quotes_in_seq_id(self):
        seq_id = 'abcd123"'
        description = "quotes"
        sequence = "ATCG"
        quality = "FFBB"
        expected = FastQRecord(seq_id=seq_id, description=description, sequence=sequence, quality=quality)

        lines = ['abcd123" quotes', "ATCG", "+", "FFBB"]

        self.assertEqual(expected, from_fastq_lines(lines))

    def test_grouper(self):
        chunksize = 4
        stuff = ["whatever"] * chunksize * 3
        for group in grouper(stuff, chunksize):
            self.assertEqual(len(group), chunksize)

    def test_filename_parsing_abspath(self):
        fqfile = "/Users/raymondgasper/Projects/work/fastq_playin/whatever.fq"
        csvfile = "/Users/raymondgasper/Projects/work/fastq_playin/whatever.csv"
        self.assertEqual(get_csv_fname(fqfile), csvfile)

    def test_filename_parsing_relpath(self):
        fqfile = "whatever.fq"
        csvfile = "whatever.csv"
        self.assertEqual(get_csv_fname(fqfile), csvfile)
