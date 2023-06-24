''' GenomicsdB dataset (accession) data model '''
from sqlalchemy.orm import column_property
from shared_resources.db import db
from shared_resources.fields import GenomeBuild

def table(genomeBuild):
    """determine bind_db --> table based on genome_build route param"""
    bind_db = GenomeBuild().deserialize(genomeBuild)
    return Dataset_GRCh38 if bind_db == 'GRCh38' else Dataset_GRCh37

class DatasetMixin:
    accession = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    attribution = db.Column(db.String)
    
    @property
    def data_source(self):
        return "NIAGADS"
    
    @property
    def type(self):
        # TODO: add column for type to view
        return "GWAS_sumstats"
    
    @property
    def attribution_internal(self):
        return self.attribution.split('|')[0]
    
    @property
    def publication(self):
        return self.attribution.split('|')[1] if '|' in self.attribution else None
    
   
class Dataset_GRCh38(DatasetMixin, db.Model):
    __bind_key__ = 'GRCh38'
    __tablename__ = 'datasetattributes'
    __table_args__ = {'schema': 'niagads', 'extend_existing':True}
    id = db.synonym('accession')
 
class Dataset_GRCh37(DatasetMixin, db.Model):
    __bind_key__ = 'GRCh37'
    __tablename__ = 'datasetattributes'
    __table_args__ = {'schema': 'niagads', 'extend_existing':True}
    id = db.synonym('accession')
 