from flask_restx import fields
from shared_resources.fields import GenomeBuild

metadata = {
    'id': fields.String(required=True, attribute="identifier",
            description="unique track identifier, usually accession number in original data source"),
    'name': fields.String(required=True, description="track name"),
    # 'assembly': GenomeBuild(attribute="genome_build", description="reference genome build", required=True),
    'output_type': fields.String(required=True, description="data type of dataset or track"),
    'data_source': fields.String(required=True, description="source repository or data collection"),
    'assay': fields.String(required=True, description="assay type"),
    'antibody_target': fields.String(description="antibody target in ChIP seq or other immunoprecipitation experiment"),
    'number_of_intervals': fields.Integer(description="Number of intervals (hits, peaks, etc) with data in the track"), 
    'bp_covered': fields.Integer(description="length in BP of the track"),
    'url': fields.String(required=True, description="URL for accessing file in FILER"),
    'index_url': fields.String(required=True, description="URL for accessing paired tabix index file in FILER")
}

