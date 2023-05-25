from flask_restx import fields

filer = {'assay': fields.String(required=True, description="assay type"),
        'antibody_target': fields.String(description="antibody target in ChIP seq or other immunoprecipitation experiment")
        }

