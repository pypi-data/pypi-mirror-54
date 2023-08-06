"""CLI for linked read related stuff."""

import click
import pandas as pd
from Bio import SeqIO
from os.path import basename

from .assign_contigs import (
    assign_contigs,
    compress_assigned_contigs,
    condense_winner_takes_all,
)
from .filter_process import (
    filter_homologous,
    rpkm_from_bams,
    crunch_alignment,
)


@click.group()
def assembly():
    """Utilities for linked reads."""
    pass


@assembly.command('crunch-genomecov')
@click.option('-s', '--sample-delim', default=None)
@click.option('-g', '--genome-delim', default='::')
@click.option('-o', '--outfile', type=click.File('w'), default='-')
@click.argument('genomecovs', type=click.File('r'), nargs=-1)
def cli_crunch_genomecov(sample_delim, genome_delim, outfile, genomecovs):
    """Reduce a bedtools genomecov file to fraction of a genome covered."""
    tbl = {}
    with click.progressbar(genomecovs) as gcs:
        for genomecov in gcs:
            sample_name = basename(genomecov.name).split(sample_delim)[0]
            tbl[sample_name] = {}
            for line in genomecov:
                tkns = line.strip().split()
                genome_name = tkns[0].split(genome_delim)[0]
                if genome_name not in tbl[sample_name]:
                    tbl[sample_name][genome_name] = [0, 0]
                depth, num_bases, total_bases = int(tkns[1]), int(tkns[2]), int(tkns[3])
                if depth > 0:
                    continue
                tbl[sample_name][genome_name][0] += total_bases - num_bases  # num covered bases
                tbl[sample_name][genome_name][1] += total_bases
            tbl[sample_name] = {
                genome_name: num / den
                for genome_name, (num, den) in tbl[sample_name].items()
                if den > 0
            }
        tbl = pd.DataFrame.from_dict(tbl, orient='columns')
        tbl.to_csv(outfile)


@assembly.command('crunch-samtools-depth')
@click.option('-d', '--delim', default=None)
@click.option('-o', '--outfile', type=click.File('w'), default='-')
@click.argument('samdepths', type=click.File('r'), nargs=-1)
def cli_crunch_genomecov(delim, outfile, samdepths):
    """Reduce a bedtools genomecov file to fraction of a genome covered."""
    tbl = {}
    with click.progressbar(samdepths) as sds:
        for samdepth in sds:
            sample_name = basename(samdepth.name).split(delim)[0]
            genome_name = basename(samdepth.name).split(delim)[1]
            tbl[sample_name] = {}
            total_bases, covered_bases = 1, 0
            for line in samdepth:
                tkns = line.strip().split()
                position, depth = int(tkns[1]), int(tkns[2])
                total_bases += 1
                if depth > 0:
                    covered_bases += 1
            tbl[sample_name][genome_name] = covered_bases / total_bases
    tbl = pd.DataFrame.from_dict(tbl, orient='columns')
    tbl.to_csv(outfile)


@assembly.command('group-contigs')
@click.option('-s', '--sep', default='\t')
@click.option('-d', '--delim', default='_')
@click.argument('group_file', type=click.File('r'))
@click.argument('fasta_file')
def cli_group_contigs(sep, delim, group_file, fasta_file):
    """Split a fasta file based on a grouping file."""
    groups = {
        tkns[0]: tkns[1]
        for tkns in (line.strip().split(sep) for line in group_file)
    }
    recs = {}
    for rec in SeqIO.parse(fasta_file, 'fasta'):
        if rec.id not in groups:
            continue
        group = groups[rec.id]
        recs[group] = recs.get(group, []) + [rec]

    for group_name, group_recs in recs.items():
        fasta_name = delim.join(group_name.split()) + '.fasta'
        with open(fasta_name, "w") as output_handle:
            SeqIO.write(group_recs, output_handle, "fasta")


@assembly.command('id-contigs')
@click.option('-s', '--sep', default='\t')
@click.option('-g', '--genbank-id-map', default=None)
@click.option('-f', '--seq-fasta', default=None, type=click.File('r'))
@click.option('--min-homology', default=95.0, type=float)
@click.option('--min-alignment-len', default=1000, type=int)
@click.argument('m8file', type=click.File('r'))
@click.argument('outfile', type=click.File('w'))
def cli_id_contigs(
        sep, genbank_id_map, seq_fasta, min_homology, min_alignment_len,
        m8file, outfile):
    """ID contigs based on the species that have the most homology to each."""
    click.echo('Identifying Contigs')
    tbl = assign_contigs(
        m8file,
        genfile=genbank_id_map,
        seqfile=seq_fasta,
        min_homology=min_homology,
        min_len=min_alignment_len,
    )
    tbl.to_csv(outfile, sep=sep)


@assembly.command('condense-ids')
@click.option('-w/-r', '--winner-takes-all/--report-all', default=False)
@click.option('-s', '--sep', default='\t')
@click.option('-r', '--rank', default=None, help='Taxonomic rank for grouping')
@click.option('--min-cov', default=0.9)
@click.option('--max-cov', default=1.0)
@click.argument('assignment_file', type=click.File('r'))
@click.argument('outfile', type=click.File('w'))
def cli_condense_ids(winner_takes_all, sep, rank, min_cov, max_cov, assignment_file, outfile):
    """ID contigs based on the species that have the most homology to each."""
    tbl = pd.read_csv(assignment_file, sep=sep, index_col=0)
    tbl = compress_assigned_contigs(tbl, rank=rank, min_cov=min_cov, max_cov=max_cov)
    if winner_takes_all:
        tbl = condense_winner_takes_all(tbl, rank)
    tbl.to_csv(outfile, sep=sep)


@assembly.command('crunch-queries')
@click.option('-s', '--sep', default='\t', help='Separation character in tables')
@click.option('-d', '--delim', default='.', help='Delimiter for sample names in queries')
@click.option('-r', '--rank', default='taxon', help='Taxonomic rank for grouping')
@click.option('-u/-a', '--allow-unassigned/--assigned-only', default=True)
@click.argument('m8file', type=click.File('r'))
@click.argument('assignment_file', type=click.File('r'))
@click.argument('outfile', type=click.File('w'))
def cli_crunch_queries(sep, delim, rank, allow_unassigned, m8file, assignment_file, outfile):
    """Map a set of queries aligned to a set of contigs to their taxonomic ids."""
    taxaids = pd.read_csv(assignment_file, sep=sep, index_col=0)
    tbl = crunch_alignment(
        m8file, taxaids,
        rank=rank, query_delim=delim, allow_unassigned=allow_unassigned
    )
    tbl.fillna(0).to_csv(outfile, sep=sep)


@assembly.command('cat-fastas')
@click.option('-d', '--delim', default='::')
@click.option('-l', '--min-len', default=1000, type=int)
@click.argument('outfile', type=click.File('w'))
@click.argument('fasta_files', type=click.File('r'), nargs=-1)
def cli_cat_fastas(delim, min_len, outfile, fasta_files):
    """Concatenate fastas, adding filenames to ids.

    For convenience also filter by length.
    """
    def seq_gen():
        for fasta_file in fasta_files:
            for rec in SeqIO.parse(fasta_file, 'fasta'):
                if len(rec.seq) < min_len:
                    continue
                rec.id = f'{fasta_file.name}{delim}{rec.id}'
                yield rec

    SeqIO.write(seq_gen(), outfile, 'fasta')


@assembly.command('filter-homologous')
@click.option('-p', '--min-perc-id', default=0.95)
@click.option('-l', '--min-len-frac', default=0.8)
@click.option('-g', '--group-file', default=None)
@click.argument('outfile', type=click.File('w'))
@click.argument('m8file', type=click.File('r'))
@click.argument('fasta_file', type=click.File('r'))
def cli_filter_homologous(min_perc_id, min_len_frac, group_file, outfile, m8file, fasta_file):
    """Filter contigs that are homologous to one another keeping the largest.

    Find connected components in the m8 file (presumed to be an
    autologous alignment). Edges exist between contigs where
    an alignment is:
    1) Greater than <min_perc_id> similar
    2) Longer than <min_len_frac> * min(len(c1), len(c2))
    For each component take the longest contig and write it to a fasta.
    """
    SeqIO.write(
        filter_homologous(
            m8file, fasta_file,
            group_filename=group_file, min_perc_id=min_perc_id, min_len_frac=min_len_frac
        ),
        outfile,
        'fasta'
    )


@assembly.command('rpkm-from-bams')
@click.option('-s', '--sep', default='\t')
@click.option('-d', '--delim', default=None)
@click.option(
    '-g', '--groups',
    type=click.File('r'), default=None, help='Two column file mapping contigs to groups.')
@click.argument('outfile', type=click.File('w'))
@click.argument('fasta', type=click.File('r'))
@click.argument('bams', type=click.Path(exists=True), nargs=-1)
def cli_rpkm_from_bams(sep, delim, groups, outfile, fasta, bams):
    """Create a table of RPKMS from bam files.

    Assumes bam files have alignment records for each read.
    Only takes primary alignment.
    """
    if '.bam' in fasta.name:
        click.echo(f'Fasta file {fasta.name} contains ".bam", missing output argument?', err=True)
        return
    if groups:
        groups = {
            tkns[0]: tkns[1]
            for tkns in (line.strip().split(sep) for line in groups)
        }
    else:
        groups = {}
    bams = {basename(bam).split(delim)[0]: bam for bam in bams}
    rpkms = rpkm_from_bams(bams, fasta, groups=groups)
    rpkms.to_csv(outfile, sep=sep)
