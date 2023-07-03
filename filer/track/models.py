''' FILER track metadata model '''
from sqlalchemy.orm import column_property

from shared_resources.db import db
from shared_resources.constants import DATASOURCE_URLS
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
    description = db.Column(db.String) 
    genome_build = db.Column(db.String)
    data_category = db.Column(db.String)
    feature_type = db.Column(db.String)
    
    # biosample
    tissue_category = db.Column(db.String)
    system_category = db.Column(db.String)
    biosample_term = db.Column(db.String)
    biosample_term_id = db.Column(db.String)
    biosample_display = db.Column(db.String)
    biosample_type = db.Column(db.String)
    life_stage = db.Column(db.String)
    
    # experiment design
    biological_replicates = db.Column(db.String)
    technical_replicates = db.Column(db.String)
    antibody_target = db.Column(db.String)
    experiment_id = db.Column(db.String)
    project = db.Column(db.String)
    experiment_info = db.Column(db.String)
    assay = db.Column(db.String)
    analysis = db.Column(db.String)
    classification = db.Column(db.String)
    
    # provenance
    data_source = db.Column(db.String)
    data_source_version = db.Column(db.String)
    is_lifted = db.Column(db.Boolean)
    download_url = db.Column(db.String)
    download_date = db.Column(db.Date) # check
    release_date = db.Column(db.Date)
    
    # FILER file properties
    file_name = db.Column(db.String)
    url = db.Column(db.String)
    md5sum = db.Column(db.String)
    raw_file_url = db.Column(db.String)
    raw_file_md5sum = db.Column(db.String)
    bp_covered = db.Column(db.Integer)
    number_of_intervals = db.Column(db.Integer)
    file_size = db.Column(db.Integer)
    output_type = db.Column(db.String)
    file_format = db.Column(db.String)
    file_schema = db.Column(db.String)
    
        
    @property
    def data_source_url(self):
        dsKey = self.data_source + '|' + self.data_source_version
        return DATASOURCE_URLS[dsKey]
    
    
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
    
    
    @property
    def type(self):
        return "track"

