from flask_restx import fields
from shared_resources.fields import GenomeBuild

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

