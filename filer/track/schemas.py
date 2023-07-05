from flask_restx import fields
from shared_resources.fields import GenomeBuild, DictItem

metadata = {
    'id': fields.String(required=True, attribute="identifier",
            description="unique track identifier, usually accession number in original data source"),
    'name': fields.String(required=True, description="track name"),
    'assembly': fields.String(attribute="genome_build", description="reference genome build", required=True, example="GRCh38"),
    'feature_type': fields.String(required=True, description="type of genomic feature annotated by the track"),
    'data_source': fields.String(required=True, description="source repository or data collection"),

    'number_of_intervals': fields.Integer(description="Number of intervals (hits, peaks, etc) with data in the track"), 
    'bp_covered': fields.Integer(description="length in BP of the track"),
    'file_size': fields.Integer(description="size of the file in bytes"),
    
    'url': fields.String(required=True, description="URL for accessing file in FILER"),
    'index_url': fields.String(required=True, description="URL for accessing paired tabix index file in FILER"),
    'md5sum': fields.String(description="file md5sum"),
}

experimental_design = {
    'assay': fields.String(required=True, description="assay type"),
    'antibody_target': fields.String(description="antibody target in ChIP seq or other immunoprecipitation experiment"),
    'replicates': DictItem(description="lists of biological or technical replicates included in this track"),
    'analysis': fields.String(description="type of (statistical) analysis or model, if any that was used to generate track data"),
    'output_type': fields.String(description="type of data"),
    'experiment_info': fields.String(description="additional information about the experiment"),
    'is_lifted': fields.Boolean(description="flag indicating whether the data were lifted from an earlier assembly version (usually GRCh37->GRCh38)")
}

provenance = {
    'data_source_url': fields.String(description="data source description/home page"),
    'data_source_version': fields.String(description="version or release date of the original data source"),
    'filer_release_date': fields.String(description="date added to FILER"),
    'experiment_id': fields.String(description="experiment ID from original data source (usually ENCODE experiment ID)"),
    'project': fields.String(description="data collection (or ENCODE project) in original data source"),
    'download_date': fields.Date(description="date downloaded from original datasource"),
}

biosample = {
    'tissue': fields.String(description="biosample tissue, if any", attribute="tissue_category"),
    'anatomical_system': fields.String(description="biosample anatomical system", attribute="system_category"),
    'biosample_term': fields.String(description="biosample ontology term"),
    'biosample_term_id': fields.String(description="biosample ontology term id"),
    'cell_line': fields.String(description="cell line, if any"),
    'life_stage': fields.String(description="biosample life stage (embryo, fetal, adult)")
}

genome_browser_config = {
    'name': fields.String(required=True, description="track name"),
    'format': fields.String(required=True, description="file schema", attribute="genome_browser_track_schema"),
    'type': fields.String(required=True, description="genome browser track type", attribute="genome_browser_track_type")
}