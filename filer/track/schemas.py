from flask_restx import fields
from shared_resources.fields import GenomeBuild

example = {
    # "Identifier": "NGDS000989",
    # "Data Source": "DASHR2",
    "File name": "BJ_SRR446315_peaks_annot_hg19.bed.gz",
    "Number of intervals": 1141,
    "bp covered": 27613,
    "Output type": "annotated peaks",
    # Genome build": "hg19",
    "cell type": "BJ",
    "Biosample type": "Cell line",
    "Biosamples term id": "Not applicable",
    "Tissue category": "Connective Tissue",
    "ENCODE Experiment id": "Not applicable",
    "Biological replicate(s)": "Not applicable",
    "Technical replicate": "Not applicable",
    "Antibody": "Not applicable",
    "Assay": "short total RNA-Seq",
    "File format": "bed bed6+51 DASHR",
    "File size": 116737,
    "Downloaded date": "6/30/18",
    "Release date": "3/19/12",
    "Date added to FILER": "7/1/18",
    "Processed File Download URL": "https://lisanwanglab.org/GADB/Annotationtracks/DASHRv2/short_total_RNA-seq/hg19/ENCODE_GEO_hg19/BJ_SRR446315_peaks_annot_hg19.bed.gz",
    "Processed file md5": "8e8efe35acaf41e1310149c1e0238821",
    "Link out URL": "http://dashr2.lisanwanglab.org/index.php",
    "Data Category": "Called peaks",
    "classification": "short total RNA-Seq annotated peaks",
    # "Track Description": "BJ cell line - Skin fibroblast; SRR446315",
    "system category": "Skeletal",
    "life stage": "Not applicable",
    "trackName": "DASHR2 BJ short total RNA-Seq annotated peaks (bed6+51 DASHR) [Orig: BJ cell line - Skin fibroblast; SRR446315] [Life stage: Not applicable]",
    "tabixFileUrl": "https://lisanwanglab.org/GADB/Annotationtracks/DASHRv2/short_total_RNA-seq/hg19/ENCODE_GEO_hg19/BJ_SRR446315_peaks_annot_hg19.bed.gz.tbi"
}

metadata = {
    'id': fields.String(required=True, attribute="Identifier",
            description="unique track identifier, usually accession number in original data source"),
    'data_source': fields.String(required=True, attribute="Data Source",
            description="source repository or data collection"),
    'name': fields.String(required=True, attribute="trackName"),
    'description': fields.String(required=True, attribute="Track Description"),
    'assay': fields.String(required=True, description="assay type"),
    'antibody_target': fields.String(description="antibody target in ChIP seq or other immunoprecipitation experiment"),
    'number_of_intervals': fields.Integer(attribute="Number of intervals",
            description="Number of intervals (hits, peaks, etc) with data in the track"), 
    'bp_covered': fields.Integer(attribute="bp covered", description="length in BP of the track"),
    'assembly': GenomeBuild(attribute="Genome build", description="reference genome build", required=True )
}

