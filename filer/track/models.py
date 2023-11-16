''' FILER track metadata model '''
from sqlalchemy.orm import column_property
from sqlalchemy import func, distinct, and_
from flask import jsonify

from shared_resources.db import db
from shared_resources.utils import extract_result_data
from shared_resources.constants import DATASOURCE_URLS
from niagads.filer.parser import split_replicates
from filer.utils import make_request
from niagads.utils import string, list


SKIP_FILTERS = ['idsOnly', 'countOnly', 'fuzzy', 'keyword', 'span', 'chr', 'start', 'end']
IGNORE_TRACKS = ['NGGT000235']

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
    
    tissue = db.synonym('tissue_category')
     
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
        return getattr(DATASOURCE_URLS, dsKey)
    
    
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
            return string.to_snake_case(attrName)


def get_track_count(filters):
    # see https://stackoverflow.com/questions/48778162/variable-filter-for-sqlalchemy-query
    # for dynamic filtering solution
    queryTarget = distinct(getattr(Track, 'identifier'))
    query = db.session.query(func.count(queryTarget))
    if filters is not None:
        expressions = [func.lower(getattr(Track, __parse_attributes(attr))) == str(value).lower()
                for attr, value in filters.items() 
                if value is not None
                and attr not in SKIP_FILTERS]
        if 'keyword' in filters:
            value = filters['keyword']
            expressions.append(Track.searchable_text.match(value))
        result = query.filter(and_(*expressions))

    return result.scalar()


def __parse_query_result(queryResult, idsOnly):
    result = extract_result_data(queryResult)    
    if idsOnly:
        return list.drop_nulls(result)
    
    return result    


def __get_filter_expressions(filters):
    expressions = [func.lower(getattr(Track, __parse_attributes(attr))) == str(value).lower()
            for attr, value in filters.items() 
            if value is not None
            and attr not in SKIP_FILTERS]
    return expressions


def get_track_metadata(filters):
    queryTarget = distinct(Track.identifier) if filters.idsOnly else Track
    query = db.session.query(queryTarget)
    expressions = __get_filter_expressions(filters) if filters is not None else None
    queryResult = query.filter(and_(*expressions)).order_by(Track.identifier) 
    return __parse_query_result(queryResult, filters.idsOnly)


def get_filter_values(filterName):
    column = __parse_attributes(filterName)
    queryTarget = getattr(Track, column)
    result = db.session.query(distinct(queryTarget)).order_by(queryTarget).all()
    return list.drop_nulls(extract_result_data(result))


def text_search(value, idsOnly, schema=None):
    queryTarget = Track.identifier if idsOnly else Track
    queryResult = db.session.query(distinct(queryTarget)).filter(Track.searchable_text.match(value)).all()
    return __parse_query_result(queryResult, idsOnly, schema)


def validate_track(id, genomeBuild, returnMetadata=False):
    result = db.one_or_404(
            statement=db.session.query(Track).filter_by(identifier=id).filter_by(genome_build=genomeBuild),
            description=f"No track with id '{id}' found in FILER.")
    return result if returnMetadata else True
    

def __get_track_ids(args):
    queryTarget = distinct(Track.identifier)
    query = db.session.query(queryTarget)
    expressions = __get_filter_expressions(args) if args is not None else None
    queryResult = query.filter(and_(*expressions)).order_by(Track.identifier) 
    result =  __parse_query_result(queryResult, idsOnly=True)
    return result

def get_bulk_overlaps(args, span):
    trackIds = [ v[0] for v in __get_track_ids(args) if v not in IGNORE_TRACKS]
    if len(trackIds) > 300:
        return {'message': 'Too many tracks;' + str(len(trackIds) + ' match the filter criteria. Please add additional filters.  Pagination coming soon')}
    
    trackIds = ','.join(trackIds)
    return make_request("get_overlaps", {"id": trackIds, "assembly": args['assembly'], "span": span})