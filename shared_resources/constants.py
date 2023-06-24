from types import SimpleNamespace

CHROMOSOMES = [*range(1,22)] + ['X', 'Y', 'N']
DATASET_TYPES = ["GWAS_sumstats", "QTL_sumstats"]
GENOME_BUILDS = ["GRCh37", "GRCh38"]

ADSP_VARIANTS_ACCESSION = "NG00067"

__urls = ({
        'pubmed': 'https://pubmed.ncbi.nlm.nih.gov', 
        'niagads': 'https://www.niagads.org', 
        'filer': 'https://tf.lisanwanglab.org/FILER',
        'gadb_metadata': 'https://tf.lisanwanglab.org/GADB/metadata'
})

URLS = SimpleNamespace(**__urls)