"""
BSD 3-Clause License

Copyright (c) 2019, Andrew Riha
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived from
   this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""

import datetime
import os
import io
import gzip
import zipfile
import binascii
from copy import deepcopy

import numpy as np
import pandas as pd
import vcf

import snps
from snps.utils import save_df_as_csv, clean_str


class Reader:
    """ Class for reading and parsing raw data / genotype files. """

    def __init__(self, file="", only_detect_source=False, resources=None):
        """ Initialize a `Reader`.

        Parameters
        ----------
        file : str or bytes
            path to file to load or bytes to load
        only_detect_source : bool
            only detect the source of the data
        resources : Resources
            instance of Resources
        """
        self._file = file
        self._only_detect_source = only_detect_source
        self._resources = resources

    def __call__(self):
        """ Read and parse a raw data / genotype file.

        Returns
        -------
        tuple : (pandas.DataFrame, str)
            dataframe of parsed SNPs, detected source of SNPs
        """
        file = self._file

        try:
            # peek into files to determine the data format
            if isinstance(file, str) and os.path.exists(file):
                if ".zip" in file:
                    with zipfile.ZipFile(file) as z:
                        with z.open(z.namelist()[0], "r") as f:
                            first_line, comments, data = self._extract_comments(f, True)
                elif ".gz" in file:
                    with gzip.open(file, "rt") as f:
                        first_line, comments, data = self._extract_comments(f, False)
                else:
                    with open(file, "r") as f:
                        first_line, comments, data = self._extract_comments(f, False)

            elif isinstance(file, bytes):
                if self.is_zip(file):

                    with zipfile.ZipFile(io.BytesIO(file)) as z:
                        namelist = z.namelist()
                        key = "GFG_filtered_unphased_genotypes_23andMe.txt"
                        key_search = [key in name for name in namelist]

                        if any(key_search):
                            filename = namelist[key_search.index(True)]
                        else:
                            filename = namelist[0]

                        with z.open(filename, "r") as f:
                            data = f.read()
                            file = io.BytesIO(data)
                            first_line, comments, data = self._extract_comments(
                                io.BytesIO(data), True
                            )

                elif self.is_gzip(file):

                    with gzip.open(io.BytesIO(file), "rb") as f:
                        data = f.read()
                        file = io.BytesIO(data)
                        first_line, comments, data = self._extract_comments(
                            io.BytesIO(data), True
                        )

                else:
                    file = io.BytesIO(file)
                    first_line, comments, data = self._extract_comments(
                        deepcopy(file), True
                    )

            else:
                return pd.DataFrame(), ""

            if "23andMe" in first_line:
                return self.read_23andme(file)
            elif "Ancestry" in first_line:
                return self.read_ancestry(file)
            elif first_line.startswith("RSID"):
                return self.read_ftdna(file)
            elif "famfinder" in first_line:
                return self.read_ftdna_famfinder(file)
            elif "MyHeritage" in first_line:
                return self.read_myheritage(file)
            elif "Living DNA" in first_line:
                return self.read_livingdna(file)
            elif "SNP Name	rsID	Sample.ID	Allele1...Top" in first_line:
                return self.read_mapmygenome(file)
            elif "lineage" in first_line or "snps" in first_line:
                return self.read_lineage_csv(file, comments)
            elif first_line.startswith("rsid"):
                return self.read_generic_csv(file)
            elif "vcf" in comments.lower():
                return self.read_vcf(file)
            elif ("Genes for Good" in comments) | ("PLINK" in comments):
                return self.read_genes_for_good(file)
            elif "CODIGO46" in comments:
                return self.read_codigo46(data)
            else:
                return pd.DataFrame(), ""
        except Exception as err:
            print(err)
            return pd.DataFrame(), ""

    @classmethod
    def read_file(cls, file, only_detect_source, resources):
        """ Read `file`.

        Parameters
        ----------
        file : str or bytes
            path to file to load or bytes to load
        only_detect_source : bool
            only detect the source of the data
        resources : Resources
            instance of Resources

        Returns
        -------
        tuple : (pandas.DataFrame, str)
            dataframe of parsed SNPs, detected source of SNPs
        """
        r = cls(file, only_detect_source, resources)
        return r()

    def _extract_comments(self, f, decode):
        line = self._read_line(f, decode)
        first_line = line
        comments = ""
        data = ""

        if first_line.startswith("#"):
            while line.startswith("#"):
                comments += line
                line = self._read_line(f, decode)
            while line:
                data += line
                line = self._read_line(f, decode)

        elif first_line.startswith("[Header]"):
            while not line.startswith("[Data]"):
                comments += line
                line = self._read_line(f, decode)
            # Ignore the [Data] row
            line = self._read_line(f, decode)
            while line:
                data += line
                line = self._read_line(f, decode)

        return first_line, comments, data

    @staticmethod
    def is_zip(bytes_data):
        """Check whether or not a bytes_data file is a valid Zip file."""
        return zipfile.is_zipfile(io.BytesIO(bytes_data))

    @staticmethod
    def is_gzip(bytes_data):
        """Check whether or not a bytes_data file is a valid gzip file."""
        return binascii.hexlify(bytes_data[:2]) == b"1f8b"

    @staticmethod
    def _read_line(f, decode):
        if decode:
            # https://stackoverflow.com/a/606199
            return f.readline().decode("utf-8")
        else:
            return f.readline()

    def read_23andme(self, file):
        """ Read and parse 23andMe file.

        https://www.23andme.com

        Parameters
        ----------
        file : str
            path to file

        Returns
        -------
        pandas.DataFrame
            genetic data normalized for use with `snps`
        str
            name of data source
        """

        if self._only_detect_source:
            return pd.DataFrame(), "23andMe"

        df = pd.read_csv(
            file,
            comment="#",
            sep="\t",
            na_values="--",
            names=["rsid", "chrom", "pos", "genotype"],
            index_col=0,
            dtype={"chrom": object},
        )

        return df, "23andMe"

    def read_ftdna(self, file):
        """Read and parse Family Tree DNA (FTDNA) file.

        https://www.familytreedna.com

        Parameters
        ----------
        file : str
            path to file

        Returns
        -------
        pandas.DataFrame
            genetic data normalized for use with `snps`
        str
            name of data source
        """

        if self._only_detect_source:
            return pd.DataFrame(), "FTDNA"

        df = pd.read_csv(
            file,
            skiprows=1,
            na_values="--",
            names=["rsid", "chrom", "pos", "genotype"],
            index_col=0,
            dtype={"chrom": object},
        )

        # remove incongruous data
        df = df.drop(df.loc[df["chrom"] == "0"].index)
        df = df.drop(
            df.loc[df.index == "RSID"].index
        )  # second header for concatenated data

        # if second header existed, pos dtype will be object (should be np.int64)
        df["pos"] = df["pos"].astype(np.int64)

        return df, "FTDNA"

    def read_ftdna_famfinder(self, file):
        """ Read and parse Family Tree DNA (FTDNA) "famfinder" file.

        https://www.familytreedna.com

        Parameters
        ----------
        file : str
            path to file

        Returns
        -------
        pandas.DataFrame
            genetic data normalized for use with `snps`
        str
            name of data source
        """

        if self._only_detect_source:
            return pd.DataFrame(), "FTDNA"

        df = pd.read_csv(
            file,
            comment="#",
            na_values="-",
            names=["rsid", "chrom", "pos", "allele1", "allele2"],
            index_col=0,
            dtype={"chrom": object},
        )

        # create genotype column from allele columns
        df["genotype"] = df["allele1"] + df["allele2"]

        # delete allele columns
        # http://stackoverflow.com/a/13485766
        del df["allele1"]
        del df["allele2"]

        return df, "FTDNA"

    def read_ancestry(self, file):
        """ Read and parse Ancestry.com file.

        http://www.ancestry.com

        Parameters
        ----------
        file : str
            path to file

        Returns
        -------
        pandas.DataFrame
            genetic data normalized for use with `snps`
        str
            name of data source
        """

        if self._only_detect_source:
            return pd.DataFrame(), "AncestryDNA"

        df = pd.read_csv(
            file,
            comment="#",
            header=0,
            sep="\t",
            na_values=0,
            names=["rsid", "chrom", "pos", "allele1", "allele2"],
            index_col=0,
            dtype={"chrom": object},
        )

        # create genotype column from allele columns
        df["genotype"] = df["allele1"] + df["allele2"]

        # delete allele columns
        # http://stackoverflow.com/a/13485766
        del df["allele1"]
        del df["allele2"]

        # https://redd.it/5y90un
        df.iloc[np.where(df["chrom"] == "23")[0], 0] = "X"
        df.iloc[np.where(df["chrom"] == "24")[0], 0] = "Y"
        df.iloc[np.where(df["chrom"] == "25")[0], 0] = "PAR"
        df.iloc[np.where(df["chrom"] == "26")[0], 0] = "MT"

        return df, "AncestryDNA"

    def read_myheritage(self, file):
        """ Read and parse MyHeritage file.

        https://www.myheritage.com

        Parameters
        ----------
        file : str
            path to file

        Returns
        -------
        pandas.DataFrame
            genetic data normalized for use with `snps`
        str
            name of data source
        """

        if self._only_detect_source:
            return pd.DataFrame(), "MyHeritage"

        df = pd.read_csv(
            file,
            comment="#",
            header=0,
            na_values="--",
            names=["rsid", "chrom", "pos", "genotype"],
            index_col=0,
            dtype={"chrom": object, "pos": np.int64},
        )

        return df, "MyHeritage"

    def read_livingdna(self, file):
        """ Read and parse LivingDNA file.

        https://livingdna.com/

        Parameters
        ----------
        file : str
            path to file

        Returns
        -------
        pandas.DataFrame
            genetic data normalized for use with `snps`
        str
            name of data source
        """

        if self._only_detect_source:
            return pd.DataFrame(), "LivingDNA"

        df = pd.read_csv(
            file,
            comment="#",
            sep="\t",
            na_values="--",
            names=["rsid", "chrom", "pos", "genotype"],
            index_col=0,
            dtype={"chrom": object},
        )

        return df, "LivingDNA"

    def read_mapmygenome(self, file):
        """ Read and parse Mapmygenome file.

        https://mapmygenome.in

        Parameters
        ----------
        file : str
            path to file

        Returns
        -------
        pandas.DataFrame
            genetic data normalized for use with `snps`
        str
            name of data source
        """

        if self._only_detect_source:
            return pd.DataFrame(), "Mapmygenome"

        df = pd.read_csv(
            file,
            comment="#",
            sep="\t",
            na_values="--",
            header=0,
            index_col=1,
            dtype={"Chr": object},
        )

        df["genotype"] = df["Allele1...Top"] + df["Allele2...Top"]
        df.rename(columns={"Chr": "chrom", "Position": "pos"}, inplace=True)
        df.index.name = "rsid"
        df = df[["chrom", "pos", "genotype"]]

        return df, "Mapmygenome"

    def read_genes_for_good(self, file):
        """ Read and parse Genes For Good file.

        https://genesforgood.sph.umich.edu/readme/readme1.2.txt

        Parameters
        ----------
        file : str
            path to file

        Returns
        -------
        pandas.DataFrame
            genetic data normalized for use with `snps`
        str
            name of data source

        """

        if self._only_detect_source:
            return pd.DataFrame(), "GenesForGood"

        df = pd.read_csv(
            file,
            comment="#",
            sep="\t",
            na_values="--",
            names=["rsid", "chrom", "pos", "genotype"],
            index_col=0,
            dtype={"chrom": object},
        )

        return df, "GenesForGood"

    def read_codigo46(self, data):
        """ Read and parse Codigo46 files.

        https://codigo46.com.mx

        Parameters
        ----------
        data : str
            data string

        Returns
        -------
        pandas.DataFrame
            genetic data normalized for use with `snps`
        str
            name of data source

        """

        if self._only_detect_source:
            return pd.DataFrame(), "Codigo46"

        codigo46_resources = self._resources.get_codigo46_resources()

        df = pd.read_csv(io.StringIO(data), sep="\t", na_values="--")

        def map_codigo_rsids(x):
            return codigo46_resources["rsid_map"].get(x)

        def map_codigo_chr(x):
            chrpos = codigo46_resources["chrpos_map"].get(x)
            return chrpos.split(":")[0] if chrpos else None

        def map_codigo_pos(x):
            chrpos = codigo46_resources["chrpos_map"].get(x)
            return chrpos.split(":")[1] if chrpos else None

        df["rsid"] = df["SNP Name"].apply(map_codigo_rsids)
        df["chrom"] = df["SNP Name"].apply(map_codigo_chr)
        df["pos"] = df["SNP Name"].apply(map_codigo_pos)
        df["genotype"] = df["Allele1 - Plus"] + df["Allele2 - Plus"]

        df = df.astype({"chrom": object, "pos": np.int64})
        df = df[["rsid", "chrom", "pos", "genotype"]]
        df.set_index(["rsid"], inplace=True)

        return df, "Codigo46"

    def read_lineage_csv(self, file, comments):
        """ Read and parse CSV file generated by lineage / snps.

        Parameters
        ----------
        file : str
            path to file
        comments : str
            comments at beginning of file

        Returns
        -------
        pandas.DataFrame
            genetic data normalized for use with `snps`
        str
            name of data source(s)
        """

        source = ""
        for comment in comments.split("\n"):
            if "Source(s):" in comment:
                source = comment.split("Source(s):")[1].strip()
                break

        if self._only_detect_source:
            return pd.DataFrame(), source

        df = pd.read_csv(
            file,
            comment="#",
            header=0,
            na_values="--",
            names=["rsid", "chrom", "pos", "genotype"],
            index_col=0,
            dtype={"chrom": object, "pos": np.int64},
        )

        return df, source

    def read_generic_csv(self, file):
        """ Read and parse generic CSV file.

        Notes
        -----
        Assumes columns are 'rsid', 'chrom' / 'chromosome', 'pos' / 'position', and 'genotype';
        values are comma separated; unreported genotypes are indicated by '--'; and one header row
        precedes data. For example:

            rsid,chromosome,position,genotype
            rs1,1,1,AA
            rs2,1,2,CC
            rs3,1,3,--

        Parameters
        ----------
        file : str
            path to file

        Returns
        -------
        pandas.DataFrame
            genetic data normalized for use with `snps`
        str
            name of data source
        """

        if self._only_detect_source:
            return pd.DataFrame(), "generic"

        df = pd.read_csv(
            file,
            skiprows=1,
            na_values="--",
            names=["rsid", "chrom", "pos", "genotype"],
            index_col=0,
            dtype={"chrom": object, "pos": np.int64},
        )

        return df, "generic"

    def read_vcf(self, file):
        """ Read and parse VCF file.

        Notes
        -----
        This function uses the PyVCF python module to parse the genotypes from VCF files:
        https://pyvcf.readthedocs.io/en/latest/index.html


        Parameters
        ----------
        file : str
            path to file

        Returns
        -------
        pandas.DataFrame
            genetic data normalized for use with `snps`
        str
            name of data source
        """

        if self._only_detect_source:
            return pd.DataFrame(), "vcf"

        df = pd.DataFrame(columns=["rsid", "chrom", "pos", "genotype"])
        df = df.astype(
            {"rsid": object, "chrom": object, "pos": np.int64, "genotype": object}
        )

        with open(file, "r") as f:
            vcf_reader = vcf.Reader(f)

            # snps does not yet support multi-sample vcf.
            if len(vcf_reader.samples) > 1:
                print(
                    "Multiple samples detected in the vcf file, please use a single sample vcf."
                )
                return df, "vcf"

            for i, record in enumerate(vcf_reader):
                # assign null genotypes if either allele is None
                # Could capture full genotype, if REF is None, but genotype is 1/1 or
                # if ALT is None, but genotype is 0/0
                if record.REF is None or record.ALT[0] is None:
                    genotype = np.nan
                # skip SNPs with missing rsIDs.
                elif record.ID is None:
                    continue
                # skip insertions and deletions
                elif len(record.REF) > 1 or len(record.ALT[0]) > 1:
                    continue
                else:
                    alleles = record.genotype(vcf_reader.samples[0]).gt_bases
                    a1 = alleles[0]
                    a2 = alleles[-1]
                    genotype = "{}{}".format(a1, a2)

                record_info = {
                    "rsid": record.ID,
                    "chrom": "{}".format(record.CHROM).strip("chr"),
                    "pos": record.POS,
                    "genotype": genotype,
                }
                # append the record to the DataFrame
                df = df.append(
                    pd.DataFrame([record_info]), ignore_index=True, sort=False
                )

        df.set_index("rsid", inplace=True, drop=True)

        return df, "vcf"


class Writer:
    """ Class for writing SNPs to files. """

    def __init__(self, snps=None, filename="", vcf=False, atomic=True, **kwargs):
        """ Initialize a `Writer`.

        Parameters
        ----------
        snps : SNPs
            SNPs to save to file or write to buffer
        filename : str or buffer
            filename for file to save or buffer to write to
        vcf : bool
            flag to save file as VCF
        atomic : bool
            atomically write output to a file on local filesystem
        **kwargs
            additional parameters to `pandas.DataFrame.to_csv`
        """
        self._snps = snps
        self._filename = filename
        self._vcf = vcf
        self._atomic = atomic
        self._kwargs = kwargs

    def __call__(self):
        if self._vcf:
            return self._write_vcf()
        else:
            return self._write_csv()

    @classmethod
    def write_file(cls, snps=None, filename="", vcf=False, atomic=True, **kwargs):
        """ Save SNPs to file.

        Parameters
        ----------
        snps : SNPs
            SNPs to save to file or write to buffer
        filename : str or buffer
            filename for file to save or buffer to write to
        vcf : bool
            flag to save file as VCF
        atomic : bool
            atomically write output to a file on local filesystem
        **kwargs
            additional parameters to `pandas.DataFrame.to_csv`

        Returns
        -------
        str
            path to file in output directory if SNPs were saved, else empty str
        """
        w = cls(snps=snps, filename=filename, vcf=vcf, atomic=atomic, **kwargs)
        return w()

    def _write_csv(self):
        """ Write SNPs to a CSV file.

        Returns
        -------
        str
            path to file in output directory if SNPs were saved, else empty str
        """
        filename = self._filename
        if not filename:
            filename = "{}_{}{}".format(
                clean_str(self._snps._source), self._snps.assembly, ".csv"
            )

        comment = (
            "# Source(s): {}\n"
            "# Assembly: {}\n"
            "# SNPs: {}\n"
            "# Chromosomes: {}\n".format(
                self._snps.source,
                self._snps.assembly,
                self._snps.snp_count,
                self._snps.chromosomes_summary,
            )
        )
        if "header" in self._kwargs:
            if isinstance(self._kwargs["header"], bool):
                if self._kwargs["header"]:
                    self._kwargs["header"] = ["chromosome", "position", "genotype"]
        else:
            self._kwargs["header"] = ["chromosome", "position", "genotype"]

        return save_df_as_csv(
            self._snps._snps,
            self._snps._output_dir,
            filename,
            comment=comment,
            atomic=self._atomic,
            **self._kwargs
        )

    def _write_vcf(self):
        """ Write SNPs to a VCF file.

        References
        ----------
        .. [1] The Variant Call Format (VCF) Version 4.2 Specification, 8 Mar 2019,
           https://samtools.github.io/hts-specs/VCFv4.2.pdf

        Returns
        -------
        str
            path to file in output directory if SNPs were saved, else empty str
        """
        filename = self._filename
        if not filename:
            filename = "{}_{}{}".format(
                clean_str(self._snps._source), self._snps.assembly, ".vcf"
            )

        comment = (
            "##fileformat=VCFv4.2\n"
            "##fileDate={}\n"
            '##source="{}; snps v{}; https://pypi.org/project/snps/"\n'.format(
                datetime.datetime.utcnow().strftime("%Y%m%d"),
                self._snps._source,
                snps.__version__,
            )
        )

        reference_sequence_chroms = (
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "10",
            "11",
            "12",
            "13",
            "14",
            "15",
            "16",
            "17",
            "18",
            "19",
            "20",
            "21",
            "22",
            "X",
            "Y",
            "MT",
        )

        df = self._snps.snps

        tasks = []

        # skip insertions and deletions
        df = df.drop(
            df.loc[
                df["genotype"].notnull()
                & (
                    (df["genotype"].str[0] == "I")
                    | (df["genotype"].str[0] == "D")
                    | (df["genotype"].str[1] == "I")
                    | (df["genotype"].str[1] == "D")
                )
            ].index
        )

        chroms_to_drop = []
        for chrom in df["chrom"].unique():
            if chrom not in reference_sequence_chroms:
                chroms_to_drop.append(chrom)
                continue

            tasks.append(
                {
                    "resources": self._snps._resources,
                    "assembly": self._snps.assembly,
                    "chrom": chrom,
                    "snps": pd.DataFrame(df.loc[(df["chrom"] == chrom)]),
                }
            )

        # drop chromosomes without reference sequence data (e.g., unassigned PAR)
        for chrom in chroms_to_drop:
            df = df.drop(df.loc[df["chrom"] == chrom].index)

        # create the VCF representation for SNPs
        results = map(self._create_vcf_representation, tasks)

        contigs = []
        vcf = []
        for result in list(results):
            contigs.append(result["contig"])
            vcf.append(result["vcf"])

        vcf = pd.concat(vcf)

        comment += "".join(contigs)
        comment += '##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">\n'
        comment += "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tSAMPLE\n"

        return save_df_as_csv(
            vcf,
            self._snps._output_dir,
            filename,
            comment=comment,
            prepend_info=False,
            header=False,
            index=False,
            na_rep=".",
            sep="\t",
        )

    def _create_vcf_representation(self, task):
        resources = task["resources"]
        assembly = task["assembly"]
        chrom = task["chrom"]
        snps = task["snps"]

        if len(snps.loc[snps["genotype"].notnull()]) == 0:
            return {"contig": "", "vcf": pd.DataFrame()}

        seqs = resources.get_reference_sequences(assembly, [chrom])
        seq = seqs[chrom]

        contig = '##contig=<ID={},URL={},length={},assembly={},md5={},species="{}">\n'.format(
            seq.ID, seq.url, seq.length, seq.build, seq.md5, seq.species
        )

        snps = snps.reset_index()

        df = pd.DataFrame(
            columns=[
                "CHROM",
                "POS",
                "ID",
                "REF",
                "ALT",
                "QUAL",
                "FILTER",
                "INFO",
                "FORMAT",
                "SAMPLE",
            ]
        )
        df = df.astype(
            {
                "CHROM": object,
                "POS": np.int64,
                "ID": object,
                "REF": object,
                "ALT": object,
                "QUAL": np.int64,
                "FILTER": object,
                "INFO": object,
                "FORMAT": object,
                "SAMPLE": object,
            }
        )

        df["CHROM"] = snps["chrom"]
        df["POS"] = snps["pos"]
        df["ID"] = snps["rsid"]

        # https://stackoverflow.com/a/24838429
        df["REF"] = list(map(chr, seq.sequence[snps.pos - seq.start]))

        df["FORMAT"] = "GT"

        seq.clear()

        df["genotype"] = snps["genotype"]

        temp = df.loc[df["genotype"].notnull()]

        # https://stackoverflow.com/a/19976286
        df.loc[df["genotype"].notnull(), "ALT"] = np.vectorize(self._compute_alt)(
            temp["REF"], temp["genotype"]
        )

        temp = df.loc[df["genotype"].notnull()]

        df.loc[df["genotype"].notnull(), "SAMPLE"] = np.vectorize(
            self._compute_genotype
        )(temp["REF"], temp["ALT"], temp["genotype"])

        df.loc[df["SAMPLE"].isnull(), "SAMPLE"] = "./."

        del df["genotype"]

        return {"contig": contig, "vcf": df}

    def _compute_alt(self, ref, genotype):
        genotype_alleles = list(set(genotype))

        if ref in genotype_alleles:
            if len(genotype_alleles) == 1:
                return "N"
            else:
                genotype_alleles.remove(ref)
                return genotype_alleles.pop(0)
        else:
            return ",".join(genotype_alleles)

    def _compute_genotype(self, ref, alt, genotype):
        alleles = [ref]

        if pd.notna(alt):
            alleles.extend(alt.split(","))

        if len(genotype) == 2:
            return "{}/{}".format(
                alleles.index(genotype[0]), alleles.index(genotype[1])
            )
        else:
            return "{}".format(alleles.index(genotype[0]))
