from flask_restx import fields

id = {
    'id': fields.String(required=True, description="unique dataset identifier or accession number in original datasource"),
}
