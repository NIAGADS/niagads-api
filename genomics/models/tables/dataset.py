''' GenomicsdB dataset (accession) data model '''
from db import genomicsdb as gdb
from shared_resources.fields import GenomeBuild

def table(genomeBuild):
    """determine bind_db --> table based on genome_build route param"""
    bind_db = GenomeBuild().deserialize(genomeBuild)
    return Dataset_GRCh38 if bind_db == 'GRCh38' else Dataset_GRCh37

class DatasetMixin:
    accession = gdb.Column(gdb.String, primary_key=True)
    name = gdb.Column(gdb.String)
    description = gdb.Column(gdb.String)
    attribution = gdb.Column(gdb.String)

class Dataset_GRCh38(DatasetMixin, gdb.Model):
    __bind_key__ = 'GRCh38'
    __tablename__ = 'datasetattributes'
    __table_args__ = {'schema': 'niagads', 'extend_existing':True}
    id = gdb.synonym('accession')
 
class Dataset_GRCh37(DatasetMixin, gdb.Model):
    __bind_key__ = 'GRCh37'
    __tablename__ = 'datasetattributes'
    __table_args__ = {'schema': 'niagads', 'extend_existing':True}
    id = gdb.synonym('accession')
 