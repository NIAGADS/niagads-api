from api.dependencies.database import DatabaseSessionManager

ROUTE_DATABASE = 'metadata'
ROUTE_SESSION_MANAGER = DatabaseSessionManager(ROUTE_DATABASE)

ROUTE_PREFIX = "/filer"
ROUTE_NAME = "FILER Functional Genomics Repository"
ROUTE_ABBREVIATION = "FILER"
ROUTE_DESCRIPTION = {}
ROUTE_TAGS = [ROUTE_NAME]

BIOSAMPLE_FIELDS = ["life_stage", "biosample_term", "system_category",
    "tissue_category", "biosample_display",
    "biosample_summary", "biosample_term_id"]

TRACK_SEARCH_FILTER_FIELD_MAP = { 
    'biosample': {
        'model_field' : 'biosample_characteristics', 
        'description': "searches across biosample characteristics, including, " +
            "but not limited to: biological system, tissue, cell type, cell line, " +
            "life stage; can be searched using ontology terms from UBERON (tissues), CL (cells), " + 
            "CLO (cell lines), and EFO (experimental factors); NOTE: biosample term matches are fuzzy and case insensitive"
        },
    'antibody': {
        'model_field': 'antibody_target',
        'description': "the antibody target, e.g. in a CHiP-SEQ experiment; " + 
            "we recommend searching for gene targets with `like` operator as many are prefixed"
    },
    'assay': {
        'model_field': 'assay',
        'description': 'type of assay'
    },
    'feature': {
        'model_field': 'feature_type',
        'description': "the type of functional genomics feature reported in the data track"
    },
    'analysis': {
        'model_field': 'analysis',
        'description': "type of statistical analysis, if relevant"
    },
    'classification': {
        'model_field': 'classification',
        'description': "specific categorization or classification of the data reported in the data track"
    },
    'category': {
        'model_field': 'data_category',
        'description': "broad categorization of the type of the data reported in the data track"
    },
    'datasource': {
        'model_field': 'data_source',
        'description': "original third-party data source for the track"
    },
}
