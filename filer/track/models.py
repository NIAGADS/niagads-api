''' FILER track metadata model '''
from sqlalchemy.orm import column_property
from sqlalchemy import func, distinct, and_

from shared_resources.db import db
from shared_resources import utils, constants
from filer.parsers import split_replicates


# [
# 'output_type',  'cell_type', 'biosample_type', 'biosamples_term_id', 
# 'tissue_category', 'encode_experiment_id', 
#  'assay', 'file_format', 
#  'filepath', 
#  
# 'data_category', 'classification', 
# 'system_category', 'life_stage']

class Track(db.Model):
    __bind_key__ = 'filer'
    identifier = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    # description = db.Column(db.String) 
    genome_build = db.Column(db.String)
    feature_type = db.Column(db.String)
    data_source = db.Column(db.String)
    
    # biosample
    tissue_category = db.Column(db.String)
    system_category = db.Column(db.String)
    biosample_term = db.Column(db.String)
    biosample_term_id = db.Column(db.String)
    biosample_display = db.Column(db.String)
    biosample_type = db.Column(db.String)
    cell_line = db.Column(db.String)
    life_stage = db.Column(db.String)
    
    # experiment design
    biological_replicates = db.Column(db.String)
    technical_replicates = db.Column(db.String)
    antibody_target = db.Column(db.String)
    assay = db.Column(db.String)
    analysis = db.Column(db.String)
    classification = db.Column(db.String)
    data_category = db.Column(db.String)
    output_type = db.Column(db.String)
    is_lifted = db.Column(db.Boolean)
    experiment_info = db.Column(db.String)
    
    # provenance
    data_source_version = db.Column(db.String)
    download_url = db.Column(db.String)
    download_date = db.Column(db.Date) # check
    release_date = db.Column(db.Date)
    filer_release_date = db.Column(db.Date)
    experiment_id = db.Column(db.String)
    project = db.Column(db.String)

    # FILER file properties
    file_name = db.Column(db.String)
    url = db.Column(db.String)
    md5sum = db.Column(db.String)
    raw_file_url = db.Column(db.String)
    raw_file_md5sum = db.Column(db.String)
    bp_covered = db.Column(db.Integer)
    number_of_intervals = db.Column(db.Integer)
    file_size = db.Column(db.Integer)

    file_format = db.Column(db.String)
    file_schema = db.Column(db.String) 
    
    searchable_text = db.Column(db.String)
    
        
    @property
    def genome_browser_track_schema(self):    
        schema = self.file_schema.split('|')
        return schema[0]
    
    @property 
    def genome_browser_track_type(self):
        # TODO: interactions
        if 'QTL' in self.feature_type:
            return 'qtl'
        else:
            return 'annotation'
    
    @property
    def index_url(self):
        return self.url + '.tbi'
    
    @property
    def data_source_url(self):
        dsKey = self.data_source + '|' + self.data_source_version
        return constants.DATASOURCE_URLS[dsKey]
    
    
    @property
    def replicates(self):
        biological = split_replicates(self.biological_replicates)
        technical = split_replicates(self.technical_replicates)
        
        if biological is None: 
            if technical is None: return None
            return { "technical": technical}
        if technical is None:
            return { "biological": biological}
        
        return { "technical": technical, "biological": biological}


def __parse_attributes(attrName):
    match attrName:
        case 'assembly':
            return 'genome_build'
        case 'dataType':
            return 'output_type'
        case _:
            return utils.to_snake_case(attrName)


def get_track_count(filters):
    # see https://stackoverflow.com/questions/48778162/variable-filter-for-sqlalchemy-query
    # for dynamic filtering solution
    queryTarget = distinct(getattr(Track, 'identifier'))
    query = db.session.query(func.count(queryTarget))
    if filters is not None:
        expressions = [getattr(Track, __parse_attributes(attr)) == value for attr, value in filters.items() if value is not None]
        query = query.filter(and_(*expressions))

    return query.scalar()


def get_filter_values(filterName):
    column = __parse_attributes(filterName)
    result = db.session.query(distinct(getattr(Track, column))).all()
    return utils.drop_nulls(utils.extract_result_data(result))


def text_search(value, idsOnly):
    queryTarget = Track.identifier if idsOnly else Track
    result = db.session.query(distinct(queryTarget)).filter(Track.searchable_text.match(value)).all()
    return utils.extract_result_data(result)