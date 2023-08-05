
import os


def sra_id2geo_id(sra_ids):
    """Query SRA ID from GEO ID"""
    import subprocess

    cmd = "esearch -db sra -query {}"
    cmd += " | efetch -format docsum"
    cmd += " | xtract -pattern DocumentSummary -element Runs"
    cmd += """ |  perl -ne '@mt = ($_ =~ /SRR\\d+/g); print "@mt"'"""

    geo_ids = list()
    for id_ in sra_ids:
        geo_ids.append(subprocess.call(cmd.format(id_).split(" ")).read())
    return


def sra2fastq(input_sra, output_dir):
    cmd = """
\t\tfastq-dump --split-3 --outdir {} {}
    """.format(
        output_dir, input_sra
    )

    return cmd


def fastq2bam(input_fastq, output_bam, sample_name, input_fastq2=None):
    cmd = """
\t\tjava -Xmx4g -jar /cm/shared/apps/picard-tools/1.118/FastqToSam.jar"""
    cmd += " FASTQ={0}".format(input_fastq)
    cmd += " SAMPLE_NAME={0}".format(sample_name)
    if input_fastq2 is not None:
        cmd += " FASTQ2={0}".format(input_fastq2)
    cmd += """ OUTPUT={0}""".format(output_bam)

    return cmd


def download_cram(link, output_dir):
    cmd = """
    cd {}
    wget '{}'
    cd -
    """.format(
        output_dir, link
    )

    return cmd


def cram2bam(input_cram, output_bam):
    cmd = """
    samtools view -b -o {} {}
    """.format(
        output_bam, input_cram
    )

    return cmd


def download_sra(link, output_dir):
    cmd = """
    cd {}
    wget '{}'
    cd -
    """.format(
        output_dir, link
    )

    return cmd


def sra2bam_job(sra_id, base_path):
    import textwrap

    from pypiper import NGSTk

    tk = NGSTk()

    # Slurm header
    job_file = os.path.join(base_path, "%s_sra2bam.sh" % sra_id)
    log_file = os.path.join(base_path, "%s_sra2bam.log" % sra_id)

    cmd = tk.slurm_header("-".join(["sra2bam", sra_id]), log_file, cpus_per_task=2)

    # SRA to FASTQ
    cmd += sra2fastq(os.path.join(base_path, sra_id + ".sra"), base_path)

    # FASTQ to BAM
    cmd += fastq2bam(
        os.path.join(base_path, sra_id + "_1.fastq"),
        os.path.join(base_path, sra_id + ".bam"),
        sra_id,
        os.path.join(base_path, sra_id + "_2.fastq"),
    )

    # Slurm footer
    cmd += tk.slurm_footer() + "\n"

    # Write job to file

    with open(job_file, "w") as handle:
        handle.write(textwrap.dedent(cmd))

    # Submit
    tk.slurm_submit_job(job_file)


def link2bam_job(sample_name, link, base_path):
    import textwrap

    from pypiper import NGSTk

    tk = NGSTk()

    # Slurm header
    job_file = os.path.join(base_path, "%s_link2bam.sh" % sample_name)
    log_file = os.path.join(base_path, "%s_link2bam.log" % sample_name)

    cmd = tk.slurm_header(
        "-".join(["link2bam", sample_name]), log_file, cpus_per_task=2
    )

    # Download CRAM
    cmd += download_cram(link, base_path)

    # CRAM to BAM
    cmd += cram2bam(
        os.path.join(base_path, sample_name + ".cram"),
        os.path.join(base_path, sample_name + ".bam"),
    )

    # Slurm footer
    cmd += tk.slurm_footer() + "\n"

    # Write job to file

    with open(job_file, "w") as handle:
        handle.write(textwrap.dedent(cmd))

    # Submit
    tk.slurm_submit_job(job_file)


def sralink2bam_job(sra_id, base_path):
    import textwrap

    from pypiper import NGSTk
    from ngs_toolkit import _LOGGER

    tk = NGSTk()

    # Slurm header
    job_file = os.path.join(base_path, "%s_sra2bam.sh" % sra_id)
    log_file = os.path.join(base_path, "%s_sra2bam.log" % sra_id)

    cmd = tk.slurm_header("-".join(["sra2bam", sra_id]), log_file, cpus_per_task=2)

    # SRA to FASTQ
    cmd += sra2fastq(sra_id, base_path)

    # FASTQ to BAM
    cmd += fastq2bam(
        os.path.join(base_path, sra_id + "_1.fastq"),
        os.path.join(base_path, sra_id + ".bam"),
        sra_id,
        os.path.join(base_path, sra_id + "_2.fastq"),
    )

    # Slurm footer
    cmd += tk.slurm_footer() + "\n"

    # Write job to file

    with open(job_file, "w") as handle:
        handle.write(textwrap.dedent(cmd))

    # Submit
    tk.slurm_submit_job(job_file)
    _LOGGER.info(job_file)


def series_matrix2csv(matrix_url, prefix=None):
    """
    matrix_url: gziped URL with GEO series matrix.
    """
    import pandas as pd
    import gzip
    import subprocess

    subprocess.call("wget {}".format(matrix_url).split(" "))
    filename = matrix_url.split("/")[-1]

    with gzip.open(filename, "rb") as f:
        file_content = f.read()

    # separate lines with only one field (project-related)
    # from lines with >2 fields (sample-related)
    prj_lines = dict()
    sample_lines = dict()

    for line in file_content.decode("utf-8").strip().split("\n"):
        line = line.strip().split("\t")
        if len(line) == 2:
            prj_lines[line[0].replace('"', "")] = line[1].replace('"', "")
        elif len(line) > 2:
            sample_lines[line[0].replace('"', "")] = [
                x.replace('"', "") for x in line[1:]
            ]

    prj = pd.Series(prj_lines)
    prj.index = prj.index.str.replace("!Series_", "")

    samples = pd.DataFrame(sample_lines)
    samples.columns = samples.columns.str.replace("!Sample_", "")

    if prefix is not None:
        prj.to_csv(os.path.join(prefix + ".project_annotation.csv"), index=True)
        samples.to_csv(os.path.join(prefix + ".sample_annotation.csv"), index=False)

    return prj, samples


# old testing suite


import os
import string

from ngs_toolkit.general import query_biomart
from ngs_toolkit.utils import location_index_to_bed
from ngs_toolkit.project_manager import create_project
import numpy as np
import pandas as pd
import patsy
import pybedtools
import yaml


class RandomDataGenerator(object):
    def generate_random_data(
        self,
        n_factors=2,
        n_variables=20000,
        n_replicates=5,
        distribution="negative_binomial",
        group_fold_differences=5,
        fraction_of_different=0.2,
        data_type="ATAC-seq",
        genome_assembly="hg19",
    ):
        if not isinstance(group_fold_differences, list):
            # _LOGGER.warning("Assuming same fold difference for all factors between samples")
            group_fold_differences = [group_fold_differences] * n_factors

        n_samples = n_factors * n_replicates
        s = list((string.ascii_lowercase[15:] * n_variables)[:n_variables])
        s = [i + str(j) for i, j in zip(s, list(range(n_variables)))]
        d = patsy.demo_data(
            *(list(string.ascii_lowercase[:n_factors]) + s),
            nlevels=2,
            min_rows=n_samples
        )
        d = pd.DataFrame(d)
        dcat = d.loc[:, d.dtypes != np.float]
        dnum = d.loc[:, d.dtypes == np.float]

        # add sample names
        names = ["S{}_{}".format(i + 1, dcat.loc[i, :].sum()) for i in dcat.index]
        dcat.index = dnum.index = names
        dcat.index.name = dnum.index.name = "sample_name"

        # add variation to groups
        for i, factor in enumerate(dcat.columns):
            af = dnum.columns.to_series().sample(frac=fraction_of_different).tolist()
            levels = dcat.loc[:, factor].unique()

            if len(levels) == 2:
                for level, f in zip(levels, [1, -1]):
                    diff = (
                        dnum.loc[:, af].mean(axis=0)
                        * (group_fold_differences[i] / 2)
                        * f
                    )  # * np.absolute(np.random.normal(0, 0.1)))
                    dnum.loc[
                        dcat.loc[:, factor] == level, dnum.columns.isin(af)
                    ] += diff
            else:
                raise NotImplementedError

        # add intersect from distribution
        dist = getattr(np.random, distribution)
        dnum = dnum + dist(1, 0.1, n_variables)

        # add overdispersion across all features
        mean = dnum.mean(axis=0)
        space = np.linspace(mean.max(), mean.min(), 100)
        step = space[0] - space[1]
        for i, lim in enumerate(space):
            cur = mean[(mean <= lim + step) & (mean > lim)].index
            dnum.loc[:, cur] *= np.random.normal(0, i + 1, len(cur))

        # make non-negative
        if dnum.min().min() < 0:
            dnum -= dnum.min().min()

        # make integer
        dnum = dnum.astype(int)

        # add random location indexes
        if data_type in ["ATAC-seq", "ChIP-seq"]:
            dnum.columns = self.get_random_genomic_locations(
                n_variables, genome_assembly=genome_assembly
            )
        if data_type in ["RNA-seq"]:
            dnum.columns = self.get_random_genes(
                n_variables, genome_assembly=genome_assembly
            )
        if data_type in ["CNV"]:
            from ngs_toolkit.utils import z_score

            dnum.columns = self.get_genomic_bins(
                n_variables, genome_assembly=genome_assembly
            )
            dnum = z_score(dnum)

        return dnum.T, dcat

    @staticmethod
    def get_random_genomic_locations(
        size, width_mean=500, width_std=400, min_width=300, genome_assembly="hg19"
    ):
        from ngs_toolkit.utils import bed_to_index

        chrom = ["chr1"] * size
        start = np.array([0] * size)
        end = np.absolute(np.random.normal(width_mean, width_std, size)).astype(int)
        df = pd.DataFrame([chrom, start.tolist(), end.tolist()]).T
        df.loc[(df[2] - df[1]) < min_width, 2] += min_width
        bed = (
            pybedtools.BedTool.from_dataframe(df)
            .shuffle(genome=genome_assembly)
            .sort()
            .to_dataframe()
        )
        return bed_to_index(bed)

    @staticmethod
    def get_random_genes(size, genome_assembly="hg19"):
        m = {"hg19": "grch37", "hg38": "grch38", "mm10": "grcm38"}
        o = {"hg19": "hsapiens", "hg38": "hsapiens", "mm10": "mmusculus"}

        g = (
            query_biomart(
                attributes=["external_gene_name"],
                ensembl_version=m[genome_assembly],
                species=o[genome_assembly],
            )
            .squeeze()
            .drop_duplicates()
        )
        return pd.Series(np.random.choice(g, size, replace=False)).sort_values()

    @staticmethod
    def get_genomic_bins(n_bins, distribution="normal", genome_assembly="hg19"):
        from ngs_toolkit.utils import bed_to_index

        bed = pybedtools.BedTool.from_dataframe(
            pd.DataFrame(dict(pybedtools.chromsizes(genome_assembly))).T.reset_index()
        )
        w = bed.makewindows(
            genome=genome_assembly, w=sum([i.length for i in bed]) / n_bins
        ).to_dataframe()
        return bed_to_index(w.head(n_bins))


def generate_project(
    output_dir="tests",
    project_name="test_project",
    organism="human",
    genome_assembly="hg19",
    data_type="ATAC-seq",
    only_metadata=False,
    sample_input_files=False,
    **kwargs
):
    output_dir = os.path.abspath(output_dir)

    # Create project with projectmanager
    create_project(
        project_name,
        genome_assemblies={organism: genome_assembly},
        overwrite=True,
        root_projects_dir=output_dir,
        git=False
    )

    # Generate random data
    g = RandomDataGenerator()
    n, c = g.generate_random_data(
        genome_assembly=genome_assembly, data_type=data_type, **kwargs
    )

    # add additional sample info
    c["protocol"] = data_type
    c["organism"] = organism
    # now save it
    c.to_csv(os.path.join(output_dir, project_name, "metadata", "annotation.csv"))

    # Make comparison table
    if "n_factors" in kwargs:
        table_file = os.path.join(
            output_dir, project_name, "metadata", "comparison_table.csv"
        )
        ct = pd.DataFrame()
        for factor in list(string.ascii_lowercase[: kwargs["n_factors"]]):
            for side, f in [(1, "2"), (0, "1")]:
                ct2 = c.loc[c[factor] == factor + f].index.to_frame()
                ct2["comparison_side"] = side
                ct2["comparison_name"] = "Factor_" + factor + "_" + "2vs1"
                ct2["sample_group"] = "Factor_" + factor + f
                ct = ct.append(ct2)
        ct["comparison_type"] = "differential"
        ct["data_type"] = data_type
        ct["comparison_genome"] = genome_assembly
        ct.to_csv(table_file, index=False)

    # add the sample_attributes and group_attributes depending on the number of factors
    if "n_factors" in kwargs:
        config_file = os.path.join(
            output_dir, project_name, "metadata", "project_config.yaml"
        )
        config = yaml.safe_load(open(config_file, "r"))
        factors = list(string.ascii_lowercase[: kwargs["n_factors"]])
        config["sample_attributes"] = ["sample_name"] + factors
        config["group_attributes"] = factors
        config["metadata"]["comparison_table"] = table_file
        yaml.safe_dump(config, open(config_file, "w"))

    # prepare dirs
    dirs = [os.path.join(output_dir, project_name, "results")]
    for d in dirs:
        if not os.path.exists(d):
            os.makedirs(d)

    if not only_metadata:
        if data_type == "ATAC-seq":
            bed = location_index_to_bed(n.index)
            bed.to_csv(
                os.path.join(
                    output_dir, project_name, "results", project_name + ".peak_set.bed"
                ),
                index=False,
                sep="\t",
                header=False,
            )
        n.to_csv(
            os.path.join(
                output_dir, project_name, "results", project_name + ".matrix_raw.csv"
            )
        )


def generate_bam_file(peak_set, output_bam, genome_assembly="hg38", chrom_sizes_file=None, index=True):
    import tempfile
    if not isinstance(peak_set, pybedtools.BedTool):
        peak_set = pybedtools.BedTool(peak_set)

    s = peak_set.to_dataframe()

    # choose a random number of reads per region
    r = np.random.negative_binomial(1000, 0.99, s.shape[0])
    i = [i for i in r for _ in range(i)]
    s = s.reindex(i)

    # shorten/enlarge by a random fraction; name reads
    d = s['end'] - s['start']
    s = s.assign(
        start=(s['start'] + d * np.random.uniform(-0.2, 0.2, s.shape[0])).astype(int),
        end=(s['end'] + d * np.random.uniform(-0.2, 0.2, s.shape[0])).astype(int),
        name=["read_{}".format(i) for i in range(s.shape[0])])

    s = pybedtools.BedTool.from_dataframe(s)
    s = s.truncate_to_chrom(genome=genome_assembly)
    s = s.sort()
    # get a file with chromosome sizes (usually not needed but only for bedToBam)
    if chrom_sizes_file is None:
        chrom_sizes_file = tempfile.NamedTemporaryFile().name
        pybedtools.get_chromsizes_from_ucsc(genome=genome_assembly, saveas=chrom_sizes_file)
    b = s.to_bam(g=chrom_sizes_file)

    b.saveas(output_bam)

    if index:
        import pysam
        pysam.index(output_bam)


def generate_peak_file(peak_set, output_peak, genome_assembly="hg38", summits=False):
    if not isinstance(peak_set, pybedtools.BedTool):
        peak_set = pybedtools.BedTool(peak_set)

    s = peak_set.to_dataframe()

    # choose a random fraction of sites to keep
    s = pybedtools.BedTool.from_dataframe(
            s.sample(frac=np.random.uniform()))
    # shorten/enlarge sites by a random fraction
    s = s.slop(
        l=np.random.uniform(-0.2, 0.2),
        r=np.random.uniform(-0.2, 0.2),
        pct=True, genome=genome_assembly)

    if summits:
        # get middle basepair
        s = s.to_dataframe()
        mid = ((s['end'] - s['start']) / 2).astype(int)
        s.loc[:, 'start'] += mid
        s.loc[:, 'end'] -= (mid - 1)
        s = pybedtools.BedTool.from_dataframe(s)

    s = s.sort()
    s.saveas(output_peak)


def generate_sample_input_files(analysis):
    import tempfile

    chrom_sizes_file = tempfile.NamedTemporaryFile().name
    pybedtools.get_chromsizes_from_ucsc(genome=analysis.genome, saveas=chrom_sizes_file)

    for sample in analysis.samples:
        if hasattr(sample, "aligned_filtered_bam"):
            if sample.aligned_filtered_bam is not None:
                d = os.path.dirname(sample.aligned_filtered_bam)
                if not os.path.exists(d):
                    os.makedirs(d)
                generate_bam_file(
                    analysis.sites, sample.aligned_filtered_bam,
                    genome_assembly=analysis.genome,
                    chrom_sizes_file=chrom_sizes_file)
        if hasattr(sample, "peaks"):
            if sample.peaks is not None:
                d = os.path.dirname(sample.peaks)
                if not os.path.exists(d):
                    os.makedirs(d)
                generate_peak_file(
                    analysis.sites, sample.peaks, summits=False,
                    genome_assembly=analysis.genome)
        if hasattr(sample, "summits"):
            if sample.summits is not None:
                d = os.path.dirname(sample.summits)
                if not os.path.exists(d):
                    os.makedirs(d)
                generate_peak_file(
                    analysis.sites, sample.summits, summits=True,
                    genome_assembly=analysis.genome)
