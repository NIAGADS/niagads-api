from flask_restx import fields

metadata = {
    'attribution': fields.String(description="submitter or first author and date of publication", 
            required=True, 
            attribute="attribution_internal",
            example="Wang et al. 2021"),
    'publication': fields.String(description="PubMED ID or DOI for primary publication", 
            example="PMID:34122051"),    
    'id': fields.String(required=True, 
            description="NIAGADS Accession Number", 
            example="NG00115")
    
}
